from CommitTree import CommitTree
from NodeColor import NodeColor
import os

class ChainHierarchyPrinter:
    CommitIndicator = '●'
    HiddenParentIndicator = '◌'

    def __init__(self, chain_repo):
        self.vertical_white_space_between_chains_off_master = True
        self.show_nodes_with_one_child = True
        self.show_reference_nodes = False
        self.show_full_branch_names = False
        self.show_nodes_with_names = True
        self.show_more_excluded_parent_dots = True
        self.align_left = True
        self.max_excluded_parents_represented = 8
        self.commit_style = ChainHierarchyPrinter.CommitIndicator
        self.parent_style = ChainHierarchyPrinter.HiddenParentIndicator

        self.tree = chain_repo.tree
        self.master_log = chain_repo.master_log
        self.text_list = []

    def print(self):
        self.text_list = []
        self.build_text_list()
        self.decorate_text_list()
        for line in self.text_list:
            print(line)

    def build_text_list(self):
        start_node = self.tree.root
        self.build_text_list_recursively(start_node, 0, False)

    def build_text_list_recursively(self, node, left_spaces, excluded_parent_count):
        if self.should_skip_over_node(node):
            self.build_text_list_recursively(node.children[0], left_spaces, excluded_parent_count + 1)
            return
            
        sorted_children = self.sorted_children(node.children)
        color = NodeColor(node)
        node_name = self.get_formatted_node_name(node)
        commit_dot = color.status_color + self.commit_style + color.reset
        excluded_parent_dots = self.get_excluded_parent_dots(excluded_parent_count)
        formatted_excluded_parents_dots = color.omitted_parent + excluded_parent_dots + color.reset
        
        line = color.name_color + node_name
        line = ' ' + line
        if (len(sorted_children) > 0):
            line = '─┐' + line
        line = commit_dot + line
        line = formatted_excluded_parents_dots + line
        line = '└' + line
        line = ' ' * left_spaces + line
        self.text_list.append(line)

        for child in sorted_children:
            self.build_text_list_recursively(child, left_spaces + 3 + len(excluded_parent_dots), 0)
        self.add_vertical_whitespace_if_needed()

    def get_excluded_parent_dots(self, excluded_parent_count):
        if (excluded_parent_count < 0):
            return ""
        if (not self.show_more_excluded_parent_dots):
            return self.parent_style
        if (excluded_parent_count < self.max_excluded_parents_represented):
            return self.parent_style * excluded_parent_count
        else:
            return self.parent_style * 3 + "···" + self.parent_style * 2

    def should_skip_over_node(self, node):
        if self.show_nodes_with_names and node.has_name:
            return False
        if self.show_reference_nodes and node.is_reference_node:
            return False
        if self.show_nodes_with_one_child and (len(node.children) == 1):
            return True
        return False

    def get_formatted_node_name(self, node):
        if (not self.show_full_branch_names):
            return os.path.basename(node.pretty_name)
        return node.pretty_name

    def add_vertical_whitespace_if_needed(self):
        if (self.vertical_white_space_between_chains_off_master):
            if (len(self.text_list) > 0 and not len(self.text_list[-1]) == 0):
                self.text_list.append('')

    def sorted_children(self, children):
        sortedList = sorted(children, key=lambda child: child.commit.commit_time)
        sortedList.reverse()
        return sortedList

    def get_master_branch_commit(self):
        return self.master_log[len(self.master_log - 1)]

    def decorate_text_list(self):
        self.add_header_to_text_list()
        self.extend_pipes_up()
        self.fix_joints()
        if (self.align_left):
           self.inline_left_commits()

    def inline_left_commits(self):
        line_number = 0
        while(line_number < len(self.text_list) - 2):
            line_number += 1
            for i in range(len(self.text_list[line_number]) - 1):
                char_index = i + 1
                if (self.text_list[line_number][char_index] == '└'):
                    self.remove_leading_spaces(line_number)
                    space_count = 0
                    current_char_index = 0
                    current_char = self.text_list[line_number - 1][current_char_index]
                    while(not (current_char == '┐' or current_char == '|')):
                        current_char = self.text_list[line_number - 1][current_char_index]
                        if (current_char == self.parent_style or current_char == self.commit_style or current_char == '·' or current_char == '·' or current_char == '─' or current_char == '┐' or current_char == '└'):
                            space_count += 1
                        current_char_index += 1
                        if (len(self.text_list[line_number - 1]) <= current_char_index):
                            break
                    self.text_list.insert(line_number, '┌' + ('─' * (space_count - 2)) +  '┘')
                    line_number += 1
                    break
                elif not self.text_list[line_number][char_index] == ' ':
                    break

    def remove_leading_spaces(self, line_number):
        lines = self.text_list[line_number:]
        removed_spaces = 0
        for i in range(len(lines)):
            line = self.text_list[line_number + i]
            count = 1
            while(len(line) > 0 and line[0] == ' ' and ((i == 0) or removed_spaces >= count)):
                count += 1
                if (i == 0):
                    removed_spaces += 1
                line = line[1:]
            self.text_list[line_number + i] = line

    def extend_pipes_up(self):
        for line_number in range(len(self.text_list)):
            line = self.text_list[line_number]
            for char_number in range(len(line)):
                char = line[char_number]
                if (char == '└'):
                    self.extend_pipes_up_recursive(char_number, line_number - 1)

    def extend_pipes_up_recursive(self, x, y):
        if (y <= 0):
            return
        if len(self.text_list) > y and len(self.text_list[y]) > x:
            if (self.text_list[y][x] != ' '):
                return
        self.replace_char_in_line(y, x, '│') 
        self.extend_pipes_up_recursive(x, y - 1)
    
    def fix_joints(self):
        for line_number in range(len(self.text_list) - 1):
            line = self.text_list[line_number]
            for char_number in range(len(line)):
                char = line[char_number]
                next_line = self.text_list[line_number + 1]
                if (len(next_line) > char_number):
                    next_char = next_line[char_number]
                    if (next_char == '│' or next_char == '└'):
                        if (char == '└'):
                            self.replace_char_in_line(line_number, char_number, '├')
                        elif (char == "─"):
                            self.replace_char_in_line(line_number, char_number, '┐')

    def replace_char_in_line(self, line_index, char_index, char):
        if (len(self.text_list[line_index]) < char_index):
            self.text_list[line_index] += " " * (char_index - len(self.text_list[line_index])) 
        replacement = self.text_list[line_index][:char_index] + char + self.text_list[line_index][char_index + 1:]
        self.text_list[line_index] = replacement

    def add_header_to_text_list(self):
        self.text_list.insert(0, '.')
        self.text_list.insert(1, '¦')
        self.text_list.insert(2, '¦')
