"""Numerical and analytical consistency tests for the acoustic model."""

import sys
from pathlib import Path
import unittest
import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "simulation"))

from acoustic_model import (  # noqa: E402
    Medium, Particle, contrast_factors, gorkov_potential, pressure_amplitude,
    radiation_force, rayleigh_parameter, wave_number,
    point_source_field_2d,
)


class AcousticModelTests(unittest.TestCase):
    def setUp(self) -> None:
        self.medium = Medium()
        self.particle = Particle()
        self.frequency = 40_000.0
        self.separation = 0.045
        self.peak = 1500.0

    def test_wavelength(self) -> None:
        wavelength = 2.0 * np.pi / wave_number(self.frequency, self.medium)
        self.assertAlmostEqual(wavelength, 0.00858, places=8)

    def test_pressure_is_periodic_over_wavelength(self) -> None:
        wavelength = self.medium.sound_speed / self.frequency
        z = np.linspace(0.0, self.separation, 101)
        p0 = pressure_amplitude(z, self.frequency, self.peak, self.separation, 0.3, self.medium)
        p1 = pressure_amplitude(z + wavelength, self.frequency, self.peak, self.separation, 0.3, self.medium)
        np.testing.assert_allclose(p0, p1, rtol=1e-12, atol=1e-9)

    def test_force_is_negative_potential_gradient(self) -> None:
        z = np.linspace(0.002, self.separation - 0.002, 20001)
        potential = gorkov_potential(z, self.frequency, self.peak, self.separation,
                                     0.2, self.medium, self.particle)
        numerical_force = -np.gradient(potential, z, edge_order=2)
        analytical_force = radiation_force(z, self.frequency, self.peak, self.separation,
                                            0.2, self.medium, self.particle)
        scale = np.max(np.abs(analytical_force))
        self.assertLess(np.max(np.abs(numerical_force[2:-2] - analytical_force[2:-2])) / scale, 2e-6)

    def test_force_scales_with_pressure_squared(self) -> None:
        z = np.array([0.021])
        f1 = radiation_force(z, self.frequency, 1000.0, self.separation, 0.0,
                             self.medium, self.particle)
        f2 = radiation_force(z, self.frequency, 2000.0, self.separation, 0.0,
                             self.medium, self.particle)
        np.testing.assert_allclose(f2, 4.0 * f1, rtol=1e-14)

    def test_default_particle_is_in_rayleigh_regime(self) -> None:
        ka = rayleigh_parameter(self.frequency, self.medium, self.particle)
        self.assertGreater(ka, 0.2)
        self.assertLess(ka, 0.3)  # conservative modelling target

    def test_default_contrast_is_positive(self) -> None:
        monopole, dipole = contrast_factors(self.medium, self.particle)
        self.assertGreater(monopole, 0.0)
        self.assertGreater(dipole, 0.0)

    def test_single_point_source_inverse_distance_scaling(self) -> None:
        field = point_source_field_2d(
            np.array([1.0, 2.0]), np.array([0.0, 0.0]),
            np.array([0.0]), np.array([0.0]), np.array([0.0]),
            self.frequency, self.medium,
        )
        self.assertAlmostEqual(abs(field[0]) / abs(field[1]), 2.0, places=12)


if __name__ == "__main__":
    unittest.main()
