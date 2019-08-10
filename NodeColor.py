from colorama import Fore, init, Style
from CommitNode import CommitNode

# Colors are ☣
# BLACK, RED, GREEN, YELLOW, BLUE, MAGENTA, CYAN, WHITE, RESET
# Styles are
# NORMAL, BRIGHT
# everything else is not supported in Windows.

class NodeColor:
    ReferenceNodeColor = Fore.LIGHTBLACK_EX
    NamedNodeColor = Fore.LIGHTBLUE_EX
    HighlightedNodeColor = Fore.LIGHTGREEN_EX
    DefaultNodeColor = Fore.WHITE

    StaleStatusColor = Fore.YELLOW + Style.NORMAL
    UpToDateStatusColor = Fore.GREEN + Style.BRIGHT

    node = None
    omitted_parent = Fore.GREEN + Style.BRIGHT
    name_color = Fore.RED
    status_color = Fore.RED
    reset = Fore.RESET

    def __init__(self, node, highlight_string):
        init(autoreset=True)
        self.node = node

        if node.has_name:
            self.name_color = NodeColor.NamedNodeColor
            if (highlight_string in node.pretty_names):
                self.name_color = NodeColor.HighlightedNodeColor
        else:
            self.name_color = NodeColor.DefaultNodeColor

        if node.parent != None:
            if node.parent.is_stale:
                self.status_color = NodeColor.StaleStatusColor
                self.omitted_parent = NodeColor.StaleStatusColor
            elif node.parent.is_part_of_master:
                self.omitted_parent = NodeColor.DefaultNodeColor + Style.BRIGHT

        if node.is_stale:
            self.status_color = NodeColor.StaleStatusColor
        elif node.is_part_of_master:
            self.status_color = NodeColor.DefaultNodeColor
        else:
            self.status_color = NodeColor.UpToDateStatusColor