# ~/yahboomcar_ws/src/yahboomcar_linefollw/cfg

import json, ast
import requests

PACKAGE = "yahboomcar_linefollw"

# Specify the URL of the param_defaults file on GitHub
param_defaults_url = 'https://raw.githubusercontent.com/tj-devstack/rosmaster-param/main/LineDetectPID.py'

# Retrieve the content of the param_defaults file
response = requests.get(param_defaults_url)
param_defaults_content = response.text

# Extract the dictionary from the param_defaults content
start_index = param_defaults_content.find("{")
end_index = param_defaults_content.rfind("}") + 1
param_defaults_dict_str = param_defaults_content[start_index:end_index]

# Convert the dictionary string to a dictionary
param_defaults = ast.literal_eval(param_defaults_dict_str)

line_config_code = "#!/usr/bin/env python\n"
line_config_code += 'PACKAGE = "yahboomcar_linefollw"\n'
line_config_code += "from dynamic_reconfigure.parameter_generator_catkin import *\n\n"
line_config_code += "gen = ParameterGenerator()\n"

for param_name, param_info in param_defaults.items():
    default_value = param_info["default"]
    min_value = param_info["min"]
    max_value = param_info["max"]
    description = param_info["description"]
    param_type = "double_t" if isinstance(default_value, float) else "int_t"
    line_config_code += f'gen.add("{param_name}", {param_type}, 0, "{description}", {default_value}, {min_value}, {max_value})\n'


line_config_code += 'exit(gen.generate(PACKAGE, "LineDetect", "LineDetectPID"))\n'

with open('LineDetectPID.cfg', 'w') as file:
    file.write(line_config_code)
