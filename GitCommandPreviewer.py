
from pygit2 import *
from CommitTree import CommitTree
from NodeColor import NodeColor
from CommitTreeToGitCommandDecoder import CommitTreeToGitCommandDecoder
import tempfile

class GitCommandPreviewer:

    def __init__(self, repo):
        self.repo = repo

    def preview_command(self, command):
        preview_repo_directory = tempfile.gettempdir()
        preview_repo = repo = init_repository(preview_repo_directory)
        decoder = CommitTreeToGitCommandDecoder(self.repo.tree)
        decoder.recursivly_generate_git_commands_entry()


