from colorama import *
from CommitNode import CommitNode

# Colors are ☣
# BLACK, RED, GREEN, YELLOW, BLUE, MAGENTA, CYAN, WHITE, RESET
# Styles are
# NORMAL, BRIGHT
# everythnig else is not supported in Windows.

class NodeColor:
    node = None
    omitted_parent = Fore.GREEN + Style.BRIGHT
    name_color = Fore.RED
    status_color = Fore.RED
    reset = Fore.RESET

    def __init__(self, node):
        init(autoreset=True)
        self.node = node

        if node.is_reference_node:
            self.name_color = Fore.BLACK + Style.BRIGHT
        elif node.has_name:
            self.name_color = Fore.WHITE + Style.BRIGHT
        else:
            self.name_color = Fore.WHITE + Style.NORMAL

        if node.parent != None:
            if node.parent.is_stale:
                self.status_color = Fore.YELLOW + Style.DIM
                self.omitted_parent = Fore.YELLOW + Style.DIM
            elif node.parent.is_part_of_master:
                self.omitted_parent = Fore.WHITE + Style.BRIGHT

        if node.is_stale:
            self.status_color = Fore.YELLOW + Style.DIM
        elif node.is_part_of_master:
            self.status_color = Fore.WHITE + Style.NORMAL
        else:
            self.status_color = Fore.GREEN + Style.BRIGHT