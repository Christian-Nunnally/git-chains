from pygit2 import *

class CommitNode:
    uid = 0

    def __init__(self, commit, pretty_name, is_reference_node, has_name):
        self.commit = commit
        self.name = commit.id
        self.pretty_name = pretty_name
        self.parent = None
        self.children = []
        self.is_reference_node = is_reference_node
        self.has_name = has_name
        self.is_stale = False
        if is_reference_node:
            self.key = CommitNode.uid
        else:
            self.key = commit.id
        CommitNode.uid += 1

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
