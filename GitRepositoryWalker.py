from Interoperability.ShellCommandExecuter import ShellCommandExecuter

class GitRepositoryWalker:
    def __init__(self, repository_directory):
        self.repository_directory = repository_directory

    def walk(self, current_commit, target_commit_id):
        print(current_commit)
        yield current_commit
        if current_commit.id != target_commit_id:
            parents_that_are_ancestors_of_target = []
            if len(current_commit.parents) != 1:
                for parent in current_commit.parents:
                    if self.is_ancestor(parent.hex, target_commit_id):
                        parents_that_are_ancestors_of_target.append(parent)
            else:
                parents_that_are_ancestors_of_target = current_commit.parents

            for parent in parents_that_are_ancestors_of_target:
                yield from self.walk(parent, target_commit_id)

    def is_ancestor(self, commit, possible_ancestor):
        args = ['git', 'merge-base', '--is-ancestor', possible_ancestor, commit]
        executer = ShellCommandExecuter(self.repository_directory, args)
        return not executer.execute_for_return_code()
