from Printer import Printer
from CommitTree import CommitTree
from NodeColor import NodeColor
import os

class ChainHierarchyPrinter(Printer):
    def __init__(self, tree, master_log):
        self.no_vertical_white_space = True
        self.single_line_vertical_white_space = False
        self.exclude_nodes_with_one_child = True
        self.verbose_branch_names = False
        self.show_omitted_parents = True
        self.show_reference_nodes = False
        self.always_print_nodes_with_names = True
        self.align_left = False
        self.horizontial_spaces = 3
        self.commit_style = '●'
        self.tree = tree
        self.master_log = master_log

    def print(self):
        text_list = self.build_text_list()
        self.decorate_text_list(text_list)
        for line in text_list:
            for char in line:
                print(char, end="")
            print()

    def build_text_list(self):
        text_list = []
        start_node = self.tree.root
        self.build_list_from_node_recursively(start_node, text_list, 0, False)
        return text_list

    def build_list_from_node_recursively(self, node, text_list, left_spaces, omitted_parent):
        if (not (self.always_print_nodes_with_names and node.has_name)):
            if (not (self.show_reference_nodes and node.is_reference_node)):
                if self.exclude_nodes_with_one_child and len(node.children) == 1:
                    self.build_list_from_node_recursively(node.children[0], text_list, left_spaces, True)
                    return

        sorted_children = self.sorted_children(node.children)

        pretty_name = str(node.pretty_name)
        if (not self.verbose_branch_names):
            pretty_name = os.path.basename(pretty_name)
        line = list(str(pretty_name))
        
        line.insert(0, ' ')
        if (len(sorted_children) > 0):
            line.insert(0, '┐')
        line.insert(0, self.commit_style)
        if (omitted_parent and self.show_omitted_parents):
            line.insert(0, '◌')
        else:
            line.insert(0, '─')
        for i in range(self.horizontial_spaces - 3):
            line.insert(0, '─')
        line.insert(0, '└')
        for i in range(left_spaces):
            line.insert(0, ' ')    
        text_list.append(line)

        sorted_children = self.sorted_children(node.children)
        for child in sorted_children:
            self.build_list_from_node_recursively(child, text_list, left_spaces + self.horizontial_spaces, False)
        
        if (not self.no_vertical_white_space):
            if (self.single_line_vertical_white_space):
                if (len(text_list) > 0 and not len(text_list[-1]) == 0):
                    text_list.append([])
            else:
                text_list.append([])

    def sorted_children(self, children):
        sortedList = sorted(children, key=lambda child: child.commit.commit_time)
        sortedList.reverse()
        return sortedList

    def get_master_branch_commit(self):
        return self.master_log[len(self.master_log - 1)]

    def decorate_text_list(self, text_list):
        self.add_header_to_text_list(text_list)
        self.normalize_text_list(text_list)
        self.extend_pipes_up(text_list)
        self.fix_joints(text_list)
        if (self.align_left):
            self.inline_left_commits(text_list)
        self.remove_tailing_whitespace(text_list)

    def inline_left_commits(self, text_list):
        for line_number in range(len(text_list) * 2 + 1):
            if (line_number >= len(text_list) - 2):
                break
            line = text_list[line_number]
            for i in range(len(line) - 1):
                char = line[i]
                if (char == '└'):
                    self.remove_leading_spaces(text_list[line_number + 1:], self.horizontial_spaces)
                    text_list.insert(line_number + 1, list('┌' + ('─' * (self.horizontial_spaces - 1)) +  '┘'))
                    break
                else:
                    break

    def remove_leading_spaces(self, text_list, spaces_to_remove):
        for line in text_list:
            for i in range(spaces_to_remove):
                if (line[0] == ' '):
                    line.pop(0)

    def remove_tailing_whitespace(self, text_list):
        for i in range(len(text_list)):
            text_list[i] = list(''.join(text_list[i]).rstrip())

    def normalize_text_list(self, text_list):
        longest_line = 0
        for line in text_list:
            if (len(line) > longest_line):
                longest_line = len(line)
        for line in text_list:
            while (len(line) < longest_line):
                line.append(' ')

    def extend_pipes_up(self, text_list):
        for line_number in range(len(text_list)):
            line = text_list[line_number]
            for char_number in range(len(line)):
                char = line[char_number]
                if (char == '└'):
                    self.extend_pipes_up_recursive(text_list, char_number, line_number - 1)

    def extend_pipes_up_recursive(self, text_list, x, y):
        if (y <= 0):
            return
        if (text_list[y][x] != ' '):
            return
        text_list[y][x] = '│'
        self.extend_pipes_up_recursive(text_list, x, y - 1)
    
    def fix_joints(self, text_list):
        for line_number in range(len(text_list) - 1):
            line = text_list[line_number]
            for char_number in range(len(line)):
                char = line[char_number]
                next_line = text_list[line_number + 1]
                if (len(next_line) > char_number):
                    next_char = next_line[char_number]
                    if (next_char == '│' or next_char == '└'):
                        if (char == '└'):
                            line[char_number] = "├"
                        elif (char == "─"):
                            line[char_number] = "┐"

    def add_header_to_text_list(self, text_list):
        text_list.insert(0, ['↓'])
        text_list.insert(1, ['.'])
        text_list.insert(2, ['¦'])
        text_list.insert(3, ['¦'])
