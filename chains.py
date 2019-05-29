from pygit2 import *
from ChainRepository import ChainRepository

local_repo_name = "C:\\Users\\bhealy\\source\\repos\\ASW\\.git"
master_branch_name = "users/bhealy/sketch/2"
repo = Repository(local_repo_name)

def __main__():
    chain_repo = ChainRepository(local_repo_name, master_branch_name)
    chain_repo.print_chains_from_tree()

__main__()