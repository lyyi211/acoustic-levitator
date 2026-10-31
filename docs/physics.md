# Physics and calculated results

Linear acoustics was used to describe the field, and the Gor’kov potential was used to calculate the force on a small particle. This chapter follows the calculation from air motion to equilibrium, geometry, electrical loading and the resulting figures. Source numbers [1]–[5] refer to the bibliography collected in the main README.

The selected design has 72 transmitter cans from HC-SR04 modules, two concave arrays, Arduino Uno, 5 V logic and a 9 V bridge. The numerical field is prescribed at 1.5 kPa peak in the common focus, independently of the electrical model. The sections below present the calculation and its results.

## 1. Sound, frequency and wavelength

A vibrating diaphragm creates small pressure and density variations in air. Air parcels oscillate about their resting positions; the wave carries energy through the medium. Ultrasound has frequency above 20 kHz. The selected 40 kHz signal completes one cycle in 25 µs.

Dry-air density of 1.2041 kg/m³, sound speed of 343.2 m/s and gravitational acceleration of 9.80665 m/s² were used. These are the actual constants in the simulation. Frequency is the number of cycles per second, wavelength is the distance travelled in one cycle, and the wave number describes spatial phase:

```math
T=\frac1f=25\ \mu\mathrm{s},\qquad
\lambda=\frac{c_0}{f}=8.580\ \mathrm{mm},\qquad
\omega=2\pi f,\qquad k=\frac{2\pi}{\lambda}=732.306\ \mathrm{m^{-1}}.
```

Temperature affects the wavelength through sound speed. For an ideal gas, the ratio of specific heats is γ, the specific gas constant is Rₛ and absolute temperature is Θ:

```math
c_0=\sqrt{\gamma R_s\Theta},\qquad \frac{\delta\lambda}{\lambda}\simeq\frac{\delta\Theta}{2\Theta}\quad(f=\mathrm{const}).
```

## 2. From conservation laws to the wave equation

Pressure and density consist of a static value and a small acoustic perturbation. In an otherwise stationary, homogeneous fluid, conservation of mass and momentum and the linear pressure–density relation give:

```math
p=p_0+p_1,\qquad \rho=\rho_0+\rho_1,
\qquad p_1=c_0^2\rho_1,
\\
\frac{\partial\rho_1}{\partial t}+\rho_0\nabla\cdot\mathbf v_1=0,
\qquad \rho_0\frac{\partial\mathbf v_1}{\partial t}=-\nabla p_1.
```

Taking a time derivative of continuity and substituting momentum eliminates velocity. A harmonic solution uses a complex pressure amplitude P and the time convention shown below. The physical pressure is its real part; the complex velocity follows from the pressure gradient [2, 3]:

```math
\nabla^2p_1-\frac1{c_0^2}\frac{\partial^2p_1}{\partial t^2}=0,
\qquad p_1(\mathbf r,t)=\mathrm{Re}\{P(\mathbf r)e^{i\omega t}\},
\\
\nabla^2P+k^2P=0,\qquad
\mathbf V=-\frac{\nabla P}{i\omega\rho_0}.
```

## 3. Standing waves and phase

Two equal waves travelling in opposite directions interfere to form a standing wave. With an appropriate origin, their pressure and axial velocity are:

```math
p_1(z,t)=p_a\cos(kz)\cos(\omega t),\qquad
v_{1z}(z,t)=\frac{p_a}{\rho_0c_0}\sin(kz)\sin(\omega t),
\\
z_n=\frac{(2n+1)\lambda}{4},\qquad
\Delta z=\frac\lambda2=4.290\ \mathrm{mm}.
```

Pressure nodes have zero pressure amplitude and maximum velocity amplitude. Antinodes have the opposite behaviour. The actual focused field is three-dimensional, so the plane-wave node spacing is a reference rather than an exact list of trap positions.

The firmware provides relative phases of 0° and 180°. In the plane-wave limit a phase change moves the pattern by:

```math
|\Delta z|=\frac{|\Delta\phi|}{2k}=\frac{\lambda|\Delta\phi|}{4\pi},
\qquad |\Delta z|_{\Delta\phi=\pi}=2.145\ \mathrm{mm}.
```

