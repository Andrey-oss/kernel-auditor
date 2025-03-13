import subprocess

def run_cmd(command: str) -> str:
    result = subprocess.run(command, shell=True, stderr=subprocess.PIPE)
    if result.returncode != 0 or result.stderr:
        return result.stderr.strip()
    return None

def run_cmd_with_output(command: str) -> str:
    result = subprocess.run(command, capture_output=True, text=True, shell=True)
    return result