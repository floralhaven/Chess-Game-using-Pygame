import pygame
import sys
import random

pygame.init()

# Constants
WIDTH, HEIGHT = 800, 800
SQUARE_SIZE = WIDTH // 8

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BROWN = (139, 69, 19)
YELLOW = (255, 255, 0)
GRAY = (169, 169, 169)
GREEN = (0, 255, 0)  # Highlight for valid moves

# Create the screen
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Chess Game")

# Chess piece class
class ChessPiece:
    def __init__(self, color, type, image):
        self.color = color
        self.type = type
        self.image = pygame.image.load(image)
        self.image = pygame.transform.scale(self.image, (SQUARE_SIZE, SQUARE_SIZE))
        self.has_moved = False

# Initialize the board
board = [[None for _ in range(8)] for _ in range(8)]
current_player = 'white'
selected_piece = None
selected_pos = None
game_over = False

# Function to initialize Chess960 back rank
def init_chess960_backrank():
    pieces = [None] * 8
    light_squares = [1, 3, 5, 7]
    dark_squares = [0, 2, 4, 6]
    
    # Place bishops on light and dark squares
    light_bishop_position = random.choice(light_squares)
    dark_bishop_position = random.choice(dark_squares)
    pieces[light_bishop_position] = 'bishop'
    pieces[dark_bishop_position] = 'bishop'
    
    # Place rooks and king with guaranteed valid positions
    remaining_positions = [i for i in range(8) if pieces[i] is None]
    
    # Set rooks on the first and last remaining positions, ensuring room for the king
    rook_left, rook_right = remaining_positions[0], remaining_positions[-1]
    pieces[rook_left] = 'rook'
    pieces[rook_right] = 'rook'
    
    # Place the king between the two rooks
    king_position = remaining_positions[1]
    pieces[king_position] = 'king'
    
    # Assign the remaining pieces
    remaining_positions = [i for i in range(8) if pieces[i] is None]
    remaining_pieces = ['queen', 'knight', 'knight']
    for pos, piece in zip(remaining_positions, remaining_pieces):
        pieces[pos] = piece

    return pieces


def init_chess960_board():
    # Place pawns
    for col in range(8):
        board[1][col] = ChessPiece('black', 'pawn', 'images/black_pawn.png')
        board[6][col] = ChessPiece('white', 'pawn', 'images/white_pawn.png')
    
    # Generate back rank for Chess960
    black_backrank = init_chess960_backrank()
    white_backrank = black_backrank[:]  # Mirror for white, same configuration
    
    # Place pieces on back rank based on Chess960 configuration
    for col, piece_type in enumerate(black_backrank):
        board[0][col] = ChessPiece('black', piece_type, f'images/black_{piece_type}.png')
        board[7][col] = ChessPiece('white', piece_type, f'images/white_{piece_type}.png')

# Function to initialize the original chess board
def init_original_board():
    # Pawns
    for col in range(8):
        board[1][col] = ChessPiece('black', 'pawn', 'images/black_pawn.png')
        board[6][col] = ChessPiece('white', 'pawn', 'images/white_pawn.png')

    # Rooks
    board[0][0] = board[0][7] = ChessPiece('black', 'rook', 'images/black_rook.png')
    board[7][0] = board[7][7] = ChessPiece('white', 'rook', 'images/white_rook.png')

    # Knights
    board[0][1] = board[0][6] = ChessPiece('black', 'knight', 'images/black_knight.png')
    board[7][1] = board[7][6] = ChessPiece('white', 'knight', 'images/white_knight.png')

    # Bishops
    board[0][2] = board[0][5] = ChessPiece('black', 'bishop', 'images/black_bishop.png')
    board[7][2] = board[7][5] = ChessPiece('white', 'bishop', 'images/white_bishop.png')

    # Queens
    board[0][3] = ChessPiece('black', 'queen', 'images/black_queen.png')
    board[7][3] = ChessPiece('white', 'queen', 'images/white_queen.png')

    # Kings
    board[0][4] = ChessPiece('black', 'king', 'images/black_king.png')
    board[7][4] = ChessPiece('white', 'king', 'images/white_king.png')

# Function to check if the game is over by checkmate or stalemate
def is_game_over():
    white_king = any(piece.type == 'king' and piece.color == 'white' for row in board for piece in row if piece)
    black_king = any(piece.type == 'king' and piece.color == 'black' for row in board for piece in row if piece)
    if not white_king:
        return 'black'  # Black wins if the white king is missing
    elif not black_king:
        return 'white'  # White wins if the black king is missing
    return None  # Game is not over


