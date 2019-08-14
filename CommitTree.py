from CommitNode import CommitNode
import subprocess

class CommitTree:
    root = None
    nodes = {}

    def __init__(self, root_id, repository_directory):
        self.root_id = root_id
        self.repository_directory = repository_directory

    def insert(self, parent_id, commit, pretty_names, has_branch_name):
        new_node = CommitNode(commit, pretty_names, has_branch_name)

        if new_node.commit.id in self.nodes:
            return self.nodes[new_node.commit.id]

        self.nodes[new_node.commit.id] = new_node
        self.link_child_with_parent(parent_id, new_node)
        self.populate_merged_branches(new_node)
        return new_node

    def link_child_with_parent(self, parent_id, child):
        if parent_id != None:
            parent_node = self.nodes[parent_id]
            parent_node.add(child)
            child.parent = parent_node 

    def populate_merged_branches(self, node):
        if node.has_name:
            args = ['git', 'branch', '--merged', node.commit.hex]
            merged_branches_output = subprocess.run(args, stdout=subprocess.PIPE, cwd=self.repository_directory).stdout.decode('utf-8')
            merged_branches = merged_branches_output.split() 
            result = []
            for merged_branch in merged_branches:
                if merged_branch != "*":
                    result.append(merged_branch) 

            node.merged_branch_names = result

    def find_root(self):
        root_nodes = self.find_all_root_nodes()
        for root_node in root_nodes:
            if not root_nodes[0].commit.hex == root_node.commit.hex and not root_nodes[0].pretty_names[0] == root_node.pretty_names[0]:
                print("Error: Unable to find a single root to the commit tree.")
        if len(root_nodes) > 0:
            self.root = root_nodes[-1]

    def find_all_root_nodes(self):
        root_nodes = []
        for node in self.nodes.values():
            node_ref = node
            while(node_ref.parent != None):
                node_ref = node_ref.parent
            root_nodes.append(node_ref)
        return root_nodes
