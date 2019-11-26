import os
import argparse
import colorama
from pygit2 import Repository
from ChainRepository import ChainRepository
from ChainHierarchyPrinter import ChainHierarchyPrinter
from BranchFilters.HeadToMasterBranchFilterer import HeadToMasterBranchFilterer
from BranchFilters.BranchFilterer import BranchFilterer
from BranchFilters.BasicBranchFilterer import BasicBranchFilterer
from LegendPrinter import LegendPrinter
from DigraphWrapper import DigraphWrapper
from Logger import Logger

def __main__():
    colorama.init(autoreset=True)
    parser = argparse.ArgumentParser()
    parser.add_argument('branches_to_include', type=str, nargs='*', help='The branches you want to include in the map')
    parser.add_argument("-r", "--render", help="generate png of repo", action="store_true")
    parser.add_argument("-v", "--verbose", help="print logging information", action="store_true")
    args = parser.parse_args()

    Logger.enable_logging = args.verbose

    repo_name = get_repo_name()
    repository = Repository(repo_name)
    branch_filterer = get_branch_filterer(repository, args.branches_to_include)
    chain_repo = ChainRepository(repository, branch_filterer)
    printer = ChainHierarchyPrinter(chain_repo.tree, chain_repo.head_name)
    if (args.render):
        digraph = DigraphWrapper(chain_repo.tree.root)
        print(str(digraph))
    LegendPrinter().print_legend()
    printer.print()
    print()

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