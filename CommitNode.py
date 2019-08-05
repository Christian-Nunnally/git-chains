from pygit2 import *

class CommitNode:
    def __init__(self, commit, pretty_name, has_name):
        self.commit = commit
        self.name = commit.id
        self.pretty_name = pretty_name
        self.parent = None
        self.children = []
        self.has_name = has_name
        self.is_stale = False
        self.is_part_of_master = False
        self.merged_branch_names = []

    def add(self, child):
        if self.can_add(child):
            self.children.append(child)
            child.parent = self

    def can_add(self, child):
        if (self.commit.id == child.commit.id):
            return False
        if (self.children.__contains__(child)):
            return False
        return True
