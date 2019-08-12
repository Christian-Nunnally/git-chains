from CommitTreeToScriptConverter import CommitTreeToScriptConverter
from PowerShellScriptExecuter import PowerShellScriptExecuter

class GitRepositoryCopier:
    
    def __init__(self, tree):
        self.tree = tree
        self.id = 0

    def copy_repository(self, temp_dir, extra_commands, skip_single_child_nodes):
        script_file_path = temp_dir + "\\repo-init.ps1"
        script_file = open(script_file_path, "x")

        post_commands = ["git checkout master-real", "git branch -D [master]"]
        commands = extra_commands + post_commands

        scriptWriter = CommitTreeToScriptConverter()
        scriptWriter.skip_single_child_nodes = skip_single_child_nodes
        scriptWriter.convert_commit_tree_to_script(self.tree, script_file, commands)

        script_file.close()
        executer = PowerShellScriptExecuter()
        executer.execute(script_file_path)
