import os
import subprocess


class PowerShellScriptExecuter:

    def __init__(self):
        self.args = ["powershell.exe"]
        self.supress_output = True

    def execute(self, script_path):
        self.args.append(script_path)
        self.execute_quiet() if self.supress_output else self.execute_verbose()

    def execute_quiet(self):
        process = subprocess.Popen(self.args, stdout=open(os.devnull, 'w'), stderr=open(os.devnull, 'w'))
        process.communicate()

    def execute_verbose(self):
        process = subprocess.Popen(self.args)
        process.communicate()
