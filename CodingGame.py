import sys
import math

# Auto-generated code below aims at helping you parse
# the standard input according to the problem statement.


class Cell:

    def __init__(self, cellRessources, my_ants, enemy_ants, neighbours_id_list, cell_id, _type) -> None:
        self.resources = cellRessources
        self.my_ants = my_ants
        self.enemy_ants = enemy_ants
        self.neighbours_id_list = neighbours_id_list
        self.neighbours_list = None
        self.id = cell_id
        self.type = _type

    def update(self, ressources, my_ants, enemy_ants):
        self.resources = ressources
        self.my_ants = my_ants
        self.enemy_ants = enemy_ants

    def update_neighbours(self, neighbour_list):
        self.neighbours_list = neighbour_list

class GameState:
    def __init__(self, cells, number_of_bases, my_base_index, opp_base_index):
        self.cells = cells
        self.number_of_cells = len(cells)
        self.number_of_bases = number_of_bases
        self.my_base_index = my_base_index
        self.opp_base_index = opp_base_index
        self.update_all_lists()
        self.distances = self.dijkstra(self.cells)

    def update_all_lists(self):
        for i in range(self.number_of_cells):
            self.update_NeighbourList(self.cells[i].neighbours_id_list, i)

    def update_NeighbourList(self, neighbours_id_list, index):
        neighbours_list = [self.cells[i] for i in neighbours_id_list if i >= 0]
        self.cells[index].update_neighbours(neighbours_list)

    def minDistance(self, distances, unvisited):
        current_min = 1e7
        min_index = 0
        for v in range(self.number_of_cells):
            if distances[v] < current_min and unvisited[v] == False:
                current_min = distances[v]
                min_index = v
        return min_index

    def dijkstra(self, cells):

        distances = [1e7] * self.number_of_cells
        distances[self.my_base_index] = 0
        unvisited = [False] * self.number_of_cells

        for cout in range(self.number_of_cells):

            u = self.minDistance(distances, unvisited)

            unvisited[u] = True

            for cell in cells[u].neighbours_list:
                if not unvisited[cell.id] and distances[u] > distances[cell.id] + 1:
                    distances[u] = distances[cell.id] + 1

        return distances


def init():
    cells = {}
    number_of_cells = int(input())

    for i in range(number_of_cells):
        # _type: 0 for empty, 1 for eggs, 2 for crystal
        # initial_resources: the initial amount of eggs/crystals on this cell
        # neigh_0: the index of the neighbouring cell for each direction
        _type, initial_resources, neigh_0, neigh_1, neigh_2, neigh_3, neigh_4, neigh_5 = [int(j) for j in
                                                                                          input().split()]

        neighbours_id_list = [neigh_0, neigh_1, neigh_2, neigh_3, neigh_4, neigh_5]

        cells[i] = Cell(initial_resources, 0, 0, neighbours_id_list, i, _type)

    number_of_bases = int(input())

    for i in input().split():
        my_base_index = int(i)
    for i in input().split():
        opp_base_index = int(i)

    game = GameState(cells, number_of_bases, my_base_index, opp_base_index)
    return game


game = init()
# game loop
while True:

    for i in range(game.number_of_cells):
        # resources: the current amount of eggs/crystals on this cell
        # my_ants: the amount of your ants on this cell
        # opp_ants: the amount of opponent ants on this cell
        resources, my_ants, opp_ants = [int(j) for j in input().split()]
        game.cells[i].update(resources, my_ants, opp_ants)

    # Write an action using print
    # To debug: print("Debug messages...", file=sys.stderr, flush=True)

    # WAIT | LINE <sourceIdx> <targetIdx> <strength> | BEACON <cellIdx> <strength> | MESSAGE <text>

    listDist = sorted(game.cells.values(),
                      key=lambda x : (x.resources, -game.distances[x.id]), reverse=True)

    cell_index = listDist[0].id

    print(f"LINE {game.cells[game.my_base_index].id} {game.cells[cell_index].id} 1;" +
          f"LINE {game.cells[game.my_base_index].id} {game.cells[listDist[1].id].id} 1")

