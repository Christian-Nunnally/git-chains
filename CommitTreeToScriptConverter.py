import os
import uuid


class CommitTreeToScriptConverter:
    def __init__(self, skip_single_child_nodes, post_conversion_commands, script_file):
        self.skip_single_child_nodes = skip_single_child_nodes
        self.post_conversion_commands = post_conversion_commands
        self.print_debug = False
        self.script_file = script_file

    def convert_commit_tree_to_script(self, commit_tree_to_copy):
        temp_dir = os.path.dirname(self.script_file.name)
        self.print_to_file("cd " + temp_dir)
        self.print_to_file("Invoke-Expression \"git init\"")
        self.recursivly_generate_git_commands(commit_tree_to_copy.root)
        self.print_all_to_file(self.get_fomatted_post_conversion_commands())

    def get_fomatted_post_conversion_commands(self):
        delete_master = ["git checkout master-real", "git branch -D master"]
        replace_master_real_with_master = ["git checkout -b master", "git branch -D master-real"]
        all_commands_to_add = delete_master + replace_master_real_with_master + self.post_conversion_commands
        return ["Invoke-Expression \"%s\"" % command for command in all_commands_to_add]
    
    def recursivly_generate_git_commands(self, current_commit):
        if self.should_skip_commit(current_commit):
            self.recursivly_generate_git_commands(current_commit.children[0])
            return

        commit_id = self.print_commands_to_make_commit_on_current_branch(current_commit.pretty_names[0])
        if current_commit.has_name:
            self.print_commands_to_make_branch_on_current_commit(current_commit)
        for child in current_commit.children:
            self.print_commands_required_for_child(child, current_commit.children[-1], commit_id)

    def should_skip_commit(self, commit):
        return self.skip_single_child_nodes and len(commit.children) == 1 and not commit.has_name

    def get_adjusted_branch_name(self, commit):
        if "master" in commit.pretty_names:
            return "master-real"
        return commit.pretty_names[0].replace(',', '')
    
    def print_commands_to_make_commit_on_current_branch(self, commit_message):
        commit_id = "$temp%s" % str(uuid.uuid4()).replace("-", "")
        self.print_to_file("New-Item %s.txt" % str(uuid.uuid4()).replace("-", ""))
        self.print_to_file("Invoke-Expression \"git add .\"")
        self.print_to_file("Invoke-Expression \"git commit -q -a -m '" + commit_message + "'\"")
        self.print_to_file(commit_id + " = Invoke-Expression \"git log --format='%H' -n 1\"")
        return commit_id
        
    def print_commands_to_make_branch_on_current_commit(self, commit):
        branch_name = self.get_adjusted_branch_name(commit)
        self.print_to_file("Invoke-Expression \"git branch %s\"" % branch_name)

    def print_commands_required_for_child(self, child, last_child, return_commit_id):
        self.recursivly_generate_git_commands(child)
        if not child == last_child:
            self.print_to_file("Invoke-Expression \"git checkout " + return_commit_id + "\"")

    def print_all_to_file(self, strings):
        for string in strings:
            self.print_to_file(string)

    def print_to_file(self, string):
        print(string, file=self.script_file)
        if self.print_debug:
            print(string)
