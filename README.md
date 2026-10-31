# Acoustic Levitator

English | [Українська](README.uk.md)

A 40 kHz acoustic levitator with two concave arrays was designed, and its Arduino Uno firmware, mechanical model and numerical calculations were developed. The design uses 72 transmitting cans desoldered from HC-SR04 modules, with 36 in each cup. The cups focus toward a common centre using their shape and emitter orientation.

OpenSCAD was used for the structure, Python for the acoustic field and particle forces, and ngspice for the electrical model.

![Acoustic levitator model](results/concave_preview.png)

## Selected design

| Parameter | Value |
|---|---|
| Controller | Arduino Uno, ATmega328P, 16 MHz |
| Nominal frequency / bank phase | 40 kHz / 0°; firmware also supports 38–42 kHz and 180° |
| Logic / bridge supply | 5 V / 9 V; bridge supply current limit 1 A |
| Bridge and inverter | TB6612FNG and 74HC14 |
| Series resistor per bank | 22 Ω, 3 W |
| Transmitter body | Approximately 16 mm diameter × 13 mm high, based on available parts |
| Socket diameter / projected pitch | 16.4 mm / 18 mm |
| Focus radius / base footprint | 90 mm / 220 × 158 mm |
| Acoustic model | 1.5 kPa prescribed peak focus pressure, 6 mm effective piston radius |
| Electrical model | 2 nF assumed per emitter; 72 nF per bank |

The HC-SR04 receiver cans and ranging boards are not part of the array. The detached transmitter's capacitance and continuous-drive rating are not established by the module's 5 V specification. The acoustic pressure and electrical load above are explicit model inputs.

## Calculated outcome

At 40 kHz, wavelength is 8.580 mm and plane-wave node spacing is 4.290 mm. A scan from −62 to +62 mm finds 15 locally stable three-dimensional sites for an isolated 0.30 mm-radius, 30 kg/m³ particle. Each particle has mass 3.393 µg. Filling all sites independently would total 50.894 µg; this independent-particle calculation excludes interparticle scattering.

Both physics chapters contain the derivation from basic acoustics, every result figure, the complete axial-equilibrium table, and the distinction between particle mass, force margin and model size limits.

## Project chapters

| Topic | English | Українська |
|---|---|---|
| Physics and all figures | [Physics and results](docs/physics.md) | [Фізика та результати](docs/physics.uk.md) |
| Structure | [Mechanical design](mechanical/README.md) | [Механічна модель](mechanical/README.uk.md) |
| Circuit | [Electronics and BOM notation](hardware/README.md) | [Електроніка та позначення BOM](hardware/README.uk.md) |
| Controller | [Arduino Uno firmware](firmware/README.md) | [Прошивка Arduino Uno](firmware/README.uk.md) |
| Calculation | [Numerical model](simulation/README.md) | [Чисельна модель](simulation/README.uk.md) |
| Outputs | [Calculation outputs](results/README.md) | [Результати розрахунків](results/README.uk.md) |
| Software | [Software used](tools/README.md) | [Використане ПЗ](tools/README.uk.md) |

## Source files and data

| Group | Direct links |
|---|---|
| CAD | [OpenSCAD](mechanical/levitator_frame.scad), [design.json](mechanical/design.json), [generated geometry](mechanical/generated_geometry.scad) |
| STL | [cup](results/concave_cup.stl), [frame](results/support_frame.stl), [assembly](results/levitator_frame.stl), [socket coupon](results/socket_fit_coupon.stl), [viewer](results/view_export.scad) |
| Electronics | [BOM](hardware/BOM.csv), [connections](hardware/netlist.csv), [diagram](hardware/block_diagram.svg), [SPICE](hardware/driver_tb6612.cir), [model parameters](hardware/generated_driver_params.inc) |
| Arduino | [acoustic_levitator.ino](firmware/acoustic_levitator/acoustic_levitator.ino) |
| Python | [field and force](simulation/acoustic_model.py), [geometry](simulation/array_geometry.py), [simulation](simulation/run_simulation.py), [trap analysis](simulation/trap_analysis.py), [electrical sweep](simulation/run_driver_sweep.py), [electrical plots](simulation/plot_driver.py) |
| Acoustic data | [geometry](results/array_geometry.csv), [frequency comparison](results/model_summary.csv), [all axial equilibria](results/axial_traps.csv), [capacity calculation](results/capacity_summary.json), [assumptions](results/simulation_metadata.json) |
| Electrical data | [waveforms](results/driver_waveforms.csv), [sensitivity study](results/driver_sweep.csv) |
| Verification | [tests](tests), [mesh analysis](results/mesh_validation.json), [mesh checker](tools/check_meshes.py), [result checker](tools/check_results.py) |

## Figures

[Axial force and potential](results/standing_wave_field.png) · [Field maps](results/array_field_2d.png) · [Phase](results/phase_sensitivity.png) · [Separation and frequency](results/frequency_separation_map.png) · [Lateral confinement](results/lateral_stability.png) · [Vertical sites](results/vertical_capacity.png) · [Electrical response](results/driver_response.png)

## Sources

The physics chapter uses the numbered references below.

1. Marzo, Barnes & Drinkwater, *TinyLev: A multi-emitter single-axis acoustic levitator* (2017). [Paper](https://doi.org/10.1063/1.4989995).
2. Gor’kov, *Forces acting on a small particle in an acoustic field within an ideal fluid* (1961). [Original work](https://www.mathnet.ru/eng/dan25473).
3. Bruus, *Acoustofluidics 7: The acoustic radiation force on small particles* (2012). [Author’s university record](https://orbit.dtu.dk/en/publications/acoustofluidics-7-the-acoustic-radiation-force-on-small-particles/).
4. ElecFreaks, *HC-SR04 ultrasonic ranging module*. [Datasheet](https://content.arduino.cc/assets/HCSR04.pdf).
5. Toshiba, *TB6612FNG*. [Datasheet](https://toshiba.semicon-storage.com/info/datasheet_en_20141001.pdf?did=10660).
