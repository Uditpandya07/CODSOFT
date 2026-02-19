import javax.swing.*;
import javax.swing.border.*;
import java.awt.*;
import java.awt.event.*;
import java.text.SimpleDateFormat;
import java.util.Date;

public class ChatBotGUI extends JFrame {

    private JTextPane chatArea;
    private JTextField inputField;
    private JButton sendButton;
    private ChatBot bot;
    private StringBuilder chatContent;

    // Colors
    private final Color BG_COLOR = new Color(18, 18, 28);
    private final Color SIDEBAR_COLOR = new Color(26, 26, 40);
    private final Color USER_BUBBLE = new Color(99, 102, 241);
    private final Color BOT_BUBBLE = new Color(36, 36, 56);
    private final Color INPUT_BG = new Color(30, 30, 46);
    private final Color ACCENT = new Color(99, 102, 241);
    private final Color TEXT_COLOR = new Color(229, 229, 229);
    private final Color MUTED = new Color(120, 120, 150);

    public ChatBotGUI() {
        bot = new ChatBot();
        chatContent = new StringBuilder();
        initUI();
    }

    private void initUI() {
        setTitle("Ninja — AI Chatbot");
        setSize(900, 650);
        setMinimumSize(new Dimension(700, 500));
        setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
        setLocationRelativeTo(null);
        setLayout(new BorderLayout());

        getContentPane().setBackground(BG_COLOR);

        // Sidebar
        JPanel sidebar = createSidebar();
        add(sidebar, BorderLayout.WEST);

        // Main chat area
        JPanel mainPanel = createMainPanel();
        add(mainPanel, BorderLayout.CENTER);

        setVisible(true);

        // Welcome message
        appendBotMessageHTML("Hey! I'm Ninja, your AI assistant 🥷 Here's what I can do:<br/><br/>" +
                "👋 <b>Greetings</b> — Say hi, good morning, good night<br/>" +
                "😄 <b>Jokes & Riddles</b> — Ask for a joke or riddle<br/>" +
                "🤖 <b>AI & Tech</b> — Ask about AI, ML, Python, Java, GitHub, Cloud<br/>" +
                "🕐 <b>Time & Date</b> — Ask current time or today's date<br/>" +
                "💡 <b>Fun Facts</b> — Space facts, animal facts, random facts<br/>" +
                "🎲 <b>Games</b> — Flip a coin, roll a dice, magic 8 ball<br/>" +
                "💼 <b>Career Advice</b> — Resume, interviews, career tips<br/>" +
                "🏋️ <b>Health & Wellness</b> — Fitness, diet, sleep, hydration<br/>" +
                "🧠 <b>Mental Health</b> — Stress, anxiety, confidence, loneliness<br/>" +
                "🎬 <b>Pop Culture</b> — Anime, Marvel, Netflix, Harry Potter<br/>" +
                "✈️ <b>Travel</b> — Destinations, vacation ideas<br/>" +
                "💪 <b>Motivation</b> — Quotes and inspiration<br/><br/>" +
                "Just type naturally and I'll do my best! 🚀");
    }

    private JPanel createSidebar() {
        JPanel sidebar = new JPanel();
        sidebar.setPreferredSize(new Dimension(220, 0));
        sidebar.setBackground(SIDEBAR_COLOR);
        sidebar.setLayout(new BorderLayout());
        sidebar.setBorder(BorderFactory.createMatteBorder(0, 0, 0, 1, new Color(40, 40, 60)));

        // Top section
        JPanel top = new JPanel();
        top.setBackground(SIDEBAR_COLOR);
        top.setLayout(new BoxLayout(top, BoxLayout.Y_AXIS));
        top.setBorder(new EmptyBorder(24, 16, 16, 16));

        // Bot avatar
        JLabel avatar = new JLabel("🤖");
        avatar.setFont(new Font("Segoe UI Emoji", Font.PLAIN, 40));
        avatar.setAlignmentX(Component.CENTER_ALIGNMENT);

        JLabel nameLabel = new JLabel("Ninja");
        nameLabel.setFont(new Font("Segoe UI", Font.BOLD, 18));
        nameLabel.setForeground(TEXT_COLOR);
        nameLabel.setAlignmentX(Component.CENTER_ALIGNMENT);

        JLabel statusLabel = new JLabel("● Online");
        statusLabel.setFont(new Font("Segoe UI", Font.PLAIN, 12));
        statusLabel.setForeground(new Color(74, 222, 128));
        statusLabel.setAlignmentX(Component.CENTER_ALIGNMENT);

        top.add(avatar);
        top.add(Box.createVerticalStrut(8));
        top.add(nameLabel);
        top.add(Box.createVerticalStrut(4));
        top.add(statusLabel);
        top.add(Box.createVerticalStrut(24));

        // Divider
        JSeparator sep = new JSeparator();
        sep.setForeground(new Color(50, 50, 70));
        top.add(sep);
        top.add(Box.createVerticalStrut(16));

        // Quick prompts label
        JLabel quickLabel = new JLabel("QUICK PROMPTS");
        quickLabel.setFont(new Font("Segoe UI", Font.BOLD, 10));
        quickLabel.setForeground(MUTED);
        quickLabel.setAlignmentX(Component.LEFT_ALIGNMENT);
        top.add(quickLabel);
        top.add(Box.createVerticalStrut(10));

        // Quick prompt buttons
        String[] prompts = {"👋 Say Hello", "😄 Tell a Joke", "💡 What is AI?", "🕐 Current Time", "💪 Motivate Me"};
        for (String prompt : prompts) {
            JButton btn = createSidebarButton(prompt);
            btn.setAlignmentX(Component.LEFT_ALIGNMENT);
            top.add(btn);
            top.add(Box.createVerticalStrut(6));
        }

        sidebar.add(top, BorderLayout.NORTH);

        // Bottom info
        JPanel bottom = new JPanel();
        bottom.setBackground(SIDEBAR_COLOR);
        bottom.setBorder(new EmptyBorder(12, 16, 16, 16));
        JLabel info = new JLabel("<html><center><font color='#787896' size='2'>CodSoft AI Internship<br/>Task 1 — Chatbot</font></center></html>");
        info.setHorizontalAlignment(SwingConstants.CENTER);
        bottom.add(info);
        sidebar.add(bottom, BorderLayout.SOUTH);

        return sidebar;
    }

