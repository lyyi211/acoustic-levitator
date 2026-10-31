"""Physical invariants of shared geometry and the focused acoustic model."""
import sys
from pathlib import Path
import unittest
import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "simulation"))
from array_geometry import curved_array, hex_sites, load_design, mechanical_dimensions
from acoustic_model import (Medium, Particle, array_pressure, array_potential,
                            array_force, piston_directivity, gorkov_potential,
                            radiation_force, wave_number)


class ConcaveArrayTests(unittest.TestCase):
    def setUp(self):
        self.design = load_design()
        self.centres, self.normals, self.banks = curved_array(self.design)
        self.medium = Medium()

    def test_three_complete_hex_rings_and_no_central_emitter(self):
        for rings in (1, 2, 3):
            xy = hex_sites(rings, 0.011)
            self.assertEqual(len(xy), 3*rings*(rings+1))
            self.assertTrue(np.all(np.linalg.norm(xy, axis=1) > 0))
        self.assertEqual(np.count_nonzero(self.banks == 0), 36)
        self.assertEqual(np.count_nonzero(self.banks == 1), 36)

    def test_all_faces_are_equidistant_and_normals_intersect_common_focus(self):
        radius = self.design["curvature_radius_mm"] * 1e-3
        np.testing.assert_allclose(np.linalg.norm(self.centres, axis=1), radius, atol=1e-14)
        np.testing.assert_allclose(self.centres + radius*self.normals, 0, atol=1e-14)
        np.testing.assert_allclose(self.centres[:36,:2], self.centres[36:,:2])
        np.testing.assert_allclose(self.centres[:36,2], -self.centres[36:,2])

    def test_socket_spacing_and_rear_shoulders_have_material(self):
        upper = self.centres[self.banks == 0] * 1e3
        distances = np.linalg.norm(upper[:,None,:] - upper[None,:,:], axis=-1)
        np.fill_diagonal(distances, np.inf)
        bore = self.design["transducer_diameter_mm"] + self.design["socket_clearance_mm"]
        self.assertGreater(distances.min() - bore, 0.5)
        self.assertGreater(self.design["shell_thickness_mm"] - self.design["transducer_body_height_mm"], 1.5)
        dims = mechanical_dimensions(self.design)
        self.assertLess(dims["base_top_mm"], -self.design["curvature_radius_mm"] - self.design["shell_thickness_mm"])
        self.assertAlmostEqual(dims["lower_seat_z_mm"], -dims["upper_seat_z_mm"] - self.design["ear_thickness_mm"])

    def test_coherent_focus_pressure_is_sum_of_72_equal_contributions(self):
        pressure = array_pressure(np.zeros((1,3)), self.centres, self.normals,
                                 np.zeros(72), 40000, self.medium)
        self.assertAlmostEqual(abs(pressure[0]), 72*0.1/(self.design["curvature_radius_mm"]*1e-3), places=10)

    def test_opposed_phase_cancels_centre_pressure(self):
        pressure = array_pressure(np.zeros((1,3)), self.centres, self.normals,
                                 self.banks*np.pi, 40000, self.medium)
        self.assertLess(abs(pressure[0]), 1e-10)

    def test_piston_axis_and_small_angle_limit(self):
        argument = np.array([0, 0.001, -0.001])
        expected = 1 - argument**2/8 + argument**4/192
        np.testing.assert_allclose(piston_directivity(argument), expected, atol=1e-14)

    def test_pressure_gradient_velocity_reproduces_analytical_potential(self):
        frequency, peak = 40000.0, 1500.0
        k = wave_number(frequency, self.medium)
        points = np.array([[0.001, 0.001, 0.0004], [0, 0, 0.0018]])
        field = lambda p: peak*np.cos(k*p[...,2]) + 0j
        numerical = array_potential(points, field, frequency, self.medium, Particle(), step=2e-6)
        analytical = gorkov_potential(points[:,2], frequency, peak, 0, 0, self.medium, Particle())
        np.testing.assert_allclose(numerical, analytical, rtol=5e-6, atol=1e-15)

    def test_vector_force_reproduces_plane_wave_and_has_no_lateral_component(self):
        frequency, peak = 40000.0, 1500.0
        k = wave_number(frequency, self.medium)
        points = np.array([[0.001, 0.001, 0.0004], [0, 0, 0.0018]])
        field = lambda p: peak*np.cos(k*p[...,2]) + 0j
        force = array_force(points, field, frequency, self.medium, Particle(), step=2e-6)
        analytical = radiation_force(points[:,2], frequency, peak, 0, 0, self.medium, Particle())
        np.testing.assert_allclose(force[:,2], analytical, rtol=5e-6, atol=1e-14)
        np.testing.assert_allclose(force[:,:2], 0, atol=1e-14)

    def test_focusing_rejects_impossible_radius(self):
        with self.assertRaises(ValueError):
            curved_array({**self.design, "curvature_radius_mm": 20})


if __name__ == "__main__":
    unittest.main()
