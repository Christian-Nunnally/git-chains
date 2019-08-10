from pygit2 import *
from CommitNode import CommitNode
import subprocess

class CommitTree:
    root = None
    nodes = {}

    def __init__(self, root_id):
        self.root_id = root_id

    def insert(self, parent_id, commit, pretty_names, has_branch_name, is_part_of_master):
        new_node = CommitNode(commit, pretty_names, has_branch_name)
        new_node.is_part_of_master = is_part_of_master

        if new_node.commit.id in self.nodes:
            return self.nodes[new_node.commit.id]

        self.nodes[new_node.commit.id] = new_node
        self.link_child_with_parent(parent_id, new_node)
        if commit.hex == self.root_id:
            self.root = new_node

        self.populate_merged_branches(new_node)
        return new_node

    def link_child_with_parent(self, parent_id, child):
        if parent_id != None:
            parent_node = self.nodes[parent_id]
            parent_node.add(child)
            child.parent = parent_node 

    def populate_merged_branches(self, node):
        merged_branches_output = subprocess.run(['git', 'branch', '--merged', node.commit.hex], stdout=subprocess.PIPE).stdout.decode('utf-8')
        merged_branches = merged_branches_output.split()
        result = []
        for merged_branch in merged_branches:
            if merged_branch != "*":
                result.append(merged_branch)

        node.merged_branch_names = result