    private JButton createSidebarButton(String text) {
        JButton btn = new JButton(text);
        btn.setFont(new Font("Segoe UI", Font.BOLD, 12));
        btn.setForeground(Color.WHITE);
        btn.setBackground(new Color(99, 102, 241));
        btn.setBorder(BorderFactory.createCompoundBorder(
                BorderFactory.createLineBorder(new Color(120, 122, 255), 1, true),
                new EmptyBorder(8, 12, 8, 12)
        ));
        btn.setCursor(new Cursor(Cursor.HAND_CURSOR));
        btn.setFocusPainted(false);
        btn.setOpaque(true);
        btn.setContentAreaFilled(true);
        btn.setMaximumSize(new Dimension(Integer.MAX_VALUE, 36));

        btn.addMouseListener(new MouseAdapter() {
            public void mouseEntered(MouseEvent e) { btn.setBackground(new Color(79, 82, 221)); }
            public void mouseExited(MouseEvent e) { btn.setBackground(new Color(99, 102, 241)); }
        });

        btn.addActionListener(e -> {
            String msg = text.substring(2).trim(); // remove emoji
            inputField.setText(msg);
            sendMessage();
        });

        return btn;
    }

    private JPanel createMainPanel() {
        JPanel mainPanel = new JPanel(new BorderLayout());
        mainPanel.setBackground(BG_COLOR);

        // Header
        JPanel header = new JPanel(new BorderLayout());
        header.setBackground(SIDEBAR_COLOR);
        header.setBorder(new EmptyBorder(14, 20, 14, 20));
        header.setBorder(BorderFactory.createCompoundBorder(
                BorderFactory.createMatteBorder(0, 0, 1, 0, new Color(40, 40, 60)),
                new EmptyBorder(14, 20, 14, 20)
        ));

        JLabel headerTitle = new JLabel("Chat with Ninja");
        headerTitle.setFont(new Font("Segoe UI", Font.BOLD, 16));
        headerTitle.setForeground(TEXT_COLOR);

        JLabel headerSub = new JLabel("Rule-Based AI Chatbot");
        headerSub.setFont(new Font("Segoe UI", Font.PLAIN, 12));
        headerSub.setForeground(MUTED);

        JPanel headerText = new JPanel();
        headerText.setBackground(SIDEBAR_COLOR);
        headerText.setLayout(new BoxLayout(headerText, BoxLayout.Y_AXIS));
        headerText.add(headerTitle);
        headerText.add(headerSub);

        header.add(headerText, BorderLayout.WEST);

        // Clear button
        JButton clearBtn = new JButton("Clear Chat");
        clearBtn.setFont(new Font("Segoe UI", Font.PLAIN, 12));
        clearBtn.setForeground(MUTED);
        clearBtn.setBackground(SIDEBAR_COLOR);
        clearBtn.setBorderPainted(false);
        clearBtn.setFocusPainted(false);
        clearBtn.setCursor(new Cursor(Cursor.HAND_CURSOR));
        clearBtn.addActionListener(e -> {
            chatArea.setText("");
            chatContent = new StringBuilder();
            appendBotMessage("Chat cleared! What would you like to talk about?");
        });
        header.add(clearBtn, BorderLayout.EAST);

        mainPanel.add(header, BorderLayout.NORTH);

        // Chat area
        chatArea = new JTextPane();
        chatArea.setContentType("text/html");
        chatArea.setEditable(false);
        chatArea.setBackground(BG_COLOR);
        chatArea.setBorder(new EmptyBorder(10, 10, 10, 10));

        JScrollPane scrollPane = new JScrollPane(chatArea);
        scrollPane.setBackground(BG_COLOR);
        scrollPane.getViewport().setBackground(BG_COLOR);
        scrollPane.setBorder(BorderFactory.createEmptyBorder());
        scrollPane.setVerticalScrollBarPolicy(JScrollPane.VERTICAL_SCROLLBAR_AS_NEEDED);

        mainPanel.add(scrollPane, BorderLayout.CENTER);

        // Input area
        JPanel inputPanel = new JPanel(new BorderLayout(10, 0));
        inputPanel.setBackground(SIDEBAR_COLOR);
        inputPanel.setBorder(BorderFactory.createCompoundBorder(
                BorderFactory.createMatteBorder(1, 0, 0, 0, new Color(40, 40, 60)),
                new EmptyBorder(14, 20, 14, 20)
        ));

        inputField = new JTextField();
        inputField.setFont(new Font("Segoe UI", Font.PLAIN, 14));
        inputField.setBackground(INPUT_BG);
        inputField.setForeground(TEXT_COLOR);
        inputField.setCaretColor(TEXT_COLOR);
        inputField.setBorder(BorderFactory.createCompoundBorder(
                BorderFactory.createLineBorder(new Color(60, 60, 90), 1, true),
                new EmptyBorder(10, 14, 10, 14)
        ));

        inputField.addActionListener(e -> sendMessage());

        sendButton = new JButton("Send ➤");
        sendButton.setFont(new Font("Segoe UI", Font.BOLD, 13));
        sendButton.setBackground(ACCENT);
        sendButton.setForeground(Color.WHITE);
        sendButton.setBorderPainted(false);
        sendButton.setFocusPainted(false);
        sendButton.setCursor(new Cursor(Cursor.HAND_CURSOR));
        sendButton.setPreferredSize(new Dimension(100, 42));

        sendButton.addMouseListener(new MouseAdapter() {
            public void mouseEntered(MouseEvent e) { sendButton.setBackground(new Color(79, 82, 221)); }
            public void mouseExited(MouseEvent e) { sendButton.setBackground(ACCENT); }
        });

        sendButton.addActionListener(e -> sendMessage());

        inputPanel.add(inputField, BorderLayout.CENTER);
        inputPanel.add(sendButton, BorderLayout.EAST);

        mainPanel.add(inputPanel, BorderLayout.SOUTH);

        return mainPanel;
    }

