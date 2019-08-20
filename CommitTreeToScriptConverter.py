import os
import uuid


class CommitTreeToScriptConverter:
    def __init__(self, skip_single_child_nodes):
        self.skip_single_child_nodes = skip_single_child_nodes
        self.print_debug = False

    def convert_commit_tree_to_script(self, commit_tree_to_copy, script_file, commands_to_add):
        temp_dir = os.path.dirname(script_file.name)
        commands_to_fix_master = ["git checkout master-real", "git branch -D master", "git checkout -b master", "git branch -D master-real"]
        commands_to_add_prefixed_with_commands_to_fix_master = commands_to_fix_master + commands_to_add

        self.print_to_file("cd " + temp_dir, script_file)

        self.print_to_file("Invoke-Expression \"git init\"", script_file)
        self.recursivly_generate_git_commands(commit_tree_to_copy.root, script_file)
        for command in commands_to_add_prefixed_with_commands_to_fix_master:
            self.print_to_file("Invoke-Expression \"%s\"" % command, script_file)

    def recursivly_generate_git_commands(self, current_commit, script_file):
        if self.skip_single_child_nodes and len(current_commit.children) == 1 and not current_commit.has_name:
            self.recursivly_generate_git_commands(current_commit.children[0], script_file)
            return

        commit_id = "$temp%s" % str(uuid.uuid4()).replace("-", "")

        self.print_commands_to_make_commit_on_current_branch(commit_id, script_file, "commit for " + current_commit.pretty_names[0])
        
        if current_commit.has_name:
            branch_name = current_commit.pretty_names[0]
            if "master" in current_commit.pretty_names:
                branch_name = "master-real"
            self.print_to_file("Invoke-Expression \"git branch %s\"" % branch_name.replace(',', ''), script_file)

        for child in current_commit.children:
            self.recursivly_generate_git_commands(child, script_file)
            if not child == current_commit.children[-1]:
                self.print_to_file("Invoke-Expression \"git checkout " + commit_id + "\"", script_file)

    def print_commands_to_make_commit_on_current_branch(self, commit_id, script_file, commit_message):
        self.print_to_file("New-Item %s.txt" % str(uuid.uuid4()).replace("-", ""), script_file)
        self.print_to_file("Invoke-Expression \"git add .\"", script_file)
        self.print_to_file("Invoke-Expression \"git commit -q -a -m '" + commit_message + "'\"", script_file)
        self.print_to_file(commit_id + " = Invoke-Expression \"git log --format='%H' -n 1\"", script_file)

    def print_to_file(self, string, file):
        print(string, file=file)
        if self.print_debug:
            print(string)
