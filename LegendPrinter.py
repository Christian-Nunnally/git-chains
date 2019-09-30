from NodeColorer import NodeColorer

class LegendPrinter:
    def print_legend(self):
        print("Legend:")
        colorer = NodeColorer()
        print(colorer.color_name("◌◌◌◌◌ hidden-commits (4)", False, False, True))
        print(colorer.color_name("◌·6·◌ hidden-commits (8)", False, False, True))
        print(colorer.color_name("●     commit", False, False, False))
        print(colorer.color_name("●     branch", True, False, False))
        print(colorer.color_name("●     current-head", True, True, False))
        print(colorer.color_name("●     merged-branch", False, False, True))