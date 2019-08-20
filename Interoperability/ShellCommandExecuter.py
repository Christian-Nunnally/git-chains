import subprocess


class ShellCommandExecuter:
    
    def __init__(self, current_working_directory, args):
        self.current_working_directory = current_working_directory
        self.args = args

    def execute_for_output(self):
        process = subprocess.run(self.args, stdout=subprocess.PIPE, cwd=self.current_working_directory)
        return process.stdout.decode('utf-8').strip()

    def execute_for_return_code(self):
        return subprocess.call(self.args, cwd=self.current_working_directory)