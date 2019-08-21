class Logger:
    enable_logging = True

    def __init__(self, owning_class):
        self.owning_class_name = type(owning_class).__name__

    def warning(self, message):
        self.log("Warning: " + message)

    def log(self, message):
        if (Logger.enable_logging):
            print("\r" + self.owning_class_name + " - " + message)

    def progress(self, progress):
        print("\r", end="")
        print(progress, end="")
