import copy

from Player import Player
from Position import Position
from Blob import Blob


class Game_Controller:

    def __init__(self, game_board):
        self.game_board = game_board

    # get game board
    def get_game_board(self):
        return self.game_board

    # mapping between input and output
    def mapping(self, choice):
        temp_choice = choice - 1
        i = int(temp_choice / self.game_board.get_board_dimenstion()[0])
        j = int(temp_choice % self.game_board.get_board_dimenstion()[1])
        return [i, j]

    # blob can copy to adjacent cell
    def can_copy(self, blob, cell):
        if (cell.get_x() >= self.game_board.get_board_dimenstion()[0]) or (cell.get_x() < 0):
            return False
        if (cell.get_y() >= self.game_board.get_board_dimenstion()[1]) or (cell.get_y() < 0):
            return False
        if self.game_board.get_board()[cell.get_x()][cell.get_y()] != '-':
            return False
        return ((abs(cell.get_x() - blob.get_position().get_x()) == 1) and (
                abs(cell.get_y() - blob.get_position().get_y()) <= 1)) or (
                       (abs(cell.get_x() - blob.get_position().get_x()) <= 1) and (
                       abs(cell.get_y() - blob.get_position().get_y()) == 1))

    # blob can move to 2 cell away
    def can_move(self, blob, cell):
        if (cell.get_x() >= self.game_board.get_board_dimenstion()[0]) or (cell.get_x() < 0):
            return False
        if (cell.get_y() >= self.game_board.get_board_dimenstion()[1]) or (cell.get_y() < 0):
            return False
        if self.game_board.get_board()[cell.get_x()][cell.get_y()] != '-':
            return False
        return ((abs(cell.get_x() - blob.get_position().get_x()) == 2) and (
                abs(cell.get_y() - blob.get_position().get_y()) <= 2)) or (
                       (abs(cell.get_x() - blob.get_position().get_x()) <= 2) and (
                       abs(cell.get_y() - blob.get_position().get_y()) == 2))

    # copy a blob to a specific cell
    def copy_blob_to(self, blob, cell_to_copy):
        new_blob = Blob(Position(cell_to_copy.get_x(), cell_to_copy.get_y()), blob.get_player())
        self.game_board.get_blobs_list().append(new_blob)  # add the new blob
        self.attack_adjacent_blobs(new_blob)

    # move a blob to a specific cell
    def move_blob_to(self, blob, cell_to_move):
        blob.set_position(Position(cell_to_move.get_x(), cell_to_move.get_y()))  # set the new position to blob
        self.attack_adjacent_blobs(blob)

    # apply blob movement
    def make_move_to_blob(self, blob_cell, cell_to_move, player):
        blob = None
        for iter_blob in self.game_board.get_blobs_list():
            if iter_blob.get_position().get_x() == blob_cell.get_x() and iter_blob.get_position().get_y() == blob_cell.get_y():
                blob = iter_blob
                break

        # if no blob has found
        if blob is None or blob.get_player().get_type() != player.get_type():
            return False

        if self.can_copy(blob, cell_to_move):
            self.copy_blob_to(blob, cell_to_move)

        elif self.can_move(blob, cell_to_move):
            self.move_blob_to(blob, cell_to_move)

        else:
            return False

        return True

    # turn the adjacent opponents into blob's team
    def attack_adjacent_blobs(self, blob):

        # check the upper cell
        if ((blob.get_position().get_x() - 1 >= 0) and (
                self.game_board.get_board()[blob.get_position().get_x() - 1][blob.get_position().get_y()] != '-')):
            temp_position = Position(blob.get_position().get_x() - 1, blob.get_position().get_y())
            for iter_blob in self.game_board.get_blobs_list():
                if iter_blob.get_position().get_x() == temp_position.get_x() and iter_blob.get_position().get_y() == temp_position.get_y():
                    iter_blob.set_player(blob.get_player())
                    break

        # check the upper right cell
        if ((blob.get_position().get_x() - 1 >= 0) and (
                blob.get_position().get_y() + 1 < self.game_board.get_board_dimenstion()[1]) and (
                self.game_board.get_board()[blob.get_position().get_x() - 1][blob.get_position().get_y() + 1] != '-')):
            temp_position = Position(blob.get_position().get_x() - 1, blob.get_position().get_y() + 1)
            for iter_blob in self.game_board.get_blobs_list():
                if iter_blob.get_position().get_x() == temp_position.get_x() and iter_blob.get_position().get_y() == temp_position.get_y():
                    iter_blob.set_player(blob.get_player())
                    break

        # check the right cell
        if ((blob.get_position().get_y() + 1 < self.game_board.get_board_dimenstion()[1]) and (
                self.game_board.get_board()[blob.get_position().get_x()][blob.get_position().get_y() + 1] != '-')):
            temp_position = Position(blob.get_position().get_x(), blob.get_position().get_y() + 1)
            for iter_blob in self.game_board.get_blobs_list():
                if iter_blob.get_position().get_x() == temp_position.get_x() and iter_blob.get_position().get_y() == temp_position.get_y():
                    iter_blob.set_player(blob.get_player())
                    break

        # check the lower right cell
        if ((blob.get_position().get_x() + 1 < self.game_board.get_board_dimenstion()[0]) and (
                blob.get_position().get_y() + 1 < self.game_board.get_board_dimenstion()[1]) and (
                self.game_board.get_board()[blob.get_position().get_x() + 1][blob.get_position().get_y() + 1] != '-')):
            temp_position = Position(blob.get_position().get_x() + 1, blob.get_position().get_y() + 1)
            for iter_blob in self.game_board.get_blobs_list():
                if iter_blob.get_position().get_x() == temp_position.get_x() and iter_blob.get_position().get_y() == temp_position.get_y():
                    iter_blob.set_player(blob.get_player())
                    break

        # check the lower cell
        if ((blob.get_position().get_x() + 1 < self.game_board.get_board_dimenstion()[0]) and (
                self.game_board.get_board()[blob.get_position().get_x() + 1][blob.get_position().get_y()] != '-')):
            temp_position = Position(blob.get_position().get_x() + 1, blob.get_position().get_y())
            for iter_blob in self.game_board.get_blobs_list():
                if iter_blob.get_position().get_x() == temp_position.get_x() and iter_blob.get_position().get_y() == temp_position.get_y():
                    iter_blob.set_player(blob.get_player())
                    break

        # check the lower left cell
        if ((blob.get_position().get_x() + 1 < self.game_board.get_board_dimenstion()[0]) and (
                blob.get_position().get_y() - 1 >= 0) and (
                self.game_board.get_board()[blob.get_position().get_x() + 1][blob.get_position().get_y() - 1] != '-')):
            temp_position = Position(blob.get_position().get_x() + 1, blob.get_position().get_y() - 1)
            for iter_blob in self.game_board.get_blobs_list():
                if iter_blob.get_position().get_x() == temp_position.get_x() and iter_blob.get_position().get_y() == temp_position.get_y():
                    iter_blob.set_player(blob.get_player())
                    break

        # check the left cell
        if ((blob.get_position().get_y() - 1 >= 0) and (
                self.game_board.get_board()[blob.get_position().get_x()][blob.get_position().get_y() - 1] != '-')):
            temp_position = Position(blob.get_position().get_x(), blob.get_position().get_y() - 1)
            for iter_blob in self.game_board.get_blobs_list():
                if iter_blob.get_position().get_x() == temp_position.get_x() and iter_blob.get_position().get_y() == temp_position.get_y():
                    iter_blob.set_player(blob.get_player())
                    break

        # check the lower left cell
        if ((blob.get_position().get_x() - 1 >= 0) and (blob.get_position().get_y() - 1 >= 0) and (
                self.game_board.get_board()[blob.get_position().get_x() - 1][blob.get_position().get_y() - 1] != '-')):
            temp_position = Position(blob.get_position().get_x() - 1, blob.get_position().get_y() - 1)
            for iter_blob in self.game_board.get_blobs_list():
                if iter_blob.get_position().get_x() == temp_position.get_x() and iter_blob.get_position().get_y() == temp_position.get_y():
                    iter_blob.set_player(blob.get_player())
                    break

    # state space
    def next_states(self, player):

        states_list = []  # to store all the possible moves
        blobs_moved = []  # to store blobs moved
        cells_to_move_to = []  # to store the cells that the blobs moved to in every state

        # iterate over blobs in the board
        for blob in self.game_board.get_blobs_list():
            if blob.get_player().get_type() == player.get_type():  # to ensure that player's blobs only will move
                for i in range(self.game_board.get_board_dimenstion()[0] * self.game_board.get_board_dimenstion()[
                    1]):  # iterate over board cells

                    cell = self.mapping(i + 1)  # get cell as [x, y]
                    pos = Position(cell[0], cell[1])

                    if (blob.get_position().get_x() != cell[0]) or (
                            blob.get_position().get_y() != cell[1]):  # to ensure not to take blob's cell

                        # if blob can copy itself to the adjacent cell
                        if self.can_copy(blob, pos):
                            temp_state = copy.deepcopy(self)
                            if temp_state.make_move_to_blob(blob.get_position(), pos, blob.get_player()):
                                states_list.append(temp_state)
                                blobs_moved.append(blob)
                                cells_to_move_to.append(pos)

                        # if blob can move to 2 cells away
                        if self.can_move(blob, pos):
                            temp_state = copy.deepcopy(self)
                            if temp_state.make_move_to_blob(blob.get_position(), pos, blob.get_player()):
                                states_list.append(temp_state)
                                blobs_moved.append(blob)
                                cells_to_move_to.append(pos)

        return states_list, blobs_moved, cells_to_move_to

    # Playing with AI
    def AI_plays(self, game_logic, depth):
        next_move = game_logic.Mini_Max_alpha_beta(self, depth, AI=True)
        self.make_move_to_blob(next_move[0].get_position(), next_move[1], Player('AI'))
