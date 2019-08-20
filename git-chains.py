import os
import argparse
import colorama
from ChainRepository import ChainRepository
from ChainHierarchyPrinter import ChainHierarchyPrinter

def __main__():
    colorama.init(autoreset=True)

    parser = argparse.ArgumentParser()
    parser.add_argument('branches_to_include', type=str, nargs='*', help='The branches you want to include in the map')
    parser.add_argument("-r", "--repo", help="Set the location for the local repo", type=str)
    args = parser.parse_args()
        
    local_repo_name = r"C:\ASW\.git"
    if args.repo:
        local_repo_name = args.repo
    elif os.path.exists("./.git"):
        local_repo_name = os.getcwd() + "\\.git"

    chain_repo = ChainRepository(local_repo_name, args.branches_to_include)
    printer = ChainHierarchyPrinter(chain_repo.tree, chain_repo.head_name)
    printer.print()

__main__()