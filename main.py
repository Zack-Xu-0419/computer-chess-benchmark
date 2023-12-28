import chess
import socket
from stockfish import Stockfish
import platform

# Detect the operating system
os_name = platform.system()



# Define the path based on the OS
if os_name == 'Windows':
    stockfish_path = ".\stockfish-windows-x86-64-avx2.exe"
elif os_name == 'Darwin':  # Darwin is the system name for macOS
    stockfish_path = "/usr/local/bin/stockfish"
else:
    raise Exception("Unsupported operating system")

# Initialize Stockfish with the appropriate path
fish = Stockfish(path=stockfish_path)

board = chess.Board()


# Create a socket object
receive_socket = socket.socket()

send_socket = socket.socket()


# Define host and port
port = 12345
host = '0.0.0.0'
send_host = '100.115.28.85'



if os_name == 'Darwin':
    # Mac plays first move
    
    send_socket.connect((send_host, port))
    send_socket.send('e2e4')
    send_socket.close()


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

while True:

    # Establish connection with client
    client_socket, addr = receive_socket.accept()

    # Receive data from the client
    data = client_socket.recv(1024).decode()

    print('Received:', data)

    client_socket.close()

    # If a move is received, push it to the board
    board.push_uci(data)
    print(board)
    # Check if the game is still Going
    if not board.is_checkmate() and not board.is_insufficient_material() and not board.can_claim_fifty_moves() and not board.can_claim_draw() and not board.can_claim_threefold_repetition():
        # Give the move to stockfish to figure out best move
        fish.set_fen_position(board.board_fen())
        move = fish.get_best_move_time(2000)
        send_socket.connect((send_host, port))
        send_socket.send(move.encode())
        send_socket.close()
    # Communicate back to other machine
