import tkinter as tk
from tkinter import filedialog, simpledialog, messagebox
from PIL import Image, ImageTk
import cv2
import numpy as np
import os
import pickle
import threading

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
CYAN    = "#06b6d4"

DB_FILE   = "faces_db.pkl"
HAAR_PATH = cv2.data.haarcascades + "haarcascade_frontalface_default.xml"


# ─────────────────────────────────────────────
#  Face Engine
# ─────────────────────────────────────────────
class FaceEngine:
    def __init__(self):
        self.detector   = cv2.CascadeClassifier(HAAR_PATH)
        self.recognizer = cv2.face.LBPHFaceRecognizer_create()
        self.label_map  = {}
        self.trained    = False
        self._load()

    def _load(self):
        if not os.path.exists(DB_FILE):
            return
        with open(DB_FILE, "rb") as f:
            data = pickle.load(f)
        faces  = data.get("faces",  [])
        labels = data.get("labels", [])
        self.label_map = data.get("label_map", {})
        if faces:
            self.recognizer.train(faces, np.array(labels))
            self.trained = True

    def _save(self, faces, labels):
        with open(DB_FILE, "wb") as f:
            pickle.dump({
                "faces":     faces,
                "labels":    labels,
                "label_map": self.label_map
            }, f)

    def register(self, image_path, name):
        img  = cv2.imread(image_path)
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        rects = self.detector.detectMultiScale(gray, 1.1, 5, minSize=(60, 60))
        if len(rects) == 0:
            return False, "No face found. Use a clearer front-facing photo."

        ids = list(self.label_map.keys())
        new_id = max(ids) + 1 if ids else 0
        self.label_map[new_id] = name

        faces, labels = [], []
        if os.path.exists(DB_FILE):
            with open(DB_FILE, "rb") as f:
                d = pickle.load(f)
            faces  = d.get("faces",  [])
            labels = d.get("labels", [])

        x, y, w, h = rects[0]
        crop = cv2.resize(gray[y:y+h, x:x+w], (100, 100))
        faces.append(crop)
        labels.append(new_id)

        self._save(faces, labels)
        self.recognizer.train(faces, np.array(labels))
        self.trained = True
        return True, f"'{name}' registered!"

    def remove(self, name):
        ids_to_remove = [k for k, v in self.label_map.items() if v == name]
        if not ids_to_remove or not os.path.exists(DB_FILE):
            return
        with open(DB_FILE, "rb") as f:
            data = pickle.load(f)
        faces  = data.get("faces",  [])
        labels = data.get("labels", [])
        keep = [(f, l) for f, l in zip(faces, labels) if l not in ids_to_remove]
        for rid in ids_to_remove:
            del self.label_map[rid]
        if keep:
            faces, labels = zip(*keep)
            faces, labels = list(faces), list(labels)
            self._save(faces, labels)
            self.recognizer.train(faces, np.array(labels))
            self.trained = True
        else:
            self._save([], [])
            self.recognizer = cv2.face.LBPHFaceRecognizer_create()
            self.trained = False

    def analyze(self, frame_bgr):
        gray  = cv2.cvtColor(frame_bgr, cv2.COLOR_BGR2GRAY)
        rects = self.detector.detectMultiScale(
            gray, scaleFactor=1.1, minNeighbors=5,
            minSize=(50, 50), flags=cv2.CASCADE_SCALE_IMAGE)
        results = []
        for (x, y, w, h) in rects:
            name  = "Unknown"
            conf  = 0.0
            color = (239, 68, 68)
            if self.trained:
                crop = cv2.resize(gray[y:y+h, x:x+w], (100, 100))
                label_id, distance = self.recognizer.predict(crop)
                confidence = max(0, round(100 - distance, 1))
                if distance < 80:
                    name  = self.label_map.get(label_id, "Unknown")
                    conf  = confidence
                    color = (34, 197, 94)
            results.append({"box": (x, y, w, h), "name": name,
                             "conf": conf, "color": color})
        return results

    def draw(self, frame_bgr, results):
        out = frame_bgr.copy()
        for r in results:
            x, y, w, h = r["box"]
            color = r["color"]
            label = f"{r['name']} {r['conf']:.0f}%" if r["conf"] > 0 else r["name"]
            cv2.rectangle(out, (x, y), (x+w, y+h), color, 2)
            (lw, lh), _ = cv2.getTextSize(label, cv2.FONT_HERSHEY_SIMPLEX, 0.6, 1)
            cv2.rectangle(out, (x, y-lh-10), (x+lw+8, y), color, -1)
            cv2.putText(out, label, (x+4, y-4),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 1)
        return out

    @property
    def known_names(self):
        return sorted(set(self.label_map.values()))


