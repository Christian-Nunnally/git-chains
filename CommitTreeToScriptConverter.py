import subprocess
import sys
import tempfile
import shutil
import os
import stat
import uuid
from CommitTree import CommitTree
from CommitNode import CommitNode
from ChainRepository import ChainRepository
from ChainHierarchyPrinter import ChainHierarchyPrinter
import random

class CommitTreeToScriptConverter:
    def __init__(self):
        self.skip_single_child_nodes = False

    def convert_commit_tree_to_script(self, commit_tree_to_copy, script_file, commands_to_add):
        temp_dir = os.path.dirname(script_file.name)

        print("cd " + temp_dir, file=script_file)

        print("Invoke-Expression \"git init\"", file=script_file)
        print("New-Item temp.txt", file=script_file)
        self.recursivly_generate_git_commands(commit_tree_to_copy.root, script_file)
        print("Invoke-Expression \"git checkout real-master\"", file=script_file)
        print("Invoke-Expression \"git branch -D master\"", file=script_file)
        print("Invoke-Expression \"git checkout -b master\"", file=script_file)
        print("Invoke-Expression \"git branch -D real-master\"", file=script_file)
        for command in commands_to_add:
            print("Invoke-Expression \"%s\"" % command, file=script_file)

    def recursivly_generate_git_commands(self, current_commit, script_file):
        if self.skip_single_child_nodes and len(current_commit.children) == 1 and not current_commit.has_name:
            self.recursivly_generate_git_commands(current_commit.children[0], script_file)
            return

        commit = "$temp%s" % str(uuid.uuid4()).replace("-", "")

        print("Add-Content -Path temp.txt -Value ' '", file=script_file)
        print("Invoke-Expression \"git stage .\"", file=script_file)
        print("Invoke-Expression \"git commit -q -m 'commit for " + current_commit.pretty_name + "'\"", file=script_file)
        print(commit + " = Invoke-Expression \"git log --format='%H' -n 1\"", file=script_file)
        
        if current_commit.has_name:
            branch_name = current_commit.pretty_name
            if branch_name == "master":
                branch_name = "real-master"
            print("Invoke-Expression \"git branch %s\"" % branch_name, file=script_file)

        for child in current_commit.children:
            self.recursivly_generate_git_commands(child, script_file)
            if not child == current_commit.children[-1]:
                print("Invoke-Expression \"git checkout " + commit + "\"", file=script_file)