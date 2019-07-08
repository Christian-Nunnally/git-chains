import sys
import os
from pygit2 import *
import argparse
from ChainRepository import ChainRepository
from ChainHierarchyPrinter import ChainHierarchyPrinter
from BranchChainSuggester import BranchChainSuggester
from colorama import *
from Legend import Legend

def __main__():
    init(autoreset=True)

    parser = argparse.ArgumentParser(description='Process some integers.')
    parser.add_argument('specified_branches', metavar=('from', 'to'), type=str, nargs='*', help='The names of branches you want to chain')
    parser.add_argument("-l", "--legend", help="Print out help", action="store_true")
    parser.add_argument("-r", "--rebase", help="Use the rebase strategy", action="store_true")
    parser.add_argument("-m", "--merge", help="Use the merge strategy", action="store_true")
    parser.add_argument("-s", "--show", help="Show the branch chain tree", action="store_true")
    parser.add_argument("-d", "--repo", help="Set the location for the local repo", type=str)
    parser.add_argument("-b", "--branch", help="Set the master branch name", type=str)
    args = parser.parse_args()

    if not args.rebase and not args.merge:
        args.merge = True

    number_of_branches_specified = len(args.specified_branches)
    if number_of_branches_specified == 0:
        args.show = True
        
    local_repo_name = "C:\ASW\.git"
    if args.repo:
        local_repo_name = args.repo
    elif os.path.exists("./.git"):
        local_repo_name = os.getcwd() + "\\.git"

    # print("using repo: " + local_repo_name)
    print()
    
    master_branch_name = "master"
    if args.branch:
        master_branch_name = args.branch

    if args.legend:
        Legend.print_legend()
        return

    chain_repo = ChainRepository(local_repo_name, master_branch_name)

    if args.show:
        printer = ChainHierarchyPrinter(chain_repo)
        printer.print()

    if number_of_branches_specified == 2:
        suggester = BranchChainSuggester(chain_repo)
        suggester.suggest(args.specified_branches, args.rebase, args.merge)
__main__()