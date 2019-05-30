class LogItem:
    def __init__(self, commit, is_reference, fake_parent_id = None):
        self.fake_parent_id = fake_parent_id
        self.commit = commit
        self.is_reference = is_reference