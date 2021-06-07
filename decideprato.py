
class DecidePrato:
    def __init__(self, data, left=None, right=None):
        self.data = data
        self.left = left
        self.right = right

    def inicio(self) -> bool:
        return self.left is None and self.right is None

    def __str__(self) -> str:
        return f"{self.data} -> (Left: {self.left} Rigth: {self.right})"