For a plane resonant cavity, separation can satisfy an integer half-wavelength condition. The concave design instead places all faces at a common geometric focus; its 180 mm pole separation is not rounded to that cavity condition:

```math
L_{\mathrm{plane\ cavity}}=n\frac\lambda2,\qquad n\in\mathbb N.
```

## 4. Why a zero-mean wave can exert a mean force

Pressure and velocity average to zero over a period, but their squares do not. Radiation force comes from second-order momentum transfer through scattering [2, 3]. For peak phasors, the time averages contain a factor of one half:

```math
\langle p_1^2\rangle=\frac{|P|^2}{2},\qquad
\langle|\mathbf v_1|^2\rangle=\frac{|\mathbf V|^2}{2},
\\
e_{\mathrm{ac}}=\frac{p_1^2}{2\rho_0c_0^2}+\frac{\rho_0|\mathbf v_1|^2}{2}.
```

A travelling plane wave has the intensity below. Complete absorption and specular reflection at a flat surface give radiation pressures of I/c₀ and 2I/c₀ respectively. A small sphere is not a flat reflector, so its force needs a scattering-based expression. An ideal standing wave can have zero net travelling intensity and still exert a gradient force.

```math
I=\langle p_1v_1\rangle=\frac{p_{\mathrm{rms}}^2}{\rho_0c_0}\quad\text{(travelling plane wave)}.
```

## 5. Particle properties and the Gor’kov potential

The particle model is a sphere of radius 0.30 mm and density 30 kg/m³, representing a light foam bead. A compressibility of 2.5 × 10⁻¹⁰ Pa⁻¹ was used as a stiff-particle approximation. The result is conditional on this stiff-particle approximation for the porous material. The host-fluid compressibility, particle volume and two contrast factors are:

```math
\kappa_0=\frac1{\rho_0c_0^2},\qquad V_p=\frac{4\pi a^3}{3},
\qquad f_1=1-\frac{\kappa_p}{\kappa_0},\qquad
f_2=\frac{2(\rho_p-\rho_0)}{2\rho_p+\rho_0}.
```

The monopole coefficient describes compressibility contrast; the dipole coefficient describes density contrast. In the small-sphere, inviscid approximation, the time-averaged potential and force are [2, 3]:

```math
U_G=V_p\left[\frac{f_1\kappa_0}{2}\langle p_1^2\rangle
-\frac{3f_2\rho_0}{4}\langle|\mathbf v_1|^2\rangle\right]
=V_p\left[\frac{f_1|P|^2}{4\rho_0c_0^2}-\frac{3f_2\rho_0|\mathbf V|^2}{8}\right],
\\
\mathbf F_{\mathrm{rad}}=-\nabla U_G.
```

For the one-dimensional standing wave, collecting the spatial terms gives the expression below. Here Φ is defined explicitly; some literature uses a contrast factor three times smaller. Positive Φ gives stable pressure-node positions in the absence of gravity.

```math
E_{\mathrm{ac}}=\frac{p_a^2}{4\rho_0c_0^2},\qquad
\Phi=f_1+\frac32f_2,\qquad
F_{\mathrm{rad},z}=V_pkE_{\mathrm{ac}}\Phi\sin(2kz).
```

## 6. Gravity and stability in three dimensions

With the vertical axis pointing upward, buoyancy reduces the effective weight. Equilibrium requires zero net force; local stability requires a restoring force after a small displacement.

```math
W_{\mathrm{eff}}=(\rho_p-\rho_0)V_pg,\qquad
\mathbf F_{\mathrm{net}}=\mathbf F_{\mathrm{rad}}-W_{\mathrm{eff}}\hat{\mathbf z},
\\
U_{\mathrm{total}}=U_G+W_{\mathrm{eff}}z,\qquad
\mathbf F_{\mathrm{net}}(\mathbf r_0)=\mathbf0,\qquad
K_{ij}=\frac{\partial^2U_{\mathrm{total}}}{\partial x_i\partial x_j}
=-\frac{\partial F_{\mathrm{net},i}}{\partial x_j}.
```

