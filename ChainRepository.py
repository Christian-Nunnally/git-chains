import pygit2

from CommitTreeBuilder import CommitTreeBuilder
from Interoperability.ShellCommandExecuter import ShellCommandExecuter
from GitRepositoryWalker import GitRepositoryWalker
from Logger import Logger

class ChainRepository():
    """ 
    Calculates and stores the useful section of a repositories log in a tree.
    
    The useful section is defined as all of the commits that are ancesters of
    the merge base between all of the local_branches_to_include.
    """
    def __init__(self, repository_path, local_branches_to_include):
        self.really_long_commit_chain_warning_limit = 500
        self.local_branches_to_include = local_branches_to_include
        self.repository_directory = repository_path[:-4]
        self.local_branch_logs_to_merge_base = []
        self.local_feature_branches = []
        self.local_branch_names = []
        self.local_branches = []
        self.branch_name_map = {}
        self.logger = Logger(self)
        self.tree = None
        self.repository = None
        self.head_name = ""
        self.initialize()

    def initialize(self):
        self.logger.log("Loading repository")
        self.initialize_repository()
        self.logger.log("Initializing branches")
        self.initialize_branches()
        self.logger.log("Calculating octopus merge base")
        self.calculate_octopus_merge_base()
        self.logger.log("Walking local branch logs to octopus merge base")
        self.generate_local_branch_logs_to_merge_base()
        self.logger.log("Building tree from local branch logs")
        self.build_commit_tree()

    def initialize_repository(self):
        self.repository = pygit2.Repository(self.repository_directory + "/.git")
        self.head_name = self.repository.head.name.split('/')[-1]

    def initialize_branches(self):
        for branch_name in self.repository.branches.local:
            if self.should_include_branch(branch_name):
                self.include_branch(branch_name)
        self.populate_branch_name_map()
        self.validate_repository()

    def validate_repository(self):
        if len(self.local_branch_names) == 0:
            self.logger.warning("No branches analyzed. Make sure you have at least one branch included in your filter.")    

    def include_branch(self, branch_name):
        self.local_branch_names.append(branch_name)
        self.local_branches.append(self.repository.branches[branch_name])

    def should_include_branch(self, branch_name):
        if len(self.local_branches_to_include) == 0:
            return True
        return branch_name in self.local_branches_to_include

    def calculate_octopus_merge_base(self):
        args = ['git', 'merge-base', '--octopus'] + self.local_branch_names
        executer = ShellCommandExecuter(self.repository_directory, args)
        self.octopus_merge_base = executer.execute_for_output()

    def generate_local_branch_logs_to_merge_base(self):
        for branch in self.local_branches:
            self.logger.log("Walking the history of " + branch.name + " to octopus merge base")
            branch_log_to_octopus_merge_base = self.generate_branch_log_to_octopus_merge_base(branch)
            self.local_branch_logs_to_merge_base.append(branch_log_to_octopus_merge_base)

    def generate_branch_log_to_octopus_merge_base(self, branch):
        number_of_commits_walked = 0
        branch_log_to_octopus_merge_base = []
        start_commit = self.repository.get(branch.target)

        walker = GitRepositoryWalker(self.repository_directory)
        for commit in walker.walk(start_commit, self.octopus_merge_base):
            print(commit.id)
            print(self.octopus_merge_base)
            branch_log_to_octopus_merge_base.append(commit)

        # for commit in self.walk_from_branch(branch.target):
        #     number_of_commits_walked += 1
        #     if self.is_ancestor(commit.hex, self.octopus_merge_base):
        #         branch_log_to_octopus_merge_base.append(commit)
        #         if commit.hex == self.octopus_merge_base:
        #             break
        #     if number_of_commits_walked == self.really_long_commit_chain_warning_limit:
        #        self.logger.warning("%s commits have been traversed from %s and the merge base has not been found. Consider filtering this branch out." % (self.really_long_commit_chain_warning_limit, branch.name))
        return branch_log_to_octopus_merge_base
        return self.reverse(branch_log_to_octopus_merge_base)

    def reverse(self, collection):
        collection.reverse()
        return collection

    def walk_from_branch(self, branch):
        return self.repository.walk(branch, pygit2.GIT_SORT_TOPOLOGICAL) 

    def is_ancestor(self, commit, possible_ancestor):
        args = ['git', 'merge-base', '--is-ancestor', possible_ancestor, commit]
        executer = ShellCommandExecuter(self.repository_directory, args)
        return not executer.execute_for_return_code()

    def populate_branch_name_map(self):
        for branch in self.local_branches:
            branch_name = self.format_branch_name(branch.name)
            self.append_to_branch_name_map(branch.target.hex, branch_name)

    def format_branch_name(self, branch_name):
        if (branch_name.startswith("refs/heads/")):
            return branch_name[len("refs/heads/"):]
        return branch_name

    def append_to_branch_name_map(self, commit_id, name):
        if (not commit_id in self.branch_name_map):
            self.branch_name_map[commit_id] = []
        self.branch_name_map[commit_id].append(name)  

    def build_commit_tree(self):
        builder = CommitTreeBuilder(self.octopus_merge_base, self.repository_directory, self.branch_name_map, self)
        self.tree = builder.build_commit_tree(self.local_branch_logs_to_merge_base)
