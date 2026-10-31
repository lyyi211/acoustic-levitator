"""Structural checks for machine-readable hardware deliverables."""

import csv
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def test_bom_is_rectangular_and_has_core_parts():
    with (ROOT / "hardware" / "BOM.csv").open(newline="", encoding="utf-8") as handle:
        rows = list(csv.DictReader(handle))
    assert rows
    assert all(None not in row for row in rows)
    references = {row["Reference"] for row in rows}
    assert {"U1", "U2", "U3", "TX1-TX72", "F1"} <= references
    by_reference = {row["Reference"]: row for row in rows}
    assert int(by_reference["TX1-TX72"]["Quantity"]) == 72
    assert int(by_reference["MECH1"]["Quantity"]) == 2
    assert int(by_reference["R2-R3"]["Quantity"]) == 2


def test_netlist_contains_safety_and_differential_bank_nets():
    with (ROOT / "hardware" / "netlist.csv").open(newline="", encoding="utf-8") as handle:
        nets = {row["Net"] for row in csv.DictReader(handle)}
    assert {"VM_FUSED", "BRIDGE_ENABLE", "BANK_A_P", "BANK_A_M",
            "BANK_B_P", "BANK_B_M", "BANK_A_LOAD", "BANK_B_LOAD"} <= nets
