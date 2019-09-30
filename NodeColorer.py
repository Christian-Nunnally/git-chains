from colorama import Fore, Style, init
from CommitNode import CommitNode

# Colors are ☣
# BLACK, RED, GREEN, YELLOW, BLUE, MAGENTA, CYAN, WHITE, RESET
# Styles are
# NORMAL, BRIGHT
# everything else is not supported in Windows.

class NodeColorer:
    GrayedNodeColor = Fore.LIGHTBLACK_EX
    NamedNodeColor = Fore.LIGHTBLUE_EX
    CheckedOutNodeColor = Fore.LIGHTGREEN_EX
    DefaultNodeColor = Fore.WHITE
    UpToDateStatusColor = Fore.GREEN + Style.BRIGHT

    def __init__(self):
        init(autoreset=True)

    def color_name(self, name, has_name, is_checked_out, should_gray_out):
        if should_gray_out:
            return NodeColorer.GrayedNodeColor + name + Fore.RESET
        if is_checked_out:
            return NodeColorer.CheckedOutNodeColor + name + Fore.RESET
        if has_name:
            return NodeColorer.NamedNodeColor + name + Fore.RESET
        return NodeColorer.DefaultNodeColor + name + Fore.RESET

    def color_status(self, status):
        return NodeColorer.UpToDateStatusColor + status + Fore.RESET

    def color_excluded_parents(self, excluded_parents):
        return NodeColorer.GrayedNodeColor + excluded_parents + Fore.RESET
