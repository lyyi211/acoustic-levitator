"""Check root selection against an analytic restoring-force example."""
import sys
from pathlib import Path
import numpy as np
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/"simulation"))
from trap_analysis import stable_axial_roots


def test_restoring_crossings_and_endpoint_roots():
    z=np.linspace(-2*np.pi,2*np.pi,1601)
    lo,hi=stable_axial_roots(z,-np.sin(z)-0.2)
    expected=np.array([-np.arcsin(0.2),2*np.pi-np.arcsin(0.2)])
    assert len(lo)==2
    assert np.all(lo<=expected) and np.all(expected<=hi)
    lo,hi=stable_axial_roots([-1,0,1],[1,0,-1])
    np.testing.assert_array_equal(lo,[-1])
    np.testing.assert_array_equal(hi,[0])


def test_no_stable_crossing_in_uniform_or_antirestoring_force():
    for values in ([1,1,1],[-1,0,1],[0,0,0]):
        lo,hi=stable_axial_roots([-1,0,1],values)
        assert len(lo)==len(hi)==0
