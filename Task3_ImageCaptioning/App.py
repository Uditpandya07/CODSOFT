import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk
from transformers import BlipProcessor, BlipForConditionalGeneration
import threading
import os

# ── Colors ──────────────────────────────────
BG      = "#0f0f1a"
PANEL   = "#1a1a2e"
CARD    = "#16213e"
ACCENT  = "#6366f1"
ACCENT2 = "#4f52dd"
TEXT    = "#e2e8f0"
MUTED   = "#64748b"
GREEN   = "#22c55e"
RED     = "#ef4444"
BORDER  = "#2d2d4e"
CELL    = "#1e1e3a"
YELLOW  = "#f59e0b"


class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Image Captioning AI — CodSoft Task 3")
        self.geometry("1000x680")
        self.minsize(800, 580)
        self.configure(bg=BG)
        self.resizable(True, True)

        self.model = None
        self.processor = None
        self.image_path = None
        self._model_ready = False

        self._build_ui()
        self._load_model()

    # ─────────────────────────────────────────
    #  UI
    # ─────────────────────────────────────────
    def _build_ui(self):
        self._build_header()
        self._build_body()
        self._build_statusbar()

    def _build_header(self):
        header = tk.Frame(self, bg=PANEL, height=70)
        header.pack(fill="x")
        header.pack_propagate(False)

        left = tk.Frame(header, bg=PANEL)
        left.pack(side="left", padx=24, pady=12)

        badge = tk.Label(left, text=" AI ", font=("Segoe UI", 9, "bold"),
                         bg=ACCENT, fg="white", padx=6, pady=2)
        badge.pack(side="left", padx=(0, 10))

        tk.Label(left, text="Image Captioning", font=("Segoe UI", 18, "bold"),
                 bg=PANEL, fg=TEXT).pack(side="left")

        right = tk.Frame(header, bg=PANEL)
        right.pack(side="right", padx=24)

        for txt, clr in [("BLIP Model", ACCENT), ("  |  ", MUTED),
                         ("CodSoft Internship", MUTED), ("  ·  Task 3", MUTED)]:
            tk.Label(right, text=txt, font=("Segoe UI", 10),
                     bg=PANEL, fg=clr).pack(side="left")

        self.model_dot = tk.Label(right, text="●", font=("Segoe UI", 14),
                                  bg=PANEL, fg=YELLOW)
        self.model_dot.pack(side="left", padx=(12, 0))
        self.model_status_lbl = tk.Label(right, text="Loading...",
                                         font=("Segoe UI", 9), bg=PANEL, fg=YELLOW)
        self.model_status_lbl.pack(side="left", padx=(2, 0))

        tk.Frame(self, bg=BORDER, height=1).pack(fill="x")

    def _build_body(self):
        body = tk.Frame(self, bg=BG)
        body.pack(fill="both", expand=True, padx=28, pady=20)

        # ── Left panel ──────────────────────
        left = tk.Frame(body, bg=BG)
        left.pack(side="left", fill="both", expand=True, padx=(0, 20))

        lbl_frame = tk.Frame(left, bg=BG)
        lbl_frame.pack(fill="x", pady=(0, 8))
        tk.Label(lbl_frame, text="📷  Input Image", font=("Segoe UI", 11, "bold"),
                 bg=BG, fg=TEXT).pack(side="left")
        self.img_name_lbl = tk.Label(lbl_frame, text="", font=("Segoe UI", 9),
                                     bg=BG, fg=MUTED)
        self.img_name_lbl.pack(side="left", padx=10)

        img_card = tk.Frame(left, bg=CELL, highlightbackground=BORDER,
                            highlightthickness=1)
        img_card.pack(fill="both", expand=True)

        self.img_box = tk.Label(img_card, bg=CELL, fg=MUTED, text="",
                                font=("Segoe UI", 12))
        self.img_box.pack(fill="both", expand=True, padx=2, pady=2)

        self.placeholder = tk.Frame(img_card, bg=CELL)
        self.placeholder.place(relx=0.5, rely=0.5, anchor="center")
        tk.Label(self.placeholder, text="🖼️", font=("Segoe UI Emoji", 40),
                 bg=CELL, fg=BORDER).pack()
        tk.Label(self.placeholder, text="No image selected",
                 font=("Segoe UI", 13, "bold"), bg=CELL, fg=MUTED).pack(pady=(8, 4))
        tk.Label(self.placeholder, text="Click 'Upload Image' to begin",
                 font=("Segoe UI", 10), bg=CELL, fg=BORDER).pack()

        self.upload_btn = tk.Button(
            left, text="📂   Upload Image",
            font=("Segoe UI", 12, "bold"),
            bg=ACCENT, fg="white", relief="flat",
            activebackground=ACCENT2, activeforeground="white",
            cursor="hand2", pady=12, command=self._upload
        )
        self.upload_btn.pack(fill="x", pady=(12, 0))
        self.upload_btn.bind("<Enter>", lambda e: self.upload_btn.config(bg=ACCENT2))
        self.upload_btn.bind("<Leave>", lambda e: self.upload_btn.config(bg=ACCENT))

        # ── Right panel ─────────────────────
        right = tk.Frame(body, bg=BG, width=320)
        right.pack(side="right", fill="y")
        right.pack_propagate(False)

        tk.Label(right, text="✨  Generated Caption", font=("Segoe UI", 11, "bold"),
                 bg=BG, fg=TEXT).pack(anchor="w", pady=(0, 8))

        cap_card = tk.Frame(right, bg=CELL, highlightbackground=BORDER,
                            highlightthickness=1, height=380)
        cap_card.pack(fill="x")

        self.caption_box = tk.Text(
            cap_card, font=("Segoe UI", 14),
            bg=CELL, fg=TEXT, wrap="word",
            relief="flat", padx=16, pady=16,
            state="disabled", cursor="arrow",
            spacing1=4, spacing2=4, height=14
        )
        self.caption_box.pack(fill="both", expand=True)

        self.cap_placeholder = tk.Frame(cap_card, bg=CELL)
        self.cap_placeholder.place(relx=0.5, rely=0.5, anchor="center")
        tk.Label(self.cap_placeholder, text="💬", font=("Segoe UI Emoji", 30),
                 bg=CELL, fg=BORDER).pack()
        tk.Label(self.cap_placeholder, text="Caption will appear here",
                 font=("Segoe UI", 11), bg=CELL, fg=BORDER).pack(pady=(8, 0))

        self.gen_btn = tk.Button(
            right, text="✨   Generate Caption",
            font=("Segoe UI", 12, "bold"),
            bg=ACCENT, fg="white", relief="flat",
            activebackground=ACCENT2, activeforeground="white",
            cursor="hand2", pady=12, state="disabled",
            command=self._generate_async
        )
        self.gen_btn.pack(fill="x", pady=(10, 6))
        self.gen_btn.bind("<Enter>", lambda e: self.gen_btn.config(bg=ACCENT2)
                          if self.gen_btn["state"] == "normal" else None)
        self.gen_btn.bind("<Leave>", lambda e: self.gen_btn.config(bg=ACCENT)
                          if self.gen_btn["state"] == "normal" else None)

        self.copy_btn = tk.Button(
            right, text="📋   Copy Caption",
            font=("Segoe UI", 11),
            bg=CARD, fg=MUTED, relief="flat",
            activebackground=BORDER, activeforeground=TEXT,
            cursor="hand2", pady=10, state="disabled",
            command=self._copy
        )
        self.copy_btn.pack(fill="x")
        self.copy_btn.bind("<Enter>", lambda e: self.copy_btn.config(bg=BORDER)
                           if self.copy_btn["state"] == "normal" else None)
        self.copy_btn.bind("<Leave>", lambda e: self.copy_btn.config(bg=CARD)
                           if self.copy_btn["state"] == "normal" else None)

    def _build_statusbar(self):
        tk.Frame(self, bg=BORDER, height=1).pack(fill="x")
        bar = tk.Frame(self, bg=PANEL, height=32)
        bar.pack(fill="x", side="bottom")
        bar.pack_propagate(False)

        self.status_var = tk.StringVar(value="Initializing...")
        self.status_lbl = tk.Label(bar, textvariable=self.status_var,
                                   font=("Segoe UI", 9), bg=PANEL, fg=MUTED)
        self.status_lbl.pack(side="left", padx=16, pady=6)

        tk.Label(bar, text="Salesforce/blip-image-captioning-base",
                 font=("Segoe UI", 9), bg=PANEL, fg=BORDER).pack(side="right", padx=16)

    # ─────────────────────────────────────────
    #  Model loading
    # ─────────────────────────────────────────
    def _load_model(self):
        def load():
            self._set_status("Loading BLIP model (first run downloads ~1GB)...", YELLOW)
            try:
                self.processor = BlipProcessor.from_pretrained(
                    "Salesforce/blip-image-captioning-base")
                self.model = BlipForConditionalGeneration.from_pretrained(
                    "Salesforce/blip-image-captioning-base")
                self._model_ready = True
                self.after(0, self._on_model_ready)
            except Exception as e:
                self.after(0, lambda: self._set_status(f"❌ Failed: {e}", RED))

        threading.Thread(target=load, daemon=True).start()

    def _on_model_ready(self):
        self.model_dot.config(fg=GREEN)
        self.model_status_lbl.config(text="Ready", fg=GREEN)
        self._set_status("✅  Model ready! Upload an image to start.", GREEN)
        if self.image_path:
            self.gen_btn.config(state="normal")

    # ─────────────────────────────────────────
    #  Upload
    # ─────────────────────────────────────────
    def _upload(self):
        path = filedialog.askopenfilename(
            filetypes=[("Image Files", "*.jpg *.jpeg *.png *.bmp *.webp")])
        if not path:
            return

        self.image_path = path
        self.img_name_lbl.config(text=os.path.basename(path))
        self.placeholder.place_forget()

        img = Image.open(path).convert("RGB")
        img.thumbnail((520, 420), Image.LANCZOS)
        photo = ImageTk.PhotoImage(img)
        self.img_box.config(image=photo, text="")
        self.img_box.image = photo

        self._set_caption("")
        self.cap_placeholder.place(relx=0.5, rely=0.5, anchor="center")
        self.copy_btn.config(state="disabled")
        self._set_status(f"Image loaded: {os.path.basename(path)}", TEXT)

        if self._model_ready:
            self.gen_btn.config(state="normal")

    # ─────────────────────────────────────────
    #  Generation
    # ─────────────────────────────────────────
    def _generate_async(self):
        if not self.image_path:
            return
        self.gen_btn.config(state="disabled", text="⏳   Generating...")
        self.copy_btn.config(state="disabled")
        self.cap_placeholder.place_forget()
        self._set_caption("Generating caption...")
        self._set_status("Generating caption...", MUTED)
        threading.Thread(target=self._generate, daemon=True).start()

    def _generate(self):
        try:
            img = Image.open(self.image_path).convert("RGB")
            inputs = self.processor(img, return_tensors="pt")
            out = self.model.generate(**inputs, max_new_tokens=50)
            caption = self.processor.decode(out[0], skip_special_tokens=True)
            self.after(0, lambda: self._on_done(caption))
        except Exception as e:
            self.after(0, lambda: self._on_error(str(e)))

    def _on_done(self, caption):
        self._set_caption(caption)
        self._set_status("✅  Caption generated successfully!", GREEN)
        self.gen_btn.config(state="normal", text="✨   Generate Caption")
        self.copy_btn.config(state="normal", fg=TEXT)

    def _on_error(self, err):
        self._set_caption(f"Error: {err}")
        self._set_status(f"❌  Error: {err}", RED)
        self.gen_btn.config(state="normal", text="✨   Generate Caption")

    # ─────────────────────────────────────────
    #  Helpers
    # ─────────────────────────────────────────
    def _set_caption(self, text):
        self.caption_box.config(state="normal")
        self.caption_box.delete("1.0", "end")
        self.caption_box.insert("1.0", text)
        self.caption_box.config(state="disabled")

    def _copy(self):
        text = self.caption_box.get("1.0", "end").strip()
        if text:
            self.clipboard_clear()
            self.clipboard_append(text)
            self._set_status("📋  Caption copied to clipboard!", GREEN)

    def _set_status(self, text, color=MUTED):
        self.status_var.set(text)
        self.status_lbl.config(fg=color)


if __name__ == "__main__":
    App().mainloop()