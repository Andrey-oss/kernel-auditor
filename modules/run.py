# pylint: disable=subprocess-run-check
# Disabled due to bug with sysctl

'''Simple module for launching commands with subprocess'''

import subprocess
from decorators.data_validators import validate_data_type

@validate_data_type(str)
def run_cmd(command: str) -> str:
    """Returns only stderr or none"""

    result = subprocess.run(command, shell=True, stderr=subprocess.PIPE)
    if result.stderr:
        return result.stderr.strip().decode()
    return None

@validate_data_type(str)
def run_cmd_with_output(command: str) -> str:
    """Returns only stdout"""

    result = subprocess.run(command, capture_output=True, text=True, shell=True, check=True)
    return result.stdout
