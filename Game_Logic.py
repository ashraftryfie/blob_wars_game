import math

from Game_Controller import Game_Controller
from Player import Player


class Game_Logic:

    def __init__(self, game_ctrl):
        self.game_ctrl = game_ctrl

    # evaluating state function
    def evaluate_state(self, state):
        if state.game_board.is_final_state():
            score = state.game_board.get_score()
            if score[0] == 0:
                return +math.inf
            if score[1] == 0:
                return -math.inf

        human_blobs = 0  # to count human's blobs
        AI_blobs = 0  # to count AI's blobs
        for blob in state.game_board.get_blobs_list():
            if blob.get_player().get_type() == 'Human':
                human_blobs += 1
            if blob.get_player().get_type() == 'AI':
                AI_blobs += 1

        return (AI_blobs - human_blobs)

    # MiniMax algorithm with alpha beta pruning
    def Mini_Max_alpha_beta(self, state, depth, AI, alpha=-math.inf, beta=+math.inf):
        if depth == 0 or state.game_board.is_final_state():
            score = self.evaluate_state(state)
            return [None, None, score]

        next_states, blobs_moved, positions = state.next_states(Player('AI') if AI else Player('Human'))

        if AI:
            best_score = [None, None, -math.inf]
            for iter_state, blob, position in zip(next_states, blobs_moved, positions):
                score = self.Mini_Max_alpha_beta(iter_state, depth - 1, not AI, alpha, beta)
                score[0], score[1] = blob, position
                best_score = best_score if best_score[2] >= score[2] else score
                alpha = max(alpha, best_score[2])
                if beta <= alpha:
                    break

            return best_score

        else:
            best_score = [None, None, +math.inf]
            for iter_state, blob, position in zip(next_states, blobs_moved, positions):
                score = self.Mini_Max_alpha_beta(iter_state, depth - 1, not AI, alpha, beta)
                score[0], score[1] = blob, position
                best_score = best_score if best_score[2] <= score[2] else score
                beta = min(beta, best_score[2])
                if alpha >= beta:
                    break

            return best_score

