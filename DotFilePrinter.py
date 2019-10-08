class DotFilePrinter:
    def __init__(self):
        self.print_debug = False

    def write_dot_file(self, chain_repository):
        with open("git_chains.dot", "w") as dot_file:
            self.dot_file = dot_file
            self.print_to_file("digraph {")
            self.recursivly_write_nodes(None, chain_repository.tree.root)
            self.print_to_file("}")

    def recursivly_write_nodes(self, parent, current):
        if (parent):
            self.print_to_file("    " + parent.name + " -> " + current.name)
        for child in current.children:
            self.recursivly_write_nodes(current, child)

    def print_to_file(self, string):
        print(string, file=self.dot_file)
        if self.print_debug:
            print(string)