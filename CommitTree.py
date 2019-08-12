from CommitNode import CommitNode
import subprocess

class CommitTree:
    root = None
    nodes = {}

    def __init__(self, root_id, repo_directory):
        self.root_id = root_id
        self.repo_directory = repo_directory

    def insert(self, parent_id, commit, pretty_names, has_branch_name, is_part_of_master):
        new_node = CommitNode(commit, pretty_names, has_branch_name)
        new_node.is_part_of_master = is_part_of_master

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
        args = ['git', 'branch', '--merged', node.commit.hex]
        merged_branches_output = subprocess.run(args, stdout=subprocess.PIPE, cwd=self.repo_directory).stdout.decode('utf-8')
        merged_branches = merged_branches_output.split()
        result = []
        for merged_branch in merged_branches:
            if merged_branch != "*":
                result.append(merged_branch)

        node.merged_branch_names = result

    def find_root(self):
        nodes_without_a_parent = []
        for node in self.nodes.values():
            node_ref = node
            while(node_ref.parent != None):
                node_ref = node_ref.parent
            nodes_without_a_parent.append(node_ref)
        
        for node_without_a_parent in nodes_without_a_parent:
            if (not nodes_without_a_parent[0].commit.hex == node_without_a_parent.commit.hex and not nodes_without_a_parent[0].pretty_names[0] == node_without_a_parent.pretty_names[0]):
                print("Error: Unable to find a single root to the commit tree.")
        self.root = nodes_without_a_parent[-1]
