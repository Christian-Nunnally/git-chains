import subprocess
import sys
import tempfile
import shutil
import os
import stat
from pygit2 import *
from CommitTree import CommitTree
from CommitNode import CommitNode
from ChainRepository import ChainRepository
from ChainHierarchyPrinter import ChainHierarchyPrinter
import random

class CommitTreeToGitCommandDecoder:
    
    def __init__(self, tree):
        self.root = tree.root
        self.id = 0

    def recursivly_generate_git_commands_entry(self, command, skip_single_child_nodes):
        with tempfile.TemporaryDirectory() as temp_dir:
            f = open(temp_dir + "\\repo-init.ps1", "x")

            print("cd " + temp_dir, file=f)
            print("Invoke-Expression \"git init\"", file=f)
            print("New-Item temp.txt", file=f)
            self.recursivly_generate_git_commands(self.root, f, skip_single_child_nodes)
            print("Invoke-Expression \"git checkout real-master\"", file=f)
            print("Invoke-Expression \"git branch -D master\"", file=f)
            print("Invoke-Expression \"git checkout -b master\"", file=f)
            print("Invoke-Expression \"git branch -D real-master\"", file=f)
            print("Invoke-Expression \"%s\"" % command, file=f)

            f.close()
            p = subprocess.Popen(["powershell.exe", 
                        temp_dir + "\\repo-init.ps1"], 
                        stdout=open(os.devnull, 'w'),
                        stderr=open(os.devnull, 'w'))
            p.communicate()

            preview_repo = ChainRepository(temp_dir + "\\.git", "master")
            preview_printer = ChainHierarchyPrinter(preview_repo)
            preview_printer.print()
            preview_repo.repo.free()
            self.make_writeable_recursive(temp_dir)

    def recursivly_generate_git_commands(self, current_commit, f, skip_single_child_nodes):
        if skip_single_child_nodes and len(current_commit.children) == 1 and not current_commit.has_name:
            self.recursivly_generate_git_commands(current_commit.children[0], f, True)
            return

        unique_id = self.get_unique_id()
        commit = "$temp%s" % unique_id

        print("Add-Content -Path temp.txt -Value ' '", file=f)
        print("Invoke-Expression \"git stage .\"", file=f)
        print("Invoke-Expression \"git commit -m 'commit for " + current_commit.pretty_name + "'\"", file=f)
        print(commit + " = Invoke-Expression \"git log --format='%H' -n 1\"", file=f)
        
        if current_commit.has_name:
            branch_name = current_commit.pretty_name
            if branch_name == "master":
                branch_name = "real-master"
            print("Invoke-Expression \"git branch %s\"" % branch_name, file=f)

        for child in current_commit.children:
            self.recursivly_generate_git_commands(child, f, skip_single_child_nodes)
            if not child == current_commit.children[-1]:
                print("Invoke-Expression \"git checkout " + commit + "\"", file=f)
    
    def get_perm(self, fname):
        return stat.S_IMODE(os.lstat(fname)[stat.ST_MODE])

    def make_writeable_recursive(self, path):
        for root, dirs, files in os.walk(path, topdown=False):
            for dir in [os.path.join(root, d) for d in dirs]:
                os.chmod(dir, self.get_perm(dir) | stat.S_IWRITE)
            for file in [os.path.join(root, f) for f in files]:
                os.chmod(file, self.get_perm(file) | stat.S_IWRITE)

    def get_unique_id(self):
        self.id += 1
        return self.id
