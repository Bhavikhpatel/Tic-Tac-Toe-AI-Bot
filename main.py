import streamlit as st
import numpy as np

def create_board():
    return np.array([[" "]*3 for _ in range(3)])

def check_winner(board, player):
    win_conditions = [
        [board[0][0], board[0][1], board[0][2]],
        [board[1][0], board[1][1], board[1][2]],
        [board[2][0], board[2][1], board[2][2]],
        [board[0][0], board[1][0], board[2][0]],
        [board[0][1], board[1][1], board[2][1]],
        [board[0][2], board[1][2], board[2][2]],
        [board[0][0], board[1][1], board[2][2]],
        [board[0][2], board[1][1], board[2][0]]
    ]
    return [player, player, player] in win_conditions

def is_board_full(board):
    return " " not in board.flatten()

def minimax(board, depth, is_maximizing, alpha, beta, ai_player, human_player):
    if check_winner(board, ai_player):
        return 10 - depth
    if check_winner(board, human_player):
        return -10 + depth
    if is_board_full(board):
        return 0
    if is_maximizing:
        best_score = float('-inf')
        for i in range(3):
            for j in range(3):
                if board[i][j] == " ":
                    board[i][j] = ai_player
                    score = minimax(board, depth + 1, False, alpha, beta, ai_player, human_player)
                    board[i][j] = " "
                    best_score = max(score, best_score)
                    alpha = max(alpha, best_score)
                    if beta <= alpha:
                        break
        return best_score
    else:
        best_score = float('inf')
        for i in range(3):
            for j in range(3):
                if board[i][j] == " ":
                    board[i][j] = human_player
                    score = minimax(board, depth + 1, True, alpha, beta, ai_player, human_player)
                    board[i][j] = " "
                    best_score = min(score, best_score)
                    beta = min(beta, best_score)
                    if beta <= alpha:
                        break
        return best_score

def get_best_move(board, ai_player, human_player):
    best_score = float('-inf')
    best_move = None
    for i in range(3):
        for j in range(3):
            if board[i][j] == " ":
                board[i][j] = ai_player
                score = minimax(board, 0, False, float('-inf'), float('inf'), ai_player, human_player)
                board[i][j] = " "
                if score > best_score:
                    best_score = score
                    best_move = (i, j)
    return best_move

def main():
    st.title("Unbeatable Tic Tac Toe")
    if 'board' not in st.session_state:
        st.session_state.board = create_board()
    if 'game_started' not in st.session_state:
        st.session_state.game_started = False
    if 'human_player' not in st.session_state:
        st.session_state.human_player = None
    if 'ai_player' not in st.session_state:
        st.session_state.ai_player = None
    if 'current_turn' not in st.session_state:
        st.session_state.current_turn = 'X'
    if 'game_over' not in st.session_state:
        st.session_state.game_over = False
    if not st.session_state.game_started:
        st.write("Choose your player:")
        col1, col2 = st.columns(2)
        with col1:
            if st.button("X"):
                st.session_state.human_player = "X"
                st.session_state.ai_player = "O"
        with col2:
            if st.button("O"):
                st.session_state.human_player = "O"
                st.session_state.ai_player = "X"
        if st.session_state.human_player:
            if st.button("START GAME"):
                st.session_state.game_started = True
                if st.session_state.ai_player == "X":
                    move = get_best_move(st.session_state.board, st.session_state.ai_player, st.session_state.human_player)
                    st.session_state.board[move[0]][move[1]] = st.session_state.ai_player
                    st.session_state.current_turn = st.session_state.human_player
    if st.session_state.game_started and not st.session_state.game_over:
        for i in range(3):
            col1, col2, col3 = st.columns(3)
            with col1:
                if st.button(st.session_state.board[i][0], key=f"00{i}"):
                    if st.session_state.board[i][0] == " " and st.session_state.current_turn == st.session_state.human_player:
                        st.session_state.board[i][0] = st.session_state.human_player
                        st.session_state.current_turn = st.session_state.ai_player
            with col2:
                if st.button(st.session_state.board[i][1], key=f"01{i}"):
                    if st.session_state.board[i][1] == " " and st.session_state.current_turn == st.session_state.human_player:
                        st.session_state.board[i][1] = st.session_state.human_player
                        st.session_state.current_turn = st.session_state.ai_player
            with col3:
                if st.button(st.session_state.board[i][2], key=f"02{i}"):
                    if st.session_state.board[i][2] == " " and st.session_state.current_turn == st.session_state.human_player:
                        st.session_state.board[i][2] = st.session_state.human_player
                        st.session_state.current_turn = st.session_state.ai_player
        if check_winner(st.session_state.board, st.session_state.human_player):
            st.success("You won! (This should be nearly impossible!)")
            st.session_state.game_over = True
        elif check_winner(st.session_state.board, st.session_state.ai_player):
            st.error("AI wins!")
            st.session_state.game_over = True
        elif is_board_full(st.session_state.board):
            st.info("It's a draw!")
            st.session_state.game_over = True
        elif st.session_state.current_turn == st.session_state.ai_player:
            move = get_best_move(st.session_state.board, st.session_state.ai_player, st.session_state.human_player)
            if move:
                st.session_state.board[move[0]][move[1]] = st.session_state.ai_player
                st.session_state.current_turn = st.session_state.human_player
            if check_winner(st.session_state.board, st.session_state.ai_player):
                st.error("AI wins!")
                st.session_state.game_over = True
            elif is_board_full(st.session_state.board):
                st.info("It's a draw!")
                st.session_state.game_over = True

    if st.session_state.game_over and st.button("Play Again"):
        st.session_state.board = create_board()
        st.session_state.game_started = False
        st.session_state.human_player = None
        st.session_state.ai_player = None
        st.session_state.current_turn = 'X'
        st.session_state.game_over = False

if __name__ == "__main__":
    main()
            
