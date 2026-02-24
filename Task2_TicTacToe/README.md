# Task 2 — Tic-Tac-Toe AI (Java)

Classic Tic-Tac-Toe against an AI that genuinely tries to beat you. Built with Java Swing for the UI and Minimax with Alpha-Beta Pruning for the AI logic.

The AI is unbeatable when played optimally — the best you can do is force a draw. Alpha-Beta Pruning makes the search faster by cutting off branches that won't affect the final decision.

## How to Run

You'll need **Java JDK 8 or above**.

```bash
javac TicTacToe.java TicTacToeGUI.java
java TicTacToeGUI
```

Or open in IntelliJ IDEA and run `TicTacToeGUI.java`.

## How it Works

- You play as **X**, AI plays as **O**
- The AI uses **Minimax** to evaluate every possible move
- **Alpha-Beta Pruning** cuts off branches that can't influence the result, making it faster
- Scores are tracked across rounds — wins, losses, draws
- Winning cells are highlighted at the end of each game

## Files

- `TicTacToe.java` — game logic, board state, Minimax algorithm
- `TicTacToeGUI.java` — dark-themed Swing interface with score tracking
