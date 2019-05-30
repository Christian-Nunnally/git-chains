from colorama import *
from NodeColor import NodeColor
from ChainHierarchyPrinter import ChainHierarchyPrinter

class Legend:

    @staticmethod
    def print_legend():
        init(autoreset=True)
        print()
        print(Fore.LIGHTWHITE_EX + "Text Colors")
        print(NodeColor.DefaultNodeColor + "\t0u812 " + Fore.RESET + "Default Node")
        print(NodeColor.ReferenceNodeColor + "\t0u812 " + Fore.RESET + "Reference Node")
        print(NodeColor.NamedNodeColor + "\t0u812 " + Fore.RESET + "Named Node")
        print(Fore.LIGHTWHITE_EX + "Status Dot Significance")
        print("\t" + ChainHierarchyPrinter.CommitIndicator + " Node status")
        print("\t" + ChainHierarchyPrinter.HiddenParentIndicator + " Hidden parent(s) status")
        print(Fore.LIGHTWHITE_EX + "Status Dot Colors")
        print(NodeColor.UpToDateStatusColor + "\t" + ChainHierarchyPrinter.CommitIndicator + Fore.LIGHTBLACK_EX + " Good status")
        print(NodeColor.StaleStatusColor + "\t" + ChainHierarchyPrinter.CommitIndicator + Fore.LIGHTBLACK_EX + " Stale status")
        print()