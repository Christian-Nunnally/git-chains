import os
import stat
import tempfile

from pygit2 import Repository
from ChainHierarchyPrinter import ChainHierarchyPrinter
from ChainRepository import ChainRepository
from GitRepositoryCopier import GitRepositoryCopier


class GitCommandPreviewer:
    def __init__(self, repo, skip_single_child_nodes, local_branches_to_include = []):
        self.repo = repo
        self.skip_single_child_nodes = skip_single_child_nodes
        self.local_branches_to_include = local_branches_to_include

    def preview_commands(self, commands):
        with tempfile.TemporaryDirectory() as temp_dir:
            self.create_skeleton_repository_from_tree(temp_dir, commands)
            temp_repository = Repository(temp_dir + "\\.git")
            self.run_git_chains_on_repository(temp_repository)
            self.make_writeable_recursive(temp_dir)

    def create_skeleton_repository_from_tree(self, temp_dir, commands):
        copier = GitRepositoryCopier(self.repo.tree, self.skip_single_child_nodes)
        copier.copy_repository(temp_dir, commands)

    def run_git_chains_on_repository(self, repo_path):
        preview_repo = ChainRepository(repo_path, self.local_branches_to_include)
        preview_printer = ChainHierarchyPrinter(preview_repo.tree, preview_repo.head_name)
        preview_printer.print()

    def make_writeable_recursive(self, path):
        for root, dirs, files in os.walk(path, topdown=False):
            self.make_dirs_writable(root, dirs)
            self.make_file_writable(root, files)

    def make_dirs_writable(self, root, dirs):
        for dir in [os.path.join(root, d) for d in dirs]:
            os.chmod(dir, self.get_perm(dir) | stat.S_IWRITE)

    def make_file_writable(self, root, files):
        for file in [os.path.join(root, f) for f in files]:
            os.chmod(file, self.get_perm(file) | stat.S_IWRITE)

    def get_perm(self, fname):
        return stat.S_IMODE(os.lstat(fname)[stat.ST_MODE])
