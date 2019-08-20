import os

from colorama import Fore

from NodeColor import NodeColor


class ChainHierarchyPrinter:
    CommitIndicator = '●'
    HiddenParentIndicator = '◌'

    def __init__(self, chain_repository):
        self.vertical_white_space_between_chains_off_master = False
        self.show_nodes_with_one_child = False
        self.show_reference_nodes = True
        self.show_full_branch_names = False
        self.show_nodes_with_names = True
        self.show_more_excluded_parent_dots = True
        self.max_excluded_parents_represented = 6
        self.commit_style = ChainHierarchyPrinter.CommitIndicator
        self.parent_style = ChainHierarchyPrinter.HiddenParentIndicator

        self.tree = chain_repository.tree
        self.repository = chain_repository.repository
        self.text_list = []

    def print(self):
        self.text_list = [] 
        self.build_text_list()
        self.decorate_text_list()
        for line in self.text_list:
            print(line)
    
    def build_text_list(self):
        if self.tree.root:
            self.build_text_list_recursively(self.tree.root, 0, False, [])
        else:
            self.text_list = ["No root node."]

    def build_text_list_recursively(self, node, left_spaces, excluded_parent_count, parent_branch_names):
        parent_branch_names = list(parent_branch_names)
        excluded_parent_dots = self.get_excluded_parent_dots(excluded_parent_count)
        
        for merged_branch_name in node.merged_branch_names:
            if (merged_branch_name in node.pretty_names or merged_branch_name in parent_branch_names):
                continue
            parent_branch_names.append(merged_branch_name)
            colored_node_name = Fore.LIGHTBLACK_EX + self.get_formatted_name(merged_branch_name)
            commit_dot = Fore.LIGHTBLACK_EX + self.commit_style + Fore.RESET
            line = "%s└%s─┐ %s" % (' ' * left_spaces, commit_dot, colored_node_name)
            self.text_list.append(line)
            left_spaces += 3

        for node_name in node.pretty_names:
            parent_branch_names.append(node_name)
        line = self.build_basic_string_node_representation(node, left_spaces, excluded_parent_dots)
        self.text_list.append(line)

        for child in node.children:
            excluded_parent_count = 0
            while self.should_skip_over_node(child):
                child = child.children[0]
                excluded_parent_count += 1
            self.build_text_list_recursively(child, left_spaces + 3 + len(excluded_parent_dots), excluded_parent_count, parent_branch_names)
        self.add_vertical_whitespace_if_needed()

    def build_basic_string_node_representation(self, node, left_spaces, excluded_parent_dots):
        current_branch_name = self.repository.head.name.split('/')[-1]
        color = NodeColor(node, current_branch_name)
        colored_node_name = color.name_color + self.get_formatted_node_name(node)
        commit_dot = color.status_color + self.commit_style + color.reset
        formatted_excluded_parents_dots = color.omitted_parent + excluded_parent_dots + color.reset
        has_children_symbol = self.get_has_children_symbol(node)
        line = "%s└%s%s%s %s" % (' ' * left_spaces, formatted_excluded_parents_dots, commit_dot, has_children_symbol, colored_node_name)
        return line

    def get_has_children_symbol(self, node):
        if len(node.children) > 0:
            return "─┐"
        return ""

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
        if ("master" in node.pretty_names): 
            return False
        if self.show_nodes_with_names and node.has_name:
            return False
        if not self.show_nodes_with_one_child and (len(node.children) == 1):
            return True
        return False 

    def get_formatted_node_name(self, node):
        result = ""
        for node_name in node.pretty_names:
            formatted_name = self.get_formatted_name(node_name)
            result += formatted_name + ", "
        return result[:-2]

    def get_formatted_name(self, name):
        if (not self.show_full_branch_names):
            return os.path.basename(name)
        return name

    def add_vertical_whitespace_if_needed(self):
        if (self.vertical_white_space_between_chains_off_master):
            if (len(self.text_list) > 0 and not len(self.text_list[-1]) == 0):
                self.text_list.append('')

    def decorate_text_list(self):
        self.add_header_to_text_list()
        self.extend_pipes_up_all_lines()
        self.fix_joints()

    def extend_pipes_up_all_lines(self):
        for line_number in range(len(self.text_list)):
            self.extend_pipes_up_line(line_number)

    def extend_pipes_up_line(self, line_number):
        line = self.text_list[line_number]
        for char_number in range(len(line)):
            if (line[char_number] == '└'):
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
            self.fix_pipe_characters_that_are_disconnected_from_below(line_number)
    
    def fix_pipe_characters_that_are_disconnected_from_below(self, line_number):
        line = self.text_list[line_number]
        next_line = self.text_list[line_number + 1]
        for char_number in range(len(line)):
            self.fix_pipe_character_if_disconnected_from_below(line, next_line, line_number, char_number)

    def fix_pipe_character_if_disconnected_from_below(self, line, next_line, line_number, char_number):
        if len(next_line) > char_number:
            char = line[char_number]
            next_char = next_line[char_number]
            self.apply_replace_rules_for_fixing_pipe_across_vertically_arranged_characters(next_char, char, line_number, char_number)

    def apply_replace_rules_for_fixing_pipe_across_vertically_arranged_characters(self, char_below, char, line_number, char_number):
        if not char_below == '│' and not char_below == '└':
            return
        if char == '└':
            self.replace_char_in_line(line_number, char_number, '├')
        elif char == "─":
            self.replace_char_in_line(line_number, char_number, '┐')

    def replace_char_in_line(self, line_index, char_index, char):
        if len(self.text_list[line_index]) < char_index:
            self.text_list[line_index] += " " * (char_index - len(self.text_list[line_index])) 
        replacement = self.text_list[line_index][:char_index] + char + self.text_list[line_index][char_index + 1:]
        self.text_list[line_index] = replacement

    def add_header_to_text_list(self):
        self.text_list.insert(0, '.')
        self.text_list.insert(1, '¦')
        self.text_list.insert(2, '¦')
