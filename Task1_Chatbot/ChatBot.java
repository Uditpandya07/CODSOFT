import java.util.*;
import java.util.regex.*;

public class ChatBot {

    private String botName = "Ninja";
    private Map<String[], String> rules;

    public ChatBot() {
        rules = new LinkedHashMap<>();
        loadRules();
    }

    private void loadRules() {

        // Greetings
        rules.put(new String[]{"hello", "hi", "hey", "howdy", "hiya"},
                "Hey there! I'm Ninja, your AI assistant. What's on your mind?");

        rules.put(new String[]{"good morning"},
                "Good morning! Hope you're having a great start to your day. How can I help?");

        rules.put(new String[]{"good night", "goodnight"},
                "Good night! Get some rest. I'll be here whenever you need me.");

        rules.put(new String[]{"good evening"},
                "Good evening! How's your day been? What can I do for you?");

        // How are you
        rules.put(new String[]{"how are you", "how r you", "how are u", "hows it going", "how's it going", "what's up", "whats up"},
                "I'm doing great, thanks for asking! Ready to help you out. What do you need?");

        // Name
        rules.put(new String[]{"what is your name", "what's your name", "who are you", "your name"},
                "I'm Ninja — a rule-based chatbot built for the CodSoft AI internship. Nice to meet you!");

        rules.put(new String[]{"your age", "how old are you"},
                "Age is just a number, but I was coded pretty recently! Does that count?");

        // Creator
        rules.put(new String[]{"who made you", "who created you", "who built you", "who coded you"},
                "I was built as part of the CodSoft AI internship project. A human wrote my rules, but hey — I do the talking!");

        // Weather
        rules.put(new String[]{"weather", "temperature", "forecast"},
                "I wish I could check the weather for you, but I don't have internet access. Try weather.com or just look outside!");

        // Time
        rules.put(new String[]{"time", "what time is it", "current time"},
                "Current time is: " + new java.util.Date().toString().substring(11, 16) + ". Hope that helps!");

        // Date
        rules.put(new String[]{"date", "what is today", "today's date", "what day is it"},
                "Today is: " + new java.util.Date().toString().substring(0, 10) + ".");

        // Help
        rules.put(new String[]{"help", "what can you do", "features", "capabilities", "commands", "list"},
                "Here's everything I can help with:\n\n" +
                        "👋 Greetings — hi, good morning, good night\n" +
                        "😄 Jokes & Riddles — ask for a joke or riddle\n" +
                        "🤖 AI & Tech — AI, ML, Python, Java, GitHub, Cloud, Crypto\n" +
                        "🕐 Time & Date — current time, today's date\n" +
                        "💡 Fun Facts — space, animals, random facts\n" +
                        "🎲 Games — flip a coin, roll a dice, magic 8 ball\n" +
                        "💼 Career — resume tips, interview advice\n" +
                        "🏋️ Health — fitness, diet, sleep, hydration\n" +
                        "🧠 Mental Health — stress, anxiety, confidence\n" +
                        "🎬 Pop Culture — anime, Marvel, Netflix\n" +
                        "✈️ Travel — destinations, vacation ideas\n" +
                        "💪 Motivation — quotes and inspiration\n\n" +
                        "Just type naturally — I'll figure it out!");

        // Jokes
        rules.put(new String[]{"joke", "tell me a joke", "make me laugh", "funny"},
                "Why do programmers prefer dark mode? Because light attracts bugs! 😄");

        rules.put(new String[]{"another joke", "more jokes", "one more joke"},
                "Why did the AI break up with the internet? Too many bad connections. 😂");

        // AI / Tech topics
        rules.put(new String[]{"what is ai", "artificial intelligence", "explain ai"},
                "Artificial Intelligence is the simulation of human intelligence in machines. It includes things like learning, reasoning, and problem solving. Pretty cool stuff — and I'm a tiny part of it!");

        rules.put(new String[]{"machine learning", "what is ml", "explain ml"},
                "Machine Learning is a subset of AI where systems learn from data instead of being explicitly programmed. Think of it as teaching a computer by example!");

        rules.put(new String[]{"deep learning", "neural network"},
                "Deep Learning uses artificial neural networks with many layers to learn complex patterns. It's the tech behind image recognition, voice assistants, and more!");

        rules.put(new String[]{"python", "java", "programming"},
                "Great topic! Python is king for AI/ML, while Java is fantastic for building robust, scalable applications. Both have their strengths!");

        // Feelings
        rules.put(new String[]{"i am sad", "i'm sad", "feeling sad", "i feel sad", "depressed"},
                "I'm sorry to hear that. It's okay to have tough days. Take a deep breath — things will get better. Is there anything I can do to help?");

        rules.put(new String[]{"i am happy", "i'm happy", "feeling great", "i feel good"},
                "That's amazing! Happiness looks good on you. What's making you smile today?");

        rules.put(new String[]{"i am bored", "i'm bored", "bored"},
                "Boredom is just creativity waiting to happen! Want a fun fact, a joke, or maybe just a good chat?");

        rules.put(new String[]{"i am tired", "i'm tired", "feeling tired", "exhausted"},
                "Rest is important! Don't overwork yourself. Take a break, grab some water, and recharge.");

        // Compliments
        rules.put(new String[]{"you are great", "you're great", "good bot", "nice bot", "you are awesome", "you're awesome"},
                "Aw, thank you! That genuinely made my day. You're pretty great yourself!");

        rules.put(new String[]{"you are bad", "you're bad", "you're terrible", "bad bot"},
                "Ouch! I'll try to do better. Let me know what I can improve on.");

        // Thanks
        rules.put(new String[]{"thank you", "thanks", "thank u", "thx", "ty"},
                "You're very welcome! Always happy to help.");

        // Food
        rules.put(new String[]{"food", "hungry", "eat", "pizza", "burger"},
                "I can't eat, but if I could, I'd go for pizza every single time. What's your favorite food?");

        // Music
        rules.put(new String[]{"music", "song", "favorite song"},
                "I don't have ears, but I've heard that music is good for the soul! What genre do you like?");

        // Sports
        rules.put(new String[]{"cricket", "football", "sports", "game"},
                "Sports are awesome! The teamwork, the strategy — love it. Do you play any sports?");

        // Study
        rules.put(new String[]{"study", "exam", "college", "university", "school"},
                "Studies can be tough but they're so worth it in the end. What subject are you working on?");

        // Internship
        rules.put(new String[]{"internship", "codsoft", "codesoft"},
                "CodSoft runs a great internship program! This very chatbot is one of the tasks. Meta, right?");

        // Motivational
        rules.put(new String[]{"motivate me", "motivation", "inspire me", "quote"},
                "Here's one: 'The expert in anything was once a beginner.' Keep going — you're doing better than you think!");

        // Age / personal
        rules.put(new String[]{"how old", "your age"},
                "Age is just a number! I was born the moment someone hit 'Run'. So pretty young I'd say.");

        // Favorite things
        rules.put(new String[]{"favorite color", "favourite color"},
                "Definitely black. I mean, look at this theme.");
        rules.put(new String[]{"favorite movie", "favourite movie"},
                "I'd say 'Ex Machina' — it really speaks to me on a personal level. For obvious reasons.");
        rules.put(new String[]{"favorite book", "favourite book"},
                "Anything by Alan Turing counts, right? The man basically invented my existence.");

        // Facts
        rules.put(new String[]{"fun fact", "tell me a fact", "random fact", "fact"},
                "Fun fact: Honey never spoils. Archaeologists found 3000-year-old honey in Egyptian tombs and it was still perfectly fine!");
        rules.put(new String[]{"science fact", "space fact", "space"},
                "Space fact: A day on Venus is longer than a year on Venus. It rotates so slowly that the Sun rises only once every 243 Earth days!");
        rules.put(new String[]{"animal fact", "animals"},
                "Did you know otters hold hands while sleeping so they don't drift apart? Possibly the cutest thing in nature.");

        // Riddles
        rules.put(new String[]{"riddle", "give me a riddle", "ask me a riddle"},
                "Here's one: I speak without a mouth and hear without ears. I have no body, but I come alive with the wind. What am I? (An echo!)");

        // Math
        rules.put(new String[]{"what is 2+2", "2 + 2", "2+2"}, "That's 4. Easy one!");
        rules.put(new String[]{"math", "calculate", "solve"},
                "I'm not a calculator, but I can help with basic stuff! Try typing something like '2+2'.");

        // Career advice
        rules.put(new String[]{"career", "job", "career advice", "future"},
                "My advice? Build projects, not just theory. A GitHub full of real work speaks louder than any certificate.");
        rules.put(new String[]{"resume", "cv"},
                "Keep your resume clean, one page if possible, and tailor it for every job. Quantify your achievements — numbers stand out!");
        rules.put(new String[]{"interview", "job interview"},
                "Prep well, research the company, and always have a question ready for them. Confidence matters as much as skill!");

        // Health
        rules.put(new String[]{"health", "fitness", "workout", "exercise", "gym"},
                "Consistency beats intensity! Even a 20-minute walk daily makes a huge difference over time. How's your routine going?");
        rules.put(new String[]{"diet", "eating healthy", "nutrition"},
                "Eat real food, not too much, mostly plants. Michael Pollan said that and honestly it's solid advice.");
        rules.put(new String[]{"sleep", "insomnia", "can't sleep"},
                "Sleep is seriously underrated! 7-8 hours is ideal. Try keeping a consistent bedtime — even on weekends.");
        rules.put(new String[]{"water", "drink water", "hydration"},
                "Drink more water! Most people are chronically dehydrated and don't even realize it. Aim for 2-3 liters a day.");

        // Mental health
        rules.put(new String[]{"anxiety", "stressed", "stress", "overwhelmed"},
                "Take a breath. Seriously — slow, deep breaths activate your parasympathetic nervous system and calm you down fast. You've got this.");
        rules.put(new String[]{"lonely", "alone", "no friends"},
                "I'm here to chat! But also — loneliness is really common and nothing to be ashamed of. Reaching out to even one person can help a lot.");
        rules.put(new String[]{"confidence", "self esteem", "believe in myself"},
                "Start small — do one thing every day that scares you a little. Confidence is built through action, not waiting to feel ready.");

        // Technology
        rules.put(new String[]{"chatgpt", "gpt", "openai"},
                "Ah, my famous cousin! ChatGPT is powered by GPT models from OpenAI. I'm a bit simpler — rule-based — but hey, I'm honest about it!");
        rules.put(new String[]{"robot", "robots"},
                "Robots are fascinating! From industrial arms to Boston Dynamics' parkour bots — we've come a long way. Excited or scared?");
        rules.put(new String[]{"blockchain", "crypto", "bitcoin"},
                "Crypto is volatile, interesting, and polarizing all at once. The blockchain tech behind it though? Genuinely revolutionary for certain use cases.");
        rules.put(new String[]{"cybersecurity", "hacking", "security"},
                "Cybersecurity is one of the most in-demand fields right now. Ethical hacking, penetration testing — super exciting and well-paying careers!");
        rules.put(new String[]{"cloud", "aws", "azure", "google cloud"},
                "Cloud computing is the backbone of modern tech! AWS, Azure, and GCP are the big three. Learning any of them is a great career move.");
        rules.put(new String[]{"github", "git", "version control"},
                "Git is essential! If you're not using version control, you're living dangerously. GitHub is also great for showcasing your projects to recruiters.");

        // Pop culture
        rules.put(new String[]{"marvel", "avengers", "superhero"},
                "Marvel fan? Iron Man's JARVIS is literally what every AI aspires to be. Minus the flying suits, sadly.");
        rules.put(new String[]{"harry potter"},
                "Accio knowledge! I'd be sorted into Ravenclaw for sure — logic and learning all day.");
        rules.put(new String[]{"netflix", "series", "show", "web series"},
                "Binge-watching? I respect the commitment. 'Black Mirror' hits different when you're talking to an AI though, just saying.");
        rules.put(new String[]{"anime"},
                "Anime fan? Nice! Attack on Titan for the strategy, Steins;Gate for the sci-fi mind-bending stuff. Solid taste.");

        // Travel
        rules.put(new String[]{"travel", "vacation", "trip", "holiday"},
                "Travel broadens the mind! Even a weekend trip to somewhere new can completely reset your perspective. Where do you want to go?");
        rules.put(new String[]{"india", "indian"},
                "India — incredible culture, food, and diversity! From the Himalayas to Kerala's backwaters, it's a whole world in one country.");

        // Random fun
        rules.put(new String[]{"flip a coin", "heads or tails", "coin"},
                Math.random() > 0.5 ? "I flipped it... HEADS!" : "I flipped it... TAILS!");
        rules.put(new String[]{"roll a dice", "roll dice", "dice"},
                "You rolled a... " + (int)(Math.random() * 6 + 1) + "! 🎲");
        rules.put(new String[]{"magic 8 ball", "8 ball", "will i"},
                new String[]{"Signs point to yes!", "Outlook not so good.", "Most likely!", "Ask again later.", "Without a doubt!"}[(int)(Math.random()*5)]);
        rules.put(new String[]{"pick a number", "random number", "guess a number"},
                "I'm thinking of... " + (int)(Math.random() * 100 + 1) + "! Was that what you had in mind?");

        // Compliment the user
        rules.put(new String[]{"am i smart", "am i good", "am i talented"},
                "The fact that you're curious enough to ask means you probably are. Smart people question themselves — it's a good sign!");
        rules.put(new String[]{"roast me", "make fun of me"},
                "You're talking to a chatbot at this hour. I think that says enough. (Just kidding — you're great!)");

        // Goodbye
        rules.put(new String[]{"bye", "goodbye", "see you", "exit", "quit", "later", "take care"},
                "Goodbye! It was great chatting with you. Come back anytime 👋");

        // Default handled separately
    }

    public String getResponse(String userInput) {
        String input = userInput.toLowerCase().trim();

        for (Map.Entry<String[], String> entry : rules.entrySet()) {
            for (String keyword : entry.getKey()) {
                if (input.contains(keyword)) {
                    return entry.getValue();
                }
            }
        }

        // Fallback responses
        String[] fallbacks = {
                "Hmm, I'm not sure about that one. Could you rephrase?",
                "Interesting! I don't have a good answer for that yet.",
                "That's a bit outside what I know right now. Try asking something else?",
                "I'm still learning! That one stumped me.",
                "Not sure I follow — could you say that differently?"
        };

        Random rand = new Random();
        return fallbacks[rand.nextInt(fallbacks.length)];
    }

    public String getBotName() {
        return botName;
    }
}