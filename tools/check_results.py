"""Cross-check numerical exports and project files after a regeneration."""
import csv
import json
import sys
from pathlib import Path
import xml.etree.ElementTree as ET
import numpy as np
from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT/"simulation"))
from array_geometry import curved_array, load_design


def main():
    d=load_design()
    centres,normals,banks=curved_array(d)
    geometry=np.loadtxt(ROOT/"results/array_geometry.csv",delimiter=",",skiprows=1,usecols=range(2,8))
    assert geometry.shape==(len(centres),6) and np.isfinite(geometry).all()
    np.testing.assert_allclose(geometry[:,:3],centres*1e3,atol=1e-9)
    np.testing.assert_allclose(geometry[:,3:],normals,atol=1e-12)
    with (ROOT/"hardware/BOM.csv").open(newline="") as stream:
        bom={row["Reference"]:row for row in csv.DictReader(stream)}
    assert int(bom["TX1-TX72"]["Quantity"])==len(centres)
    print("PASS shared geometry: CAD/model layout and BOM describe 36+36 emitters")
    with (ROOT/"results/model_summary.csv").open(newline="") as stream:
        rows=list(csv.DictReader(stream))
    assert len(rows)==3
    for row in rows:
        values=[float(value) for key,value in row.items() if key!="locally_stable_3d"]
        assert np.isfinite(values).all()
        weight=float(row["effective_weight_N"])
        assert abs(float(row["Fz_N"])-weight)<weight*1e-6
        assert abs(float(row["Fx_N"]))<weight*1e-6
        assert abs(float(row["Fy_N"]))<weight*1e-6
        assert row["locally_stable_3d"]=="True"
        assert all(float(row[f"stiffness_eigenvalue_{i}_N_per_m"])>0 for i in (1,2,3))
    print("PASS conditional model equilibria: finite, gravity balanced, positive local 3-D stiffness")
    waves=np.loadtxt(ROOT/"results/driver_waveforms.csv",skiprows=1)
    assert waves.shape[1]==5 and len(waves)>3000 and np.isfinite(waves).all()
    assert np.all(np.diff(waves[:,0])>0)
    assert np.ptp(waves[:,2]) <= 2*d["bridge_supply_v"]*(1+1e-6)
    np.testing.assert_allclose(waves[:,4],d["series_resistance_ohm"]*waves[:,3]**2,rtol=1e-7,atol=1e-12)
    log=(ROOT/"results/validation/ngspice.log").read_text().lower()
    assert not any(word in log for word in ("error","warning","failed"))
    print("PASS ideal SPICE: finite waveform, time ordering, bank voltage and resistor power consistency")
    with (ROOT/"results/driver_sweep.csv").open(newline="") as stream:
        sweep=list(csv.DictReader(stream))
    assert len(sweep)==9
    assert all(np.isfinite([float(v) for v in row.values()]).all() for row in sweep)
    for name in ("standing_wave_field","phase_sensitivity","array_field_2d",
                 "frequency_separation_map","lateral_stability","concave_preview",
                 "vertical_capacity","driver_response"):
        with Image.open(ROOT/f"results/{name}.png") as image:
            image.verify()
    ET.parse(ROOT/"hardware/block_diagram.svg")
    metadata=json.loads((ROOT/"results/simulation_metadata.json").read_text())
    assert metadata["design"]==d and metadata["pressure_is_assumed_not_voltage_calibrated"]
    capacity=json.loads((ROOT/"results/capacity_summary.json").read_text())
    with (ROOT/"results/axial_traps.csv").open(newline="") as stream:
        traps=list(csv.DictReader(stream))
    assert len(traps)==capacity["axially_stable_count"]
    stable_count=0
    for row in traps:
        eigenvalues=np.array([float(row[f"K{i}_N_per_m"]) for i in (1,2,3)])
        assert np.isfinite(eigenvalues).all()
        assert abs(float(row["z_m"]))<=capacity["scan_half_width_m"]
        assert float(row["residual_force_N"])<capacity["effective_weight_N"]*1e-5
        stable=bool(np.all(eigenvalues>0))
        assert (row["stable_3d"]=="True")==stable
        stable_count+=stable
    assert stable_count==capacity["locally_stable_3d_count"]
    np.testing.assert_allclose(capacity["independent_particle_total_mass_kg"],
                               stable_count*capacity["particle_mass_kg"])
    assert not capacity["simultaneous_occupancy_validated"]
    assert metadata["capacity"]==capacity
    print("PASS capacity exports: force balance, stiffness, site count and independent-particle mass")
    print("PASS artifacts: nine sweep cases, eight valid PNGs, valid SVG and current assumption metadata")


if __name__=="__main__":
    main()
