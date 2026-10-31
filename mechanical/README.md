# Mechanical design

Two identical concave cups and a shared support frame were designed in OpenSCAD. Each cup contains 36 radial sockets in three hexagonal rings of 6, 12 and 18 elements. The selected components are transmitting cans desoldered from HC-SR04 modules, rather than complete ranging boards or receiver cans.

| Parameter | CAD value |
|---|---:|
| Transmitter body diameter / height | 16 / 13 mm |
| Socket diameter / seating depth | 16.4 / 13 mm |
| Projected centre pitch | 18 mm |
| Common focus radius | 90 mm |
| Cup outside diameter / shell thickness | 142 / 15 mm |
| Rear lead opening / central access opening | 6 / 8 mm |
| Base footprint | 220 × 158 mm |
| Mounting | Four M4 × 20 mm bolts, four nuts, eight washers |

The body dimensions come from approximate measurements of the available parts. The socket has 0.4 mm diametral clearance and a rear shoulder. The two cups face inward; each mounting tab rests on a frame shelf. The base, posts and shelves form a continuous part.

Face centres lie on a sphere about the common focus. The virtual poles are 180 mm apart; there is no emitter at either pole. The closest opposed face centres are 144 mm apart. These are geometric distances, not an imposed cavity resonance condition.

The CAD includes individual cup and frame models, an assembled view and a socket coupon. `design.json` supplies the dimensions shared by the CAD and acoustic model. Mesh analysis records connectivity, surface closure, winding and hole topology.
