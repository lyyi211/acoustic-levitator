# Numerical model

All 72 sources were modelled as oriented baffled pistons, and pressure, the Gor’kov potential, radiation force and local stiffness were calculated in three dimensions. Geometry comes from the same parameters as the OpenSCAD structure. The assumed active piston radius is 6 mm; the outside can radius is 8 mm.

The reference in-phase focus pressure is 1.5 kPa peak. It fixes the source amplitude once; phase, frequency and geometry comparisons retain that same amplitude. It is not calculated from the 9 V bridge supply. The material model is a spherical particle of radius 0.30 mm, density 30 kg/m³ and compressibility 2.5 × 10⁻¹⁰ Pa⁻¹.

The vertical scan covers −62 to +62 mm. It finds 18 axially stable equilibria, of which 15 also have positive stiffness in all three directions. These are isolated-particle positions. Simultaneous occupancy and scattering between particles are not modelled. Each particle has mass 3.393 µg; occupying all 15 positions would give an independent-particle total of 50.894 µg.

The scan uses a 0.10 mm grid, bisection of force crossings and 20 µm finite differences. A second calculation uses a 0.05 mm grid and 10 µm differences to check sensitivity. The field model excludes reflections, thermoviscous effects, acoustic streaming, source mismatch and nonlinear propagation. The complete derivation, figures and interpretation are collected in the physics chapter, directly accessible from the main README.
