from BranchFilters.BranchFilterer import BranchFilterer

class BasicBranchFilterer(BranchFilterer):
    def __init__(self, branch_names_to_include):
        self.branch_names_to_include = branch_names_to_include

    def should_include_branch(self, branch_name):
        return branch_name in self.branch_names_to_include