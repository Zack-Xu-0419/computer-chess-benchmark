from stockfish import Stockfish

# Using latest stockfish (at time of programming)

fish = Stockfish(path=".\stockfish-windows-x86-64-avx2.exe")

fish.set_fen_position("rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1")
print(fish.get_best_move())