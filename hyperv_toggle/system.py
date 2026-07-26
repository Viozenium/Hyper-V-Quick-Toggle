"""Interazione con il sistema operativo: privilegi, elevazione UAC, bcdedit."""

import ctypes
import os
import subprocess
import sys


def is_admin() -> bool:
    try:
        return bool(ctypes.windll.shell32.IsUserAnAdmin())
    except Exception:
        return False


def elevate_and_relaunch() -> bool:
    """
    Tenta il relaunch con privilegi elevati tramite UAC.
    Restituisce True se il relaunch è stato avviato, False se l'utente
    ha rifiutato o si è verificato un errore.
    """
    try:
        script_dir = os.path.dirname(os.path.abspath(sys.argv[0]))
        ret = ctypes.windll.shell32.ShellExecuteW(
            None,
            "runas",
            sys.executable,
            " ".join(f'"{a}"' for a in sys.argv),
            script_dir,
            1,
        )
        return int(ret) > 32
    except Exception:
        return False


def run_command(cmd_list: list[str]) -> str:
    """Esegue un comando di sistema e restituisce stdout."""
    try:
        result = subprocess.run(
            cmd_list,
            capture_output=True,
            text=True,
            check=True,
            creationflags=subprocess.CREATE_NO_WINDOW,
        )
        return result.stdout.strip()
    except subprocess.CalledProcessError as e:
        raise RuntimeError(e.stderr.strip() or f"Comando fallito: {' '.join(cmd_list)}")
    except FileNotFoundError:
        raise RuntimeError(f"Comando non trovato: {cmd_list[0]}")


def get_hyperv_state() -> str | None:
    """
    Legge lo stato attuale di hypervisorlaunchtype da bcdedit.
    Restituisce la stringa dello stato oppure None se non trovata.
    """
    output = run_command(["bcdedit"])
    for line in output.splitlines():
        if "hypervisorlaunchtype" in line.lower():
            parts = line.split()
            return parts[-1].lower() if parts else None
    return None
