import chess
import socket
from stockfish import Stockfish
import platform
import chess.pgn
import os

# Detect the operating system
os_name = platform.system()

game = chess.pgn.Game()


send_host = '0.0.0.0'

# Define the path based on the OS
if os_name == 'Windows':
    stockfish_path = ".\stockfish-windows-x86-64-avx2.exe"
    send_host = '100.115.0.1'
elif os_name == 'Darwin':  # Darwin is the system name for macOS
    stockfish_path = "/usr/local/bin/stockfish"
    send_host = '100.115.59.53'

else:
    raise Exception("Unsupported operating system")

# Initialize Stockfish with the appropriate path
fish = Stockfish(path=stockfish_path, parameters={"Hash": 2048, "Threads": 15})



# Create a socket object
receive_socket = socket.socket()

send_socket = socket.socket()


# Define host and port
port = 12345
host = '0.0.0.0'




# role = input("machine a or b:\n")
# if role == 'a':
#     port = 12345
# else:
#     port = 54321


# Bind to the port
receive_socket.bind((host, port))

# Wait for client connection
receive_socket.listen(5)

print("Server listening...")
node = game

def play_game():
    board = chess.Board()
    decisive = False
    if os_name == 'Darwin':
        # Mac plays first move
        
        send_socket.connect((send_host, port))
        send_socket.send('e2e4')
        send_socket.close()
    while not decisive:

        # Establish connection with client
        client_socket, addr = receive_socket.accept()

        # Receive data from the client
        data = client_socket.recv(1024).decode()

        print('Received:', data)

        client_socket.close()

        # If a move is received, push it to the board
        board.push_uci(data)
        print(board)
        print("White to move" if board.turn else "Black to move")

        # Check game status only after a move is received
        if board.is_checkmate():
            print("Checkmate. White wins!" if not board.turn else "Checkmate. Black wins!")
            decisive = True
        elif board.is_stalemate():
            print("Game drawn due to stalemate.")
            decisive = True
        elif board.is_insufficient_material():
            print("Game drawn due to insufficient material.")
            decisive = True
        elif board.can_claim_fifty_moves():
            print("Game drawn due to fifty-move rule.")
            decisive = True
        elif board.can_claim_threefold_repetition():
            print("Game drawn due to threefold repetition.")
            decisive = True
        elif board.can_claim_draw():
            print("Game drawn (draw claim).")
            decisive = True
        else:
            # If the game is still ongoing, let Stockfish make a move
            fish.set_fen_position(board.fen())
            move = fish.get_best_move_time(5000)
            board.push_uci(move)
            # Send the move
            send_socket = socket.socket()
            send_socket.connect((send_host, port))
            send_socket.send(move.encode())
            print(f"sent {move}")
            send_socket.close()
    
        game = chess.pgn.Game()
        game.headers["Event"] = "Example Game"
        game.headers["White"] = "Player1"
        game.headers["Black"] = "Player2"

        node = game

        for move in board.move_stack:
            node = node.add_variation(move)

        # Export to PGN
        pgn_string = str(game)
        # put the pgn into a folder: games/number
        pgn_folder = "games"
        if not os.path.exists(pgn_folder):
            os.makedirs(pgn_folder)
        pgn_file = os.path.join(pgn_folder, f"{len(os.listdir(pgn_folder))}.pgn")
        with open(pgn_file, "w") as f:
            f.write(pgn_string)

        print(pgn_string)

        # Communicate back to other machine
    return True

for i in range(10):
    play_game()