from CommitTreeToScriptConverter import CommitTreeToScriptConverter
from Interoperability.PowerShellScriptExecuter import PowerShellScriptExecuter


class GitRepositoryCopier:
    
    def __init__(self, tree, skip_single_child_nodes):
        self.skip_single_child_nodes = skip_single_child_nodes
        self.script_file_name = "\\repo-init.ps1"
        self.tree = tree
        self.id = 0

    def copy_repository(self, temp_dir, extra_commands):
        script_file_path = temp_dir + self.script_file_name
        self.write_copy_script(script_file_path, extra_commands)
        self.execute_script(script_file_path)

    def write_copy_script(self, script_file_path, extra_commands):
        with open(script_file_path, "x") as script_file:
            scriptWriter = CommitTreeToScriptConverter(self.skip_single_child_nodes)
            scriptWriter.convert_commit_tree_to_script(self.tree, script_file, extra_commands)

    def execute_script(self, script_file_path):
        executer = PowerShellScriptExecuter()
        executer.execute(script_file_path)
