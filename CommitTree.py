from Interoperability.ShellCommandExecuter import ShellCommandExecuter
from Logger import Logger

class CommitTree:
    root = None
    nodes = {}

    def __init__(self, root_id, repository_directory):
        self.logger = Logger(self)
        self.root_id = root_id
        self.repository_directory = repository_directory

    def insert(self, node):
        if not node.commit.id in self.nodes:
            self.nodes[node.commit.id] = node
            self.link_child_with_parent(node)
            self.populate_merged_branches(node)

    def link_child_with_parent(self, child):
        if child.parent_id:
            parent_node = self.nodes[child.parent_id]
            parent_node.add(child)
            child.parent = parent_node 

    def populate_merged_branches(self, node):
        if node.has_name:
            branches_merged_into_parents = set(self.get_parents_merged_branches(node))
            all_branches_merged_into_node = set(self.get_merged_branch_names(node.commit.hex))
            node.merged_branch_names = list(set(all_branches_merged_into_node - branches_merged_into_parents))
        
    def get_parents_merged_branches(self, node):
        if (node.parent):
            return node.parent.merged_branch_names + self.get_parents_merged_branches(node.parent) + node.parent.pretty_names
        return []

    def get_merged_branch_names(self, hex):
        args = ['git', 'branch', '--merged', hex]
        executer = ShellCommandExecuter(self.repository_directory, args)
        merged_branches = executer.execute_for_output().split()
        if "*" in merged_branches:
            merged_branches.remove("*")
        while "+" in merged_branches:
            merged_branches.remove("+")
        return merged_branches

    def find_root(self):
        root_nodes = self.find_all_root_nodes()
        if self.are_the_same(root_nodes):
            self.root = root_nodes[-1]
            return
        self.root = root_nodes[0]
        self.logger.warning("Unable to find a single root to the commit tree.")

    def are_the_same(self, nodes):
        for node in nodes:
            if not nodes[0].commit.hex == node.commit.hex:
                if not nodes[0].pretty_names[0] == node.pretty_names[0]:
                    return False
        return len(nodes) > 0

    def find_all_root_nodes(self):
        root_nodes = []
        for node in self.nodes.values():
            while(node.parent != None):
                node = node.parent
            root_nodes.append(node)
        return root_nodes
