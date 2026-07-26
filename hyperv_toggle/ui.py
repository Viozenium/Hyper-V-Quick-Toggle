"""Finestra principale dell'applicazione (Tkinter)."""

import threading
import tkinter as tk
from tkinter import messagebox, ttk

from . import __app_name__
from .constants import (
    ACCENT_BLUE,
    ACCENT_GRAY,
    ACCENT_GREEN,
    ACCENT_ORA,
    ACCENT_RED,
    DARK_BG,
    STATO_OFF,
    STATO_ON,
)
from .system import get_hyperv_state, run_command
from .theme import apply_dark_theme


class HyperVApp(tk.Tk):

    def __init__(self) -> None:
        super().__init__()
        self.title(__app_name__)
        self.geometry("420x360")
        self.minsize(380, 340)
        self.resizable(True, False)
        self.configure(bg=DARK_BG)
        self._busy = False

        apply_dark_theme(self)
        self._build_ui()
        self.update_status()

    # ----------------------
    # Costruzione UI

    def _build_ui(self) -> None:
        pad = {"padx": 20, "pady": 5}

        ttk.Label(self, text="Gestione Hyper-V", style="Title.TLabel").pack(
            pady=(18, 4)
        )
        ttk.Separator(self, orient="horizontal").pack(fill="x", padx=20, pady=(0, 8))

        self.status_label = ttk.Label(
            self,
            text="Lettura in corso...",
            style="Status.TLabel",
            foreground=ACCENT_GRAY,
        )
        self.status_label.pack(**pad)

        self.progress = ttk.Progressbar(self, mode="indeterminate", length=200)
        self.progress.pack(pady=(0, 4))
        self.progress.pack_forget()

        ttk.Separator(self, orient="horizontal").pack(fill="x", padx=20, pady=8)

        btn_frame = ttk.Frame(self)
        btn_frame.pack(fill="x", padx=20)

        self.btn_on = ttk.Button(
            btn_frame,
            text=f"✔  Attiva Hyper-V  ({STATO_ON})",
            command=lambda: self._set_hyperv(STATO_ON),
        )
        self.btn_on.pack(fill="x", pady=3)

        self.btn_off = ttk.Button(
            btn_frame,
            text=f"✖  Disattiva Hyper-V  ({STATO_OFF})",
            command=lambda: self._set_hyperv(STATO_OFF),
        )
        self.btn_off.pack(fill="x", pady=3)

        ttk.Separator(self, orient="horizontal").pack(fill="x", padx=20, pady=8)

        aux_frame = ttk.Frame(self)
        aux_frame.pack(fill="x", padx=20)

        self.btn_refresh = ttk.Button(
            aux_frame, text="○  Aggiorna stato", command=self.update_status
        )
        self.btn_refresh.pack(fill="x", pady=2)

        self.btn_reboot = ttk.Button(
            aux_frame, text="⟳  Riavvia PC", command=self._reboot
        )
        self.btn_reboot.pack(fill="x", pady=2)

        ttk.Button(aux_frame, text="✕  Esci", command=self.destroy).pack(
            fill="x", pady=2
        )

        self.btn_on.state(["disabled"])
        self.btn_off.state(["disabled"])

    # ----------------------
    # Gestione busy state

    def _set_busy(self, busy: bool) -> None:
        """Mostra/nasconde la progress bar e blocca/sblocca i pulsanti."""
        self._busy = busy
        if busy:
            self.progress.pack(pady=(0, 4))
            self.progress.start(12)
            for btn in (self.btn_on, self.btn_off, self.btn_refresh, self.btn_reboot):
                btn.state(["disabled"])
        else:
            self.progress.stop()
            self.progress.pack_forget()
            self.btn_refresh.state(["!disabled"])
            self.btn_reboot.state(["!disabled"])

    # ----------------------
    # Logica con threading

    def update_status(self) -> None:
        """Legge lo stato di Hyper-V in un thread separato."""
        if self._busy:
            return
        self._set_busy(True)
        self.status_label.config(text="Lettura in corso...", foreground=ACCENT_GRAY)
        threading.Thread(target=self._worker_read_status, daemon=True).start()

    def _worker_read_status(self) -> None:
        """Eseguito nel thread secondario: legge lo stato e notifica la UI."""
        try:
            stato = get_hyperv_state()
            self.after(0, self._on_status_read, stato, None)
        except Exception as e:
            self.after(0, self._on_status_read, None, str(e))

    def _on_status_read(self, stato: str | None, error: str | None) -> None:
        """Callback sul thread UI dopo la lettura dello stato."""
        self._set_busy(False)

        if error:
            self.status_label.config(
                text="Errore nella verifica", foreground=ACCENT_RED
            )
            messagebox.showerror("Errore", error, parent=self)
            return

        if stato is None:
            self.status_label.config(text="Stato non rilevabile", foreground=ACCENT_RED)
            return

        colore = ACCENT_GREEN if stato == STATO_ON else ACCENT_ORA
        self.status_label.config(
            text=f"Stato corrente: {stato.upper()}", foreground=colore
        )

        if stato == STATO_ON:
            self.btn_on.state(["disabled"])
            self.btn_off.state(["!disabled"])
        else:
            self.btn_off.state(["disabled"])
            self.btn_on.state(["!disabled"])

    def _set_hyperv(self, stato: str) -> None:
        """Mostra conferma, poi imposta Hyper-V in un thread separato."""
        if self._busy:
            return
        azione = "attivare" if stato == STATO_ON else "disattivare"
        if not messagebox.askyesno(
            "Conferma azione",
            f"Confermi di voler {azione} Hyper-V?\n\n"
            "Sarà necessario riavviare il PC per applicare le modifiche.",
            parent=self,
        ):
            return

        self._set_busy(True)
        self.status_label.config(
            text=f"Impostazione Hyper-V su '{stato}'...", foreground=ACCENT_BLUE
        )
        threading.Thread(
            target=self._worker_set_hyperv, args=(stato,), daemon=True
        ).start()

    def _worker_set_hyperv(self, stato: str) -> None:
        try:
            run_command(["bcdedit", "/set", "hypervisorlaunchtype", stato])
            self.after(0, self._on_set_done, stato, None)
        except Exception as e:
            self.after(0, self._on_set_done, stato, str(e))

    def _on_set_done(self, stato: str, error: str | None) -> None:
        """Callback sul thread UI dopo la modifica dello stato."""
        self._set_busy(False)
        if error:
            messagebox.showerror("Errore", error, parent=self)
        else:
            messagebox.showinfo(
                "Operazione completata",
                f"Hyper-V impostato su '{stato}'.\nRiavvia il PC per applicare le modifiche.",
                parent=self,
            )
        self.update_status()

    def _reboot(self) -> None:
        """Riavvia il sistema con conferma utente."""
        if self._busy:
            return
        if not messagebox.askyesno(
            "Conferma riavvio",
            "Vuoi riavviare il sistema adesso?\nAssicurati di aver salvato tutto il lavoro.",
            parent=self,
        ):
            return

        self._set_busy(True)
        self.status_label.config(text="Riavvio in corso...", foreground=ACCENT_ORA)
        threading.Thread(target=self._worker_reboot, daemon=True).start()

    def _worker_reboot(self) -> None:
        try:
            run_command(["shutdown", "/r", "/t", "0"])
        except Exception as e:
            self.after(
                0,
                lambda: (
                    self._set_busy(False),
                    messagebox.showerror("Errore riavvio", str(e), parent=self),
                    self.update_status(),
                ),
            )
