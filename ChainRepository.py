from pygit2 import *
from ChainHierarchyPrinter import ChainHierarchyPrinter
from CommitNode import CommitNode
from CommitTree import CommitTree

class ChainRepository():
    number_of_commits_to_walk_master = 200

    def __init__(self, repo_path, master_branch_name):
        self.flatten_merges_into_tree = True
        self.tree = None
        self.repo = Repository(repo_path)
        self.master_branch_name = master_branch_name
        self.local_branch_logs_to_master = []
        self.local_branch_logs_to_master_by_start_commit = {}
        self.local_branches = []
        self.master_log = []
        self.local_feature_branches = []
        self.master_branch = None
        self.commit_name_map = {}

        # the order that these initialization methods are called matters.
        self.load_local_branches()
        self.load_master_and_feature_branches()
        self.generate_master_log()
        self.generate_local_branch_logs_to_master()
        self.build_commit_tree()

    def load_local_branches(self):
        local_branche_names = list(self.repo.branches.local)
        for local_branch_name in local_branche_names:
            self.local_branches.append(self.repo.branches[local_branch_name])

    def load_master_and_feature_branches(self):
        self.master_branch = self.repo.branches[self.master_branch_name]
        for local_branch in self.local_branches:
            if (local_branch.target.hex == self.master_branch.target.hex):
                continue
            self.local_feature_branches.append(local_branch)

    def generate_master_log(self):
        self.master_log.clear()
        commit_count = 0
        for commit in self.repo.walk(self.master_branch.target, GIT_SORT_TOPOLOGICAL):
            commit_count += 1
            self.master_log.append(commit)
            if (commit_count > self.number_of_commits_to_walk_master):
                break
        self.master_log.reverse()

    def generate_local_branch_logs_to_master(self):
        for local_branch in self.local_branches:
            branch_log_to_master = self.generate_branch_log_to_master(local_branch)
            if (len(branch_log_to_master) > 0):
                start_commit = branch_log_to_master[0]
                if (start_commit in self.local_branch_logs_to_master_by_start_commit):
                    self.local_branch_logs_to_master_by_start_commit[start_commit].append(branch_log_to_master)
                else:
                    self.local_branch_logs_to_master_by_start_commit[start_commit] = [branch_log_to_master]
                self.local_branch_logs_to_master.append(branch_log_to_master)

    def generate_branch_log_to_master(self, branch):
        branch_log_to_master = []
        commit = self.repo.get(branch.target)
        self.generate_branch_log_to_master_recursive(commit, branch_log_to_master, 0, self.number_of_commits_to_walk_master, None, None)
        branch_log_to_master.reverse()
        return branch_log_to_master

    def generate_branch_log_to_master_recursive(self, commit, branch_log, iterations, max_depth_to_search_for_master_commit, stop_commit, fake_parent):
        if (not stop_commit == None and commit.hex == stop_commit.hex):
            return
        if (len(commit.parents) > 0 and not stop_commit == None and commit.parents[0].hex == stop_commit.hex):
            branch_log.append(commit)
        else:
            branch_log.append(commit)
        if commit in self.master_log:
            return
        if (len(commit.parents) == 0):
            branch_log = []
            return
        if iterations > self.number_of_commits_to_walk_master:
            return
        
        if (len(commit.parents) == 2 and self.flatten_merges_into_tree):
            merge_base = self.repo.merge_base(commit.parents[0].oid, commit.parents[1].oid)
            new_fake_parent = commit.parents[0].oid
            self.generate_branch_log_to_master_recursive(commit.parents[1], branch_log, iterations + 1, max_depth_to_search_for_master_commit, merge_base, new_fake_parent)

        self.generate_branch_log_to_master_recursive(commit.parents[0], branch_log, iterations + 1, max_depth_to_search_for_master_commit, None, fake_parent)

    def get_local_branch_logs_starting_with_commit(self, commit):
        if (commit in self.local_branch_logs_to_master_by_start_commit):
            return self.local_branch_logs_to_master_by_start_commit[commit]
        local_branch_logs_starting_with_commit = []
        for local_branch_log in self.local_branch_logs_to_master:
            if (local_branch_log[0].hex == commit.hex):
                local_branch_logs_starting_with_commit.append(local_branch_log)
        return local_branch_logs_starting_with_commit
    
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

    def build_commit_tree(self):
        self.tree = CommitTree()
        master_parent_id = None
        for master_commit in self.master_log:
            master_commit_name = self.get_combined_branch_name_from_commit(master_commit)
            master_commit_has_name = self.does_commit_have_name(master_commit)
            master_parent_node = self.tree.insert(master_parent_id, master_commit, master_commit_name, master_commit_has_name, True)
            master_parent_id = master_parent_node.commit.id
            local_branch_logs_from_commit = self.get_local_branch_logs_starting_with_commit(master_commit)

            for local_branch_log in local_branch_logs_from_commit:
                parent_id = master_parent_id
                for commit in local_branch_log[1:]:
                    commit_name = self.get_combined_branch_name_from_commit(commit)
                    commit_has_name = self.does_commit_have_name(commit)
                    parent_node = self.tree.insert(parent_id, commit, commit_name, commit_has_name, False)
                    parent_id = parent_node.commit.id
        self.tree.refresh_nodes_staleness_status()

    def get_combined_branch_name_from_commit(self, commit):
        names = self.get_commit_names(commit)
        combined_names = ""
        for name in names:
            if not name == names[0]:
                combined_names = combined_names + ", "
            combined_names = combined_names + name
        return combined_names