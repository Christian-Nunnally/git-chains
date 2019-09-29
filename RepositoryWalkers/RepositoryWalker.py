from pygit2 import GIT_SORT_TOPOLOGICAL

class RepositoryWalker:
    def __init__(self, repository):
        self.repository = repository

    def walk(self, branch):
        for commit in self.repository.walk(branch.target, GIT_SORT_TOPOLOGICAL):
            yield commit