"""Sweep the ideal capacitive bank; explicitly reject ngspice's soft errors."""
import csv
from pathlib import Path
import re
import subprocess
from array_geometry import export_geometry, load_design

ROOT = Path(__file__).resolve().parents[1]


def main():
    export_geometry()
    design=load_design()
    deck=(ROOT/"hardware/driver_tb6612.cir").read_text()
    parameters=(ROOT/"hardware/generated_driver_params.inc").read_text()
    work=ROOT/".tools/tmp/driver-sweep"
    work.mkdir(parents=True,exist_ok=True)
    rows=[]
    keys=["vdiff_pp", "vbank_pp", "irms", "ipeak", "resistor_power"]
    for voltage in (5.0,7.0,9.0):
        for scale in (0.8,1.0,1.2):
            case=f"vm{voltage:g}-c{scale:g}"
            params=re.sub(r"VM=[\d.]+",f"VM={voltage}",parameters)
            params=params.replace("LOAD_SCALE=1 ",f"LOAD_SCALE={scale} ")
            text=deck.replace(".include hardware/generated_driver_params.inc",params)
            text=text.replace("results/driver_waveforms.csv",str((work/f"{case}.csv").relative_to(ROOT)))
            path=work/f"{case}.cir"
            path.write_text(text)
            run=subprocess.run(["ngspice","-b",str(path)],cwd=ROOT,text=True,capture_output=True)
            output=run.stdout+run.stderr
            (ROOT/f"results/validation/driver-{case}.log").write_text(output)
            if run.returncode or re.search(r"(?im)error|failed|warning",output):
                raise RuntimeError(f"SPICE failed in {case}: {output}")
            values=[]
            for key in keys:
                match=re.search(rf"(?m)^{key}\s*=\s*([-+\deE.]+)",output)
                if not match:
                    raise RuntimeError(f"Missing SPICE measurement {key} in {case}")
                values.append(float(match[1]))
            rows.append([voltage,scale,36*design["emitter_capacitance_pf"]*1e-12*scale,*values])
            print(case,dict(zip(keys,values)))
    with (ROOT/"results/driver_sweep.csv").open("w",newline="") as stream:
        writer=csv.writer(stream, lineterminator="\n")
        writer.writerow(["bridge_supply_V","capacitance_scale","bank_capacitance_F",*keys])
        writer.writerows(rows)


if __name__ == "__main__":
    main()
