from colorama import *
from CommitNode import CommitNode

# Colors are ☣
# BLACK, RED, GREEN, YELLOW, BLUE, MAGENTA, CYAN, WHITE, RESET
# Styles are
# NORMAL, BRIGHT
# everythnig else is not supported in Windows.

class NodeColor:
    node = None
    omitted_parent = Fore.CYAN + Style.BRIGHT
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