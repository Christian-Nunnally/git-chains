from pygit2 import *
from ChainHierarchyPrinter import ChainHierarchyPrinter
from CommitNode import CommitNode
from CommitTree import CommitTree
import subprocess

class ChainRepository():
    def __init__(self, repo_path, master_branch_name, local_branches_to_include = []):
        self.tree = None
        self.repo = Repository(repo_path)
        # self.master_branch_name = master_branch_name
        self.local_branch_logs_to_merge_base = []
        self.local_branches = []
        # self.master_log = []
        self.local_feature_branches = []
        # self.master_branch = None
        self.commit_name_map = {}
        # self.local_branch_merge_bases_with_master = []
        self.local_branches_to_include = local_branches_to_include

        # the order that these initialization methods are called matters.
        self.initialize_branches()
        self.calculate_octopus_merge_base()
        self.generate_local_branch_logs_to_merge_base()
        self.build_commit_tree()

    def initialize_branches(self):
        for local_branch_name in self.repo.branches.local:
            if len(self.local_branches_to_include) == 0 or local_branch_name in self.local_branches_to_include:
                self.local_branches.append(self.repo.branches[local_branch_name])
        # self.master_branch = self.repo.branches[self.master_branch_name]

    def calculate_octopus_merge_base(self):
        args = ['git', 'merge-base', '--octopus']
        for local_branch_name in self.repo.branches.local:
            args.append(local_branch_name)
        self.octopus_merge_base = subprocess.run(args, stdout=subprocess.PIPE).stdout.decode('utf-8').strip()

    def generate_local_branch_logs_to_merge_base(self):
        for local_branch in self.local_branches:
            branch_log_to_octopus_merge_base = self.generate_branch_log_to_octopus_merge_base(local_branch)
            self.local_branch_logs_to_merge_base.append(branch_log_to_octopus_merge_base)

    def generate_branch_log_to_octopus_merge_base(self, branch):
        commit = self.repo.get(branch.target)
        branch_log_to_octopus_merge_base = []

        for commit in self.walk_from_branch(branch.target):
            if commit.hex == self.octopus_merge_base:
                branch_log_to_octopus_merge_base.append(commit)
                break
            is_ancestor = subprocess.call(['git', 'merge-base', '--is-ancestor', commit.hex, self.octopus_merge_base])
            if (is_ancestor):
                branch_log_to_octopus_merge_base.append(commit)
            else: 
                print("nope")
        branch_log_to_octopus_merge_base.reverse()
        return branch_log_to_octopus_merge_base

    def walk_first_parent(self, branch):
        walker = self.repo.walk(branch, GIT_SORT_TOPOLOGICAL)
        walker.simplify_first_parent()
        return walker

    def walk_from_branch(self, branch):
        walker = self.repo.walk(branch, GIT_SORT_TOPOLOGICAL) 
        return walker

    def get_commit_names(self, commit):
        if (len(self.commit_name_map) == 0): 
            for branch in self.local_branches:
                branch_name = branch.name
                if (branch_name.startswith("refs/heads/")):
                    branch_name = branch_name[len("refs/heads/"):]
                if (not branch.target.hex in self.commit_name_map):
                    self.commit_name_map[branch.target.hex] = []
                self.commit_name_map[branch.target.hex].append(branch_name)
        if (commit.hex in self.commit_name_map):
            return self.commit_name_map[commit.hex]
        return ['{:7.7}'.format(commit.hex)]

    def does_commit_have_name(self, commit):
        return commit.hex in self.commit_name_map

    # def build_commit_tree(self):
    #     self.tree = CommitTree()
    #     master_parent_id = None
    #     parent_id = None
    #     for master_commit in self.master_log:
    #         node = self.insert_commit_into_tree(master_commit, master_parent_id, True)
    #         master_parent_id = node.commit.id

    #         if master_commit.hex in [x.hex for x in self.local_branch_merge_bases_with_master]:
    #             local_branch_logs_from_commit = self.get_local_branch_logs_starting_at_commit(master_commit)
    #             for local_branch_log in local_branch_logs_from_commit:
    #                 parent_id = master_parent_id
    #                 for commit in local_branch_log[1:]:
    #                     node = self.insert_commit_into_tree(commit, parent_id, False)
    #                     parent_id = node.commit.id

    def build_commit_tree(self):
        self.tree = CommitTree(self.octopus_merge_base)
        for log in self.local_branch_logs_to_merge_base:
            parent_id = None
            for commit in log:
                node = self.insert_commit_into_tree(commit, parent_id, False)
                parent_id = node.commit.id

    # def get_local_branch_logs_starting_at_commit(self, start_commit):
    #     local_branch_logs_from_commit = []
    #     for local_branch_log in self.local_branch_logs_to_merge_base:
    #         if local_branch_log[0].hex == start_commit.hex:
    #             local_branch_logs_from_commit.append(local_branch_log)
    #     return local_branch_logs_from_commit

    def insert_commit_into_tree(self, commit, parent_id, is_part_of_master):
        commit_name = self.get_combined_branch_name_from_commit(commit)
        print(commit_name, commit.hex)
        commit_has_name = self.does_commit_have_name(commit)
        return self.tree.insert(parent_id, commit, commit_name, commit_has_name, True)

    def get_combined_branch_name_from_commit(self, commit):
        names = self.get_commit_names(commit)
        combined_names = ""
        for name in names:
            if not name == names[0]:
                combined_names = combined_names + ", "
            combined_names = combined_names + name
        return combined_names

# 1. git merge-base --octopus A B C D
# 2. walk all branches back to the best merge base
# 3. add to trees