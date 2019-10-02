import sys
import os
import argparse
from ChainRepository import ChainRepository
from ChainHierarchyPrinter import ChainHierarchyPrinter
from GitCommandPreviewer import GitCommandPreviewer
from pygit2 import Repository
from BranchFilters.BranchFilterer import BranchFilterer
from BranchFilters.BasicBranchFilterer import BasicBranchFilterer
from LegendPrinter import LegendPrinter

def __main__():
    parser = argparse.ArgumentParser(description='Process some integers.')
    parser.add_argument("-f", "--full", help="Replay all commits during preview", action="store_true")
    parser.add_argument("-r", "--reduce", help="Filter to only the branches in the command", action="store_true")

    args, unknown_args = parser.parse_known_args()
    command = "git " + ' '.join(unknown_args)

    validate()
    repo_name = os.getcwd() + "\\.git"

    branch_filterer = BranchFilterer()
    if args.reduce:
        branch_filterer = BasicBranchFilterer(unknown_args)

    repository = Repository(repo_name)
    chain_repo = ChainRepository(repository, branch_filterer)
    commands = ["git checkout " + chain_repo.head_name, command]
    
    LegendPrinter().print_legend()
    print("\nBefore `%s`" % command)
    ChainHierarchyPrinter(chain_repo.tree, chain_repo.head_name).print()
    print("\nAfter `%s`" % command)
    GitCommandPreviewer(chain_repo, not args.full, branch_filterer).preview_commands(commands)
    print()

def validate():
    if not os.path.exists("./.git"):
        print("Must be run inside a repository")

__main__()