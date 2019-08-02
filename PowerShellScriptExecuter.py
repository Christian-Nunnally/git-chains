import os
import subprocess

class PowerShellScriptExecuter:

    def __init__(self):
        self.supress_output = False

    def execute(self, script_path):
        p = None
        args = ["powershell.exe", script_path]
        if (self.supress_output):
            p = subprocess.Popen(args, stdout=open(os.devnull, 'w'), stderr=open(os.devnull, 'w'))
        else:
            p = subprocess.Popen(args)
        p.communicate()