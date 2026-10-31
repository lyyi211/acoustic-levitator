"""Generate concave-array geometry, fields, stability estimates and plots."""
from pathlib import Path
import csv
import json
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from trap_analysis import write_capacity
from array_geometry import curved_array, export_geometry, load_design
from acoustic_model import (Medium, Particle, array_pressure, array_potential,
                            array_force, rayleigh_parameter)

ROOT = Path(__file__).resolve().parents[1]
RESULTS = ROOT / "results"
MEDIUM, PARTICLE = Medium(), Particle()
DESIGN = load_design()
FREQUENCY = DESIGN["frequency_hz"]
CENTRES, NORMALS, BANKS = curved_array(DESIGN)
REFERENCE_DISTANCE = DESIGN["pressure_reference_distance_mm"] * 1e-3
PISTON_RADIUS = DESIGN["assumed_piston_radius_mm"] * 1e-3
# Normalise ONLY the nominal geometry and frequency, once. This is an input
# pressure assumption; it is deliberately independent of the electrical voltage.
UNIT_FOCUS = abs(array_pressure(np.zeros((1, 3)), CENTRES, NORMALS, np.zeros(len(CENTRES)),
                               FREQUENCY, MEDIUM, PISTON_RADIUS, 1, REFERENCE_DISTANCE)[0])
REFERENCE_PEAK = DESIGN["assumed_focus_peak_pa"] / UNIT_FOCUS
EFFECTIVE_WEIGHT = (PARTICLE.density - MEDIUM.density) * PARTICLE.volume * 9.80665


def make_field(frequency=FREQUENCY, phase=0.0, planar=False):
    centres, normals = CENTRES.copy(), NORMALS.copy()
    if planar:
        centres[:, 2] = np.where(BANKS == 0, 1, -1) * DESIGN["curvature_radius_mm"] * 1e-3
        normals[:] = 0
        normals[:, 2] = np.where(BANKS == 0, -1, 1)
    phases = np.where(BANKS == 0, 0.0, phase)
    def field(points):
        return array_pressure(points, centres, normals, phases, frequency, MEDIUM,
                              PISTON_RADIUS, REFERENCE_PEAK, REFERENCE_DISTANCE)
    return field


def axial_points(z):
    z = np.asarray(z)
    return np.column_stack((np.zeros_like(z), np.zeros_like(z), z))


def save_axial_plot():
    z = np.linspace(-0.012, 0.012, 801)
    points, field = axial_points(z), make_field()
    pressure = np.abs(field(points))
    potential = array_potential(points, field, FREQUENCY, MEDIUM, PARTICLE)
    force = array_force(points, field, FREQUENCY, MEDIUM, PARTICLE)[:, 2]
    fig, axes = plt.subplots(3, 1, figsize=(9, 8), sharex=True, constrained_layout=True)
    axes[0].plot(z*1e3, pressure/1e3)
    axes[0].set_ylabel("Peak |pressure| (kPa)")
    axes[1].plot(z*1e3, (potential + EFFECTIVE_WEIGHT*z)*1e9, color="tab:purple")
    axes[1].set_ylabel("Potential + gravity (nJ)")
    axes[2].plot(z*1e3, force*1e6, label="Acoustic force (+z)")
    axes[2].axhline(EFFECTIVE_WEIGHT*1e6, color="tab:red", ls="--", label="Effective weight")
    axes[2].set_ylabel("Force (uN)")
    axes[2].set_xlabel("z from common focus (mm)")
    axes[2].legend()
    for ax in axes:
        ax.grid(alpha=0.25)
    fig.suptitle("Concave 36+36 at 40 kHz; assumed 1.5 kPa at focus, no voltage calibration")
    fig.savefig(RESULTS/"standing_wave_field.png", dpi=180)
    plt.close(fig)


