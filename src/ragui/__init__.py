class RagUI:
    def __init__(self):
        self.pipelines = {}

    def pipeline(self, name):
        def decorator(func):
            self.pipelines[func.__name__] = func
            return func

        return decorator
