import tkinter as tk
from tkinter import ttk
import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import requests, zipfile, os, io, threading

# ── Colors ──────────────────────────────────
BG      = "#0d0d1a"
PANEL   = "#13132b"
CARD    = "#1a1a35"
CELL    = "#1e1e3f"
ACCENT  = "#6366f1"
ACCENT2 = "#4f52dd"
TEXT    = "#f0f0ff"
MUTED   = "#6b7280"
SUBTLE  = "#374151"
GREEN   = "#22c55e"
RED     = "#ef4444"
BORDER  = "#2a2a50"
YELLOW  = "#f59e0b"
STAR_ON = "#fbbf24"
STAR_OFF= "#2a2a50"
PINK    = "#ec4899"
PINK2   = "#be185d"

# ─────────────────────────────────────────────
#  Bollywood Data
# ─────────────────────────────────────────────
BOLLYWOOD_DATA = [
    ("Dilwale Dulhania Le Jayenge", 1995, "Romance|Drama", 4.8, 95000),
    ("3 Idiots", 2009, "Comedy|Drama", 4.9, 120000),
    ("Lagaan", 2001, "Drama|Sport", 4.7, 60000),
    ("Dangal", 2016, "Drama|Sport|Biography", 4.9, 130000),
    ("PK", 2014, "Comedy|Drama|Sci-Fi", 4.7, 110000),
    ("Dil Chahta Hai", 2001, "Comedy|Drama|Romance", 4.7, 70000),
    ("Kabhi Khushi Kabhie Gham", 2001, "Drama|Romance|Family", 4.5, 75000),
    ("Kal Ho Naa Ho", 2003, "Drama|Romance", 4.6, 80000),
    ("Taare Zameen Par", 2007, "Drama|Family", 4.8, 90000),
    ("Rang De Basanti", 2006, "Drama|Action", 4.8, 85000),
    ("Swades", 2004, "Drama", 4.7, 55000),
    ("Chak De! India", 2007, "Drama|Sport", 4.7, 80000),
    ("Mughal-E-Azam", 1960, "Drama|Romance|History", 4.6, 40000),
    ("Sholay", 1975, "Action|Adventure|Drama", 4.9, 85000),
    ("Deewar", 1975, "Action|Drama|Crime", 4.7, 50000),
    ("Zindagi Na Milegi Dobara", 2011, "Adventure|Drama|Romance", 4.8, 95000),
    ("Queen", 2014, "Drama|Comedy", 4.7, 70000),
    ("Gangs of Wasseypur", 2012, "Crime|Action|Drama", 4.8, 75000),
    ("Andhadhun", 2018, "Thriller|Crime|Drama", 4.8, 100000),
    ("Article 15", 2019, "Drama|Crime|Thriller", 4.6, 60000),
    ("Tumbbad", 2018, "Horror|Fantasy|Drama", 4.7, 55000),
    ("Masaan", 2015, "Drama|Romance", 4.6, 45000),
    ("Udta Punjab", 2016, "Drama|Crime", 4.5, 50000),
    ("Dil Dhadakne Do", 2015, "Drama|Comedy|Family", 4.4, 65000),
    ("Bajrangi Bhaijaan", 2015, "Drama|Adventure", 4.7, 110000),
    ("Sultan", 2016, "Drama|Sport|Action", 4.5, 90000),
    ("Tiger Zinda Hai", 2017, "Action|Thriller", 4.3, 80000),
    ("War", 2019, "Action|Thriller", 4.3, 85000),
    ("Pathaan", 2023, "Action|Thriller", 4.2, 90000),
    ("Jawan", 2023, "Action|Thriller|Drama", 4.4, 95000),
    ("Animal", 2023, "Action|Drama|Crime", 4.1, 88000),
    ("Stree", 2018, "Horror|Comedy", 4.5, 80000),
    ("Bhediya", 2022, "Horror|Comedy", 4.2, 60000),
    ("Shershaah", 2021, "Action|Drama|Biography", 4.7, 100000),
    ("URI: The Surgical Strike", 2019, "Action|War|Drama", 4.6, 95000),
    ("Raazi", 2018, "Thriller|Drama|War", 4.6, 75000),
    ("Gunjan Saxena", 2020, "Drama|Biography", 4.5, 60000),
    ("Thappad", 2020, "Drama", 4.5, 55000),
    ("Kapoor & Sons", 2016, "Drama|Family", 4.5, 65000),
    ("Wake Up Sid", 2009, "Drama|Romance|Comedy", 4.5, 60000),
    ("Yeh Jawaani Hai Deewani", 2013, "Romance|Drama|Comedy", 4.5, 90000),
    ("Ae Dil Hai Mushkil", 2016, "Romance|Drama", 4.2, 70000),
    ("Tamasha", 2015, "Drama|Romance", 4.3, 65000),
    ("Rockstar", 2011, "Drama|Romance|Music", 4.5, 70000),
    ("Jab We Met", 2007, "Romance|Comedy|Drama", 4.7, 85000),
    ("Veer Zaara", 2004, "Romance|Drama", 4.6, 70000),
    ("Devdas", 2002, "Drama|Romance", 4.4, 55000),
    ("Black", 2005, "Drama", 4.6, 60000),
    ("Barfi!", 2012, "Comedy|Drama|Romance", 4.7, 80000),
    ("Kahaani", 2012, "Thriller|Mystery|Drama", 4.7, 70000),
    ("Piku", 2015, "Comedy|Drama", 4.6, 70000),
    ("Pink", 2016, "Drama|Thriller", 4.7, 75000),
    ("Badla", 2019, "Thriller|Mystery", 4.5, 65000),
    ("Drishyam", 2015, "Thriller|Drama|Crime", 4.7, 80000),
    ("A Wednesday", 2008, "Thriller|Drama", 4.7, 65000),
    ("Special 26", 2013, "Crime|Thriller", 4.5, 60000),
    ("Fukrey", 2013, "Comedy|Crime", 4.5, 65000),
    ("Delhi Belly", 2011, "Comedy|Crime", 4.4, 60000),
    ("Go Goa Gone", 2013, "Comedy|Horror", 4.3, 55000),
    ("Badlapur", 2015, "Thriller|Drama|Action", 4.5, 60000),
    ("Newton", 2017, "Drama|Comedy", 4.5, 50000),
    ("Lunchbox", 2013, "Drama|Romance", 4.6, 60000),
    ("Gully Boy", 2019, "Drama|Music|Biography", 4.5, 80000),
    ("Sanju", 2018, "Biography|Drama", 4.3, 85000),
    ("Scam 1992", 2020, "Drama|Biography|Crime", 4.9, 110000),
    ("Panchayat", 2020, "Comedy|Drama", 4.8, 95000),
    ("Mirzapur", 2018, "Crime|Action|Drama", 4.6, 100000),
    ("Sacred Games", 2018, "Crime|Thriller|Drama", 4.5, 90000),
    ("Kuch Kuch Hota Hai", 1998, "Romance|Drama|Comedy", 4.6, 85000),
    ("My Name Is Khan", 2010, "Drama", 4.5, 75000),
    ("Jodhaa Akbar", 2008, "Drama|Romance|History", 4.5, 65000),
    ("Don", 2006, "Action|Thriller|Crime", 4.4, 70000),
    ("Dhoom", 2004, "Action|Thriller", 4.3, 70000),
    ("Baazigar", 1993, "Thriller|Romance|Drama", 4.5, 55000),
    ("Krrish", 2006, "Action|Sci-Fi|Romance", 4.2, 65000),
    ("Bombay", 1995, "Drama|Romance", 4.6, 50000),
    ("Roja", 1992, "Drama|Romance|Thriller", 4.6, 45000),
    ("Guru", 2007, "Drama|Biography", 4.5, 55000),
    ("Super 30", 2019, "Drama|Biography", 4.4, 75000),
    ("Uri: The Surgical Strike", 2019, "Action|War|Drama", 4.6, 95000),
    ("Aspirants", 2021, "Drama|Comedy", 4.8, 80000),
    ("Kota Factory", 2019, "Drama", 4.7, 75000),
    ("Paatal Lok", 2020, "Crime|Thriller|Drama", 4.6, 75000),
    ("Delhi Crime", 2019, "Crime|Drama|Thriller", 4.6, 70000),
]


