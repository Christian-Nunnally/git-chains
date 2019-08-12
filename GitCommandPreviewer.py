from ChainRepository import ChainRepository
from ChainHierarchyPrinter import ChainHierarchyPrinter
from GitRepositoryCopier import GitRepositoryCopier
import tempfile
import os
import stat

class GitCommandPreviewer:

    def __init__(self, repo, local_branches_to_include = []):
        self.repo = repo
        self.local_branches_to_include = local_branches_to_include

    def preview_commands(self, commands, skip_single_child_nodes):
        with tempfile.TemporaryDirectory() as temp_dir:
            copier = GitRepositoryCopier(self.repo.tree)
            copier.copy_repository(temp_dir, commands, skip_single_child_nodes)

            preview_repo = ChainRepository(temp_dir + "\\.git", self.local_branches_to_include)
            preview_printer = ChainHierarchyPrinter(preview_repo)
            preview_printer.print()
            preview_repo.repo.free()
            self.make_writeable_recursive(temp_dir)

    def make_writeable_recursive(self, path):
        for root, dirs, files in os.walk(path, topdown=False):
            for dir in [os.path.join(root, d) for d in dirs]:
                os.chmod(dir, self.get_perm(dir) | stat.S_IWRITE)
            for file in [os.path.join(root, f) for f in files]:
                os.chmod(file, self.get_perm(file) | stat.S_IWRITE)

    def get_perm(self, fname):
        return stat.S_IMODE(os.lstat(fname)[stat.ST_MODE])


