from typing import List, Optional


class Grid:
    """
    Protected 2d array to manage obstacles.
    Provides quick accessing of obstacles and the underlying grid
    Uses [row, col] in public interface
    """

    def __init__(
        self, height: int, width: int, obstacles: Optional[List[List[int]]] = None
    ) -> None:
        self.height = height
        self.width = width
        self.obstacles = []
        if obstacles:
            self.obstacles = obstacles

    def __str__(self):
        ret = "\n".join(map(lambda row: str(row), self.grid))
        return ret

    def __repr__(self) -> str:
        return str(self)

    def isObstacle(self, cell: List[int]) -> bool:
        """
        Cell should be [row, col]
        """
        return cell in self.obstacles

    def addObstacle(self, cell: List[int]):
        """
        Cell should be [row, col]
        """
        if cell not in self.obstacles:
            self.obstacles.append(cell)

    def removeObstacle(self, cell: List[int]):
        """
        Cell should be [row, col]
        """
        if cell in self.obstacles:
            self.obstacles.remove(cell)

    @property
    def grid(self):
        return [
            [0 if [row, col] not in self.obstacles else 1 for col in range(self.width)]
            for row in range(self.height)
        ]
