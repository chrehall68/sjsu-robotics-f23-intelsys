# File by Eliot Hall
# 9/16/23
# solution for the maze thing, basically is just going to be
# dijstra's shortest path algorithm

from heapq import heappop, heappush
from typing import List


class WeightedCoordinate:
    """
    Custom coordinate class useful for sorted data structures
    """

    def __init__(self, coord: List[int], distance: int) -> None:
        self.distance = distance
        self.coord = coord

    def __lt__(self, __o) -> bool:
        return self.distance < __o.distance

    def __le__(self, __o) -> bool:
        return self.distance <= __o.distance

    def __gt__(self, __o) -> bool:
        return not self <= __o

    def __ge__(self, __o) -> bool:
        return not self < __o

    def __eq__(self, __o) -> bool:
        return self.coord[0] == __o.coord[0] and self.coord[1] == __o.coord[1]

    def __hash__(self) -> int:
        # needed for set insertion
        return hash(tuple(self.coord))


def djikstra(
    maze: List[List[int]], start: List[int], end: List[int]
) -> List[List[int]]:
    """
    assume 0s mean movable and 1s mean non-movable

    Returns list of coordinates to go through to reach
    end in the shortest moves possible while avoiding obstacles
    or an empty list if impossible
    """
    weights = [[float("inf") for _ in range(len(maze[0]))] for _ in range(len(maze))]

    def get_neighbors(coord: List[int]):
        """
        Find all valid neighboring coordinates
        A coordinate is valid if it is not 1 and if it is within the maze
        """
        ret = []
        for x in [coord[0] - 1, coord[0] + 1]:
            if x >= 0 and x < len(maze) and maze[x][coord[1]] != 1:
                ret.append([x, coord[1]])

        for y in [coord[1] - 1, coord[1] + 1]:
            if y >= 0 and y < len(maze[0]) and maze[coord[0]][y] != 1:
                ret.append([coord[0], y])
        return ret

    def manhattan_distance(coord: List[int]):
        # not the pythagorean distance; assumes you can only go in cardinal directions
        return abs(coord[0] - end[0]) + abs(coord[1] - end[1])

    def reconstruct_path():
        # go backwards and find out what we should actually take to get to the end
        ret = [end]
        while ret[-1] != start:
            neighbors = get_neighbors(ret[-1])
            minPath = min(
                map(lambda n: (weights[n[0]][n[1]], n), neighbors),
                key=lambda val: val[0],
            )
            ret.append(minPath[1])
        return ret

    # weights is how many steps it took to get there
    weights[start[0]][start[1]] = 0

    # initialize heap and visited set
    connections = [WeightedCoordinate(start, manhattan_distance(start))]
    visited = set()

    # explore until we reached it or explored all possibilities
    while len(connections) != 0:
        con = heappop(connections)
        con = con.coord
        neighbors = get_neighbors(con)

        for neighbor in neighbors:
            # update the distance
            weights[neighbor[0]][neighbor[1]] = min(
                weights[con[0]][con[1]] + 1, weights[neighbor[0]][neighbor[1]]
            )

            # add it to the heap (and visited set) if we haven't seen it
            temp = WeightedCoordinate(neighbor, manhattan_distance(neighbor))
            if temp not in visited:
                heappush(connections, temp)
                visited.add(temp)

            # if we made it to the end, construct the path that we took
            if neighbor == end:
                return list(reversed(reconstruct_path()))

    # was impossible -_-
    return


if __name__ == "__main__":
    print(
        djikstra(
            [[0, 0, 1, 1], [0, 1, 0, 0], [0, 0, 0, 0], [0, 1, 0, 0], [0, 0, 0, 0]],
            start=[0, 0],
            end=[4, 3],
        )
    )
