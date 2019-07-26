import subprocess
import sys
import tempfile
import shutil
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

    def recursivly_generate_git_commands_entry(self):
        temp_dir = tempfile.TemporaryDirectory()
        f = open(temp_dir.name + "\\repo-init.ps1", "x")

        print("cd " + temp_dir.name, file=f)
        print("Invoke-Expression \"git init\"", file=f)
        print("New-Item temp.txt", file=f)
        self.recursivly_generate_git_commands(self.root, f)
        print("Invoke-Expression \"git checkout real-master\"", file=f)
        print("Invoke-Expression \"git branch -D master\"", file=f)
        print("Invoke-Expression \"git checkout -b master\"", file=f)
        print("Invoke-Expression \"git branch -D real-master\"", file=f)

        f.close()
        p = subprocess.Popen(["powershell.exe", 
                    temp_dir.name + "\\repo-init.ps1"], 
                    stdout=sys.stdout)
        p.communicate()

        preview_repo = ChainRepository(temp_dir.name + "\\.git", "master")
        preview_printer = ChainHierarchyPrinter(preview_repo)
        preview_printer.print()

    def recursivly_generate_git_commands(self, current_commit, f):
        unique_id = self.get_unique_id()
        commit = "$temp%s" % unique_id

        print("Add-Content -Path temp.txt -Value ' '", file=f)
        # print("New-Item temp%s.txt" % random.randint(1000000000, 9999999999))
        print("Invoke-Expression \"git stage .\"", file=f)
        print("Invoke-Expression \"git commit -m 'commit for " + current_commit.pretty_name + "'\"", file=f)
        print(commit + " = Invoke-Expression \"git log --format='%H' -n 1\"", file=f)
        
        if current_commit.has_name:
            branch_name = current_commit.pretty_name
            if branch_name == "master":
                branch_name = "real-master"
            print("Invoke-Expression \"git branch %s\"" % branch_name, file=f)

        for child in current_commit.children:
            self.recursivly_generate_git_commands(child, f)
            print("Invoke-Expression \"git checkout " + commit + "\"", file=f)

        print("Invoke-Expression \"git checkout " + commit + "\"", file=f)
    
    def get_unique_id(self):
        self.id += 1
        return self.id