# ─────────────────────────────────────────────
#  Engine
# ─────────────────────────────────────────────
class Engine:
    def __init__(self):
        self.all_movies = None
        self.hollywood  = None
        self.bollywood  = None
        self.cosine_sim = None
        self.indices    = None
        self.ratings_df = None

    def load(self, cb):
        movies_path  = "ml-latest-small/movies.csv"
        ratings_path = "ml-latest-small/ratings.csv"

        if not os.path.exists(movies_path):
            cb("Downloading MovieLens dataset (~3MB)...")
            r = requests.get(
                "https://files.grouplens.org/datasets/movielens/ml-latest-small.zip",
                timeout=30)
            zipfile.ZipFile(io.BytesIO(r.content)).extractall(".")

        cb("Loading Hollywood data...")
        hw = pd.read_csv(movies_path)
        self.ratings_df = pd.read_csv(ratings_path)

        hw["year"] = hw["title"].str.extract(r'\((\d{4})\)$')
        hw["clean_title"] = hw["title"].str.replace(
            r'\s*\(\d{4}\)', '', regex=True).str.strip()
        hw["genres_str"] = hw["genres"].str.replace("|", " ", regex=False)

        stats = self.ratings_df.groupby("movieId").agg(
            avg_rating=("rating", "mean"),
            num_ratings=("rating", "count")
        ).reset_index()
        hw = hw.merge(stats, on="movieId", how="left")
        hw["avg_rating"]  = hw["avg_rating"].round(1).fillna(0)
        hw["num_ratings"] = hw["num_ratings"].fillna(0).astype(int)
        hw["source"] = "Hollywood"
        self.hollywood = hw

        cb("Loading Bollywood data...")
        bw_rows = []
        for i, (title, year, genres, rating, n_ratings) in enumerate(BOLLYWOOD_DATA):
            bw_rows.append({
                "movieId": 900000 + i,
                "clean_title": title,
                "title": f"{title} ({year})",
                "year": str(year),
                "genres": genres,
                "genres_str": genres.replace("|", " "),
                "avg_rating": rating,
                "num_ratings": n_ratings,
                "source": "Bollywood"
            })
        self.bollywood = pd.DataFrame(bw_rows)

        cb("Building similarity matrix...")
        cols = ["movieId","clean_title","title","year",
                "genres","genres_str","avg_rating","num_ratings","source"]
        self.all_movies = pd.concat(
            [self.hollywood[cols], self.bollywood[cols]], ignore_index=True)

        tfidf = TfidfVectorizer(stop_words="english")
        mat   = tfidf.fit_transform(self.all_movies["genres_str"])
        self.cosine_sim = cosine_similarity(mat, mat)
        self.indices = pd.Series(
            self.all_movies.index,
            index=self.all_movies["clean_title"].str.lower()
        ).drop_duplicates()
        cb("Ready!")

    def recommend(self, title, n=12):
        key = title.lower().strip()
        if key not in self.indices:
            matches = [k for k in self.indices.index if key in k]
            if not matches:
                return None, f"'{title}' not found."
            key = matches[0]
        idx = self.indices[key]
        scores = sorted(enumerate(self.cosine_sim[idx]),
                        key=lambda x: x[1], reverse=True)[1:n+1]
        res = self.all_movies.iloc[[i for i, _ in scores]].copy()
        res["similarity"] = [round(s*100) for _, s in scores]
        return res, None

    def search(self, query, n=12):
        q = query.lower()
        mask = self.all_movies["clean_title"].str.lower().str.contains(q, na=False)
        return self.all_movies[mask].sort_values("num_ratings", ascending=False).head(n)

    def by_genre(self, genre, source="All", n=12):
        df = self.all_movies
        if source != "All":
            df = df[df["source"] == source]
        df = df[df["genres"].str.contains(genre, na=False)]
        df = df.sort_values(["avg_rating", "num_ratings"], ascending=False)
        if source in ("All", "Hollywood"):
            df = df[df["num_ratings"] >= 20]
        return df.head(n)

    def genres(self):
        g = set()
        for row in self.all_movies["genres"].dropna():
            for x in row.split("|"):
                if x not in ("(no genres listed)", ""):
                    g.add(x)
        return sorted(g)


