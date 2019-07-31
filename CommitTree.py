from CommitNode import CommitNode

class CommitTree:
    root = None
    nodes = {}

    def insert(self, parent_id, commit, pretty_name, has_name, is_part_of_master):
        new_node = CommitNode(commit, pretty_name, has_name)
        new_node.is_part_of_master = is_part_of_master

        if new_node.commit.id in self.nodes:
            return self.nodes[new_node.commit.id]

        self.nodes[new_node.commit.id] = new_node
        self.link_child_with_parent(parent_id, new_node)
        if self.root == None:
            self.root = new_node
        return new_node

    def link_child_with_parent(self, parent_id, child):
        if parent_id != None:
            parent_node = self.nodes[parent_id]
            parent_node.add(child)
            child.parent = parent_node
    
    def get_nodes_with_sub_string_in_name(self, sub_string):
        return self.get_nodes_with_sub_string_in_name_recursive(self.root, sub_string)

    def get_nodes_with_sub_string_in_name_recursive(self, node, sub_string):
        found_nodes = []
        if node.pretty_name == sub_string:
            found_nodes.append(node)
        if sub_string in node.pretty_name:
            found_nodes.append(node)
        for child in node.children:
            found_nodes += self.get_nodes_with_sub_string_in_name_recursive(child, sub_string)
        return found_nodes