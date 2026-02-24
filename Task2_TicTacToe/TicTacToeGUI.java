import javax.swing.*;
import javax.swing.border.*;
import java.awt.*;
import java.awt.event.*;

public class TicTacToeGUI extends JFrame {

    private TicTacToe game;
    private JButton[] cells;
    private JLabel statusLabel;
    private JLabel scoreLabel;
    private JButton resetButton;

    private int playerScore = 0;
    private int aiScore = 0;
    private int draws = 0;

    // Colors
    private final Color BG_COLOR = new Color(15, 15, 25);
    private final Color PANEL_COLOR = new Color(25, 25, 40);
    private final Color CELL_COLOR = new Color(35, 35, 55);
    private final Color CELL_HOVER = new Color(50, 50, 75);
    private final Color X_COLOR = new Color(99, 102, 241);
    private final Color O_COLOR = new Color(239, 68, 68);
    private final Color WIN_COLOR = new Color(74, 222, 128);
    private final Color TEXT_COLOR = new Color(229, 229, 229);
    private final Color MUTED = new Color(120, 120, 150);
    private final Color ACCENT = new Color(99, 102, 241);

    public TicTacToeGUI() {
        game = new TicTacToe();
        initUI();
    }

    private void initUI() {
        setTitle("Tic-Tac-Toe — AI Challenge");
        setSize(520, 680);
        setMinimumSize(new Dimension(420, 580));
        setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
        setLocationRelativeTo(null);
        setLayout(new BorderLayout(0, 0));
        getContentPane().setBackground(BG_COLOR);

        // Header
        add(createHeader(), BorderLayout.NORTH);

        // Center - game board + status
        JPanel centerPanel = new JPanel(new BorderLayout(0, 16));
        centerPanel.setBackground(BG_COLOR);
        centerPanel.setBorder(new EmptyBorder(20, 30, 20, 30));

        centerPanel.add(createScorePanel(), BorderLayout.NORTH);
        centerPanel.add(createBoard(), BorderLayout.CENTER);
        centerPanel.add(createStatusPanel(), BorderLayout.SOUTH);

        add(centerPanel, BorderLayout.CENTER);

        // Bottom reset button
        add(createBottomPanel(), BorderLayout.SOUTH);

        setVisible(true);
    }

    private JPanel createHeader() {
        JPanel header = new JPanel(new BorderLayout());
        header.setBackground(PANEL_COLOR);
        header.setBorder(BorderFactory.createCompoundBorder(
            BorderFactory.createMatteBorder(0, 0, 1, 0, new Color(50, 50, 70)),
            new EmptyBorder(16, 24, 16, 24)
        ));

        JLabel title = new JLabel("Tic-Tac-Toe AI");
        title.setFont(new Font("Segoe UI", Font.BOLD, 20));
        title.setForeground(TEXT_COLOR);

        JLabel subtitle = new JLabel("Minimax + Alpha-Beta Pruning");
        subtitle.setFont(new Font("Segoe UI", Font.PLAIN, 12));
        subtitle.setForeground(MUTED);

        JPanel titlePanel = new JPanel();
        titlePanel.setBackground(PANEL_COLOR);
        titlePanel.setLayout(new BoxLayout(titlePanel, BoxLayout.Y_AXIS));
        titlePanel.add(title);
        titlePanel.add(subtitle);

        header.add(titlePanel, BorderLayout.WEST);

        JLabel tag = new JLabel("CodSoft AI Internship");
        tag.setFont(new Font("Segoe UI", Font.PLAIN, 11));
        tag.setForeground(MUTED);
        header.add(tag, BorderLayout.EAST);

        return header;
    }

    private JPanel createScorePanel() {
        JPanel scorePanel = new JPanel(new GridLayout(1, 3, 12, 0));
        scorePanel.setBackground(BG_COLOR);

        scorePanel.add(createScoreCard("You (X)", "0", X_COLOR, "playerScore"));
        scorePanel.add(createScoreCard("Draws", "0", new Color(234, 179, 8), "draws"));
        scorePanel.add(createScoreCard("AI (O)", "0", O_COLOR, "aiScore"));

        return scorePanel;
    }

