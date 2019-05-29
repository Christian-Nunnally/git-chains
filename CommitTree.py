from pygit2 import *
from CommitNode import CommitNode

class CommitTree:
    root = None
    nodes = {}

    def insert(self, parent_id, commit, pretty_name, has_name):
        print(parent_id)
        is_reference_node = not self.is_child_of_parent(parent_id, commit)
        new_node = CommitNode(commit, pretty_name, is_reference_node, has_name)

        if new_node.key in self.nodes:
            return self.nodes[new_node.key]

        self.nodes[new_node.key] = new_node
        self.link_child_with_parent(parent_id, new_node)
        print("Inserted " + pretty_name + " parent = " + str(parent_id))
        if self.root == None:
            self.root = new_node
        return new_node

    def is_child_of_parent(self, parent_id, commit):
        if (parent_id == None):
            return True
        for parent in commit.parents:
            if parent.id == parent_id:
                return True
        return len(commit.parents) == 0 or parent_id is None

    def link_child_with_parent(self, parent_id, child):
        if parent_id != None:
            parent_node = self.nodes[parent_id]
            parent_node.add(child)
            child.parent = parent_node

    def print_tree(self):
        self.print_node(self.root)

    def print_node(self, node):
        if node == None:
            return
        print(node.name)
        print(len(node.children))
        for child in node.children:
            if (child != node):
                self.print_node(child)