    private void sendMessage() {
        String userText = inputField.getText().trim();
        if (userText.isEmpty()) return;

        appendUserMessage(userText);
        inputField.setText("");

        // Simulate slight delay for realism
        Timer timer = new Timer(400, e -> {
            String response = bot.getResponse(userText);
            appendBotMessage(response);
        });
        timer.setRepeats(false);
        timer.start();
    }

    private void appendUserMessage(String message) {
        String time = new SimpleDateFormat("hh:mm a").format(new Date());
        chatContent.append(
                "<div style='text-align:right; margin: 10px 0;'>" +
                        "<span style='font-size:11px; color:#787896;'>You · " + time + "</span><br/>" +
                        "<span style='background:#6366f1; color:#ffffff; padding:10px 14px; border-radius:18px 18px 4px 18px; display:inline-block; max-width:70%; font-family:Segoe UI; font-size:13px;'>" +
                        escapeHtml(message) + "</span></div>"
        );
        updateChat();
    }

    private void appendBotMessageHTML(String message) {
        String time = new SimpleDateFormat("hh:mm a").format(new Date());
        chatContent.append(
                "<div style='text-align:left; margin: 10px 0;'>" +
                        "<span style='font-size:11px; color:#787896;'>Ninja · " + time + "</span><br/>" +
                        "<span style='background:#24243A; color:#e5e5e5; padding:10px 14px; border-radius:18px 18px 18px 4px; display:inline-block; max-width:70%; font-family:Segoe UI; font-size:13px;'>" +
                        message + "</span></div>"
        );
        updateChat();
    }

    private void appendBotMessage(String message) {
        String time = new SimpleDateFormat("hh:mm a").format(new Date());
        chatContent.append(
                "<div style='text-align:left; margin: 10px 0;'>" +
                        "<span style='font-size:11px; color:#787896;'>Ninja · " + time + "</span><br/>" +
                        "<span style='background:#24243A; color:#e5e5e5; padding:10px 14px; border-radius:18px 18px 18px 4px; display:inline-block; max-width:70%; font-family:Segoe UI; font-size:13px;'>" +
                        escapeHtml(message) + "</span></div>"
        );
        updateChat();
    }

    private void updateChat() {
        String html = "<html><body style='background:#12121c; padding:10px; font-family:Segoe UI;'>" +
                chatContent.toString() + "</body></html>";
        chatArea.setText(html);
        chatArea.setCaretPosition(chatArea.getDocument().getLength());
    }

    private String escapeHtml(String text) {
        return text.replace("&", "&amp;")
                .replace("<", "&lt;")
                .replace(">", "&gt;")
                .replace("\"", "&quot;")
                .replace("\n", "<br/>");
    }

    public static void main(String[] args) {
        try {
            UIManager.setLookAndFeel(UIManager.getCrossPlatformLookAndFeelClassName());
        } catch (Exception e) {
            e.printStackTrace();
        }

        SwingUtilities.invokeLater(() -> new ChatBotGUI());
    }
}