    private JPanel createScoreCard(String title, String value, Color color, String id) {
        JPanel card = new JPanel(new BorderLayout());
        card.setBackground(PANEL_COLOR);
        card.setBorder(BorderFactory.createCompoundBorder(
            BorderFactory.createLineBorder(new Color(50, 50, 70), 1, true),
            new EmptyBorder(12, 16, 12, 16)
        ));

        JLabel titleLabel = new JLabel(title, SwingConstants.CENTER);
        titleLabel.setFont(new Font("Segoe UI", Font.PLAIN, 12));
        titleLabel.setForeground(MUTED);

        JLabel valueLabel = new JLabel(value, SwingConstants.CENTER);
        valueLabel.setFont(new Font("Segoe UI", Font.BOLD, 28));
        valueLabel.setForeground(color);
        valueLabel.setName(id);

        card.add(titleLabel, BorderLayout.NORTH);
        card.add(valueLabel, BorderLayout.CENTER);

        return card;
    }

    private JPanel createBoard() {
        JPanel boardPanel = new JPanel(new GridLayout(3, 3, 8, 8));
        boardPanel.setBackground(BG_COLOR);
        boardPanel.setBorder(new EmptyBorder(8, 0, 8, 0));

        cells = new JButton[9];
        for (int i = 0; i < 9; i++) {
            final int index = i;
            cells[i] = new JButton("");
            cells[i].setFont(new Font("Segoe UI", Font.BOLD, 48));
            cells[i].setBackground(CELL_COLOR);
            cells[i].setForeground(TEXT_COLOR);
            cells[i].setBorder(BorderFactory.createLineBorder(new Color(50, 50, 75), 2, true));
            cells[i].setFocusPainted(false);
            cells[i].setCursor(new Cursor(Cursor.HAND_CURSOR));
            cells[i].setPreferredSize(new Dimension(120, 120));

            cells[i].addMouseListener(new MouseAdapter() {
                public void mouseEntered(MouseEvent e) {
                    if (cells[index].getText().isEmpty()) {
                        cells[index].setBackground(CELL_HOVER);
                    }
                }
                public void mouseExited(MouseEvent e) {
                    if (cells[index].getText().isEmpty()) {
                        cells[index].setBackground(CELL_COLOR);
                    }
                }
            });

            cells[i].addActionListener(e -> handlePlayerMove(index));
            boardPanel.add(cells[i]);
        }

        return boardPanel;
    }

    private JPanel createStatusPanel() {
        JPanel statusPanel = new JPanel(new BorderLayout());
        statusPanel.setBackground(PANEL_COLOR);
        statusPanel.setBorder(BorderFactory.createCompoundBorder(
            BorderFactory.createLineBorder(new Color(50, 50, 70), 1, true),
            new EmptyBorder(12, 16, 12, 16)
        ));

        statusLabel = new JLabel("Your turn! Click a cell to play.", SwingConstants.CENTER);
        statusLabel.setFont(new Font("Segoe UI", Font.BOLD, 14));
        statusLabel.setForeground(TEXT_COLOR);

        statusPanel.add(statusLabel, BorderLayout.CENTER);
        return statusPanel;
    }

    private JPanel createBottomPanel() {
        JPanel bottomPanel = new JPanel(new FlowLayout(FlowLayout.CENTER));
        bottomPanel.setBackground(BG_COLOR);
        bottomPanel.setBorder(new EmptyBorder(0, 0, 20, 0));

        resetButton = new JButton("New Game");
        resetButton.setFont(new Font("Segoe UI", Font.BOLD, 14));
        resetButton.setBackground(ACCENT);
        resetButton.setForeground(Color.WHITE);
        resetButton.setBorderPainted(false);
        resetButton.setFocusPainted(false);
        resetButton.setCursor(new Cursor(Cursor.HAND_CURSOR));
        resetButton.setPreferredSize(new Dimension(160, 44));

        resetButton.addMouseListener(new MouseAdapter() {
            public void mouseEntered(MouseEvent e) { resetButton.setBackground(new Color(79, 82, 221)); }
            public void mouseExited(MouseEvent e) { resetButton.setBackground(ACCENT); }
        });

        resetButton.addActionListener(e -> resetGame());
        bottomPanel.add(resetButton);

        return bottomPanel;
    }

