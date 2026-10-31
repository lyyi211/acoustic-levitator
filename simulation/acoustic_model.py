"""Acoustic levitation models in SI units: analytical 1-D and focused 3-D arrays.

The analytical reference superposes counter-propagating plane waves; the array
model sums oriented piston sources and derives velocity from pressure gradients. Gor'kov's
small-sphere potential is used, so the particle radius must satisfy k*a << 1.
Losses, finite apertures, streaming, viscosity and transducer coupling are
outside the scope of this first-order model.
"""

from dataclasses import dataclass
import numpy as np


@dataclass(frozen=True)
class Medium:
    density: float = 1.2041  # kg/m^3, dry air near 20 degC
    sound_speed: float = 343.2  # m/s

    @property
    def compressibility(self) -> float:
        return 1.0 / (self.density * self.sound_speed**2)


@dataclass(frozen=True)
class Particle:
    radius: float = 0.30e-3  # m; ka=0.22 at 40 kHz
    density: float = 30.0  # kg/m^3, representative expanded polystyrene
    compressibility: float = 2.5e-10  # 1/Pa, approximate solid polymer value

    @property
    def volume(self) -> float:
        return 4.0 * np.pi * self.radius**3 / 3.0


def contrast_factors(medium: Medium, particle: Particle) -> tuple[float, float]:
    """Return monopole f1 and dipole f2 Gor'kov contrast factors."""
    f1 = 1.0 - particle.compressibility / medium.compressibility
    f2 = 2.0 * (particle.density - medium.density) / (
        2.0 * particle.density + medium.density
    )
    return f1, f2


def wave_number(frequency: float, medium: Medium) -> float:
    return 2.0 * np.pi * frequency / medium.sound_speed


def pressure_amplitude(
    z: np.ndarray, frequency: float, pressure_peak: float, separation: float,
    phase_difference: float, medium: Medium,
) -> np.ndarray:
    """Standing-wave pressure amplitude; pressure_peak is its antinode peak."""
    q = wave_number(frequency, medium) * (z - separation / 2.0) + phase_difference / 2.0
    return pressure_peak * np.cos(q)


def velocity_amplitude(
    z: np.ndarray, frequency: float, pressure_peak: float, separation: float,
    phase_difference: float, medium: Medium,
) -> np.ndarray:
    q = wave_number(frequency, medium) * (z - separation / 2.0) + phase_difference / 2.0
    return pressure_peak * np.sin(q) / (medium.density * medium.sound_speed)


def gorkov_potential(
    z: np.ndarray, frequency: float, pressure_peak: float, separation: float,
    phase_difference: float, medium: Medium, particle: Particle,
) -> np.ndarray:
    """Time-averaged Gor'kov potential energy in joules."""
    p = pressure_amplitude(z, frequency, pressure_peak, separation, phase_difference, medium)
    v = velocity_amplitude(z, frequency, pressure_peak, separation, phase_difference, medium)
    f1, f2 = contrast_factors(medium, particle)
    return particle.volume * (
        f1 * p**2 / (4.0 * medium.density * medium.sound_speed**2)
        - 3.0 * f2 * medium.density * v**2 / 8.0
    )


def radiation_force(
    z: np.ndarray, frequency: float, pressure_peak: float, separation: float,
    phase_difference: float, medium: Medium, particle: Particle,
) -> np.ndarray:
    """Analytical +z acoustic radiation force, equal to -dU/dz."""
    k = wave_number(frequency, medium)
    q = k * (z - separation / 2.0) + phase_difference / 2.0
    f1, f2 = contrast_factors(medium, particle)
    coefficient = (
        particle.volume * pressure_peak**2 * k
        * (f1 + 1.5 * f2) / (4.0 * medium.density * medium.sound_speed**2)
    )
    return coefficient * np.sin(2.0 * q)


def rayleigh_parameter(frequency: float, medium: Medium, particle: Particle) -> float:
    return wave_number(frequency, medium) * particle.radius


