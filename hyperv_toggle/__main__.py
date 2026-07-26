"""Entry point dell'applicazione: gestisce l'elevazione UAC e avvia la UI."""

import sys
import tkinter as tk
from tkinter import messagebox

from .system import elevate_and_relaunch, is_admin
from .ui import HyperVApp


def main() -> None:
    if not is_admin():
        relaunched = elevate_and_relaunch()
        if not relaunched:
            root = tk.Tk()
            root.withdraw()
            messagebox.showerror(
                "Privilegi insufficienti",
                "L'applicazione richiede privilegi di amministratore.\n\n"
                "Riavviala manualmente con 'Esegui come amministratore'.",
            )
            root.destroy()
        sys.exit(0)

    app = HyperVApp()
    app.mainloop()


if __name__ == "__main__":
    main()
