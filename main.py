import chess
import socket
from stockfish import Stockfish
import platform
import chess.pgn
import os

# Detect the operating system
os_name = platform.system()

white = "Darwin"
thinkTime = 200

game = chess.pgn.Game()


send_host = '0.0.0.0'

# Define the path based on the OS
if os_name == 'Windows':
    stockfish_path = ".\stockfish-windows-x86-64-avx2.exe"
    send_host = '100.115.28.85'
elif os_name == 'Darwin':  # Darwin is the system name for macOS
    stockfish_path = "/usr/local/bin/stockfish"
    send_host = '100.115.59.53'

else:
    raise Exception("Unsupported operating system")

# Initialize Stockfish with the appropriate path
fish = Stockfish(path=stockfish_path, parameters={"Hash": 2048, "Threads": 15})





# Define host and port
port = 12345
host = '0.0.0.0'




# role = input("machine a or b:\n")
# if role == 'a':
#     port = 12345
# else:
#     port = 54321




print("Server listening...")
node = game


# Create a socket object
receive_socket = socket.socket()

send_socket = socket.socket()
# Bind to the port
receive_socket.bind((host, port))

# Wait for client connection
receive_socket.listen(5)

def play_game():
    global send_socket
    global receive_socket
    
    board = chess.Board()
    decisive = False
    if os_name == white:
        # White plays the first move
        print("Sent First Move")
        
        send_socket = socket.socket()
        send_socket.connect((send_host, port))
        send_socket.send('e2e4'.encode())
        send_socket.close()
        board.push_uci('e2e4')
    while not decisive:

        win = ""
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
            # Set who won
            win = "White" if not board.turn else "Black"
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
            move = fish.get_best_move_time(thinkTime)
            board.push_uci(move)
            # Check for dicisiveness after sending the move
            if board.is_checkmate() or board.is_stalemate() or board.is_insufficient_material() or board.can_claim_fifty_moves() or board.can_claim_threefold_repetition() or board.can_claim_draw():
                win = "White" if not board.turn else "Black"
                decisive = True
            # Send the move
            send_socket = socket.socket()
            send_socket.connect((send_host, port))
            send_socket.send(move.encode())
            print(f"sent {move}")
            send_socket.close()
            continue
            
    
        game = chess.pgn.Game()
        game.headers["Event"] = "Example Game"
        game.headers["White"] = "Player1"
        game.headers["Black"] = "Player2"
        # If win is not "", then put result as win, otherwise draw
        game.headers["Result"] = win if win else "1/2-1/2"

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