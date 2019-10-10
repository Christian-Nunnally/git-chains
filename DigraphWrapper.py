from graphviz import Digraph

class DigraphWrapper:
    def __init__(self, root_commit_node):
        self.node_shape = 'circle'
        self.node_width = "1.5"
        self.include_merged_branches = True
        self.exclude_intermediate_commits = True

        self.digraph = Digraph(format='svg')
        self.included_names = []
        self.build_digraph(None, root_commit_node)
        self.digraph.render('temp', view=True)

    def build_digraph(self, parent_node, current_node):
        if self.exclude_intermediate_commits and not current_node.has_name and len(current_node.children) == 1:
            self.build_digraph(parent_node, current_node.children[0])
            return

        current_node_name = str(current_node.name).split('/')[-1]
        current_node_pretty_name = ' - '.join(self.clean_branch_name_for_labels(current_node.pretty_names))
        
        color = self.pick_node_color(current_node)
        shape = self.pick_node_shape(current_node)
        width = self.pick_node_width(current_node)
        self.add_node(current_node_name, current_node_pretty_name, color, shape, width)
        if current_node.has_name:
            self.included_names.append(current_node_pretty_name)

        if self.include_merged_branches:
            if len(current_node.merged_branch_names) > 1:
                simple_branch_names = self.clean_branch_name_for_labels(current_node.merged_branch_names[1:])
                self.add_list_of_ancestor_nodes(current_node_name, simple_branch_names, current_node_name)

        if parent_node:
            self.digraph.edge(str(parent_node.name), current_node_name)
        for child in current_node.children:
            self.build_digraph(current_node, child)

    def add_list_of_ancestor_nodes(self, child, ancestors, node_uniquifier):
        if not any(ancestors):
            return
        print(ancestors[0])
        for n in self.included_names:
            print("n: " + n)
        if ancestors[0] in self.included_names:
            self.add_list_of_ancestor_nodes(child, ancestors[1:], node_uniquifier)
            return
        parent_name = node_uniquifier + ancestors[0]
        self.add_node(parent_name, ancestors[0], 'lightgrey', self.node_shape, self.node_width)
        self.digraph.edge(parent_name, child)
        self.add_list_of_ancestor_nodes(parent_name, ancestors[1:], node_uniquifier)

    def clean_branch_name_for_labels(self, branch_names):
        branch_names = self.strip_directories_from_branch_names(branch_names)
        return self.replace_dash_with_newline(branch_names)

    def strip_directories_from_branch_names(self, branch_names):
        stripped_names = []
        for name in branch_names:
            stripped_names.append(name.split('/')[-1])
        return stripped_names

    def replace_dash_with_newline(self, branch_names):
        replaced_names = []
        for name in branch_names:
            replaced_names.append(name.replace('-', '\n'))
        return replaced_names

    def add_node(self, name, label, color, shape, width):
        self.digraph.node(name, label, shape=shape, style='filled', color=color, fontname="consolas", width=width)

    def pick_node_color(self, node):
        if (node.has_name):
            return 'lightgreen'
        return 'white'

    def pick_node_shape(self, node):
        if (node.has_name):
            return self.node_shape
        return 'box'

    def pick_node_width(self, node):
        if (node.has_name):
            return self.node_width
        return '.3'
