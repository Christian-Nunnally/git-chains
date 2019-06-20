from pygit2 import *
from CommitNode import CommitNode

class CommitTree:
    root = None
    nodes = {}

    def insert(self, parent_id, commit, pretty_name, has_name, is_part_of_master, is_reference_node):
        new_node = CommitNode(commit, pretty_name, is_reference_node, has_name)
        new_node.is_part_of_master = is_part_of_master

        if new_node.key in self.nodes:
            return self.nodes[new_node.key]

        self.nodes[new_node.key] = new_node
        self.link_child_with_parent(parent_id, new_node)
        if self.root == None:
            self.root = new_node
        return new_node

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
    
    def get_nodes_with_sub_string_in_name(self, sub_string):
        return self.get_nodes_with_sub_string_in_name_recursive(self.root, sub_string)

    def get_nodes_with_sub_string_in_name_recursive(self, node, sub_string):
        found_nodes = []
        if not node.is_reference_node and node.pretty_name == sub_string:
            return [node]
        if node.pretty_name.__contains__(sub_string):
            if (not node.is_reference_node):
                found_nodes.append(node)
        for child in node.children:
            found_nodes += self.get_nodes_with_sub_string_in_name_recursive(child, sub_string)
        return found_nodes

    def refresh_nodes_staleness_status(self):
        self.refresh_nodes_staleness_status_recursive(self.root)

    def refresh_nodes_staleness_status_recursive(self, node):
        node.is_stale = False
        if not node.parent == None and not node.parent.is_part_of_master:
            if node.parent.is_stale:
                node.is_stale = True
            else:
                for sibling in node.parent.children:
                    if (not sibling == node):
                        if (sibling.commit.commit_time < node.commit.commit_time):
                            node.is_stale = True
                            break
        for child in node.children:
            self.refresh_nodes_staleness_status_recursive(child)