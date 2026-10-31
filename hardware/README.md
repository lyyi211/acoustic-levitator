# Electronics

Arduino Uno, a TB6612FNG dual bridge and a 74HC14 inverter were selected for two coherent channels. The design uses 5 V logic and a 9 V bridge supply with a 1 A current limit. Each channel feeds 36 parallel transmitters through a 22 Ω, 3 W noninductive resistor.

| Signal | Connection |
|---|---|
| D9 / D10 | AIN1 / BIN1 and the two inverter inputs |
| Inverter outputs | AIN2 / BIN2 |
| D8 | STBY with a 100 kΩ pulldown |
| PWMA, PWMB, VCC | 5 V |
| AO1 / AO2 | Upper bank through R2 |
| BO1 / BO2 | Lower bank through R3 |
| VM | Fused 9 V supply |
| GND | Common return |

The design includes three 100 nF bypass capacitors and a 470 µF bulk capacitor.

The HC-SR04 board contains a transmitter, receiver and burst-ranging electronics. Only the transmitting cans are included in the array. The module's 5 V supply specification does not define the detached transmitter's continuous-drive rating.

A capacitance of 2 nF per transmitter was used for the electrical calculation. This capacitance is an assumed model input:

```math
C_{\mathrm{bank}}=36C_T=72\ \mathrm{nF},\qquad V_{\mathrm{bridge,pp}}=2V_M=18\ \mathrm{V}.
```

The nominal ideal circuit gives 17.983 V peak-to-peak at the bank, 201.6 mA RMS, 775.4 mA peak and 0.895 W resistor dissipation per bank. The sensitivity study covers 5, 7 and 9 V and capacitance factors 0.8, 1.0 and 1.2.

`Reference` in the BOM means the component's schematic identifier, not a citation or supplier. `U1` identifies Arduino Uno; `U2` and `U3` identify the bridge and inverter; `TX1–TX72` identify the transmitters. `R`, `C`, `F`, `J`, `PS` and `MECH` denote resistors, capacitors, fuse, connectors, power supply and mechanical parts. Quantity is the number of physical parts represented by a row.
