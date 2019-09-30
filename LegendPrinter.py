from NodeColorer import NodeColorer

class LegendPrinter:
    def print_legend(self):
        print()
        print("---- Legend ----")
        colorer = NodeColorer()
        print(colorer.color_name("● head", True, True, False))
        print(colorer.color_name("● branch", True, False, False))
        print(colorer.color_name("● commit", False, False, False))
        print(colorer.color_name("● merged-branch", False, False, True))
        print(colorer.color_excluded_parents("◌ hidden-commit"))