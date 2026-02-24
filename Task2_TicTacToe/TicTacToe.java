public class TicTacToe {

    public static final char PLAYER = 'X';
    public static final char AI = 'O';
    public static final char EMPTY = '_';

    private char[] board;

    public TicTacToe() {
        board = new char[9];
        resetBoard();
    }

    public void resetBoard() {
        for (int i = 0; i < 9; i++) {
            board[i] = EMPTY;
        }
    }

    public char[] getBoard() {
        return board;
    }

    public boolean makeMove(int index, char player) {
        if (index >= 0 && index < 9 && board[index] == EMPTY) {
            board[index] = player;
            return true;
        }
        return false;
    }

    public boolean isBoardFull() {
        for (char c : board) {
            if (c == EMPTY) return false;
        }
        return true;
    }

    public char checkWinner() {
        int[][] winCombos = {
            {0, 1, 2}, {3, 4, 5}, {6, 7, 8}, // rows
            {0, 3, 6}, {1, 4, 7}, {2, 5, 8}, // cols
            {0, 4, 8}, {2, 4, 6}              // diagonals
        };

        for (int[] combo : winCombos) {
            if (board[combo[0]] != EMPTY &&
                board[combo[0]] == board[combo[1]] &&
                board[combo[1]] == board[combo[2]]) {
                return board[combo[0]];
            }
        }
        return EMPTY;
    }

    public int[] getWinningCombo() {
        int[][] winCombos = {
            {0, 1, 2}, {3, 4, 5}, {6, 7, 8},
            {0, 3, 6}, {1, 4, 7}, {2, 5, 8},
            {0, 4, 8}, {2, 4, 6}
        };

        for (int[] combo : winCombos) {
            if (board[combo[0]] != EMPTY &&
                board[combo[0]] == board[combo[1]] &&
                board[combo[1]] == board[combo[2]]) {
                return combo;
            }
        }
        return null;
    }

    public boolean isGameOver() {
        return checkWinner() != EMPTY || isBoardFull();
    }

    // Minimax with Alpha-Beta Pruning
    public int minimax(char[] board, int depth, boolean isMaximizing, int alpha, int beta) {
        char winner = checkWinnerForBoard(board);

        if (winner == AI) return 10 - depth;
        if (winner == PLAYER) return depth - 10;
        if (isBoardFullForBoard(board)) return 0;

        if (isMaximizing) {
            int best = Integer.MIN_VALUE;
            for (int i = 0; i < 9; i++) {
                if (board[i] == EMPTY) {
                    board[i] = AI;
                    int score = minimax(board, depth + 1, false, alpha, beta);
                    board[i] = EMPTY;
                    best = Math.max(best, score);
                    alpha = Math.max(alpha, best);
                    if (beta <= alpha) break; // Alpha-Beta Pruning
                }
            }
            return best;
        } else {
            int best = Integer.MAX_VALUE;
            for (int i = 0; i < 9; i++) {
                if (board[i] == EMPTY) {
                    board[i] = PLAYER;
                    int score = minimax(board, depth + 1, true, alpha, beta);
                    board[i] = EMPTY;
                    best = Math.min(best, score);
                    beta = Math.min(beta, best);
                    if (beta <= alpha) break; // Alpha-Beta Pruning
                }
            }
            return best;
        }
    }

    public int getBestMove() {
        int bestScore = Integer.MIN_VALUE;
        int bestMove = -1;

        for (int i = 0; i < 9; i++) {
            if (board[i] == EMPTY) {
                board[i] = AI;
                int score = minimax(board, 0, false, Integer.MIN_VALUE, Integer.MAX_VALUE);
                board[i] = EMPTY;
                if (score > bestScore) {
                    bestScore = score;
                    bestMove = i;
                }
            }
        }
        return bestMove;
    }

    private char checkWinnerForBoard(char[] b) {
        int[][] winCombos = {
            {0, 1, 2}, {3, 4, 5}, {6, 7, 8},
            {0, 3, 6}, {1, 4, 7}, {2, 5, 8},
            {0, 4, 8}, {2, 4, 6}
        };

        for (int[] combo : winCombos) {
            if (b[combo[0]] != EMPTY &&
                b[combo[0]] == b[combo[1]] &&
                b[combo[1]] == b[combo[2]]) {
                return b[combo[0]];
            }
        }
        return EMPTY;
    }

    private boolean isBoardFullForBoard(char[] b) {
        for (char c : b) {
            if (c == EMPTY) return false;
        }
        return true;
    }
}
