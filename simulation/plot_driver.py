"""Electrical figures from the exported nominal waveform and sensitivity cases."""
from pathlib import Path
import csv
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
ROOT=Path(__file__).resolve().parents[1]


def main():
    data=np.loadtxt(ROOT/'results/driver_waveforms.csv',skiprows=1)
    selection=data[:,0]>=data[-1,0]-75e-6
    t=(data[selection,0]-data[-1,0]+75e-6)*1e6
    fig,axes=plt.subplots(3,1,figsize=(10,8),constrained_layout=True)
    axes[0].plot(t,data[selection,1],label='Bridge differential voltage')
    axes[0].plot(t,data[selection,2],label='Bank voltage')
    axes[0].set(xlabel='Time in final 75 us (us)',ylabel='Voltage (V)');axes[0].legend()
    axes[1].plot(t,data[selection,3]*1e3,color='tab:orange')
    axes[1].set(xlabel='Time in final 75 us (us)',ylabel='Bank current (mA)')
    with (ROOT/'results/driver_sweep.csv').open() as f:rows=list(csv.DictReader(f))
    for scale in (.8,1.,1.2):
        r=[x for x in rows if float(x['capacitance_scale'])==scale]
        axes[2].plot([float(x['bridge_supply_V']) for x in r],[float(x['resistor_power']) for x in r],'o-',label=f'Capacitance factor {scale:g}')
    axes[2].set(xlabel='Bridge supply (V)',ylabel='Mean resistor power (W)');axes[2].legend()
    for ax in axes:ax.grid(alpha=.25)
    fig.suptitle('Ideal electrical model: 72 nF bank, 22 ohm damping; nominal supply 9 V')
    fig.savefig(ROOT/'results/driver_response.png',dpi=180);plt.close(fig)

if __name__=='__main__':main()
