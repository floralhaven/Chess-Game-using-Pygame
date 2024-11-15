import unittest
from unittest.mock import patch
import pygame
import random
from main import *

class TestChessGame(unittest.TestCase):

    def setUp(self):
        pygame.init()
        # Setting up a screen for pygame as it's required even for non-visual tests
        self.screen = pygame.display.set_mode((800, 800))
    
    def test_chess960_backrank_initialization(self):
        """Test if Chess960 backrank is initialized correctly."""
        for _ in range(10):  # Test multiple times to account for randomness
            backrank = init_chess960_backrank()
            self.assertEqual(len(backrank), 8, "Backrank should contain 8 pieces.")
            self.assertEqual(backrank.count('king'), 1, "Backrank must contain one king.")
            self.assertEqual(backrank.count('queen'), 1, "Backrank must contain one queen.")
            self.assertEqual(backrank.count('rook'), 2, "Backrank must contain two rooks.")
            self.assertEqual(backrank.count('knight'), 2, "Backrank must contain two knights.")
            self.assertEqual(backrank.count('bishop'), 2, "Backrank must contain two bishops.")
            rook_positions = [i for i, piece in enumerate(backrank) if piece == 'rook']
            king_position = backrank.index('king')
            self.assertTrue(rook_positions[0] < king_position < rook_positions[1], "King must be between rooks.")

    def test_standard_board_initialization(self):
        """Test if the standard chess board is initialized correctly."""
        init_original_board()
        # Check if the correct pieces are in place
        self.assertEqual(board[0][0].type, 'rook', "Black rook should be at (0,0).")
        self.assertEqual(board[7][0].type, 'rook', "White rook should be at (7,0).")
        self.assertEqual(board[0][1].type, 'knight', "Black knight should be at (0,1).")
        self.assertEqual(board[7][3].type, 'queen', "White queen should be at (7,3).")
        self.assertEqual(board[0][4].type, 'king', "Black king should be at (0,4).")
        self.assertEqual(board[6][0].type, 'pawn', "White pawn should be at (6,0).")
        self.assertEqual(board[1][0].type, 'pawn', "Black pawn should be at (1,0).")

    def test_pawn_moves_generation(self):
        """Test if pawn move generation is correct."""
        init_original_board()
        white_pawn = board[6][4]
        black_pawn = board[1][4]
        white_pawn_moves = get_valid_moves(white_pawn, 6, 4)
        black_pawn_moves = get_valid_moves(black_pawn, 1, 4)
        # White pawn should have two valid moves from the starting position
        self.assertIn((5, 4), white_pawn_moves, "White pawn should be able to move one step forward.")
        self.assertIn((4, 4), white_pawn_moves, "White pawn should be able to move two steps forward from initial position.")
        # Black pawn should have two valid moves from the starting position
        self.assertIn((2, 4), black_pawn_moves, "Black pawn should be able to move one step forward.")
        self.assertIn((3, 4), black_pawn_moves, "Black pawn should be able to move two steps forward from initial position.")

    def test_game_over_king_missing(self):
        """Test if the game detects checkmate/stalemate correctly by missing kings."""
        init_original_board()
        board[0][4] = None  # Remove black king
        winner = is_game_over()
        self.assertEqual(winner, 'white', "White should win if the black king is missing.")
        # Reset and remove white king
        init_original_board()
        board[7][4] = None  # Remove white king
        winner = is_game_over()
        self.assertEqual(winner, 'black', "Black should win if the white king is missing.")

    def test_piece_movement_and_turn_toggle(self):
        """Test piece movement and turn toggle after a move."""
        init_original_board()
        global selected_piece, selected_pos, current_player
        selected_piece = board[6][4]  # White pawn
        selected_pos = (6, 4)
        valid_moves = get_valid_moves(selected_piece, 6, 4)
        new_pos = (4, 4)  # Move two steps forward
        self.assertIn(new_pos, valid_moves, "The move should be valid for white pawn from initial position.")
        board[new_pos[0]][new_pos[1]] = selected_piece
        board[selected_pos[0]][selected_pos[1]] = None
        selected_piece.has_moved = True
        selected_piece = None
        selected_pos = None
        current_player = 'black' if current_player == 'white' else 'white'
        self.assertEqual(current_player, 'black', "Turn should toggle to black after white moves.")

if __name__ == '__main__':
    unittest.main()
