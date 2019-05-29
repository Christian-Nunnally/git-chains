from colorama import *
from CommitNode import CommitNode

class NodeColor:
    node = None
    color = Fore.RED
    reset = Fore.RESET

    def __init__(self, node):
        init(autoreset=True)
        self.node = node
        if (node.is_reference_node):
            self.color = Fore.YELLOW + Style.BRIGHT
        elif (node.children):
            self.color = Fore.GREEN + Style.BRIGHT
        else:
            self.color = Fore.BLUE + Style.BRIGHT