# ─────────────────────────────────────────────
#  App
# ─────────────────────────────────────────────
class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Face Detection & Recognition — CodSoft Task 5")
        self.geometry("1150x720")
        self.minsize(900, 600)
        self.configure(bg=BG)
        self.resizable(True, True)
        self.engine       = FaceEngine()
        self._webcam_on   = False
        self._cap         = None
        self._mode        = "image"
        self._current_bgr = None
        self._build()

    def _build(self):
        self._header()
        self._body()
        self._statusbar()
        self._refresh_list()

    # ── Header ──────────────────────────────
    def _header(self):
        h = tk.Frame(self, bg=PANEL, height=66)
        h.pack(fill="x")
        h.pack_propagate(False)
        l = tk.Frame(h, bg=PANEL)
        l.pack(side="left", padx=22, pady=10)
        tk.Label(l, text=" AI ", font=("Segoe UI", 9, "bold"),
                 bg=ACCENT, fg="white", padx=7, pady=3).pack(side="left", padx=(0,12))
        tk.Label(l, text="Face Detection & Recognition",
                 font=("Segoe UI", 18, "bold"), bg=PANEL, fg=TEXT).pack(side="left")
        r = tk.Frame(h, bg=PANEL)
        r.pack(side="right", padx=22)
        for t, c in [("OpenCV Haar + LBPH", ACCENT), ("  |  ", SUBTLE),
                     ("CodSoft Internship", MUTED), ("  ·  Task 5", SUBTLE)]:
            tk.Label(r, text=t, font=("Segoe UI", 10), bg=PANEL, fg=c).pack(side="left")
        tk.Frame(self, bg=BORDER, height=1).pack(fill="x")

    # ── Body ────────────────────────────────
    def _body(self):
        wrap = tk.Frame(self, bg=BG)
        wrap.pack(fill="both", expand=True, padx=22, pady=16)

        # Sidebar
        sb = tk.Frame(wrap, bg=PANEL, width=260)
        sb.pack(side="left", fill="y", padx=(0, 18))
        sb.pack_propagate(False)

        tk.Label(sb, text="📷  Mode", font=("Segoe UI", 11, "bold"),
                 bg=PANEL, fg=TEXT).pack(anchor="w", padx=14, pady=(14, 8))
        mf = tk.Frame(sb, bg=PANEL)
        mf.pack(fill="x", padx=14)
        self.img_btn = tk.Button(mf, text="🖼️  Image",
                                 font=("Segoe UI", 10, "bold"),
                                 bg=ACCENT, fg=TEXT, relief="flat",
                                 cursor="hand2", pady=8,
                                 command=lambda: self._set_mode("image"))
        self.img_btn.pack(side="left", fill="x", expand=True, padx=(0, 4))
        self.cam_btn_mode = tk.Button(mf, text="📹  Webcam",
                                      font=("Segoe UI", 10, "bold"),
                                      bg=CELL, fg=TEXT, relief="flat",
                                      cursor="hand2", pady=8,
                                      command=lambda: self._set_mode("webcam"))
        self.cam_btn_mode.pack(side="left", fill="x", expand=True)

        self._div(sb)

        # Image controls
        self.img_panel = tk.Frame(sb, bg=PANEL)
        self.img_panel.pack(fill="x")
        tk.Label(self.img_panel, text="🔍  Image Analysis",
                 font=("Segoe UI", 11, "bold"), bg=PANEL, fg=TEXT).pack(
                     anchor="w", padx=14, pady=(0, 8))
        self._mk_btn(self.img_panel, "📂  Upload Image", self._upload, ACCENT, ACCENT2)
        self._mk_btn(self.img_panel, "🔍  Detect Faces", self._detect, CARD, BORDER)

        # Webcam controls
        self.cam_panel = tk.Frame(sb, bg=PANEL)
        tk.Label(self.cam_panel, text="📹  Webcam",
                 font=("Segoe UI", 11, "bold"), bg=PANEL, fg=TEXT).pack(
                     anchor="w", padx=14, pady=(0, 8))
        self.cam_toggle = self._mk_btn(
            self.cam_panel, "▶  Start Webcam", self._toggle_cam, GREEN, "#16a34a")

        self._div(sb)

        tk.Label(sb, text="👤  Register Face",
                 font=("Segoe UI", 11, "bold"), bg=PANEL, fg=TEXT).pack(
                     anchor="w", padx=14, pady=(0, 8))
        self._mk_btn(sb, "➕  Add Known Face", self._reg_face, CYAN, "#0891b2")

        self._div(sb)

        tk.Label(sb, text="📋  Known Faces",
                 font=("Segoe UI", 11, "bold"), bg=PANEL, fg=TEXT).pack(
                     anchor="w", padx=14, pady=(0, 6))
        lf = tk.Frame(sb, bg=CELL, highlightbackground=BORDER, highlightthickness=1)
        lf.pack(fill="x", padx=14)
        self.known_list = tk.Listbox(lf, font=("Segoe UI", 10),
                                     bg=CELL, fg=TEXT,
                                     selectbackground=ACCENT,
                                     relief="flat", height=5,
                                     bd=0, highlightthickness=0)
        self.known_list.pack(fill="x", padx=8, pady=8)
        self._mk_btn(sb, "🗑️  Remove Selected", self._remove, "#7f1d1d", "#991b1b")

        # Main display
        main = tk.Frame(wrap, bg=BG)
        main.pack(side="right", fill="both", expand=True)

        top = tk.Frame(main, bg=BG)
        top.pack(fill="x", pady=(0, 10))
        self.disp_title = tk.Label(top, text="Upload an image or start webcam",
                                   font=("Segoe UI", 13, "bold"), bg=BG, fg=TEXT)
        self.disp_title.pack(side="left")
        self.count_lbl = tk.Label(top, text="",
                                  font=("Segoe UI", 10), bg=BG, fg=MUTED)
        self.count_lbl.pack(side="left", padx=10)

        self.disp_frame = tk.Frame(main, bg=CELL,
                                   highlightbackground=BORDER, highlightthickness=1)
        self.disp_frame.pack(fill="both", expand=True)
        self.disp_lbl = tk.Label(self.disp_frame, bg=CELL)
        self.disp_lbl.pack(fill="both", expand=True)

        # Placeholder
        self.ph = tk.Frame(self.disp_frame, bg=CELL)
        self.ph.place(relx=0.5, rely=0.5, anchor="center")
        tk.Label(self.ph, text="👁️", font=("Segoe UI Emoji", 52),
                 bg=CELL, fg=BORDER).pack()
        tk.Label(self.ph, text="No image loaded",
                 font=("Segoe UI", 13, "bold"), bg=CELL, fg=MUTED).pack(pady=(10, 4))
        tk.Label(self.ph, text="Upload an image or start webcam to begin",
                 font=("Segoe UI", 10), bg=CELL, fg=SUBTLE).pack()

        # Results bar
        self.res_frame = tk.Frame(main, bg=PANEL,
                                  highlightbackground=BORDER, highlightthickness=1)
        self.res_frame.pack(fill="x", pady=(10, 0))
        self.res_lbl = tk.Label(self.res_frame,
                                text="Results will appear here after detection",
                                font=("Segoe UI", 10), bg=PANEL, fg=MUTED,
                                padx=14, pady=10, justify="left")
        self.res_lbl.pack(anchor="w")

    def _statusbar(self):
        tk.Frame(self, bg=BORDER, height=1).pack(fill="x")
        bar = tk.Frame(self, bg=PANEL, height=30)
        bar.pack(fill="x", side="bottom")
        bar.pack_propagate(False)
        self.status_var = tk.StringVar(value="Ready")
        self.status_lbl = tk.Label(bar, textvariable=self.status_var,
                                   font=("Segoe UI", 9), bg=PANEL, fg=MUTED)
        self.status_lbl.pack(side="left", padx=16)
        tk.Label(bar, text="Haar Cascade + LBPH Face Recognizer  |  OpenCV",
                 font=("Segoe UI", 9), bg=PANEL, fg=SUBTLE).pack(side="right", padx=16)

    # ── Helpers ─────────────────────────────
    def _mk_btn(self, parent, text, cmd, bg, hover):
        b = tk.Button(parent, text=text, font=("Segoe UI", 11, "bold"),
                      bg=bg, fg=TEXT, relief="flat",
                      activebackground=hover, activeforeground=TEXT,
                      cursor="hand2", pady=9, command=cmd)
        b.pack(fill="x", padx=14, pady=(0, 6))
        b.bind("<Enter>", lambda e: b.config(bg=hover))
        b.bind("<Leave>", lambda e: b.config(bg=bg))
        return b

    def _div(self, p):
        tk.Frame(p, bg=BORDER, height=1).pack(fill="x", padx=14, pady=12)

    def _status(self, t, c=MUTED):
        self.status_var.set(t)
        self.status_lbl.config(fg=c)

    def _show_img(self, bgr):
        rgb   = cv2.cvtColor(bgr, cv2.COLOR_BGR2RGB)
        pil   = Image.fromarray(rgb)
        w = max(self.disp_frame.winfo_width(),  100)
        h = max(self.disp_frame.winfo_height(), 100)
        pil.thumbnail((w-4, h-4), Image.LANCZOS)
        photo = ImageTk.PhotoImage(pil)
        self.disp_lbl.config(image=photo)
        self.disp_lbl.image = photo
        self.ph.place_forget()

    def _refresh_list(self):
        self.known_list.delete(0, "end")
        for name in self.engine.known_names:
            self.known_list.insert("end", f"  👤  {name}")
        n = len(self.engine.known_names)
        self._status(f"Ready  |  {n} known face{'s' if n!=1 else ''} loaded")

    def _set_mode(self, mode):
        self._mode = mode
        if mode == "image":
            self.img_btn.config(bg=ACCENT)
            self.cam_btn_mode.config(bg=CELL)
            self.cam_panel.pack_forget()
            self.img_panel.pack(fill="x")
            if self._webcam_on:
                self._stop_cam()
        else:
            self.cam_btn_mode.config(bg=ACCENT)
            self.img_btn.config(bg=CELL)
            self.img_panel.pack_forget()
            self.cam_panel.pack(fill="x")

    # ── Image Mode ──────────────────────────
    def _upload(self):
        path = filedialog.askopenfilename(
            filetypes=[("Image Files", "*.jpg *.jpeg *.png *.bmp")])
        if not path:
            return
        self._current_bgr = cv2.imread(path)
        self._show_img(self._current_bgr)
        self.disp_title.config(text=os.path.basename(path))
        self.count_lbl.config(text="")
        self.res_lbl.config(text="Image loaded — click 'Detect Faces'")
        self._status("Image loaded.", YELLOW)

    def _detect(self):
        if self._current_bgr is None:
            messagebox.showwarning("No Image", "Upload an image first.")
            return
        self._status("Detecting...", YELLOW)

        def run():
            results  = self.engine.analyze(self._current_bgr)
            annotated = self.engine.draw(self._current_bgr, results)
            self.after(0, lambda: self._show_detect(annotated, results))

        threading.Thread(target=run, daemon=True).start()

    def _show_detect(self, annotated, results):
        self._show_img(annotated)
        n = len(results)
        self.count_lbl.config(text=f"{n} face{'s' if n!=1 else ''} detected")
        if n == 0:
            self.res_lbl.config(text="No faces detected.")
            self._status("No faces detected.", MUTED)
            return
        lines = []
        for i, r in enumerate(results, 1):
            if r["name"] == "Unknown":
                lines.append(f"  Face {i}:  Unknown  (not in database)")
            else:
                lines.append(f"  Face {i}:  {r['name']}  —  {r['conf']:.0f}% confidence")
        self.res_lbl.config(text="\n".join(lines))
        self._status(f"Done! {n} face(s) detected.", GREEN)

    # ── Webcam Mode ─────────────────────────
    def _toggle_cam(self):
        if self._webcam_on:
            self._stop_cam()
        else:
            self._start_cam()

    def _start_cam(self):
        self._cap = cv2.VideoCapture(0)
        if not self._cap.isOpened():
            messagebox.showerror("Error", "Cannot open webcam.")
            return
        self._webcam_on = True
        self.cam_toggle.config(text="⏹  Stop Webcam", bg=RED)
        self.disp_title.config(text="Live Webcam")
        self._status("Webcam active — detecting in real time...", GREEN)
        threading.Thread(target=self._cam_loop, daemon=True).start()

    def _stop_cam(self):
        self._webcam_on = False
        if self._cap:
            self._cap.release()
            self._cap = None
        self.cam_toggle.config(text="▶  Start Webcam", bg=GREEN)
        self.disp_title.config(text="Webcam stopped")
        self.count_lbl.config(text="")
        self._status("Webcam stopped.", MUTED)

    def _cam_loop(self):
        count   = 0
        cached  = []
        while self._webcam_on:
            ret, frame = self._cap.read()
            if not ret:
                break
            if count % 5 == 0:
                cached = self.engine.analyze(frame)
            annotated = self.engine.draw(frame, cached)
            n = len(cached)
            self.after(0, lambda f=annotated, c=n: self._cam_update(f, c))
            count += 1
        self.after(0, lambda: self.cam_toggle.config(
            text="▶  Start Webcam", bg=GREEN))

    def _cam_update(self, frame, n):
        self._show_img(frame)
        self.count_lbl.config(
            text=f"{n} face{'s' if n!=1 else ''} detected" if n > 0
            else "No faces detected")

    # ── Register / Remove ───────────────────
    def _reg_face(self):
        path = filedialog.askopenfilename(
            title="Select a clear photo of the person",
            filetypes=[("Image Files", "*.jpg *.jpeg *.png")])
        if not path:
            return
        name = simpledialog.askstring("Register", "Enter person's name:", parent=self)
        if not name or not name.strip():
            return
        ok, msg = self.engine.register(path, name.strip())
        if ok:
            messagebox.showinfo("Success", msg)
            self._status(msg, GREEN)
        else:
            messagebox.showerror("Error", msg)
            self._status(msg, RED)
        self._refresh_list()

    def _remove(self):
        sel = self.known_list.curselection()
        if not sel:
            messagebox.showwarning("Select", "Select a name to remove.")
            return
        name = self.known_list.get(sel[0]).replace("👤", "").strip()
        self.engine.remove(name)
        self._refresh_list()
        self._status(f"'{name}' removed.", MUTED)

    def on_close(self):
        self._stop_cam()
        self.destroy()


if __name__ == "__main__":
    app = App()
    app.protocol("WM_DELETE_WINDOW", app.on_close)
    app.mainloop()