# Start Menu function
def start_menu():
    font = pygame.font.SysFont('Arial', 36)
    title = font.render('Select Game Mode', True, WHITE)
    chess960_button = pygame.Rect(WIDTH // 2.05 - 100, HEIGHT // 2.1 - 100, 220, 100)
    original_button = pygame.Rect(WIDTH // 2.05 - 100, HEIGHT // 2.1 + 50, 220, 100)

    while True:
        screen.fill(BLACK)
        screen.blit(title, (WIDTH // 2 - title.get_width() // 2, HEIGHT // 4))
        
        pygame.draw.rect(screen, GRAY, chess960_button)
        pygame.draw.rect(screen, GRAY, original_button)

        chess960_text = font.render('Chess960', True, WHITE)
        original_text = font.render('Original Chess', True, WHITE)

        screen.blit(chess960_text, (WIDTH // 2 - chess960_text.get_width() // 2, HEIGHT // 2 - 90))
        screen.blit(original_text, (WIDTH // 2 - original_text.get_width() // 2, HEIGHT // 2 + 60))

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            
            if event.type == pygame.MOUSEBUTTONDOWN:
                if chess960_button.collidepoint(event.pos):
                    return 'Chess960'
                if original_button.collidepoint(event.pos):
                    return 'Original'

# Function to draw the board
def draw_board():
    for row in range(8):
        for col in range(8):
            color = WHITE if (row + col) % 2 == 0 else BROWN
            pygame.draw.rect(screen, color, (col * SQUARE_SIZE, row * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))
    
    if selected_pos:
        pygame.draw.rect(screen, YELLOW, (selected_pos[1] * SQUARE_SIZE, selected_pos[0] * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))

# Function to draw the pieces
def draw_piece():
    for row in range(8):
        for col in range(8):
            piece = board[row][col]
            if piece:
                screen.blit(piece.image, (col * SQUARE_SIZE, row * SQUARE_SIZE))

# Function to highlight valid moves
def highlight_valid_moves(valid_moves):
    for (r, c) in valid_moves:
        pygame.draw.rect(screen, GREEN, (c * SQUARE_SIZE, r * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))

# Function to get valid moves for a piece
def get_valid_moves(piece, row, col):
    moves = []
    if piece.type == 'pawn':
        direction = -1 if piece.color == 'white' else 1
        if 0 <= row + direction < 8 and board[row + direction][col] is None:
            moves.append((row + direction, col))
            if (piece.color == 'white' and row == 6) or (piece.color == 'black' and row == 1):
                if board[row + 2*direction][col] is None:
                    moves.append((row + 2*direction, col))
        for dc in [-1, 1]:
            if 0 <= row + direction < 8 and 0 <= col + dc < 8:
                if board[row + direction][col + dc] and board[row + direction][col + dc].color != piece.color:
                    moves.append((row + direction, col + dc))

    elif piece.type == 'rook':
        for dr, dc in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
            r, c = row + dr, col + dc
            while 0 <= r < 8 and 0 <= c < 8:
                if board[r][c] is None:
                    moves.append((r, c))
                elif board[r][c].color != piece.color:
                    moves.append((r, c))
                    break
                else:
                    break
                r, c = r + dr, c + dc

    elif piece.type == 'knight':
        for dr, dc in [(2, 1), (2, -1), (-2, 1), (-2, -1), (1, 2), (1, -2), (-1, 2), (-1, -2)]:
            r, c = row + dr, col + dc
            if 0 <= r < 8 and 0 <= c < 8 and (board[r][c] is None or board[r][c].color != piece.color):
                moves.append((r, c))

    elif piece.type == 'bishop':
        for dr, dc in [(1, 1), (1, -1), (-1, 1), (-1, -1)]:
            r, c = row + dr, col + dc
            while 0 <= r < 8 and 0 <= c < 8:
                if board[r][c] is None:
                    moves.append((r, c))
                elif board[r][c].color != piece.color:
                    moves.append((r, c))
                    break
                else:
                    break
                r, c = r + dr, c + dc

    elif piece.type == 'queen':
        for dr, dc in [(1, 0), (-1, 0), (0, 1), (0, -1), (1, 1), (1, -1), (-1, 1), (-1, -1)]:
            r, c = row + dr, col + dc
            while 0 <= r < 8 and 0 <= c < 8:
                if board[r][c] is None:
                    moves.append((r, c))
                elif board[r][c].color != piece.color:
                    moves.append((r, c))
                    break
                else:
                    break
                r, c = r + dr, c + dc

    elif piece.type == 'king':
        for dr in [-1, 0, 1]:
            for dc in [-1, 0, 1]:
                if dr == 0 and dc == 0:
                    continue
                r, c = row + dr, col + dc
                if 0 <= r < 8 and 0 <= c < 8 and (board[r][c] is None or board[r][c].color != piece.color):
                    moves.append((r, c))

    return moves

# Main function to run the game
def main():
    global selected_piece, selected_pos, current_player, game_over
    game_mode = start_menu()  # Get game mode from the start menu

    # Initialize the board based on selected game mode
    if game_mode == 'Chess960':
        init_chess960_board()
    elif game_mode == 'Original':
        init_original_board()

    winning_player = None  # Track the winning player

    while True:
        if game_over:
            # Display the game-over screen
            screen.fill(BLACK)
            font = pygame.font.SysFont('Arial', 36)
            if winning_player:
                text = font.render(f'{winning_player.capitalize()} wins! Play again? (Y/N)', True, WHITE)
            else:
                text = font.render('Game Over! Play again? (Y/N)', True, WHITE)
            screen.blit(text, (WIDTH // 2 - text.get_width() // 2, HEIGHT // 2 - text.get_height() // 2))
            pygame.display.flip()
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_y:
                        main()  # Restart the game
                    elif event.key == pygame.K_n:
                        pygame.quit()
                        sys.exit()
            continue

        # Event Handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                col, row = event.pos[0] // SQUARE_SIZE, event.pos[1] // SQUARE_SIZE
                piece = board[row][col]

                if selected_pos:
                    if (row, col) in get_valid_moves(selected_piece, selected_pos[0], selected_pos[1]):
                        board[row][col] = selected_piece
                        board[selected_pos[0]][selected_pos[1]] = None
                        selected_piece.has_moved = True
                        selected_pos = None
                        current_player = 'black' if current_player == 'white' else 'white'
                        
                        # Check if the game is over after a move
                        winning_player = is_game_over()
                        game_over = winning_player is not None  # True if there's a winner
                    else:
                        selected_pos = None
                elif piece and piece.color == current_player:
                    selected_piece = piece
                    selected_pos = (row, col)

        # Drawing
        draw_board()
        if selected_piece and selected_pos:
            valid_moves = get_valid_moves(selected_piece, selected_pos[0], selected_pos[1])
            highlight_valid_moves(valid_moves)
        draw_piece()
        pygame.display.flip()

if __name__ == "__main__":
    main()
