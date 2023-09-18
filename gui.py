from typing import Optional, List, Callable
from grid.grid import Grid
from grid.dijkstra import dijkstra
from gridDisplay import GridDisplay
import pygame
from constants import *
import random

pygame.init()


class Scene:
    """
    Scene manager that takes care of moving the robot
    and knowing where the end goal is.
    """

    def __init__(self, height: int, width: int, obstacle_rate: float = 0.1) -> None:
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

    def getUniqueCoord(self, used: List[List[int]]):
        num_options = self.grid.width * self.grid.height - 1
        choice = random.randint(0, num_options)
        while [choice // self.grid.width, choice % self.grid.width] in used:
            choice = random.randint(0, num_options)

        return [choice // self.grid.width, choice % self.grid.width]

    def render(self) -> pygame.SurfaceType:
        return self.grid_display.render(self.robot_pos, self.end_goal)

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

    def moveLeft(self):
        self.move([-1, 0])

    def moveRight(self):
        self.move([1, 0])

    def moveUp(self):
        self.move([0, -1])

    def moveDown(self):
        self.move([0, 1])

    def getInstructions(self) -> List[Callable]:
        """
        Returns functions to call (moveUp, moveDown, etc) to get to the
        end goal, if possible, else empty list, in reverse order
        (so that getINstructions.pop() returns the first function to call)
        """
        ret = dijkstra(self.grid.grid, self.robot_pos, self.end_goal)
        instructions = []
        for i in range(1, len(ret)):
            if ret[i][1] > ret[i - 1][1]:
                instructions.append(self.moveDown)
            if ret[i][1] < ret[i - 1][1]:
                instructions.append(self.moveUp)
            if ret[i][0] > ret[i - 1][0]:
                instructions.append(self.moveRight)
            if ret[i][0] < ret[i - 1][0]:
                instructions.append(self.moveLeft)
        return list(reversed(instructions))


class GUI:
    """
    GUI manager that takes care of drawing everything and passing events to
    the scene
    """

    def __init__(self, initial_grid_size: Optional[List[int]] = [10, 10]) -> None:
        self.scene = Scene(*initial_grid_size)
        self.screen = pygame.display.set_mode((500, 500), flags=pygame.RESIZABLE)
        self.on_autopilot = False

        # useful for resetting
        self.scene_height = initial_grid_size[0]
        self.scene_width = initial_grid_size[1]

    def run(self):
        instructions = []
        while 1:
            self.screen.fill(WHITE)
            self.scene.draw(self.screen)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return

                if event.type == pygame.KEYDOWN:
                    if not self.on_autopilot:
                        if event.key == pygame.K_s:
                            self.scene.moveDown()
                        if event.key == pygame.K_a:
                            self.scene.moveLeft()
                        if event.key == pygame.K_d:
                            self.scene.moveRight()
                        if event.key == pygame.K_w:
                            self.scene.moveUp()
                        if event.key == pygame.K_r:
                            self.reset()
                    if event.key == pygame.K_p:
                        self.on_autopilot = True
                        instructions = self.scene.getInstructions()

            if self.on_autopilot:
                if len(instructions) == 0:
                    self.on_autopilot = False
                else:
                    instructions.pop()()

            pygame.display.update()
            pygame.time.wait(50)

    def reset(self):
        self.scene = Scene(self.scene_height, self.scene_width)
