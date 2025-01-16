from pathlib import Path


class BetterFile:
    def __init__(self, filename: str):
        self.path = Path(filename)
