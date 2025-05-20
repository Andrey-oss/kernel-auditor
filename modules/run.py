import subprocess

def run_cmd(command: str) -> str:
    """Returns only stderr or none"""
    
    result = subprocess.run(command, shell=True, stderr=subprocess.PIPE)
    if result.stderr:
        return result.stderr.strip().decode()
    return None

def run_cmd_with_output(command: str) -> str:
    """Returns only stdout"""

    result = subprocess.run(command, capture_output=True, text=True, shell=True)
    return result.stdout