def point_source_field_2d(
    x: np.ndarray, z: np.ndarray, source_x: np.ndarray, source_z: np.ndarray,
    source_phase: np.ndarray, frequency: float, medium: Medium,
) -> np.ndarray:
    """Dimensionless complex field from coherent isotropic 2-D point sources.

    A 1/r spreading law is used as a qualitative array-factor approximation.
    It does not represent calibrated pressure from real baffled transducers.
    """
    field = np.zeros(np.broadcast_shapes(x.shape, z.shape), dtype=complex)
    k = wave_number(frequency, medium)
    for sx, sz, phase in zip(source_x, source_z, source_phase):
        distance = np.hypot(x - sx, z - sz)
        if np.any(distance <= 0.0):
            raise ValueError("Evaluation coordinates must not coincide with a source")
        field += np.exp(1j * (k * distance + phase)) / distance
    return field


def piston_directivity(argument: np.ndarray) -> np.ndarray:
    """2 J1(s)/s, using a convergent series for |s| <= 8.

    Avoids a SciPy dependency. The model piston arguments are checked against this range.
    This is a baffled-piston approximation, not measured transducer directivity.
    """
    argument = np.asarray(argument, dtype=float)
    if np.any(np.abs(argument) > 8):
        raise ValueError("Piston directivity series supports |ka sin(theta)| <= 8")
    term = np.ones_like(argument)
    result = term.copy()
    for m in range(1, 40):
        term = term * (-argument**2 / 4) / (m * (m + 1))
        result += term
    return result


def array_pressure(
    points: np.ndarray, centres: np.ndarray, normals: np.ndarray,
    phases: np.ndarray, frequency: float, medium: Medium,
    piston_radius: float = 4e-3, reference_peak: float = 1.0,
    reference_distance: float = 0.1,
) -> np.ndarray:
    """Peak pressure phasor in Pa from oriented far-field piston sources.

    Uses exp(-ikr) with exp(+iwt) time convention. The per-emitter reference
    pressure is an assumed or calibrated input, not predicted from voltage.
    Only the emitting forward hemisphere is included; reflections are omitted.
    """
    points = np.asarray(points, dtype=float)
    centres, normals = np.asarray(centres), np.asarray(normals)
    phases = np.asarray(phases)
    if points.shape[-1] != 3 or centres.shape != normals.shape or centres.shape[1] != 3:
        raise ValueError("Coordinates and normals must have three components")
    if phases.shape != (len(centres),):
        raise ValueError("Each source requires one phase")
    if not np.allclose(np.linalg.norm(normals, axis=1), 1.0):
        raise ValueError("Source normals must be unit vectors")
    k = wave_number(frequency, medium)
    pressure = np.zeros(points.shape[:-1], dtype=complex)
    for centre, normal, phase in zip(centres, normals, phases):
        delta = points - centre
        distance = np.linalg.norm(delta, axis=-1)
        if np.any(distance <= 0):
            raise ValueError("Evaluation point coincides with a source")
        cosine = np.clip(np.sum(delta * normal, axis=-1) / distance, -1, 1)
        argument = k * piston_radius * np.sqrt(np.maximum(0, 1 - cosine**2))
        directivity = np.where(cosine > 0, piston_directivity(argument), 0)
        pressure += reference_peak * reference_distance * directivity / distance * np.exp(
            -1j * k * distance + 1j * phase)
    return pressure


def array_potential(points: np.ndarray, field, frequency: float, medium: Medium,
                    particle: Particle, step: float = 20e-6) -> np.ndarray:
    """3-D Gor'kov potential using velocity from the complex pressure gradient."""
    points = np.asarray(points, dtype=float)
    pressure = field(points)
    velocity_squared = np.zeros(points.shape[:-1])
    for axis in range(3):
        offset = np.eye(3)[axis] * step
        gradient = (field(points + offset) - field(points - offset)) / (2 * step)
        velocity = -gradient / (1j * 2 * np.pi * frequency * medium.density)
        velocity_squared += np.abs(velocity)**2
    f1, f2 = contrast_factors(medium, particle)
    return particle.volume * (f1 * np.abs(pressure)**2 / (
        4 * medium.density * medium.sound_speed**2) - 3 * f2 * medium.density * velocity_squared / 8)


def array_force(points: np.ndarray, field, frequency: float, medium: Medium,
                particle: Particle, step: float = 20e-6) -> np.ndarray:
    points = np.asarray(points, dtype=float)
    force = np.empty_like(points)
    for axis in range(3):
        offset = np.eye(3)[axis] * step
        force[..., axis] = -(array_potential(points + offset, field, frequency, medium, particle, step)
                            - array_potential(points - offset, field, frequency, medium, particle, step)) / (2 * step)
    return force

