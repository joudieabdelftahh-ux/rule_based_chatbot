

import tkinter as tk
from tkinter import font as tkfont
from datetime import datetime


from bot_brain import RuleBot


class ChatUI:
    """""
         Render the chat window and all widgets
        Send user messages to RuleBot and display replies
        Show timestamps on each message bubble
    """

    #  Theme
    BG_WINDOW   = "#f5f4f0"
    BG_HEADER   = "#faf9f6"
    BG_MESSAGES = "#ffffff"
    BG_INPUT    = "#faf9f6"

    BUBBLE_USER = "#EEEDFE"
    BUBBLE_BOT  = "#f0efea"
    TEXT_USER   = "#26215C"
    TEXT_BOT    = "#1a1a1a"
    TEXT_TIME   = "#aaaaaa"
    TEXT_HEADER = "#1a1a1a"
    TEXT_MUTED  = "#888888"

    ACCENT      = "#534AB7"
    ACCENT_DARK = "#3C3489"
    BORDER      = "#e0ded7"

    CHIP_SUGGESTIONS = [
        "Hi there!",
        "Tell me a joke",
        "What's your name?",
        "What do you do?",
        "How are you?",
    ]

    def __init__(self, root: tk.Tk):
        self._root = root
        self._bot = RuleBot()
        self._setup_window()
        self._build_ui()
        self._post_bot_message("Hey! I'm RuleBot. Say hello, ask for a joke, or ask what I do.")

    #  Window setup 

    def _setup_window(self):
        self._root.title("RuleBot")
        self._root.geometry("480x620")
        self._root.resizable(False, False)
        self._root.configure(bg=self.BG_WINDOW)

        # Fonts
        self._font_body   = tkfont.Font(family="Helvetica", size=11)
        self._font_small  = tkfont.Font(family="Helvetica", size=9)
        self._font_header = tkfont.Font(family="Helvetica", size=12, weight="bold")
        self._font_sub    = tkfont.Font(family="Helvetica", size=9)
        self._font_chip   = tkfont.Font(family="Helvetica", size=9)

    #  UI 

    def _build_ui(self):
        self._build_header()
        self._build_message_area()
        self._build_chips()
        self._build_input_row()

    def _build_header(self):
        frame = tk.Frame(self._root, bg=self.BG_HEADER, pady=10)
        frame.pack(fill="x", side="top")

        # Separator line at bottom of header
        tk.Frame(frame, bg=self.BORDER, height=1).pack(fill="x", side="bottom")

        inner = tk.Frame(frame, bg=self.BG_HEADER)
        inner.pack(padx=16, fill="x")

        # Avatar circle
        avatar = tk.Canvas(inner, width=36, height=36, bg=self.BG_HEADER,
                           highlightthickness=0)
        avatar.pack(side="left", padx=(0, 10))
        avatar.create_oval(2, 2, 34, 34, fill="#EEEDFE", outline="#CECBF6")
        avatar.create_text(18, 18, text="R", font=tkfont.Font(family="Helvetica",
                           size=13, weight="bold"), fill=self.ACCENT)

        # Name + status
        info = tk.Frame(inner, bg=self.BG_HEADER)
        info.pack(side="left")
        tk.Label(info, text="RuleBot", font=self._font_header,
                 bg=self.BG_HEADER, fg=self.TEXT_HEADER).pack(anchor="w")
        tk.Label(info, text="● Online", font=self._font_sub,
                 bg=self.BG_HEADER, fg="#1D9E75").pack(anchor="w")

    def _build_message_area(self):
        container = tk.Frame(self._root, bg=self.BG_MESSAGES)
        container.pack(fill="both", expand=True)

        # Scrollable canvas
        self._canvas = tk.Canvas(container, bg=self.BG_MESSAGES,
                                 highlightthickness=0, bd=0)
        scrollbar = tk.Scrollbar(container, orient="vertical",
                                 command=self._canvas.yview)

        self._canvas.configure(yscrollcommand=scrollbar.set)
        scrollbar.pack(side="right", fill="y")
        self._canvas.pack(side="left", fill="both", expand=True)

        # Inner frame holds all message rows
        self._msg_frame = tk.Frame(self._canvas, bg=self.BG_MESSAGES)
        self._canvas_window = self._canvas.create_window(
            (0, 0), window=self._msg_frame, anchor="nw"
        )

        # Resize window when frame grows
        self._msg_frame.bind("<Configure>", self._on_frame_configure)
        self._canvas.bind("<Configure>", self._on_canvas_configure)

        # Mouse-wheel scrolling
        self._canvas.bind_all("<MouseWheel>", self._on_mousewheel)

    def _build_chips(self):
        frame = tk.Frame(self._root, bg=self.BG_INPUT, pady=6)
        frame.pack(fill="x")
        tk.Frame(frame, bg=self.BORDER, height=1).pack(fill="x", side="top")

        chip_row = tk.Frame(frame, bg=self.BG_INPUT)
        chip_row.pack(padx=10, pady=(6, 0), fill="x")

        for label in self.CHIP_SUGGESTIONS:
            btn = tk.Button(
                chip_row,
                text=label,
                font=self._font_chip,
                bg="#ffffff",
                fg="#555555",
                relief="flat",
                bd=0,
                padx=8, pady=4,
                cursor="hand2",
                command=lambda l=label: self._on_chip_click(l),
            )
            btn.pack(side="left", padx=3)
            # Hover effects
            btn.bind("<Enter>", lambda e, b=btn: b.configure(bg="#EEEDFE", fg=self.ACCENT))
            btn.bind("<Leave>", lambda e, b=btn: b.configure(bg="#ffffff", fg="#555555"))

    def _build_input_row(self):
        frame = tk.Frame(self._root, bg=self.BG_INPUT, pady=8)
        frame.pack(fill="x", side="bottom")
        tk.Frame(frame, bg=self.BORDER, height=1).pack(fill="x", side="top")

        inner = tk.Frame(frame, bg=self.BG_INPUT)
        inner.pack(padx=12, pady=(8, 0), fill="x")

        # Text entry
        self._entry = tk.Entry(
            inner,
            font=self._font_body,
            bg="#ffffff",
            fg=self.TEXT_BOT,
            insertbackground=self.ACCENT,
            relief="flat",
            bd=0,
        )
        self._entry.pack(side="left", fill="x", expand=True, ipady=6)
        self._entry.bind("<Return>", lambda e: self._on_send())
        self._entry.bind("<KeyRelease>", self._on_key_release)

        # Char 
        self._char_label = tk.Label(inner, text="0/200", font=self._font_small,
                                    bg=self.BG_INPUT, fg=self.TEXT_MUTED)
        self._char_label.pack(side="left", padx=(6, 6))

        #  button
        send_btn = tk.Button(
            inner,
            text="Send",
            font=self._font_chip,
            bg=self.ACCENT,
            fg="#ffffff",
            relief="flat",
            bd=0,
            padx=14, pady=5,
            cursor="hand2",
            command=self._on_send,
        )
        send_btn.pack(side="left")
        send_btn.bind("<Enter>", lambda e: send_btn.configure(bg=self.ACCENT_DARK))
        send_btn.bind("<Leave>", lambda e: send_btn.configure(bg=self.ACCENT))

    #  Message rendering 

    def _post_user_message(self, text: str):
        self._add_bubble(text, role="user")

    def _post_bot_message(self, text: str):
        self._add_bubble(text, role="bot")

    def _add_bubble(self, text: str, role: str):
        """Add a single message bubble row to the message frame."""
        is_user = role == "user"
        timestamp = datetime.now().strftime("%I:%M %p")

        row = tk.Frame(self._msg_frame, bg=self.BG_MESSAGES)
        row.pack(fill="x", padx=12, pady=4, anchor="e" if is_user else "w")

        # Wrapper aligns bubble left or right
        wrapper = tk.Frame(row, bg=self.BG_MESSAGES)
        wrapper.pack(side="right" if is_user else "left")

        # Timestamp
        tk.Label(
            wrapper,
            text=timestamp,
            font=self._font_small,
            bg=self.BG_MESSAGES,
            fg=self.TEXT_TIME,
        ).pack(anchor="e" if is_user else "w", pady=(0, 2))

        # Bubble
        bubble = tk.Label(
            wrapper,
            text=text,
            font=self._font_body,
            bg=self.BUBBLE_USER if is_user else self.BUBBLE_BOT,
            fg=self.TEXT_USER if is_user else self.TEXT_BOT,
            wraplength=280,
            justify="left",
            padx=12, pady=8,
        )
        bubble.pack(anchor="e" if is_user else "w")

        self._scroll_to_bottom()

    #  handlers

    def _on_send(self):
        text = self._entry.get().strip()
        if not text:
            return
        self._entry.delete(0, tk.END)
        self._char_label.configure(text="0/200")
        self._post_user_message(text)
        # Schedule bot reply after a short delay to feel natural
        self._root.after(600, lambda: self._post_bot_message(self._bot.get_response(text)))

    def _on_chip_click(self, label: str):
        self._entry.delete(0, tk.END)
        self._entry.insert(0, label)
        self._on_send()

    def _on_key_release(self, event):
        count = len(self._entry.get())
        if count > 200:
            self._entry.delete(200, tk.END)
            count = 200
        self._char_label.configure(text=f"{count}/200")

    def _on_frame_configure(self, event):
        self._canvas.configure(scrollregion=self._canvas.bbox("all"))

    def _on_canvas_configure(self, event):
        self._canvas.itemconfig(self._canvas_window, width=event.width)

    def _on_mousewheel(self, event):
        self._canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")

    def _scroll_to_bottom(self):
        self._root.update_idletasks()
        self._canvas.yview_moveto(1.0)

#Enytry

def main():
    root = tk.Tk()
    ChatUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()
