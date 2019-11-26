from CommitTreeBuilder import CommitTreeBuilder
from Interoperability.ShellCommandExecuter import ShellCommandExecuter
from Logger import Logger
from RepositoryWalkers.BranchToCommitWalker import BranchToCommitWalker

class ChainRepository():
    """ 
    Calculates and stores a section of a repositories log in a tree.
    
    The tree will contain commits that are both:
    - An ancester of at least one of the inlcuded branches.
    - A child of the merge base between all of the included branches.

    The branch_inclusion_filterer is a predicate that decides which branches should be included. 
    """
    def __init__(self, repository, branch_inclusion_filterer):
        self.branch_inclusion_filterer = branch_inclusion_filterer
        self.repository_directory = repr(repository).split('\'')[1][:-4]
        self.local_branch_logs_to_merge_base = []
        self.local_feature_branches = []
        self.local_branch_names = [] 
        self.local_branches = []
        self.branch_name_map = {}
        self.logger = Logger(self)
        self.tree = None
        self.repository = repository
        self.head_name = self.repository.head.name.split('/')[-1]
        self.initialize()

    def initialize(self):
        self.logger.log("Initializing branches")
        self.initialize_branches()
        self.logger.log("Calculating octopus merge base")
        self.calculate_octopus_merge_base()
        self.logger.log("Walking local branch logs to octopus merge base")
        self.generate_local_branch_logs_to_merge_base()
        self.logger.log("Building tree from local branch logs")
        self.build_commit_tree()

    def initialize_branches(self):
        for branch_name in self.repository.branches.local:
            if self.branch_inclusion_filterer.should_include_branch(branch_name):
                self.logger.log("Including: " + branch_name)
                self.include_branch(branch_name)
            else:
                self.logger.log("Excluding: " + branch_name)
        self.logger.log("Populating branch name map")
        self.populate_branch_name_map()
        self.validate_repository()

    def validate_repository(self):
        if len(self.local_branch_names) == 0:
            self.logger.warning("No branches analyzed. Make sure you have at least one branch included in your filter.")    

    def include_branch(self, branch_name):
        self.local_branch_names.append(branch_name)
        self.local_branches.append(self.repository.branches[branch_name])

    def calculate_octopus_merge_base(self):
        args = ['git', 'merge-base', '--octopus'] + self.local_branch_names
        executer = ShellCommandExecuter(self.repository_directory, args)
        self.octopus_merge_base = executer.execute_for_output()

    def generate_local_branch_logs_to_merge_base(self):
        walker = BranchToCommitWalker(self.repository, self.octopus_merge_base)
        for branch in self.local_branches:
            self.logger.log("Walking the history of " + branch.name + " to octopus merge base")
            branch_log_to_merge_base = self.reverse([c for c in walker.walk(branch)])
            self.local_branch_logs_to_merge_base.append(branch_log_to_merge_base)

    def reverse(self, collection):
        collection.reverse()
        return collection

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
