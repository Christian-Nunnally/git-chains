import sys
from pygit2 import *
import argparse
from ChainRepository import ChainRepository
from ChainHierarchyPrinter import ChainHierarchyPrinter
from BranchChainSuggester import BranchChainSuggester
from Legend import Legend

local_repo_name = "C:\TestingRepo\.git"
master_branch_name = "master"

def __main__():
    Legend.print_legend()

    chain_repo = ChainRepository(local_repo_name, master_branch_name)

    parser = argparse.ArgumentParser(description='Process some integers.')
    parser.add_argument('specified_branches', metavar=('from', 'to'), type=str, nargs='*', help='The names of branches you want to chain')
    parser.add_argument('help', type=bool, help='Prints the help for Chains')
    args = parser.parse_args()

    number_of_branches_specified = len(args.specified_branches)
    if number_of_branches_specified == 0:
        printer = ChainHierarchyPrinter(chain_repo)
        printer.print()
    elif number_of_branches_specified == 1:
        pass
    elif number_of_branches_specified == 2:
        suggester = BranchChainSuggester(chain_repo)
        suggester.suggest(args.specified_branches)
    print()

__main__()