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
        self.print_debug = True

    def convert_commit_tree_to_script(self, commit_tree_to_copy, script_file, commands_to_add):
        temp_dir = os.path.dirname(script_file.name)

        self.print_to_file("cd " + temp_dir, script_file)

        self.print_to_file("Invoke-Expression \"git init\"", script_file)
        self.recursivly_generate_git_commands(commit_tree_to_copy.root, script_file)
        self.print_to_file("Invoke-Expression \"git checkout real-master\"", script_file)
        self.print_to_file("Invoke-Expression \"git branch -D master\"", script_file)
        self.print_to_file("Invoke-Expression \"git checkout -b master\"", script_file)
        self.print_to_file("Invoke-Expression \"git branch -D real-master\"", script_file)
        for command in commands_to_add:
            self.print_to_file("Invoke-Expression \"%s\"" % command, script_file)

    def recursivly_generate_git_commands(self, current_commit, script_file):
        if self.skip_single_child_nodes and len(current_commit.children) == 1 and not current_commit.has_name:
            self.recursivly_generate_git_commands(current_commit.children[0], script_file)
            return

        commit = "$temp%s" % str(uuid.uuid4()).replace("-", "")

        self.print_to_file("New-Item %s.txt" % str(uuid.uuid4()).replace("-", ""), script_file)
        self.print_to_file("Invoke-Expression \"git add .\"", script_file)
        self.print_to_file("Invoke-Expression \"git commit -q -a -m 'commit for " + current_commit.pretty_name + "'\"", script_file)
        self.print_to_file(commit + " = Invoke-Expression \"git log --format='%H' -n 1\"", script_file)
        
        if current_commit.has_name:
            branch_name = current_commit.pretty_name
            if branch_name == "master":
                branch_name = "real-master"
            self.print_to_file("Invoke-Expression \"git branch %s\"" % branch_name, script_file)

        for child in current_commit.children:
            self.recursivly_generate_git_commands(child, script_file)
            if not child == current_commit.children[-1]:
                self.print_to_file("Invoke-Expression \"git checkout " + commit + "\"", script_file)

    def print_to_file(self, string, file):
        print(string, file)
        if self.print_debug:
            print(string)