    private void handlePlayerMove(int index) {
        if (game.isGameOver()) return;

        if (game.makeMove(index, TicTacToe.PLAYER)) {
            cells[index].setText("X");
            cells[index].setForeground(X_COLOR);
            cells[index].setBackground(CELL_COLOR);

            if (game.isGameOver()) {
                handleGameOver();
                return;
            }

            statusLabel.setText("AI is thinking...");
            statusLabel.setForeground(MUTED);
            disableBoard();

            // AI move with slight delay for effect
            Timer timer = new Timer(500, e -> {
                int aiMove = game.getBestMove();
                game.makeMove(aiMove, TicTacToe.AI);
                cells[aiMove].setText("O");
                cells[aiMove].setForeground(O_COLOR);

                if (game.isGameOver()) {
                    handleGameOver();
                } else {
                    enableBoard();
                    statusLabel.setText("Your turn! Click a cell to play.");
                    statusLabel.setForeground(TEXT_COLOR);
                }
            });
            timer.setRepeats(false);
            timer.start();
        }
    }

    private void handleGameOver() {
        char winner = game.checkWinner();
        int[] winCombo = game.getWinningCombo();

        if (winner == TicTacToe.PLAYER) {
            playerScore++;
            statusLabel.setText("You won! Congratulations! 🎉");
            statusLabel.setForeground(WIN_COLOR);
            highlightWinningCells(winCombo, X_COLOR);
            updateScores();
        } else if (winner == TicTacToe.AI) {
            aiScore++;
            statusLabel.setText("AI wins! Better luck next time. 🤖");
            statusLabel.setForeground(O_COLOR);
            highlightWinningCells(winCombo, O_COLOR);
            updateScores();
        } else {
            draws++;
            statusLabel.setText("It's a draw! Well played. 🤝");
            statusLabel.setForeground(new Color(234, 179, 8));
            updateScores();
        }
        disableBoard();
    }

    private void highlightWinningCells(int[] combo, Color color) {
        if (combo == null) return;
        for (int i : combo) {
            cells[i].setBackground(new Color(color.getRed(), color.getGreen(), color.getBlue(), 80));
            cells[i].setBackground(new Color(40, 60, 40));
            cells[i].setBorder(BorderFactory.createLineBorder(color, 3, true));
        }
    }

    private void updateScores() {
        // Find and update score labels
        for (Component c : ((JPanel)((JPanel)getContentPane().getComponent(1)).getComponent(0)).getComponents()) {
            JPanel card = (JPanel) c;
            for (Component comp : card.getComponents()) {
                if (comp instanceof JLabel) {
                    JLabel label = (JLabel) comp;
                    if ("playerScore".equals(label.getName())) label.setText(String.valueOf(playerScore));
                    if ("aiScore".equals(label.getName())) label.setText(String.valueOf(aiScore));
                    if ("draws".equals(label.getName())) label.setText(String.valueOf(draws));
                }
            }
        }
    }

    private void disableBoard() {
        for (JButton cell : cells) cell.setEnabled(false);
    }

    private void enableBoard() {
        for (int i = 0; i < 9; i++) {
            if (cells[i].getText().isEmpty()) cells[i].setEnabled(true);
        }
    }

    private void resetGame() {
        game.resetBoard();
        for (JButton cell : cells) {
            cell.setText("");
            cell.setEnabled(true);
            cell.setBackground(CELL_COLOR);
            cell.setForeground(TEXT_COLOR);
            cell.setBorder(BorderFactory.createLineBorder(new Color(50, 50, 75), 2, true));
        }
        statusLabel.setText("Your turn! Click a cell to play.");
        statusLabel.setForeground(TEXT_COLOR);
    }

    public static void main(String[] args) {
        try {
            UIManager.setLookAndFeel(UIManager.getCrossPlatformLookAndFeelClassName());
        } catch (Exception e) {
            e.printStackTrace();
        }
        SwingUtilities.invokeLater(() -> new TicTacToeGUI());
    }
}
