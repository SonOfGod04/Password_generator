#!/usr/bin/env python3
"""Tkinter front end for the password generator.

The password is shown in a read-only field (never in a dialog) and the
clipboard is cleared automatically after a delay.
"""
from __future__ import annotations

import tkinter as tk
from tkinter import ttk

from password_core import (
    DEFAULT_LENGTH, MAX_LENGTH, MIN_LENGTH,
    estimate_entropy_bits, generate_password, strength_label,
)

CLIPBOARD_CLEAR_MS = 30_000


# --------------------------------------------------------------------------
class PasswordApp(ttk.Frame):
    def __init__(self, root: tk.Tk) -> None:
        super().__init__(root, padding=16)
        self.root = root
        self._clear_job: str | None = None

        self.length = tk.IntVar(value=DEFAULT_LENGTH)
        self.lower = tk.BooleanVar(value=True)
        self.upper = tk.BooleanVar(value=True)
        self.digits = tk.BooleanVar(value=True)
        self.symbols = tk.BooleanVar(value=True)
        self.no_ambiguous = tk.BooleanVar(value=False)
        self.password = tk.StringVar()
        self.status = tk.StringVar()

        self._build()
        self.grid(sticky="nsew")
        self.generate()

    def _build(self) -> None:
        self.columnconfigure(0, weight=1)

        row = ttk.Frame(self)
        row.grid(sticky="ew")
        ttk.Label(row, text="Length").pack(side="left")
        ttk.Spinbox(
            row, from_=MIN_LENGTH, to=MAX_LENGTH, width=5,
            textvariable=self.length, command=self.generate,
        ).pack(side="left", padx=8)

        for text, var in (
            ("Lowercase (a-z)", self.lower),
            ("Uppercase (A-Z)", self.upper),
            ("Digits (0-9)", self.digits),
            ("Symbols (!@#...)", self.symbols),
            ("Avoid look-alikes (I, l, 1, O, 0)", self.no_ambiguous),
        ):
            ttk.Checkbutton(self, text=text, variable=var,
                            command=self.generate).grid(sticky="w", pady=1)

        ttk.Entry(self, textvariable=self.password, state="readonly",
                  font=("Consolas", 12), justify="center"
                  ).grid(sticky="ew", pady=(12, 4))
        ttk.Label(self, textvariable=self.status).grid(sticky="w")

        buttons = ttk.Frame(self)
        buttons.grid(sticky="ew", pady=(10, 0))
        buttons.columnconfigure((0, 1), weight=1)
        ttk.Button(buttons, text="Generate", command=self.generate
                   ).grid(row=0, column=0, sticky="ew", padx=(0, 4))
        ttk.Button(buttons, text="Copy", command=self.copy
                   ).grid(row=0, column=1, sticky="ew", padx=(4, 0))

        self.root.bind("<Return>", lambda _e: self.generate())

    def _options(self) -> dict[str, bool]:
        return dict(
            lower=self.lower.get(), upper=self.upper.get(),
            digits=self.digits.get(), symbols=self.symbols.get(),
            exclude_ambiguous=self.no_ambiguous.get(),
        )

    def generate(self) -> None:
        try:
            length = self.length.get()  # raises TclError on non-integer input
            options = self._options()
            self.password.set(generate_password(length, **options))
        except (tk.TclError, ValueError) as exc:
            self.password.set("")
            msg = "Length must be a whole number." if isinstance(exc, tk.TclError) else str(exc)
            self.status.set(msg)
            return
        bits = estimate_entropy_bits(length, **options)
        self.status.set(f"Strength: {strength_label(bits)} (~{bits:.0f} bits)")

    def copy(self) -> None:
        pw = self.password.get()
        if not pw:
            return
        self.root.clipboard_clear()
        self.root.clipboard_append(pw)
        self.status.set(f"Copied. Clipboard clears in {CLIPBOARD_CLEAR_MS // 1000}s.")
        if self._clear_job:
            self.root.after_cancel(self._clear_job)
        self._clear_job = self.root.after(CLIPBOARD_CLEAR_MS, self._clear_clipboard, pw)

    def _clear_clipboard(self, copied: str) -> None:
        self._clear_job = None
        try:
            # Only clear if the user hasn't copied something else since.
            if self.root.clipboard_get() == copied:
                self.root.clipboard_clear()
        except tk.TclError:
            pass  # clipboard empty or unavailable


def main() -> None:
    root = tk.Tk()
    root.title("Password Generator")
    root.resizable(False, False)
    PasswordApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
