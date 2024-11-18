from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

PLAYER = "Santa"
AI = "Grinch"
board = [["" for _ in range(3)] for _ in range(3)]

def is_winner(b, player):
    return any(all(b[r][c] == player for c in range(3)) for r in range(3)) or \
           any(all(b[r][c] == player for r in range(3)) for c in range(3)) or \
           all(b[i][i] == player for i in range(3)) or \
           all(b[i][2 - i] == player for i in range(3))

def is_draw(b):
    return all(all(cell != "" for cell in row) for row in b)

def minimax(board, depth, is_maximizing, alpha, beta):
    if is_winner(board, AI):
        return 10 - depth
    if is_winner(board, PLAYER):
        return depth - 10
    if is_draw(board):
        return 0

    if is_maximizing:
        best_score = float('-inf')
        for r in range(3):
            for c in range(3):
                if board[r][c] == "":
                    board[r][c] = AI
                    score = minimax(board, depth + 1, False, alpha, beta)
                    board[r][c] = ""
                    best_score = max(best_score, score)
                    alpha = max(alpha, best_score)
                    if beta <= alpha:  # Prune the branch
                        break
        return best_score
    else:
        best_score = float('inf')
        for r in range(3):
            for c in range(3):
                if board[r][c] == "":
                    board[r][c] = PLAYER
                    score = minimax(board, depth + 1, True, alpha, beta)
                    board[r][c] = ""
                    best_score = min(best_score, score)
                    beta = min(beta, best_score)
                    if beta <= alpha:  # Prune the branch
                        break
        return best_score

def best_move():
    best_score = float('-inf')
    move = None
    for r in range(3):
        for c in range(3):
            if board[r][c] == "":
                board[r][c] = AI
                score = minimax(board, 0, False, float('-inf'), float('inf'))
                board[r][c] = ""
                if score > best_score:
                    best_score = score
                    move = (r, c)
    return move

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/move", methods=["POST"])
def player_move():
    global board
    data = request.get_json()
    row, col = int(data["row"]), int(data["col"])
    if board[row][col] != "":
        return jsonify({"status": "invalid"})
    board[row][col] = PLAYER
    if is_winner(board, PLAYER):
        return jsonify({"status": "win", "winner": PLAYER, "board": board})
    if is_draw(board):
        return jsonify({"status": "draw", "board": board})
    r, c = best_move()
    board[r][c] = AI
    if is_winner(board, AI):
        return jsonify({"status": "win", "winner": AI, "ai_move": [r, c], "board": board})
    if is_draw(board):
        return jsonify({"status": "draw", "ai_move": [r, c], "board": board})
    return jsonify({"status": "continue", "ai_move": [r, c], "board": board})

@app.route("/reset", methods=["POST"])
def reset():
    global board
    board = [["" for _ in range(3)] for _ in range(3)]
    return jsonify({"status": "reset"})

if __name__ == "__main__":
    app.run(debug=True)