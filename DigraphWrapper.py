from graphviz import Digraph

class DigraphWrapper:
    def __init__(self, root_commit_node):
        self.node_shape = 'circle'
        self.node_width = "1.5"
        self.include_merged_branches = True

        self.digraph = Digraph(format='svg')
        self.build_digraph(None, root_commit_node)
        self.digraph.render('temp', view=True)

    def build_digraph(self, parent_node, current_node):
        current_node_name = str(current_node.name).split('/')[-1]
        current_node_pretty_name = ' - '.join(self.strip_directories_from_branch_names(current_node.pretty_names))
        self.digraph.node(current_node_name, current_node_pretty_name, shape=self.node_shape, fontname="consolas", width=self.node_width)
        
        self.add_node(current_node_name, current_node_pretty_name, self.pick_node_color(current_node))
        if self.include_merged_branches:
            self.add_list_of_ancestor_nodes(current_node_name, self.strip_directories_from_branch_names(current_node.merged_branch_names))

        if parent_node:
            self.digraph.edge(str(parent_node.name), current_node_name)
        for child in current_node.children:
            self.build_digraph(current_node, child)

    def add_list_of_ancestor_nodes(self, child, ancestors):
        if not any(ancestors):
            return
        self.add_node(ancestors[0], ancestors[0], 'lightgrey')
        self.digraph.edge(ancestors[0], child)
        self.add_list_of_ancestor_nodes(ancestors[0], ancestors[1:])

    def strip_directories_from_branch_names(self, branch_names):
        stripped_names = []
        for name in branch_names:
            stripped_names.append(name.split('/')[-1])
        return stripped_names

    def add_node(self, name, label, color):
        self.digraph.node(name, label, shape=self.node_shape, style='filled', color=color, fontname="consolas", width=self.node_width)

    def pick_node_color(self, node):
        if (node.has_name):
            return 'lightgreen'
        return 'white'
