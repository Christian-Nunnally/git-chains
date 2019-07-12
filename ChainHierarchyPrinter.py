from CommitTree import CommitTree
from NodeColor import NodeColor
import os

class ChainHierarchyPrinter:
    CommitIndicator = '●'
    HiddenParentIndicator = '◌'

    def __init__(self, chain_repo):
        self.vertical_white_space_between_chains_off_master = True
        self.show_nodes_with_one_child = False
        self.show_reference_nodes = True
        self.show_full_branch_names = False
        self.show_nodes_with_names = True
        self.show_more_excluded_parent_dots = True
        self.max_excluded_parents_represented = 6
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
        if (excluded_parent_count <= 0):
            return ""
        if (not self.show_more_excluded_parent_dots):
            return self.parent_style
        if (excluded_parent_count < self.max_excluded_parents_represented):
            return self.parent_style * excluded_parent_count
        else:
            return self.parent_style * 1 + "·"+ str(excluded_parent_count - 2) +"·" + self.parent_style * 1

    def should_skip_over_node(self, node):
        if (node.name == "master"):
            return False
        if self.show_nodes_with_names and node.has_name:
            return False
        if self.show_reference_nodes and node.is_reference_node:
            return False
        if not self.show_nodes_with_one_child and (len(node.children) == 1):
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
        sorted_children = []
        for child in children:
            if (child.is_part_of_master):
                sorted_children.append(child)
        for child in children:
            if (not child.is_part_of_master):
                sorted_children.append(child)
        sorted_children.reverse()
        return sorted_children

    def get_master_branch_commit(self):
        return self.master_log[len(self.master_log - 1)]

    def decorate_text_list(self):
        self.add_header_to_text_list()
        self.extend_pipes_up()
        self.fix_joints()

    def extend_pipes_up(self):
        for line_number in range(len(self.text_list)):
            line = self.text_list[line_number]
            for char_number in range(len(line)):
                char = line[char_number]
                if (char == '└'):
                    self.extend_pipes_up_recursive(char_number, line_number - 1)

    def extend_pipes_up_recursive(self, x, y):
        if y <= 0:
            return
        if self.is_text_list_filled(x, y):
            return
        self.replace_char_in_line(y, x, '│') 
        self.extend_pipes_up_recursive(x, y - 1)
    
    def is_text_list_filled(self, x, y):
        return len(self.text_list) > y and len(self.text_list[y]) > x and self.text_list[y][x] != ' '

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
