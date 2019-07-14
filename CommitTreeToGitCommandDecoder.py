
from pygit2 import *
from CommitTree import CommitTree
from CommitNode import CommitNode
import random

class CommitTreeToGitCommandDecoder:
    
    def __init__(self, tree):
        self.root = tree.root
        self.id = 0

    def recursivly_generate_git_commands_entry(self):
        print("Invoke-Expression \"git init\"")
        self.recursivly_generate_git_commands(self.root)

    def recursivly_generate_git_commands(self, current_commit):
        unique_id = self.get_unique_id()
        commit = "$temp%s" % unique_id

        print("New-Item temp%s.txt" % random.randint(1000000000, 9999999999))
        print("Invoke-Expression \"git add .\"")
        print("Invoke-Expression \"git commit -m 'commit for " + current_commit.pretty_name + "'\"")
        print(commit + " = Invoke-Expression \"git log --format='%H' -n 1\"")
        
        if current_commit.has_name:
            branch_name = current_commit.pretty_name
            if branch_name == "master":
                branch_name = "real-master"
            print("Invoke-Expression \"git branch %s\"" % current_commit.pretty_name)

        for child in current_commit.children:
            self.recursivly_generate_git_commands(child)

        print("Invoke-Expression \"git checkout " + commit + "\"")
    
    def get_unique_id(self):
        self.id += 1
        return self.id