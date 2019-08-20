import sys
import os
import argparse
from ChainRepository import ChainRepository
from ChainHierarchyPrinter import ChainHierarchyPrinter
from colorama import *
from GitCommandPreviewer import GitCommandPreviewer

def __main__():
    init(autoreset=True)

    parser = argparse.ArgumentParser(description='Process some integers.')
    parser.add_argument("-f", "--full", help="Replay all commits during preview", action="store_true")
    parser.add_argument("-d", "--repo", help="Set the location for the local repo", type=str)
    parser.add_argument("-r", "--reduce", help="Filter to only the branches in the command", action="store_true")

    args, unknown_args = parser.parse_known_args()

    local_repo_name = "C:\ASW\.git"
    if args.repo:
        local_repo_name = args.repo
    elif os.path.exists("./.git"):
        local_repo_name = os.getcwd() + "\\.git"

    local_branches_to_include = []
    if args.reduce:
        local_branches_to_include = unknown_args

    print("\n\nCurrent state:")
    chain_repo = ChainRepository(local_repo_name, local_branches_to_include)
    printer = ChainHierarchyPrinter(chain_repo)
    printer.print()
    
    command = "git " + ' '.join(unknown_args)
    print("\nAfter `%s`:" % command)
    current_branch = chain_repo.repository.head.name.split('/')[-1]
    commands = ["git checkout " + current_branch, command, "git branch"]

    previewer = GitCommandPreviewer(chain_repo, not args.full, local_branches_to_include)
    previewer.preview_commands(commands)

__main__()