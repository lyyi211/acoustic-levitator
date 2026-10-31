# Calculation outputs

This folder contains the mechanical exports, acoustic figures and numerical tables for the 16 × 13 mm transmitter design. The physics chapter includes the figures with explanations; direct links to every group of files are collected in the main README.

The mechanical files describe two cups, a shared frame, the assembly and a socket coupon. `mesh_validation.json` stores mesh properties. `array_geometry.csv` contains the 72 face centres and normals; `model_summary.csv` contains equilibria at 38, 40 and 42 kHz. `axial_traps.csv` lists every axially stable equilibrium in the scanned interval and its three stiffness eigenvalues. `capacity_summary.json` records the particle mass, site count and stated modelling limits.

`simulation_metadata.json` records the assumptions. `driver_waveforms.csv` is a whitespace-separated table of time, bridge voltage, bank voltage, current and resistor power. `driver_sweep.csv` contains nine electrical sensitivity cases.
