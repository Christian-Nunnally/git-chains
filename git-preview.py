import sys
import os
from pygit2 import *
import argparse
from ChainRepository import ChainRepository
from ChainHierarchyPrinter import ChainHierarchyPrinter
from BranchChainSuggester import BranchChainSuggester
from colorama import *
from GitCommandPreviewer import GitCommandPreviewer

def __main__():
    init(autoreset=True)

    parser = argparse.ArgumentParser(description='Process some integers.')
    # parser.add_argument('git command', metavar=('from', 'to'), type=str, nargs='*', help='The names of branches you want to chain')
    parser.add_argument("-f", "--full", help="Replay all commits during preview", action="store_true")
    parser.add_argument("-d", "--repo", help="Set the location for the local repo", type=str)
    parser.add_argument("-b", "--branch", help="Set the master branch name", type=str)
    args, unknown_args = parser.parse_known_args()

    local_repo_name = "C:\ASW\.git"
    if args.repo:
        local_repo_name = args.repo
    elif os.path.exists("./.git"):
        local_repo_name = os.getcwd() + "\\.git"

    print()
    
    master_branch_name = "master"
    if args.branch:
        master_branch_name = args.branch

    chain_repo = ChainRepository(local_repo_name, master_branch_name)
    printer = ChainHierarchyPrinter(chain_repo)
    printer.print()
    
    command = "git " + ' '.join(unknown_args)
    previewer = GitCommandPreviewer(chain_repo)
    previewer.preview_command(command, not args.full)

__main__()