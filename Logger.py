class Logger:
    enable_logging = False

    def __init__(self, owning_class):
        self.owning_class_name = type(owning_class).__name__

    def warning(self, message):
        self.log("Warning: " + message)

    def log(self, message):
        if (Logger.enable_logging):
            print(self.owning_class_name + " - " + message)
