import sys
import os
import unittest
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app import app, board, is_winner, is_draw

class TicTacToeTestCase(unittest.TestCase):
    def setUp(self):
        """Set up test client and reset the game board."""
        self.client = app.test_client()  # Create a Flask test client
        self.client.post('/reset')  # Ensure the game starts fresh

    def test_move_endpoint(self):
        """Test making a valid move."""
        response = self.client.post('/move', json={"row": 0, "col": 0})
        data = response.get_json()
        self.assertIn("status", data)
        self.assertIn(data["status"], ["continue", "win", "draw"])
        self.assertEqual(data["status"], "continue")  # Check that the game continues
        self.assertIn("ai_move", data)  # Ensure the AI responded with a move

    def test_invalid_move(self):
        """Test making an invalid move (cell already occupied)."""
        self.client.post('/move', json={"row": 0, "col": 0})  # Make a valid move
        response = self.client.post('/move', json={"row": 0, "col": 0})  # Same cell
        data = response.get_json()
        self.assertEqual(data["status"], "invalid")  # Should return invalid

    def test_reset_endpoint(self):
        """Test resetting the board."""
        self.client.post('/move', json={"row": 0, "col": 0})  # Make a move
        response = self.client.post('/reset')  # Reset the game
        data = response.get_json()
        self.assertEqual(data["status"], "reset")  # Verify reset response
        self.assertEqual(board, [["" for _ in range(3)] for _ in range(3)])  # Empty board

    def test_win_logic(self):
        """Test the game correctly identifies a win."""
        board[0] = ["Santa", "Santa", "Santa"]  # Simulate a win
        self.assertTrue(is_winner(board, "Santa"))
        self.assertFalse(is_winner(board, "Grinch"))

    def test_draw_logic(self):
        """Test the game correctly identifies a draw."""
        full_board = [
            ["Santa", "Grinch", "Santa"],
            ["Grinch", "Santa", "Grinch"],
            ["Grinch", "Santa", "Grinch"],
        ]
        self.assertTrue(is_draw(full_board))
        self.assertFalse(is_winner(full_board, "Santa"))
        self.assertFalse(is_winner(full_board, "Grinch"))

if __name__ == "__main__":
    unittest.main()