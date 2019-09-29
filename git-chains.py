import os
import argparse
import colorama
from pygit2 import Repository
from ChainRepository import ChainRepository
from ChainHierarchyPrinter import ChainHierarchyPrinter
from BranchFilters.HeadToMasterBranchFilterer import HeadToMasterBranchFilterer
from BranchFilters.BranchFilterer import BranchFilterer

def __main__():
    colorama.init(autoreset=True)

    parser = argparse.ArgumentParser()
    parser.add_argument('branches_to_include', type=str, nargs='*', help='The branches you want to include in the map')
    args = parser.parse_args()

    if not os.path.exists("./.git"):
        print("Must run inside a repository")
        return
    repo_name = os.getcwd() + "\\.git"

    repository = Repository(repo_name)
    branch_filterer = None
    if "all" in args.branches_to_include:
        branch_filterer = BranchFilterer()
    else:
        branch_filterer = HeadToMasterBranchFilterer(repository)
    chain_repo = ChainRepository(repository, branch_filterer)
    printer = ChainHierarchyPrinter(chain_repo.tree, chain_repo.head_name)
    printer.print()

__main__()