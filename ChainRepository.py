import pygit2
import subprocess
from CommitTree import CommitTree

class ChainRepository():
    def __init__(self, repo_path, master_branch_name, local_branches_to_include = []):
        self.tree = None
        self.repo = pygit2.Repository(repo_path)
        self.local_branch_logs_to_merge_base = []
        self.local_branches = []
        self.local_feature_branches = []
        self.commit_name_map = {}
        self.local_branches_to_include = local_branches_to_include
        self.included_local_branch_names = []

        # the order that these initialization methods are called matters.
        self.initialize_branches()
        self.calculate_octopus_merge_base()
        self.generate_local_branch_logs_to_merge_base()
        self.build_commit_tree()

    def initialize_branches(self):
        for local_branch_name in self.repo.branches.local:
            if len(self.local_branches_to_include) == 0 or local_branch_name in self.local_branches_to_include:
                self.included_local_branch_names.append(local_branch_name)
                self.local_branches.append(self.repo.branches[local_branch_name])

    def calculate_octopus_merge_base(self):
        args = ['git', 'merge-base', '--octopus'] + self.included_local_branch_names
        self.octopus_merge_base = subprocess.run(args, stdout=subprocess.PIPE).stdout.decode('utf-8').strip()

    def generate_local_branch_logs_to_merge_base(self):
        for local_branch in self.local_branches:
            branch_log_to_octopus_merge_base = self.generate_branch_log_to_octopus_merge_base(local_branch)
            self.local_branch_logs_to_merge_base.append(branch_log_to_octopus_merge_base)

    def generate_branch_log_to_octopus_merge_base(self, branch):
        branch_log_to_octopus_merge_base = []

        for commit in self.walk_from_branch(branch.target):
            if self.is_ancestor(commit.hex, self.octopus_merge_base):
                branch_log_to_octopus_merge_base.append(commit)
                if commit.hex == self.octopus_merge_base:
                    break
        branch_log_to_octopus_merge_base.reverse()
        return branch_log_to_octopus_merge_base

    def walk_from_branch(self, branch):
        return self.repo.walk(branch, pygit2.GIT_SORT_TOPOLOGICAL) 

    def is_ancestor(self, commit, possible_ancestor):
        args = ['git', 'merge-base', '--is-ancestor', possible_ancestor, commit]
        return_value = subprocess.call(args)
        return not return_value

    def get_commit_names(self, commit):
        self.populate_commit_name_map_if_empty()
        if commit.hex in self.commit_name_map:
            return self.commit_name_map[commit.hex]
        return ['{:7.7}'.format(commit.hex)]

    def populate_commit_name_map_if_empty(self):
        if len(self.commit_name_map) == 0:
            self.populate_commit_name_map()

    def populate_commit_name_map(self):
        for branch in self.local_branches:
            branch_name = branch.name
            if (branch_name.startswith("refs/heads/")):
                branch_name = branch_name[len("refs/heads/"):]
            self.append_to_commit_name_map(branch.target.hex, branch_name)

    def append_to_commit_name_map(self, commit_id, name):
        if (not commit_id in self.commit_name_map):
            self.commit_name_map[commit_id] = []
        self.commit_name_map[commit_id].append(name)  

    def does_commit_have_name(self, commit):
        return commit.hex in self.commit_name_map

    def build_commit_tree(self):
        self.tree = CommitTree(self.octopus_merge_base)
        for log in self.local_branch_logs_to_merge_base:
            parent_id = None
            for commit in log:
                node = self.insert_commit_into_tree(commit, parent_id, False)
                parent_id = node.commit.id

    def insert_commit_into_tree(self, commit, parent_id, is_part_of_master):
        commit_names = self.get_commit_names(commit)
        commit_has_name = self.does_commit_have_name(commit)
        return self.tree.insert(parent_id, commit, commit_names, commit_has_name, True)