All three eigenvalues of the stiffness matrix must be positive. An axial force crossing alone does not establish sideways trapping. In the numerical calculation the force Jacobian is symmetrised before evaluating its eigenvalues.

The ideal plane-wave support condition and corresponding pressure threshold are:

```math
kE_{\mathrm{ac}}|\Phi|>(\rho_p-\rho_0)g,\qquad
p_{a,\min}=\sqrt{\frac{4\rho_0c_0^2(\rho_p-\rho_0)g}{k|\Phi|}}
=301.20\ \mathrm{Pa}.
```

This is a necessary force-amplitude threshold for the one-dimensional reference, not a lateral-stability threshold for the actual array. Volume cancels because weight and Rayleigh force both scale with particle volume. It does not make arbitrarily large particles valid.

## 7. Curved-array geometry and the source field

Each set of 36 transmitters was arranged on three hexagonal rings, with 18 mm projected pitch and a 90 mm focus radius. The 16 × 13 mm can dimensions come from approximate measurements. The 16.4 mm bores, 15 mm shell and enlarged 220 × 158 mm base accommodate these parts. A point on the upper or lower spherical surface and its inward normal satisfy:

```math
\mathbf r_n=(x_n,y_n,\ \pm\sqrt{R^2-x_n^2-y_n^2}),\qquad
|\mathbf r_n|=R=90\ \mathrm{mm},\qquad \mathbf n_n=-\frac{\mathbf r_n}{R}.
```

Equal propagation distances and inward axes provide geometric focusing [1]. The array pressure sums forward-radiating baffled-piston far fields. J₁ is the first-order Bessel function, b is the effective piston radius, dₙ is source-to-observation distance, and θₙ is the angle to the inward normal:

```math
P(\mathbf r)=\sum_{n=1}^{72} A_{\mathrm{ref}}\frac{r_{\mathrm{ref}}}{d_n}
D(\theta_n)e^{-ikd_n+i\phi_n},\qquad
D(\theta)=\frac{2J_1(kb\sin\theta)}{kb\sin\theta},\quad D(0)=1,
\\
b=6\ \mathrm{mm},\qquad r_{\mathrm{ref}}=0.1\ \mathrm m,\qquad
A_{\mathrm{ref}}=\frac{1500R}{72r_{\mathrm{ref}}}=18.75\ \mathrm{Pa}.
```

Sources contribute only in their forward hemisphere. The assumed 6 mm active radius is distinct from the 8 mm can radius. Reference amplitude is fixed once at the nominal geometry and retained in comparisons. Pressure-gradient velocity is used throughout; a plane-wave impedance relation is not imposed on the focused field.

The prescribed field excludes enclosure reflections, mutual source coupling, real membrane modes, thermoviscous losses, streaming, amplitude/phase mismatch and nonlinear propagation. A small-particle potential also omits interparticle scattering. These assumptions set the scope of the reported counts and masses.

![Mechanical assembly](../results/concave_preview.png)

The two cups share one frame; the tabs meet supporting shelves. The rendering shows the enlarged geometry.

## 8. Pressure, potential and force along the axis

![Axial field](../results/standing_wave_field.png)

The upper panel shows peak pressure magnitude. The middle panel adds gravity to the acoustic potential; a local minimum is a candidate vertical equilibrium. The lower panel compares upward acoustic force with effective weight. A crossing is vertically stable when the acoustic-force curve slopes downward. The plots explain why a pressure node alone is not a complete equilibrium test.

The nearest stable positive-axis equilibrium at 40 kHz is 2.3615 mm from the common focus. The force there balances 31.9377 nN of effective weight.

| Frequency, kHz | Wavelength, mm | Equilibrium z, mm | K₁, µN/m | K₂, µN/m | K₃, µN/m |
|---:|---:|---:|---:|---:|---:|
| 38.0000 | 9.0316 | 2.4836 | 47.7405 | 47.7405 | 720.5525 |
| 40.0000 | 8.5800 | 2.3615 | 52.9028 | 52.9028 | 798.4328 |
| 42.0000 | 8.1714 | 2.2508 | 58.3301 | 58.3301 | 880.2910 |

All three eigenvalues are positive at these selected equilibria. The frequency comparison holds the source amplitude constant and excludes the frequency-dependent resonance response of a transmitter.

