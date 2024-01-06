import chess
import chess.pgn

# Initialize the chess board with some moves
board = chess.Board()
board.push_uci("e2e4")
board.push_uci("e7e5")

# Create a new game and set up headers (optional)
game = chess.pgn.Game()
game.headers["Event"] = "Example Game"
game.headers["White"] = "Player1"
game.headers["Black"] = "Player2"
node = game

for move in board.move_stack:
    node = node.add_variation(move)

# Export to PGN
pgn_string = str(game)
print(pgn_string)
