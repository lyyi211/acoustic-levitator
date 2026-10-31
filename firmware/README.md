# Arduino Uno firmware

The Arduino Uno's 16 MHz ATmega328P and Timer1 were used to generate two coherent bank signals. D9 (OC1A) controls the upper array, D10 (OC1B) the lower array, and D8 the TB6612FNG standby input. The nominal frequency is 40 kHz; the firmware supports 38–42 kHz and relative phases of 0° and 180°.

Timer1 operates in Fast PWM mode 14 with no prescaler. At the nominal frequency:

```math
f=\frac{f_{\mathrm{CPU}}}{1+\mathrm{ICR1}}=\frac{16\,000\,000}{400}=40\,000\ \mathrm{Hz},\qquad \mathrm{ICR1}=399.
```

Both outputs have 50% duty at 40 kHz. Other requested frequencies are rounded to a whole number of timer ticks. Geometric focusing replaces individual emitter phase channels.

The serial interface runs at 115200 baud. Its commands are `F` for frequency, `P` for phase, `E` for bridge enable, `S` for state and `H` for command descriptions. The bridge is disabled on reset; changes to frequency or phase briefly disable it before restoring the previous state. Invalid arguments and oversized lines are rejected.

The source is `acoustic_levitator/acoustic_levitator.ino`.