## 9. What focusing changes

![Planar and concave fields](../results/array_field_2d.png)

Both maps use the same 72 source amplitudes and one colour scale in the vertical plane through the axis. The curved array brings equal-phase waves together at the common focus. The planar comparison keeps common electrical phase rather than compensating propagation distances individually. Thus this figure compares two geometries under the same two-channel control; it is not a claim that electronically focused planar arrays cannot levitate.

## 10. Phase and geometric sensitivity

![Phase comparison](../results/phase_sensitivity.png)

Changing the bank phase from 0 to 180° changes the centre from constructive interference to cancellation and moves the nearby pressure pattern. The curve is pressure only: it does not by itself show stable loaded positions.

![Frequency and separation](../results/frequency_separation_map.png)

This map changes frequency and symmetrically moves the two arrays apart or together, while retaining their source orientations and amplitudes. It shows sensitivity to geometric focus misalignment. It is not a transducer resonance curve: frequency-dependent electrical impedance, source output and cavity reflections are absent.

## 11. Sideways confinement

![Lateral stability](../results/lateral_stability.png)

This section passes through the selected vertical equilibrium. The potential rises on either side of the axis and the lateral force points back toward the centre for small displacements. That is the local mechanism preventing the bead from simply falling sideways out of an otherwise vertically stable layer. Positive stiffness describes small displacements; it does not specify the complete capture region or loading dynamics.

## 12. How many objects can occupy a vertical column?

The reference plane-wave spacing is 4.290 mm. A central interval from −62 to +62 mm was scanned, inset 10 mm from the closest opposed face-centre planes. For a uniform node lattice, the maximum number of nodes that can fit in an interval of length L is:

```math
N_{\mathrm{plane,max}}=\left\lfloor\frac{L}{\lambda/2}\right\rfloor+1=\left\lfloor\frac{124}{4.290}\right\rfloor+1=29.
```

This number only describes a uniform plane-wave lattice; it is not a guaranteed count or a rigorous upper bound for the nonuniform focused field. The actual calculation finds force–weight crossings and evaluates all three stiffness eigenvalues at each crossing.

![Vertical trapping positions](../results/vertical_capacity.png)

The upper panel marks the equilibria on the force curve. Green points have three positive stiffness eigenvalues; red crosses lose lateral confinement. The lower panel shows those eigenvalues explicitly. There are **18 axially stable equilibria, including 15 locally stable three-dimensional sites**, for an isolated model particle at 1.5 kPa reference pressure. The count is unchanged when the scan grid is halved from 0.10 to 0.05 mm and the finite-difference step from 20 to 10 µm.

The table gives every axially stable position in the scanned interval:

| z, mm | Minimum stiffness, µN/m | 3-D stable |
|---:|---:|---|
| -39.6780 | 3.8110 | Yes |
| -34.7094 | 3.1700 | Yes |
| -30.4404 | -5.7870 | No |
| -26.6466 | 0.8747 | Yes |
| -21.7573 | 11.4235 | Yes |
| -16.9031 | 24.5050 | Yes |
| -12.0691 | 37.5331 | Yes |
| -7.2502 | 47.8106 | Yes |
| -2.4414 | 53.2892 | Yes |
| 2.3615 | 52.9077 | Yes |
| 7.1617 | 46.6205 | Yes |
| 11.9592 | 35.3752 | Yes |
| 16.7438 | 21.0100 | Yes |
| 21.4647 | 5.6839 | Yes |
| 25.8145 | -8.7864 | No |
| 33.9018 | 4.0173 | Yes |
| 38.7466 | 0.6267 | Yes |
| 43.1816 | -6.5920 | No |

One particle per stable site gives a **15-particle independent-occupancy scenario** within the single-particle model. Particles scatter sound, perturb one another and may merge or destabilise during loading. This model does not solve those interactions, off-axis traps or equilibria outside the stated interval. The simultaneous-occupancy problem additionally depends on these interactions.

## 13. Particle mass, weight and size limits

Mass is not the same as force: mass is reported in micrograms, weight in nanonewtons. For the selected sphere:

