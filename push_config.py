# ~/yahboomcar_ws/src/yahboomcar_linefollw/cfg

param_defaults = {}

with open('LineDetectPID.cfg', 'r') as file:
    lines = file.readlines()

for line in lines:
    line = line.strip()
    if line.startswith('gen.add'):
        parts = [a.strip() for a in line.split('gen.add(')[-1].replace(')','').replace('"','').split(',')]
        # remove the parentheses and quotes around each part
        param_name = parts[0]
        default_value = parts[4]
        description = parts[3]
        min_value = parts[5]
        max_value = parts[6]

        param_defaults[param_name] = {
            "default": int(default_value) if description not in ['linear', 'ResponseDist'] else float(default_value),
            "min": int(min_value),
            "max": int(max_value) if description != 'linear' else 1.0,
            "description": description
        }

comment = '# ROSMASTER params\n'
import json
with open('LineDetectPID.py', 'w') as file:
    file.write(comment + json.dumps(param_defaults, indent=4))