def save_phase_plot():
    z = np.linspace(-0.008, 0.008, 601)
    fig, ax = plt.subplots(figsize=(9, 4.5), constrained_layout=True)
    for phase in (0.0, np.pi):
        ax.plot(z*1e3, np.abs(make_field(phase=phase)(axial_points(z)))/1e3,
                label=f"Bank phase {phase/np.pi:.0f} pi (firmware supported)")
    ax.set(xlabel="z from focus (mm)", ylabel="Peak |pressure| (kPa)",
           title="Binary bank phase in the curved-array model")
    ax.grid(alpha=0.25)
    ax.legend()
    fig.savefig(RESULTS/"phase_sensitivity.png", dpi=180)
    plt.close(fig)


def save_field_map():
    x, z = np.meshgrid(np.linspace(-0.035, 0.035, 241), np.linspace(-0.035, 0.035, 241))
    points = np.stack((x, np.zeros_like(x), z), axis=-1)
    curved = np.abs(make_field()(points))
    flat = np.abs(make_field(planar=True)(points))
    maximum = max(curved.max(), flat.max())/1e3
    fig, axes = plt.subplots(1, 2, figsize=(11, 5), constrained_layout=True)
    for ax, values, title in zip(axes, (flat, curved),
                                 ("Planar, common phase", "Concave, geometric focusing")):
        image = ax.pcolormesh(x*1e3, z*1e3, values/1e3, shading="auto", cmap="magma",
                              vmin=0, vmax=maximum)
        ax.set(xlabel="x (mm)", ylabel="z (mm)", title=title, aspect="equal")
    fig.colorbar(image, ax=axes, label="Peak |pressure| (kPa), assumed source amplitude")
    fig.suptitle("Same 72 model emitters and drive amplitude; y=0 slice")
    fig.savefig(RESULTS/"array_field_2d.png", dpi=180)
    plt.close(fig)


def save_gap_map():
    errors = np.linspace(-0.004, 0.004, 81)
    frequencies = np.linspace(38000, 42000, 41)
    pressure = []
    for frequency in frequencies:
        total = np.zeros(len(errors), dtype=complex)
        for bank in (0, 1):
            points = axial_points(np.where(bank == 0, -errors/2, errors/2))
            mask = BANKS == bank
            total += array_pressure(points, CENTRES[mask], NORMALS[mask], np.zeros(mask.sum()),
                                    frequency, MEDIUM, PISTON_RADIUS, REFERENCE_PEAK, REFERENCE_DISTANCE)
        pressure.append(np.abs(total)/DESIGN["assumed_focus_peak_pa"])
    fig, ax = plt.subplots(figsize=(9, 5), constrained_layout=True)
    image = ax.imshow(pressure, origin="lower", aspect="auto",
                      extent=[-4, 4, 38, 42], cmap="viridis")
    fig.colorbar(image, ax=ax, label="Centre pressure / nominal assumed centre pressure")
    ax.set(xlabel="Symmetric array separation error (mm)", ylabel="Frequency (kHz)",
           title="Geometric focus misalignment; excludes resonance and reflections")
    fig.savefig(RESULTS/"frequency_separation_map.png", dpi=180)
    plt.close(fig)


