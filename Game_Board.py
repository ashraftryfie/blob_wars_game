import copy

from Blob import Blob
from Game_Controller import Game_Controller
from Player import Player
from Position import Position


class Game_Board:
    # n, m = 0, 0  # n and m are board dimensions where n refers to row number and m refers to column number
    # board = [[]]  # 2D array to represent the board
    # blobs = []  # the blobs in the board

    def __init__(self, n, m, blobs_list):
        self.n = n
        self.m = m
        self.blobs = blobs_list
        self.board = [['-' for i in range(n)] for j in range(m)]

    # get blobs list in the board
    def get_blobs_list(self):
        return self.blobs

    # get board dimenstion
    def get_board_dimenstion(self):
        return self.n, self.m

    # get game board
    def get_board(self):
        return self.board

    # display the board
    def display_board(self):
        self.board = [['-' for i in range(self.n)] for j in range(self.m)]
        for blob in self.blobs:
            self.board[blob.get_position().get_x()][blob.get_position().get_y()] = blob.get_color()
        print()
        for row in self.board:
            for cell in row:
                print(f' {cell} ', end='')
            print()
        total_score = self.get_score()
        print('\nHuman : ', total_score[0], '', 'AI : ', total_score[1], '\n\n')

    # calculate the score for the human and for the AI
    def get_score(self):
        human_score = 0  # Human's score
        AI_score = 0  # AI's score

        for blob in self.blobs:
            if blob.get_player().get_type() == 'Human':
                human_score += 1

            if blob.get_player().get_type() == 'AI':
                AI_score += 1

        return human_score, AI_score

    # check if this state is a final state
    def is_final_state(self):

        is_filled = True  # to check weather the board is filled
        player_won = True  # to check if any player has won
        no_moves_left = False  # to check if a player has no moves left, so the empty cells will be filled with the opponent's blobs

        # check the board if filled
        for row in self.board:
            for cell in row:
                if cell == '-':
                    is_filled = False
                    break

        # check if Human's blobs or AI's blobs is gone
        helper = self.get_blobs_list()[
            0].get_player().get_type()  # to store the first player type and then check if there is another player in the game
        for blob in self.get_blobs_list():
            if blob.get_player().get_type() != helper:
                player_won = False
                break

        next_moves_for_human = len(Game_Controller(self).next_states(Player('Human'))[0])
        next_moves_for_AI = len(Game_Controller(self).next_states(Player('AI'))[0])

        if next_moves_for_human == 0 or next_moves_for_AI == 0:
            no_moves_left = True
            for i in range(self.n):
                for j in range(self.m):
                    if self.board[i][j] == '-':
                        self.blobs.append(
                            Blob(Position(i, j), Player('AI') if next_moves_for_human == 0 else Player('Human')))

        return (is_filled or player_won or no_moves_left)


    def pass_turn(self):
        for i in range(self.n):
            for j in range(self.m):
                if self.board[i][j] == '-':
                    self.blobs.append(
                        Blob(Position(i, j), Player('AI')))