```math
m=\rho_p\frac{4\pi a^3}{3}=3.39292\times10^{-9}\ \mathrm{kg}
=3.39292\ \mu\mathrm g=0.00339292\ \mathrm{mg},
\\
mg=33.2732\ \mathrm{nN},\qquad W_{\mathrm{eff}}=31.9377\ \mathrm{nN},
\qquad M_{15}=15m=50.8938\ \mu\mathrm g=0.0508938\ \mathrm{mg}.
```

The summed mass assumes independent occupancy of all 15 sites. It is not a single payload supported by one trap.

The small-sphere approximation requires the size parameter to be much smaller than one. A value of 0.3 was adopted as an explicit modelling cutoff, not a physical maximum levitated size:

```math
ka=\frac{2\pi a}{\lambda}=0.21969,\qquad
ka\le0.3\ \Longrightarrow\ a\le0.409665\ \mathrm{mm},
\\
m_{ka\le0.3,\,\rho_p=30}=8.63964\ \mu\mathrm g.
```

At fixed material properties, both weight and force scale with volume, so this model gives the same equilibrium locations within its small-particle approximation. The 8.640 µg value is the mass at the chosen validity cutoff of the small-particle model.

The largest sampled upward acoustic force for the original 0.30 mm particle is 616.619 nN. Its force-equivalent supported mass, including buoyancy, is 63.014 µg:

```math
m_{\mathrm{force\ equivalent}}=\frac{\max_zF_{\mathrm{rad},z}}g+\rho_0V_p=63.014\ \mu\mathrm g.
```

This is a force-margin diagnostic for the specified particle, not a permissible replacement-particle mass: changing density changes contrast, and changing size changes both scattering and weight. A true maximum payload requires those properties and the actual acoustic amplitude. Force scales with pressure squared, so halving pressure quarters acoustic force; the number of supported stable sites can also change.

```math
P\mapsto\alpha P\quad\Longrightarrow\quad U_G\mapsto\alpha^2U_G,\qquad \mathbf F_{\mathrm{rad}}\mapsto\alpha^2\mathbf F_{\mathrm{rad}}.
```

## 14. Electrical drive and its relation to acoustics

Arduino Uno generates 40 kHz from a 16 MHz timer clock. The 74HC14 supplies complementary bridge inputs and the TB6612FNG applies differential voltage to each bank. Logic uses 5 V; the selected bridge supply is 9 V. Each bank has a 22 Ω, 3 W series resistor. For the ideal bridge:

```math
f=\frac{16\,000\,000}{399+1}=40\,000\ \mathrm{Hz},\qquad
V_{\mathrm{bridge,pp}}=2V_M=18\ \mathrm V.
```

The HC-SR04 module emits short ranging bursts and has separate transmit and receive cans [4]. The selected parts are detached transmitters. The module's 5 V rating does not specify their continuous AC drive limit. A capacitance of 2 nF per can was adopted as an assumed input for the electrical sensitivity calculation. A nominal capacitive bank gives:

```math
C_{\mathrm{bank}}=36C_T=72\ \mathrm{nF},\qquad
|X_C|=\frac1{2\pi fC_{\mathrm{bank}}}=55.26\ \Omega,
\\
i_C=C\frac{dv_C}{dt},\qquad P_R=R\langle i^2\rangle=RI_{\mathrm{rms}}^2.
```

A square wave contains harmonics, so its edge current cannot be estimated from the fundamental reactance alone. SPICE integrates the charging transients through the resistor and a 0.5 Ω total bridge resistance [5]. The capacitance-only approximation omits motional resonance; near 40 kHz the actual complex impedance can differ substantially.

![Electrical model](../results/driver_response.png)

The first panel shows bridge and bank voltage over three steady-state periods; the second shows edge-current pulses. The third gives resistor dissipation for nine sensitivity cases. At the selected 9 V and nominal 72 nF, bank voltage is 17.983 V peak-to-peak, RMS current 201.6 mA, peak current 775.4 mA, and resistor power 0.895 W per bank. The largest resistor power in the sweep is 1.074 W. These values describe the ideal circuit; semiconductor switching losses, parasitic inductance, heating and the acoustic conversion efficiency are absent.