def equilibrium_summary():
    rows = []
    for frequency in (38000.0, 40000.0, 42000.0):
        field = make_field(frequency)
        z = np.linspace(-0.01, 0.01, 501)
        net = array_force(axial_points(z), field, frequency, MEDIUM, PARTICLE)[:, 2] - EFFECTIVE_WEIGHT
        stable = np.flatnonzero((net[:-1] > 0) & (net[1:] < 0))
        if not len(stable):
            raise RuntimeError(f"No axial equilibrium at assumed amplitude for {frequency} Hz")
        bracket = min(stable, key=lambda i: abs((z[i]+z[i+1])/2))
        low, high = z[bracket], z[bracket+1]
        for _ in range(22):
            mid = (low+high)/2
            value = array_force(axial_points([mid]), field, frequency, MEDIUM, PARTICLE)[0,2] - EFFECTIVE_WEIGHT
            if value > 0:
                low = mid
            else:
                high = mid
        point = np.array([[0.0, 0.0, (low+high)/2]])
        step = 50e-6
        jacobian = np.empty((3, 3))
        for axis in range(3):
            offset = np.eye(3)[axis]*step
            jacobian[:,axis] = (array_force(point+offset, field, frequency, MEDIUM, PARTICLE)[0]
                                - array_force(point-offset, field, frequency, MEDIUM, PARTICLE)[0])/(2*step)
        stiffness = -(jacobian+jacobian.T)/2
        eigenvalues = np.linalg.eigvalsh(stiffness)
        force = array_force(point, field, frequency, MEDIUM, PARTICLE)[0]
        rows.append([frequency, MEDIUM.sound_speed/frequency, rayleigh_parameter(frequency, MEDIUM, PARTICLE),
                     point[0,2], *force, EFFECTIVE_WEIGHT, *eigenvalues, bool(np.all(eigenvalues>0))])
    with (RESULTS/"model_summary.csv").open("w", newline="") as stream:
        writer = csv.writer(stream, lineterminator="\n")
        writer.writerow(["frequency_Hz", "wavelength_m", "ka", "equilibrium_z_m", "Fx_N", "Fy_N", "Fz_N",
                         "effective_weight_N", "stiffness_eigenvalue_1_N_per_m", "stiffness_eigenvalue_2_N_per_m",
                         "stiffness_eigenvalue_3_N_per_m", "locally_stable_3d"])
        writer.writerows(rows)
    nominal = rows[1]
    z = nominal[3]
    x_axis = np.linspace(-0.01, 0.01, 201)
    points = np.column_stack((x_axis, np.zeros_like(x_axis), np.full_like(x_axis,z)))
    field = make_field()
    potential = array_potential(points, field, FREQUENCY, MEDIUM, PARTICLE)
    force = array_force(points, field, FREQUENCY, MEDIUM, PARTICLE)[:,0]
    fig, axes = plt.subplots(2,1, figsize=(9,6), sharex=True, constrained_layout=True)
    axes[0].plot(x_axis*1e3, (potential-potential[len(x_axis)//2])*1e9)
    axes[0].set_ylabel("Relative potential (nJ)")
    axes[1].plot(x_axis*1e3, force*1e6)
    axes[1].set(xlabel="Lateral x (mm)", ylabel="Fx (uN)")
    for ax in axes:
        ax.grid(alpha=0.25)
    fig.suptitle(f"Lateral confinement at model equilibrium z={z*1e3:.3f} mm; assumed pressure")
    fig.savefig(RESULTS/"lateral_stability.png", dpi=180)
    plt.close(fig)
    return rows


def main():
    RESULTS.mkdir(exist_ok=True)
    export_geometry()
    save_axial_plot()
    save_phase_plot()
    save_field_map()
    save_gap_map()
    rows = equilibrium_summary()
    capacity = write_capacity(RESULTS, DESIGN, CENTRES, make_field(), FREQUENCY, MEDIUM, PARTICLE)
    metadata = {"capacity": capacity, "design": DESIGN, "source_count": len(CENTRES), "reference_peak_pa": REFERENCE_PEAK,
                "reference_distance_m": REFERENCE_DISTANCE, "pressure_is_assumed_not_voltage_calibrated": True,
                "rayleigh_parameter": rayleigh_parameter(FREQUENCY, MEDIUM, PARTICLE),
                "all_reported_equilibria_locally_stable_3d": all(row[-1] for row in rows)}
    (RESULTS/"simulation_metadata.json").write_text(json.dumps(metadata, indent=2)+"\n")
    print(f"Generated concave 36+36 results in {RESULTS}")
    print(f"Assumed nominal focus peak: {DESIGN['assumed_focus_peak_pa']} Pa; ka={metadata['rayleigh_parameter']:.4f}")
    print(f"3D stable equilibria at all three frequencies: {metadata['all_reported_equilibria_locally_stable_3d']}")


if __name__ == "__main__":
    main()
