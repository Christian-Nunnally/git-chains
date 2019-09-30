from BranchFilters.BranchFilterer import BranchFilterer

class OringBranchFilterer(BranchFilterer):
    def __init__(self, filterers):
        self.filterers = filterers
    
    def should_include_branch(self, branch_name):
        for filter in self.filterers:
            if (filter.should_include_branch(branch_name)):
                return True
        return False