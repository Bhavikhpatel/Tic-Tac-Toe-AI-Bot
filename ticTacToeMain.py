from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

class GameState:
    def __init__(self):
        self.reset()
    
    def reset(self):
        self.layout = [[None, None, None], [None, None, None], [None, None, None]]
        self.move_no = 1
        self.user_token = None
        self.game_over = False

# Single game instance - Note: this means all users share the same game
game = GameState()

def check_winner(board, token):
    # Check rows
    for i in range(3):
        if board[i][0] == board[i][1] == board[i][2] == token:
            return True
    # Check columns
    for i in range(3):
        if board[0][i] == board[1][i] == board[2][i] == token:
            return True
    # Check diagonals
    if board[0][0] == board[1][1] == board[2][2] == token:
        return True
    if board[0][2] == board[1][1] == board[2][0] == token:
        return True
    return False

def is_board_full(board):
    return all(all(cell is not None for cell in row) for row in board)

def minimax(board, is_maximizing, alpha, beta, ai_token):
    player_token = 'o' if ai_token == 'x' else 'x'
    
    if check_winner(board, ai_token):
        return 1
    elif check_winner(board, player_token):
        return -1
    elif is_board_full(board):
        return 0

    if is_maximizing:
        best_score = float('-inf')
        for i in range(3):
            for j in range(3):
                if board[i][j] is None:
                    board[i][j] = ai_token
                    score = minimax(board, False, alpha, beta, ai_token)
                    board[i][j] = None
                    best_score = max(score, best_score)
                    alpha = max(alpha, score)
                    if beta <= alpha:
                        break
        return best_score
    else:
        best_score = float('inf')
        for i in range(3):
            for j in range(3):
                if board[i][j] is None:
                    board[i][j] = player_token
                    score = minimax(board, True, alpha, beta, ai_token)
                    board[i][j] = None
                    best_score = min(score, best_score)
                    beta = min(beta, score)
                    if beta <= alpha:
                        break
        return best_score

def make_ai_move(ai_token):
    board = game.layout
    best_score = float('-inf')
    best_move = None
    alpha = float('-inf')
    beta = float('inf')
    
    for i in range(3):
        for j in range(3):
            if board[i][j] is None:
                board[i][j] = ai_token
                score = minimax(board, False, alpha, beta, ai_token)
                board[i][j] = None
                if score > best_score:
                    best_score = score
                    best_move = (i, j)
                alpha = max(alpha, score)
                if beta <= alpha:
                    break
                    
    if best_move:
        i, j = best_move
        board[i][j] = ai_token
        game.move_no += 1
        
        if check_winner(board, ai_token):
            game.game_over = True
            return {'status': 'ai_won', 'move': [i, j]}
        elif game.move_no > 9:
            game.game_over = True
            return {'status': 'tie', 'move': [i, j]}
        return {'status': 'continue', 'move': [i, j]}

@app.route('/')
def index():
    game.reset()
    return render_template('index.html')

@app.route('/select_token', methods=['POST'])
def select_token():
    token = request.json.get('token')
    if token not in ['x', 'o']:
        return jsonify({'error': 'Invalid token'}), 400
    
    game.user_token = token
    
    if token == 'o':
        result = make_ai_move('x')
        return jsonify(result)
    
    return jsonify({'status': 'success'})

@app.route('/make_move', methods=['POST'])
def make_move():
    if game.game_over:
        return jsonify({'error': 'Game is over'}), 400
        
    data = request.json
    row, col = data.get('row'), data.get('col')
    
    if not (0 <= row <= 2 and 0 <= col <= 2):
        return jsonify({'error': 'Invalid move'}), 400
        
    if game.layout[row][col] is not None:
        return jsonify({'error': 'Cell already taken'}), 400
        
    game.layout[row][col] = game.user_token
    game.move_no += 1
    
    if check_winner(game.layout, game.user_token):
        game.game_over = True
        return jsonify({'status': 'player_won'})
    elif game.move_no > 9:
        game.game_over = True
        return jsonify({'status': 'tie'})
        
    ai_token = 'o' if game.user_token == 'x' else 'x'
    result = make_ai_move(ai_token)
    return jsonify(result)

@app.route('/reset', methods=['POST'])
def reset():
    game.reset()
    return jsonify({'status': 'success'})

if __name__ == '__main__':
    app.run(debug=True)
