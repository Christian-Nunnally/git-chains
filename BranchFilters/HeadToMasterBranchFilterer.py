from BranchFilters.BranchFilterer import BranchFilterer
from Interoperability.ShellCommandExecuter import ShellCommandExecuter
from RepositoryWalkers.BranchToCommitWalker import BranchToCommitWalker
from Logger import Logger

class HeadToMasterBranchFilterer(BranchFilterer):
    def __init__(self, repository):
        self.logger = Logger(self)
        self.repository = repository
        self.repository_directory = repr(repository).split('\'')[1][:-4]
        self.head_branch_name = self.repository.head.name[11:]
        self.generate_log_from_head_to_merge_base()

    def generate_log_from_head_to_merge_base(self):
        self.logger.log("Determining commit ids between the current head and master:")
        self.log_from_head_to_merge_base = []
        self.logger.log("v head v")
        for id in self.walk_log_from_head_to_merge_base():
            self.log_from_head_to_merge_base.append(id)
            self.logger.log(id)
        self.logger.log("^ master ^")        

    def walk_log_from_head_to_merge_base(self):
        head_master_merge_base = self.get_merge_base("master", self.head_branch_name)
        walker = BranchToCommitWalker(self.repository, head_master_merge_base)
        head_branch = self.repository.branches[self.head_branch_name]
        for commit in walker.walk(head_branch):
            yield commit.hex

    def get_merge_base(self, branch_name, other_branch_name):
        args = ['git', 'merge-base', branch_name, other_branch_name]
        executer = ShellCommandExecuter(self.repository_directory, args)
        return executer.execute_for_output()

    def should_include_branch(self, branch_name):
        merge_base = self.get_merge_base(self.head_branch_name, branch_name)
        return merge_base in self.log_from_head_to_merge_base
