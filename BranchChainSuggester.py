from CommitTree import CommitTree
from CommitNode import CommitNode
from colorama import *

class BranchChainSuggester:
    def __init__(self, chain_repo):
        self.chain_repo = chain_repo
        self.tree = self.chain_repo.tree

    def suggest(self, branches_names_to_chain):
        if (len(branches_names_to_chain) != 2):
            return
        
        from_branch_head_commit = self.get_single_branch_from_substring_of_name(branches_names_to_chain[0])
        to_branch_head_commit = self.get_single_branch_from_substring_of_name(branches_names_to_chain[1])

        if (from_branch_head_commit == None or to_branch_head_commit == None):
            return
        if (from_branch_head_commit == to_branch_head_commit):
            print("You cant merge or rebase a branch with itself")
            return

        from_branch_name = from_branch_head_commit.pretty_name
        to_branch_name = to_branch_head_commit.pretty_name
        
        merge_base = self.chain_repo.repo.merge_base(from_branch_head_commit.commit.id, to_branch_head_commit.commit.id)
        if (merge_base == from_branch_head_commit):
            print(from_branch_name + " is already full merged in to " + to_branch_name)
        else:
            print("\nTo ensure all the changes in " + from_branch_name + " are in " + to_branch_name + " via a rebase:")
            print("\n\t" + "git rebase " + from_branch_name + " " + to_branch_name + "\n")
    
    def get_single_branch_from_substring_of_name(self, name_substring):
        matching_branch_head_commits = self.chain_repo.tree.get_nodes_with_sub_string_in_name(name_substring)
        if (not len(matching_branch_head_commits) == 1):
            print(name_substring + " is not a substring of a unique commit, please make the branch name more specific")
            print("Commits that partially match " + name_substring + ":\n")
            for commit in matching_branch_head_commits:
                print("\t" + commit.pretty_name)
            return None
        return matching_branch_head_commits[0]
