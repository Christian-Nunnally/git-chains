from CommitTree import CommitTree
from CommitNode import CommitNode

class CommitTreeBuilder:
    def __init__(self, root_commit_id, repository_directory, branch_name_map, chain_repository):
        self.root_commit_id = root_commit_id
        self.repository_directory = repository_directory
        self.chain_repository = chain_repository
        self.branch_name_map = branch_name_map

    def build_commit_tree(self, commit_branches_to_build_tree):
        tree = CommitTree(self.root_commit_id, self.repository_directory)
        self.insert_branches_into_tree(tree, commit_branches_to_build_tree)
        tree.find_root()
        return tree

    def insert_branches_into_tree(self, tree, commit_branches_to_build_tree):
        if self.are_valid_commit_branches(commit_branches_to_build_tree):
            for commit_chain in commit_branches_to_build_tree:
                self.insert_commit_chain_into_tree(tree, commit_chain)

    def insert_commit_chain_into_tree(self, tree, commit_chain, parent_id = None):
        for commit in commit_chain:
            self.insert_commit_into_tree(tree, commit, parent_id)
            parent_id = commit.id

    def are_valid_commit_branches(self, commit_branches_to_build_tree):
        if len(commit_branches_to_build_tree) == 0 or len(commit_branches_to_build_tree[0]) == 0:
            return False
        if not commit_branches_to_build_tree[0][0].hex == self.root_commit_id:
            print("ohno")
            return False
        return True
    
    def insert_commit_into_tree(self, tree, commit, parent_id):
        commit_names = self.get_commit_names(commit)
        commit_has_name = commit.hex in self.branch_name_map
        node = CommitNode(commit, commit_names, commit_has_name, parent_id)
        tree.insert(node)

    def get_commit_names(self, commit):
        if commit.hex in self.branch_name_map:
            return self.branch_name_map[commit.hex]
        return ['{:7.7}'.format(commit.hex)]