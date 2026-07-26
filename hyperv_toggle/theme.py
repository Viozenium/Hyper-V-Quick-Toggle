"""Tema grafico dark per l'interfaccia ttk."""

import tkinter as tk
from tkinter import ttk

from .constants import ACCENT_BLUE, DARK_BG, DARK_BTN, DARK_BTN_ACT, DARK_FG, FONT


def apply_dark_theme(root: tk.Tk) -> None:
    style = ttk.Style(root)
    style.theme_use("clam")
    style.configure(
        ".",
        background=DARK_BG,
        foreground=DARK_FG,
        fieldbackground=DARK_BG,
        troughcolor=DARK_BG,
        bordercolor="#444",
        darkcolor=DARK_BG,
        lightcolor=DARK_BG,
        relief="flat",
        font=(FONT, 10),
    )
    style.configure(
        "TButton",
        background=DARK_BTN,
        foreground=DARK_FG,
        padding=(10, 6),
        relief="flat",
        borderwidth=0,
    )
    style.map(
        "TButton",
        background=[("active", DARK_BTN_ACT), ("disabled", "#1a1a1a")],
        foreground=[("disabled", "#555")],
    )
    style.configure("TLabel", background=DARK_BG, foreground=DARK_FG)
    style.configure(
        "Title.TLabel",
        background=DARK_BG,
        foreground=DARK_FG,
        font=(FONT, 13, "bold"),
    )
    style.configure("Status.TLabel", background=DARK_BG, font=(FONT, 10, "bold"))
    style.configure("TSeparator", background="#444")
    style.configure(
        "TProgressbar",
        troughcolor=DARK_BG,
        background=ACCENT_BLUE,
        bordercolor=DARK_BG,
        lightcolor=ACCENT_BLUE,
        darkcolor=ACCENT_BLUE,
    )
