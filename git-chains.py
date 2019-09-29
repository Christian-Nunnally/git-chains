import os
import argparse
import colorama
from pygit2 import Repository
from ChainRepository import ChainRepository
from ChainHierarchyPrinter import ChainHierarchyPrinter
from BranchFilters.HeadToMasterBranchFilterer import HeadToMasterBranchFilterer
from BranchFilters.BranchFilterer import BranchFilterer
from BranchFilters.BasicBranchFilterer import BasicBranchFilterer

def __main__():
    colorama.init(autoreset=True)
    parser = argparse.ArgumentParser()
    parser.add_argument('branches_to_include', type=str, nargs='*', help='The branches you want to include in the map')
    args = parser.parse_args()
    repo_name = get_repo_name()
    repository = Repository(repo_name)
    branch_filterer = get_branch_filterer(repository, args.branches_to_include)
    chain_repo = ChainRepository(repository, branch_filterer)
    printer = ChainHierarchyPrinter(chain_repo.tree, chain_repo.head_name)
    printer.print()

def get_repo_name():
    if not os.path.exists("./.git"):
        print("Must run inside a repository")
        return
    return os.getcwd() + "\\.git"

def get_branch_filterer(repository, branches_to_include):
    if len(branches_to_include) > 0:
        if "all" in branches_to_include:
            return BranchFilterer()
        return BasicBranchFilterer(branches_to_include)
    return HeadToMasterBranchFilterer(repository)

__main__()