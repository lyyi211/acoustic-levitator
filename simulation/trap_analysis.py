"""Axial single-particle equilibria and conditional payload calculations."""
import csv
import json
import numpy as np
from acoustic_model import array_force, contrast_factors, wave_number


def stable_axial_roots(z, net_force):
    """Brackets with a restoring axial force; excludes tangential marginal roots."""
    z, net_force = np.asarray(z), np.asarray(net_force)
    indices = np.flatnonzero((net_force[:-1] > 0) & (net_force[1:] <= 0))
    return z[indices], z[indices + 1]


def scan_traps(field, frequency, medium, particle, limit, grid_step=0.1e-3,
               difference_step=20e-6):
    def points(z):
        z = np.asarray(z)
        return np.column_stack((np.zeros_like(z), np.zeros_like(z), z))
    weight = (particle.density-medium.density)*particle.volume*9.80665
    def force(z):
        return array_force(points(z), field, frequency, medium, particle, difference_step)
    z = np.linspace(-limit, limit, int(np.ceil(2*limit/grid_step))+1)
    sampled_force = force(z)[:, 2]
    lo, hi = stable_axial_roots(z, sampled_force-weight)
    for _ in range(25):
        mid = (lo+hi)/2
        positive = force(mid)[:, 2] > weight
        lo, hi = np.where(positive, mid, lo), np.where(positive, hi, mid)
    roots = (lo+hi)/2
    pts = points(roots)
    jacobian = np.empty((len(roots), 3, 3))
    for axis in range(3):
        offset = np.eye(3)[axis]*difference_step
        jacobian[:, :, axis] = (array_force(pts+offset, field, frequency, medium, particle, difference_step)
                               - array_force(pts-offset, field, frequency, medium, particle, difference_step))/(2*difference_step)
    stiffness = -(jacobian+np.swapaxes(jacobian, 1, 2))/2
    eig = np.linalg.eigvalsh(stiffness)
    residual = force(roots)-[0, 0, weight]
    stable = np.all(eig > 0, axis=1) & (np.linalg.norm(residual,axis=1)<weight*1e-5)
    return z, sampled_force, roots, eig, stable, residual


def write_capacity(results, design, centres, field, frequency, medium, particle):
    import matplotlib.pyplot as plt
    # Common central slab, inset 10 mm from the innermost face centres.
    limit = np.min(np.abs(centres[:,2]))-0.01
    z, force, roots, eig, stable, residual = scan_traps(field,frequency,medium,particle,limit)
    # Independent grid and derivative-step refinement of the reported count.
    refined = scan_traps(field,frequency,medium,particle,limit,0.05e-3,10e-6)
    if len(roots)!=len(refined[2]) or not np.array_equal(stable,refined[4]):
        raise RuntimeError('Trap count changed under grid/derivative refinement')
    if not np.allclose(roots,refined[2],rtol=0,atol=2e-6):
        raise RuntimeError('Equilibrium positions not converged within 2 micrometres')
    with (results/'axial_traps.csv').open('w',newline='') as f:
        w=csv.writer(f, lineterminator="\n");w.writerow(['z_m','K1_N_per_m','K2_N_per_m','K3_N_per_m','stable_3d','residual_force_N'])
        w.writerows([r,*e,bool(s),np.linalg.norm(err)] for r,e,s,err in zip(roots,eig,stable,residual))
    k=wave_number(frequency,medium); f1,f2=contrast_factors(medium,particle)
    phi=f1+1.5*f2
    p_threshold=np.sqrt(4*medium.density*medium.sound_speed**2*(particle.density-medium.density)*9.80665/(k*abs(phi)))
    max_radius=0.3/k
    mass=particle.volume*particle.density
    max_model_mass=4*np.pi*max_radius**3/3*particle.density
    count=int(stable.sum())
    data={'scan_half_width_m':float(limit),'scan_grid_m':0.0001,'refined_grid_m':0.00005,
          'derivative_step_m':0.00002,'refined_derivative_step_m':0.00001,
          'axially_stable_count':len(roots),'locally_stable_3d_count':count,
          'particle_mass_kg':mass,'particle_weight_N':mass*9.80665,
          'effective_weight_N':(particle.density-medium.density)*particle.volume*9.80665,
          'independent_particle_total_mass_kg':count*mass,
          'rayleigh_radius_limit_m':max_radius,'rayleigh_mass_limit_kg':max_model_mass,
          'plane_wave_pressure_threshold_pa':float(p_threshold),
          'plane_wave_lattice_count_max':int(np.floor(2*limit/(medium.sound_speed/frequency/2)))+1,
          'sampled_peak_upward_force_N':float(force.max()),
          'force_equivalent_supported_mass_kg':float(force.max()/9.80665+medium.density*particle.volume),
          'simultaneous_occupancy_validated':False,
          'count_scope':'Single-particle on-axis equilibria in the stated central slab; no multiple scattering'}
    (results/'capacity_summary.json').write_text(json.dumps(data,indent=2)+'\n')
    fig,axes=plt.subplots(2,1,figsize=(10,7),constrained_layout=True)
    axes[0].plot(z*1e3,force*1e9,label='Acoustic force')
    axes[0].axhline(data['effective_weight_N']*1e9,color='black',ls='--',label='Effective weight')
    axes[0].scatter(roots[stable]*1e3,np.full(count,data['effective_weight_N']*1e9),color='green',label='3-D stable single-particle site',zorder=3)
    axes[0].scatter(roots[~stable]*1e3,np.full((~stable).sum(),data['effective_weight_N']*1e9),color='red',marker='x',label='Axially stable, laterally unstable')
    axes[0].set(ylabel='Force (nN)',xlabel='z from focus (mm)');axes[0].legend(fontsize=8)
    for i in range(3):axes[1].plot(roots*1e3,eig[:,i]*1e6,'o-',label=f'Stiffness eigenvalue {i+1}')
    axes[1].axhline(0,color='black',lw=0.8)
    axes[1].set(xlabel='Equilibrium z (mm)',ylabel='Stiffness (uN/m)');axes[1].legend(fontsize=8)
    for ax in axes:ax.grid(alpha=.25)
    fig.suptitle(f'{count} locally stable sites; isolated 0.30 mm-radius particles; prescribed 1.5 kPa')
    fig.savefig(results/'vertical_capacity.png',dpi=180);plt.close(fig)
    return data
