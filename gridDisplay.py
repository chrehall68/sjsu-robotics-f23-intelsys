from grid.grid import Grid
import pygame
from constants import *
from typing import List


class GridDisplay:
    """
    Uses [x, y]
    """

    CELL_SIZE = 30

    def __init__(self, grid: Grid) -> None:
        self.grid = grid

    def render(
        self, robot_pos: List[int], end_goal: List[int], path: List[int]
    ) -> pygame.surface.SurfaceType:
        height = (
            self.grid.height
            * GridDisplay.CELL_SIZE
            # + (self.grid.height - 1 if self.grid.width else 0)
            # * GridDisplay.CELL_BOUNDARY_SIZE
        )
        width = (
            self.grid.width
            * GridDisplay.CELL_SIZE
            # + (self.grid.width - 1 if self.grid.width else 0)
            # * GridDisplay.CELL_BOUNDARY_SIZE
        )

        # make the surface
        ret = pygame.Surface((width, height))
        ret.fill(GRAY)

        # draw the squares
        for row in range(self.grid.height):
            pygame.draw.line(
                ret,
                BLACK,
                (0, row * GridDisplay.CELL_SIZE),
                (width, row * GridDisplay.CELL_SIZE),
            )
        for col in range(self.grid.width):
            pygame.draw.line(
                ret,
                BLACK,
                (col * GridDisplay.CELL_SIZE, 0),
                (col * GridDisplay.CELL_SIZE, height),
            )

        # draw obstacles
        for row in range(self.grid.height):
            for col in range(self.grid.width):
                if self.grid.isObstacle([row, col]):
                    pygame.draw.circle(
                        ret,
                        BLACK,
                        (
                            col * GridDisplay.CELL_SIZE + GridDisplay.CELL_SIZE // 2,
                            row * GridDisplay.CELL_SIZE + GridDisplay.CELL_SIZE // 2,
                        ),
                        GridDisplay.CELL_SIZE // 2,
                    )
                elif [row, col] == robot_pos:
                    pygame.draw.rect(
                        ret,
                        BLUE,
                        pygame.Rect(
                            (
                                col * GridDisplay.CELL_SIZE,
                                row * GridDisplay.CELL_SIZE,
                                GridDisplay.CELL_SIZE,
                                GridDisplay.CELL_SIZE,
                            )
                        ),
                    )
                elif [row, col] == end_goal:
                    pygame.draw.rect(
                        ret,
                        RED,
                        pygame.Rect(
                            (
                                col * GridDisplay.CELL_SIZE,
                                row * GridDisplay.CELL_SIZE,
                                GridDisplay.CELL_SIZE,
                                GridDisplay.CELL_SIZE,
                            )
                        ),
                    )
                elif [row, col] in path:
                    pygame.draw.rect(
                        ret,
                        GREEN,
                        pygame.Rect(
                            (
                                col * GridDisplay.CELL_SIZE,
                                row * GridDisplay.CELL_SIZE,
                                GridDisplay.CELL_SIZE,
                                GridDisplay.CELL_SIZE,
                            )
                        ),
                    )

        return ret

    def draw(self, screen: pygame.surface.SurfaceType):
        screen.blit(self.render(), (0, 0))
