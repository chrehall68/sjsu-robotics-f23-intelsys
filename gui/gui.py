# project imports
from grid.grid import Grid
from grid.a_star import a_star
from gui.gridDisplay import GridDisplay
from gui.constants import *

# outside imports
import random
from typing import List, Callable
import pygame

pygame.init()


class Scene:
    """
    Scene manager that takes care of moving the robot
    and knowing where the end goal is.

    Public interface is provided in [x, y] format since
    this is meant to interact with the GUI, which also uses that format.
    """

    def __init__(self, width: int, height: int, obstacle_rate: float = 0.2) -> None:
        self.grid = Grid(height, width)

        # add end goal
        used_options = []
        self.end_goal = self.getUniqueCoord(used_options)
        used_options.append(self.end_goal)

        # add start
        self.robot_pos = self.getUniqueCoord(used_options)
        used_options.append(self.robot_pos)

        # add obstacles
        for _ in range(int(height * width * obstacle_rate)):
            choice = self.getUniqueCoord(used_options)
            used_options.append(choice)
            self.grid.addObstacle(choice)

        self.grid_display = GridDisplay(self.grid)

        # for path
        self.path = []

    def getUniqueCoord(self, used: List[List[int]]):
        num_options = self.grid.width * self.grid.height - 1
        choice = random.randint(0, num_options)
        while [choice // self.grid.width, choice % self.grid.width] in used:
            choice = random.randint(0, num_options)

        return [choice // self.grid.width, choice % self.grid.width]

    def render(self) -> pygame.SurfaceType:
        return self.grid_display.render(self.robot_pos, self.end_goal, self.path)

    def draw(self, screen: pygame.Surface) -> None:
        screen.blit(self.render(), (0, 0))

    def move(self, dir: List[int]):
        next_pos = [self.robot_pos[0] + dir[0], self.robot_pos[1] + dir[1]]
        if (
            not self.grid.isObstacle(next_pos)
            and (next_pos[0] >= 0 and next_pos[0] < self.grid.height)
            and (next_pos[1] >= 0 and next_pos[1] < self.grid.width)
        ):
            self.robot_pos = next_pos

    def moveUp(self):
        self.move([-1, 0])

    def moveDown(self):
        self.move([1, 0])

    def moveLeft(self):
        self.move([0, -1])

    def moveRight(self):
        self.move([0, 1])

    def getInstructions(self) -> List[Callable]:
        """
        Returns functions to call (moveUp, moveDown, etc) to get to the
        end goal, if possible, else empty list, in reverse order
        (so that getINstructions.pop() returns the first function to call)
        """
        self.path = a_star(self.grid.grid, self.robot_pos, self.end_goal)
        instructions = []
        for i in range(1, len(self.path)):
            # since path is in [row, col] format, make sure to convert
            if self.path[i][1] > self.path[i - 1][1]:
                instructions.append(self.moveRight)
            if self.path[i][1] < self.path[i - 1][1]:
                instructions.append(self.moveLeft)
            if self.path[i][0] > self.path[i - 1][0]:
                instructions.append(self.moveDown)
            if self.path[i][0] < self.path[i - 1][0]:
                instructions.append(self.moveUp)
        return list(reversed(instructions))

    def toggleObstacle(self, cell: List[int]):
        """
        Cell should be [x, y]
        """
        # convert to [row, col]
        cell = [cell[1], cell[0]]
        if self.grid.isObstacle(cell):
            self.grid.removeObstacle(cell)
        elif cell != self.robot_pos and cell != self.end_goal:
            self.grid.addObstacle(cell)

    def setEndGoal(self, cell: List[int]):
        """
        Cell should be [x, y]
        """
        # convert to [row, col]
        cell = [cell[1], cell[0]]
        if not self.grid.isObstacle(cell):
            self.end_goal = cell

    def clearPath(self):
        self.path = []


class GUI:
    """
    GUI manager that takes care of drawing everything and passing events to
    the scene
    """

    GUI_EXTRA_SPACE = 300  # extra width for instructions; in px
    FONT_SIZE = 20  # font size, in px
    MIN_HEIGHT = 10  # min height in blocks; otherwise display gets weird

    def __init__(self, grid_size: List[int]) -> None:
        """
        initial_grid_size should be width, height
        """
        self.scene = Scene(grid_size[0], max(grid_size[1], GUI.MIN_HEIGHT))

        # screen sizes
        self.scene_size = self.scene.render().get_size()
        self.screen_size = (
            self.scene_size[0] + GUI.GUI_EXTRA_SPACE,
            self.scene_size[1],
        )
        self.screen = pygame.display.set_mode(self.screen_size)
        pygame.display.set_caption("Intelsys sim")

        # font
        self.font = pygame.font.SysFont("arial", size=GUI.FONT_SIZE)

        # movement and other gui stuff
        self.on_autopilot = False
        self.setting_end_goal = False
        self.setting_obstacle = False

        # useful for resetting
        self.scene_height = grid_size[0]
        self.scene_width = grid_size[1]

    def run(self):
        instructions = []
        while 1:
            self.draw()
            self.scene.draw(self.screen)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return

                # key events
                if event.type == pygame.KEYDOWN:
                    if not self.on_autopilot:
                        if event.key == pygame.K_s:
                            self.scene.moveDown()
                            self.scene.clearPath()
                        if event.key == pygame.K_a:
                            self.scene.moveLeft()
                            self.scene.clearPath()
                        if event.key == pygame.K_d:
                            self.scene.moveRight()
                            self.scene.clearPath()
                        if event.key == pygame.K_w:
                            self.scene.moveUp()
                            self.scene.clearPath()
                        if event.key == pygame.K_r:
                            self.reset()
                            self.scene.clearPath()
                        if event.key == pygame.K_p:
                            self.on_autopilot = True
                            instructions = self.scene.getInstructions()

                # mouse click events
                if event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_pos = pygame.mouse.get_pos()
                    if (
                        mouse_pos[0] < self.scene_size[0]
                        and mouse_pos[1] < self.scene_size[1]
                    ):
                        coord = [
                            mouse_pos[0] // GridDisplay.CELL_SIZE,
                            mouse_pos[1] // GridDisplay.CELL_SIZE,
                        ]
                        if event.button == 1:  # left click
                            self.scene.toggleObstacle(coord)
                        else:  # right click
                            self.scene.setEndGoal(coord)

            if self.on_autopilot:
                if len(instructions) == 0:
                    self.on_autopilot = False
                else:
                    instructions.pop()()

            pygame.display.update()
            pygame.time.wait(50)

    def reset(self):
        self.scene = Scene(self.scene_height, self.scene_width)

    def render(self):
        ret = pygame.Surface(self.screen_size)
        ret.fill(WHITE)

        texts = [
            "Robot simulator.",
            " - You are blue",
            " - Goal is red",
            " - Obstacles are black",
            "",
            "Basic instructions:",
            " - Use wasd to move.",
            " - Use p to autopilot.",
            " - Use r to reset.",
            "",
            "Advanced:",
            " - Left click to toggle obstacles.",
            " - Right click to set Goal",
        ]
        rendered_texts = [self.font.render(text, True, BLACK) for text in texts]

        for i in range(len(rendered_texts)):
            ret.blit(rendered_texts[i], (self.scene_size[0], i * GUI.FONT_SIZE))

        return ret

    def draw(self):
        self.screen.blit(self.render(), (0, 0))
