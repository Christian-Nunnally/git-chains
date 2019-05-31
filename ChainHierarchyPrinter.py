from CommitTree import CommitTree
from NodeColor import NodeColor
import os

class ChainHierarchyPrinter:
    CommitIndicator = '●'
    HiddenParentIndicator = '◌'

    def __init__(self, chain_repo):
        self.vertical_white_space_between_chains_off_master = True
        self.exclude_nodes_with_one_child = False
        self.verbose_branch_names = False
        self.show_reference_nodes = False
        self.always_print_nodes_with_names = True
        self.show_individual_excluded_parents = False
        self.align_left = False
        self.horizontial_spaces = 3
        self.commit_style = ChainHierarchyPrinter.CommitIndicator
        self.parent_style = ChainHierarchyPrinter.HiddenParentIndicator

        self.tree = chain_repo.tree
        self.master_log = chain_repo.master_log

    def print(self):
        text_list = self.build_text_list()
        self.decorate_text_list(text_list)
        for line in text_list:
            print(line)

    def build_text_list(self):
        text_list = []
        start_node = self.tree.root
        self.build_text_list_recursively(start_node, text_list, 0, False)
        return text_list

    def build_text_list_recursively(self, node, text_list, left_spaces, omitted_parents):
        if self.should_skip_over_node(node):
            self.build_text_list_recursively(node.children[0], text_list, left_spaces, omitted_parents + 1)
            return
            
        sorted_children = self.sorted_children(node.children)

        pretty_name = node.pretty_name
        if (not self.verbose_branch_names):
            pretty_name = os.path.basename(pretty_name)
        color = NodeColor(node)
        line = str(color.name_color + pretty_name)
        
        line = ' ' + line
        if (len(sorted_children) > 0):
            line = '┐' + line

        line = color.status_color + self.commit_style + color.reset + line

        if (omitted_parents > 0):
            if (not self.show_individual_excluded_parents):
                omitted_parents = 1
            line = color.omitted_parent + (self.parent_style * omitted_parents) + color.reset + line
        else:
            line = '─' + line

        for i in range(self.horizontial_spaces - 3):
            line = '─' + line

        line = '└' + line
        for i in range(left_spaces):
            line = ' ' + line
            
        text_list.append(line)

        sorted_children = self.sorted_children(node.children)
        for child in sorted_children:
            self.build_text_list_recursively(child, text_list, left_spaces + self.horizontial_spaces, 0)
        
        self.add_vertical_whitespace_if_needed(text_list)

    def should_skip_over_node(self, node):
        if self.always_print_nodes_with_names and node.has_name:
            return False
        if self.show_reference_nodes and node.is_reference_node:
            return False
        if self.exclude_nodes_with_one_child and (len(node.children) == 1):
            return True
        return False

    def add_vertical_whitespace_if_needed(self, text_list):
        if (self.vertical_white_space_between_chains_off_master):
            if (len(text_list) > 0 and not len(text_list[-1]) == 0):
                text_list.append('')

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
        line_number = 0
        while(True):
            if (line_number >= len(text_list) - 3):
                break
            line_number += 1
            if (text_list[line_number][0] == '└'):
                self.remove_leading_spaces(text_list, line_number + 1, self.horizontial_spaces)
                text_list.insert(line_number + 1, '┌' + ('─' * (self.horizontial_spaces - 1)) +  '┘')
        line_number = len(text_list) - 1

    def remove_leading_spaces(self, text_list, line_number, spaces_to_remove):
        lines = text_list[line_number:]
        for i in range(len(lines)):
            line = text_list[line_number + i]
            line = line[spaces_to_remove:]
            text_list[line_number + i] = line

    def remove_tailing_whitespace(self, text_list):
        for i in range(len(text_list)):
            text_list[i] = text_list[i].rstrip()

    def normalize_text_list(self, text_list):
        longest_line = 0
        for line in text_list:
            if (len(line) > longest_line):
                longest_line = len(line)
        for i in range(len(text_list)):
            while (len(text_list[i]) < longest_line):
                text_list[i] = text_list[i] + ' '

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
        self.replace_char_in_line(text_list, y, x, '│') 
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
                            self.replace_char_in_line(text_list, line_number, char_number, '├')
                        elif (char == "─"):
                            self.replace_char_in_line(text_list, line_number, char_number, '┐')

    def replace_char_in_line(self, text_list, line_index, char_index, char):
        text_list[line_index] = text_list[line_index][:char_index] + char + text_list[line_index][char_index + 1:]

    def add_header_to_text_list(self, text_list):
        text_list.insert(0, '.')
        text_list.insert(1, '¦')
        text_list.insert(2, '¦')
