import sys
import os
from pygit2 import *
import argparse
from ChainRepository import ChainRepository
from ChainHierarchyPrinter import ChainHierarchyPrinter
from colorama import *
from Legend import Legend
from GitCommandPreviewer import GitCommandPreviewer

def __main__():
    init(autoreset=True)

    parser = argparse.ArgumentParser(description='Process some integers.')
    parser.add_argument('specified_branches', metavar=('from', 'to'), type=str, nargs='*', help='The names of branches you want to chain')
    parser.add_argument("-l", "--legend", help="Print out help", action="store_true")
    parser.add_argument("-d", "--repo", help="Set the location for the local repo", type=str)
    parser.add_argument("-b", "--branch", help="Set the master branch name", type=str)
    args = parser.parse_args()
        
    local_repo_name = r"C:\ASW\.git"
    if args.repo:
        local_repo_name = args.repo
    elif os.path.exists("./.git"):
        local_repo_name = os.getcwd() + "\\.git"

    master_branch_name = "master"
    if args.branch:
        master_branch_name = args.branch

    if args.legend:
        Legend.print_legend()
        return

    chain_repo = ChainRepository(local_repo_name, master_branch_name)
    printer = ChainHierarchyPrinter(chain_repo)
    printer.print()

__main__()