from graphviz import Digraph

class DigraphWrapper:
    def __init__(self, root_commit_node):
        self.print_debug = False
        self.digraph = Digraph(format='png')
        self.build_digraph(None, root_commit_node)
        self.digraph.render("test_render.png")

    def build_digraph(self, parent_node, currnet_node):
        self.digraph.node(str(currnet_node.name), str(' - '.join(currnet_node.pretty_names)))
        if (parent_node):
            self.digraph.edge(str(parent_node.name), str(currnet_node.name))
        for child in currnet_node.children:
            self.build_digraph(currnet_node, child)