# ─────────────────────────────────────────────
#  App
# ─────────────────────────────────────────────
class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Movie Recommendation System — CodSoft Task 4")
        self.geometry("1200x740")
        self.minsize(950, 620)
        self.configure(bg=BG)
        self.engine = Engine()
        self._ready = False
        self._build()
        threading.Thread(target=self._load, daemon=True).start()

    # ── Load ────────────────────────────────
    def _load(self):
        try:
            self.engine.load(lambda m: self._status(m, YELLOW))
            self._ready = True
            self.after(0, self._on_ready)
        except Exception as e:
            self.after(0, lambda: self._status(f"❌ {e}", RED))

    def _on_ready(self):
        self._status("✅  Ready! Search a movie or browse by genre.", GREEN)
        self.search_btn.config(state="normal")
        self.genre_btn.config(state="normal")
        g = self.engine.genres()
        self.genre_var.set(g[0])
        self.genre_combo["values"] = g
        self.dot.config(fg=GREEN)
        self.dot_lbl.config(text="Ready", fg=GREEN)
        hw = len(self.engine.hollywood)
        bw = len(self.engine.bollywood)
        rt = len(self.engine.ratings_df)
        us = self.engine.ratings_df["userId"].nunique()
        self.stats_lbl.config(
            text=f"🎬  {hw:,} Hollywood\n🎭  {bw:,} Bollywood\n"
                 f"⭐  {rt:,} ratings\n👤  {us:,} users",
            fg=MUTED)

    # ── Build UI ────────────────────────────
    def _build(self):
        self._header()
        self._body()
        self._statusbar()

    def _header(self):
        h = tk.Frame(self, bg=PANEL, height=66)
        h.pack(fill="x")
        h.pack_propagate(False)

        l = tk.Frame(h, bg=PANEL)
        l.pack(side="left", padx=22, pady=10)
        tk.Label(l, text=" AI ", font=("Segoe UI", 9, "bold"),
                 bg=ACCENT, fg="white", padx=7, pady=3).pack(side="left", padx=(0,12))
        tk.Label(l, text="Movie Recommender",
                 font=("Segoe UI", 19, "bold"), bg=PANEL, fg=TEXT).pack(side="left")

        r = tk.Frame(h, bg=PANEL)
        r.pack(side="right", padx=22)
        for t, c in [("Hollywood + Bollywood", ACCENT), ("  |  ", SUBTLE),
                     ("Content-Based Filtering", MUTED), ("  ·  Task 4", SUBTLE)]:
            tk.Label(r, text=t, font=("Segoe UI", 10), bg=PANEL, fg=c).pack(side="left")
        self.dot = tk.Label(r, text="●", font=("Segoe UI", 13), bg=PANEL, fg=YELLOW)
        self.dot.pack(side="left", padx=(14, 0))
        self.dot_lbl = tk.Label(r, text="Loading...", font=("Segoe UI", 9),
                                bg=PANEL, fg=YELLOW)
        self.dot_lbl.pack(side="left", padx=(3, 0))

        tk.Frame(self, bg=BORDER, height=1).pack(fill="x")

    def _body(self):
        wrap = tk.Frame(self, bg=BG)
        wrap.pack(fill="both", expand=True, padx=22, pady=18)

        # ── Sidebar ─────────────────────────
        sb = tk.Frame(wrap, bg=PANEL, width=270)
        sb.pack(side="left", fill="y", padx=(0, 18))
        sb.pack_propagate(False)

        self._sb_section(sb, "🔍  Search Movie")

        self.search_var = tk.StringVar()
        e = tk.Entry(sb, textvariable=self.search_var, font=("Segoe UI", 12),
                     bg=CELL, fg=TEXT, insertbackground=TEXT, relief="flat",
                     highlightbackground=ACCENT, highlightthickness=1)
        e.pack(fill="x", padx=14, ipady=9)
        e.bind("<Return>", lambda _: self._do_search())

        self.search_src = tk.StringVar(value="All")
        self._radio_row(sb, self.search_src)

        self.search_btn = self._btn(sb, "Get Recommendations",
                                    self._do_search, ACCENT, ACCENT2)

        self._divider(sb)
        self._sb_section(sb, "🎬  Browse by Genre")

        self.genre_var = tk.StringVar(value="Loading...")
        style = ttk.Style()
        style.theme_use("clam")
        style.configure("C.TCombobox", fieldbackground=CELL, background=CELL,
                        foreground=TEXT, bordercolor=BORDER, arrowcolor=MUTED,
                        selectbackground=ACCENT, selectforeground=TEXT)
        style.map("C.TCombobox", fieldbackground=[("readonly", CELL)])
        self.genre_combo = ttk.Combobox(sb, textvariable=self.genre_var,
                                        font=("Segoe UI", 11), state="readonly",
                                        style="C.TCombobox")
        self.genre_combo.pack(fill="x", padx=14, ipady=5)

        self.genre_src = tk.StringVar(value="All")
        self._radio_row(sb, self.genre_src)

        self.genre_btn = self._btn(sb, "Show Top Movies",
                                   self._do_genre, CARD, BORDER)

        self._divider(sb)

        stat_card = tk.Frame(sb, bg=CELL, highlightbackground=BORDER,
                             highlightthickness=1)
        stat_card.pack(fill="x", padx=14, pady=(0, 14))
        tk.Label(stat_card, text="📊  Dataset",
                 font=("Segoe UI", 10, "bold"), bg=CELL, fg=TEXT,
                 padx=12, pady=10).pack(anchor="w")
        tk.Frame(stat_card, bg=BORDER, height=1).pack(fill="x", padx=10)
        self.stats_lbl = tk.Label(stat_card, text="Loading...",
                                  font=("Segoe UI", 10), bg=CELL, fg=MUTED,
                                  justify="left", padx=12, pady=10)
        self.stats_lbl.pack(anchor="w")

        # ── Results ─────────────────────────
        right = tk.Frame(wrap, bg=BG)
        right.pack(side="right", fill="both", expand=True)

        top_bar = tk.Frame(right, bg=BG)
        top_bar.pack(fill="x", pady=(0, 12))
        self.result_title = tk.Label(top_bar, text="Welcome",
                                     font=("Segoe UI", 14, "bold"), bg=BG, fg=TEXT)
        self.result_title.pack(side="left")
        self.result_count = tk.Label(top_bar, text="",
                                     font=("Segoe UI", 10), bg=BG, fg=MUTED)
        self.result_count.pack(side="left", padx=10)

        # Canvas + scrollbar
        c_wrap = tk.Frame(right, bg=BG)
        c_wrap.pack(fill="both", expand=True)
        self.canvas = tk.Canvas(c_wrap, bg=BG, highlightthickness=0)
        vsb = tk.Scrollbar(c_wrap, orient="vertical", command=self.canvas.yview)
        self.rf = tk.Frame(self.canvas, bg=BG)
        self.rf.bind("<Configure>",
                     lambda e: self.canvas.configure(
                         scrollregion=self.canvas.bbox("all")))
        self.canvas.create_window((0, 0), window=self.rf, anchor="nw")
        self.canvas.configure(yscrollcommand=vsb.set)
        self.canvas.pack(side="left", fill="both", expand=True)
        vsb.pack(side="right", fill="y")
        self.canvas.bind_all("<MouseWheel>",
                             lambda e: self.canvas.yview_scroll(
                                 -1*(e.delta//120), "units"))

        self._welcome()

    def _statusbar(self):
        tk.Frame(self, bg=BORDER, height=1).pack(fill="x")
        bar = tk.Frame(self, bg=PANEL, height=30)
        bar.pack(fill="x", side="bottom")
        bar.pack_propagate(False)
        self.status_var = tk.StringVar(value="Loading dataset...")
        self.status_lbl = tk.Label(bar, textvariable=self.status_var,
                                   font=("Segoe UI", 9), bg=PANEL, fg=MUTED)
        self.status_lbl.pack(side="left", padx=16)
        tk.Label(bar, text="TF-IDF + Cosine Similarity  |  MovieLens + Bollywood",
                 font=("Segoe UI", 9), bg=PANEL, fg=SUBTLE).pack(side="right", padx=16)

    # ── Sidebar helpers ─────────────────────
    def _sb_section(self, parent, text):
        tk.Label(parent, text=text, font=("Segoe UI", 11, "bold"),
                 bg=PANEL, fg=TEXT).pack(anchor="w", padx=14, pady=(14, 8))

    def _radio_row(self, parent, var):
        f = tk.Frame(parent, bg=PANEL)
        f.pack(fill="x", padx=14, pady=(6, 0))
        for label, color in [("All", MUTED), ("Hollywood", ACCENT), ("Bollywood", PINK)]:
            rb = tk.Radiobutton(f, text=label, variable=var, value=label,
                                bg=PANEL, fg=TEXT, selectcolor=CELL,
                                activebackground=PANEL, activeforeground=TEXT,
                                font=("Segoe UI", 10), cursor="hand2")
            rb.pack(side="left", padx=(0, 6))

    def _btn(self, parent, text, cmd, bg, hover, state="disabled"):
        b = tk.Button(parent, text=text, font=("Segoe UI", 11, "bold"),
                      bg=bg, fg=TEXT, relief="flat", activebackground=hover,
                      activeforeground=TEXT, cursor="hand2", pady=10,
                      state=state, command=cmd)
        b.pack(fill="x", padx=14, pady=(8, 0))
        b.bind("<Enter>", lambda e: b.config(bg=hover) if b["state"]=="normal" else None)
        b.bind("<Leave>", lambda e: b.config(bg=bg)    if b["state"]=="normal" else None)
        return b

    def _divider(self, parent):
        tk.Frame(parent, bg=BORDER, height=1).pack(fill="x", padx=14, pady=14)

    # ── Actions ─────────────────────────────
    def _do_search(self):
        q = self.search_var.get().strip()
        if not q or not self._ready:
            return
        res, err = self.engine.recommend(q)
        src = self.search_src.get()
        if res is not None and src != "All":
            res = res[res["source"] == src]
        if err or (res is not None and res.empty):
            res = self.engine.search(q)
            if src != "All":
                res = res[res["source"] == src]
            if res.empty:
                self._error(f"No results for '{q}'")
                return
            self._show(res, f'Search: "{q}"', False)
        else:
            self._show(res, f'Similar to "{q}"', True)

    def _do_genre(self):
        g   = self.genre_var.get()
        src = self.genre_src.get()
        if not g or not self._ready:
            return
        res = self.engine.by_genre(g, src)
        lbl = f"Top {src + ' ' if src != 'All' else ''}{g} Movies"
        self._show(res, lbl, False)

    # ── Display ─────────────────────────────
    def _clear(self):
        for w in self.rf.winfo_children():
            w.destroy()

    def _welcome(self):
        self._clear()
        self.result_title.config(text="Welcome!")
        self.result_count.config(text="")
        f = tk.Frame(self.rf, bg=BG)
        f.pack(expand=True, pady=80)
        tk.Label(f, text="🎬", font=("Segoe UI Emoji", 52), bg=BG, fg=SUBTLE).pack()
        tk.Label(f, text="Search movies or browse by genre",
                 font=("Segoe UI", 14), bg=BG, fg=MUTED).pack(pady=14)
        tk.Label(f, text="Supports both Hollywood and Bollywood films",
                 font=("Segoe UI", 11), bg=BG, fg=SUBTLE).pack()

    def _error(self, msg):
        self._clear()
        self.result_title.config(text="No Results")
        self.result_count.config(text="")
        f = tk.Frame(self.rf, bg=BG)
        f.pack(pady=80)
        tk.Label(f, text="😕", font=("Segoe UI Emoji", 40), bg=BG).pack()
        tk.Label(f, text=msg, font=("Segoe UI", 12), bg=BG, fg=RED).pack(pady=10)
        tk.Label(f, text="Try a different title or check spelling",
                 font=("Segoe UI", 10), bg=BG, fg=MUTED).pack()

    def _show(self, df, title, show_sim):
        self._clear()
        self.canvas.yview_moveto(0)
        self.result_title.config(text=title)
        self.result_count.config(text=f"{len(df)} results")
        for _, row in df.iterrows():
            self._card(row, show_sim)

    def _card(self, row, show_sim):
        source = row.get("source", "Hollywood")
        is_bw  = source == "Bollywood"
        acc    = PINK if is_bw else ACCENT

        # Outer card
        outer = tk.Frame(self.rf, bg=BORDER)
        outer.pack(fill="x", pady=4, padx=2)
        inner = tk.Frame(outer, bg=CARD)
        inner.pack(fill="x", padx=1, pady=1)
        body = tk.Frame(inner, bg=CARD)
        body.pack(fill="x", padx=18, pady=14)

        # ── Row 1: title + badges ────────────
        r1 = tk.Frame(body, bg=CARD)
        r1.pack(fill="x")

        title = row.get("clean_title", "Unknown")
        year  = row.get("year", "")
        yr    = f" ({year})" if pd.notna(year) and year else ""
        tk.Label(r1, text=title + yr, font=("Segoe UI", 13, "bold"),
                 bg=CARD, fg=TEXT).pack(side="left")

        # Source badge
        tk.Label(r1, text=f"  {source}  ", font=("Segoe UI", 8, "bold"),
                 bg=acc, fg="white", padx=2).pack(side="right", padx=(6, 0))

        # Match badge
        if show_sim and "similarity" in row:
            sim  = int(row["similarity"])
            clr  = GREEN if sim >= 70 else YELLOW if sim >= 40 else MUTED
            tk.Label(r1, text=f"  {sim}% match  ", font=("Segoe UI", 8, "bold"),
                     bg=clr, fg="white", padx=2).pack(side="right")

        # ── Row 2: genres ────────────────────
        genres = row.get("genres", "").replace("|", "   ·   ")
        tk.Label(body, text=genres, font=("Segoe UI", 10),
                 bg=CARD, fg=MUTED).pack(anchor="w", pady=(5, 0))

        # ── Row 3: stars + rating ────────────
        r3 = tk.Frame(body, bg=CARD)
        r3.pack(anchor="w", pady=(8, 0))

        avg = float(row.get("avg_rating", 0) or 0)
        n   = int(row.get("num_ratings", 0) or 0)

        # Convert 5-scale rating to stars (out of 5)
        full  = int(avg)
        half  = 1 if (avg - full) >= 0.5 else 0
        empty = 5 - full - half

        star_str = "★" * full + ("½" if half else "") + "☆" * empty
        tk.Label(r3, text=star_str, font=("Segoe UI", 13),
                 bg=CARD, fg=STAR_ON).pack(side="left")
        tk.Label(r3, text=f"   {avg}/5   ({n:,} ratings)",
                 font=("Segoe UI", 10), bg=CARD, fg=MUTED).pack(side="left")

        # Left accent bar
        bar = tk.Frame(inner, bg=acc, width=4)
        bar.place(x=0, y=0, relheight=1)

    def _status(self, text, color=MUTED):
        self.status_var.set(text)
        self.status_lbl.config(fg=color)


if __name__ == "__main__":
    App().mainloop()