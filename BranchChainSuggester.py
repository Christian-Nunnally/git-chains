from CommitTree import CommitTree
from CommitNode import CommitNode
from colorama import *

class BranchChainSuggester:
    def __init__(self, chain_repo):
        self.chain_repo = chain_repo
        self.tree = self.chain_repo.tree

    def suggest(self, branches_names_to_chain, suggest_rebase, suggest_merge):
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
        colored_from_branch_name = Fore.BLUE + Style.BRIGHT + from_branch_name + Fore.RESET
        colored_to_branch_name = Fore.BLUE + Style.BRIGHT + to_branch_name + Fore.RESET
        
        if (suggest_rebase):
            self.suggest_rebase(from_branch_head_commit, to_branch_head_commit, colored_from_branch_name, colored_to_branch_name)
        if (suggest_merge):
            self.suggest_merge(from_branch_head_commit, to_branch_head_commit, colored_from_branch_name, colored_to_branch_name)
    
    def suggest_rebase(self, from_branch_head_commit, to_branch_head_commit, colored_from_branch_name, colored_to_branch_name):
        merge_base = self.chain_repo.repo.merge_base(from_branch_head_commit.commit.id, to_branch_head_commit.commit.id)
        if (merge_base == from_branch_head_commit.commit.id):
            print(colored_from_branch_name + " is already fully merged in to " + colored_to_branch_name)
        else:
            print("\nTo ensure all the changes in " + colored_from_branch_name + " are in " + colored_to_branch_name + " via a rebase:")
            print("\n\t" + "git rebase " + colored_from_branch_name + " " + colored_to_branch_name + "\n")
        
    def suggest_merge(self, from_branch_head_commit, to_branch_head_commit, colored_from_branch_name, colored_to_branch_name):
        merge_base = self.chain_repo.repo.merge_base(from_branch_head_commit.commit.id, to_branch_head_commit.commit.id)
        if (merge_base == from_branch_head_commit.commit.id):
            print(colored_from_branch_name + " is already fully merged in to " + colored_to_branch_name)
        else:
            print("\nTo ensure all the changes in " + colored_from_branch_name + " are in " + colored_to_branch_name + " via a merge:")
            print("\n\t" + "git checkout " + colored_to_branch_name)
            print("\t" + "git merge " + colored_from_branch_name + "\n")

    def get_single_branch_from_substring_of_name(self, name_substring):
        colored_name_substring = Fore.BLUE + Style.BRIGHT + name_substring + Fore.RESET
        matching_branch_head_commits = self.chain_repo.tree.get_nodes_with_sub_string_in_name(name_substring)
        if (not len(matching_branch_head_commits) == 1):
            print(colored_name_substring + " is not a substring of a unique commit, please be more specific")
            if (len(matching_branch_head_commits) != 0):
                print("Commits that partially match " + colored_name_substring + ":\n")
                for commit in matching_branch_head_commits:
                    substring_index = commit.pretty_name.index(name_substring)
                    print("\t" + commit.pretty_name[:substring_index] + colored_name_substring + commit.pretty_name[substring_index + len(name_substring):])
                print()
            return None
        return matching_branch_head_commits[0]
