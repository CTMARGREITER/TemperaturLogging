import subprocess

def run(cmd):
    output = subprocess.run(["powershell", "-Command", cmd], capture_output=True)
    completed = output.stdout.decode("utf-8").strip()
    return completed

if __name__ == "__main__":
    output = run("(gwmi win32_process -F \"CommandLine LIKE '%main.py%'\").Commandline")
    if "python.exe" in output:
        print("main.py is running")
    else:
        print("main.py is not running")
        subprocess.run(["./.venv/Scripts/python", "./main.py"])