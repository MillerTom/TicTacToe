import random

WINNING_ROWS = [(0, 1, 2), (3, 4, 5), (6, 7, 8),
                (0, 3, 6), (1, 4, 7), (2, 5, 8),
                (0, 4, 8), (2, 4, 6)]
OPPONENTS = {'X': 'O', 'O': 'X'}


class Game:
    def __init__(self, player_letter):
        self.player_letter = player_letter
        self.computer_letter = OPPONENTS[self.player_letter]
        self._is_over = False

    @staticmethod
    def copy_board(board):
        # Make a duplicate of the board list and return it's duplicate.
        copy_board = []

        for i in board:
            copy_board.append(i)

        return copy_board

    @staticmethod
    def is_space_free(board, move):
        # Return true if the passed move is free on the passed board.
        return board[move] == ''

    @staticmethod
    def is_winner(board, player):
        """
        Given a board and a player's letter, this function returns True if the player has won.
        """
        for row in WINNING_ROWS:
            is_win = True
            for pos in row:
                if not board[pos] == player:
                    is_win = False
                    break
            if is_win:
                return True
        return None

    def make_move(self, board, letter, move):
        if self.is_space_free(board, move):
            board[move] = letter
            return board

    def choose_random_move_from_list(self, board, moves_list):
        """
        Returns a valid move from the passed list on the passed board.
        Returns None if there is no valid move.
        """
        possible_moves = []
        for i in moves_list:
            if self.is_space_free(board, i):
                possible_moves.append(i)

        if len(possible_moves) != 0:
            return random.choice(possible_moves)
        else:
            return None

    def get_computer_move(self, board):
        """
        Simple AI for Computer moves
        """
        corner_list = [0, 2, 6, 8]
        side_list = [1, 3, 5, 7]

        # First, check if we can win in the next move
        for i in xrange(9):
            copy = self.copy_board(board)
            if self.is_space_free(copy, i):
                self.make_move(copy, self.computer_letter, i)
                if self.is_winner(copy, self.computer_letter):
                    return i

        # Check if the player could win on his next move, and block them.
        for i in xrange(9):
            copy = self.copy_board(board)
            if self.is_space_free(copy, i):
                self.make_move(copy, self.player_letter, i)
                if self.is_winner(copy, self.player_letter):
                    return i

        # Try to take the center, if it is free.
        if self.is_space_free(board, 4):
            return 4

        if not self.is_board_full(board):
            for i in corner_list:
                copy_list = corner_list
                copy_list.remove(i)
                if board[i] == self.player_letter:
                    for j in copy_list:
                        if board[j] == self.player_letter:
                            return self.choose_random_move_from_list(board, side_list)

        # Try to take one of the corners, if they are free.
        move = self.choose_random_move_from_list(board, corner_list)
        if move is not None:
            return move

        # Move on one of the sides.
        return self.choose_random_move_from_list(board, side_list)

    def is_board_full(self, board):
        # Return True if every space on the board has been taken. Otherwise return False.
        for i in xrange(9):
            if self.is_space_free(board, i):
                return False
        return True