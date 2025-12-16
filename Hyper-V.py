import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from sv_ttk import set_theme
import ctypes
import subprocess

__version__ = "1.0.2"
__app_name__ = "Hyper-V Quick Toggle"
__author__ = "Mizu"

# --------------------------------------------------------
# Costanti
    
STATO_ON = "auto"
STATO_OFF = "off"

# --------------------------------------------------------
# Funzioni di sistema

def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False

def run_command(cmd_list):
    try:
        result = subprocess.run(
            cmd_list,
            capture_output=True,
            text=True,
            check=True,
            creationflags=subprocess.CREATE_NO_WINDOW
        )
        return result.stdout.strip()
    except subprocess.CalledProcessError as e:
        raise RuntimeError(e.stderr.strip())
    except Exception as e:
        raise RuntimeError(str(e))

def reboot():
    try:
        run_command(["shutdown", "/r", "/t", "0"])
    except Exception as e:
        messagebox.showerror("Errore", str(e))

def get_status():
    try:
        output = run_command(["bcdedit"])
        print(output)
        if("hypervisorlaunchtype    off" in output.lower()):
                messagebox.showinfo("Successo", f" Stato attuale: \"OFF\"")
        else:
            messagebox.showinfo("Successo", f" Stato attuale \"ON\"")
    except Exception as e:
        messagebox.showerror("Errore", str(e))

def set_hyperV(stato):
    try:        
        run_command(["bcdedit", "/set", "hypervisorlaunchtype", stato])
        messagebox.showinfo("Successo", f"Hyper-V portato a stato {stato}.\nRiavvia il PC per applicare la modifica.")
    except Exception as e:
        messagebox.showerror("Errore", str(e))

class HyperVApp(tk.Tk):
    
    # Label informativa
    def __init__(self):
        super().__init__()
        self.title("HyperV")
        self.geometry("400x275")
        self.minsize(380, 225)
        set_theme("dark")
        self.create_widgets()
    
    # Creazione della finestra principale dell'applicazione
    # Pulsanti per selezionare le varie opzioni
    def create_widgets(self):
        ttk.Label(self, text="Opzioni disponibili:").pack(pady=10)

        ttk.Button(self, text=f"Accendi HyperV ({STATO_ON})",
                   width=25, command=lambda: set_hyperV(STATO_ON)).pack(pady=5)

        ttk.Button(self, text=f"Spegni HyperV ({STATO_OFF})",
                   width=25, command=lambda: set_hyperV(STATO_OFF)).pack(pady=5)

        ttk.Button(self, text="Riavvia il PC", width=25, command=reboot).pack(pady=5)
        ttk.Button(self, text="Verifica HyperV", width=25, command=get_status).pack(pady=5)
        ttk.Button(self, text="Esci", width=25, command=self.destroy).pack(pady=5)

def main():
    
    # --------------------------------------------------------
    # Controllo privilegi di amministratore
    
    if not is_admin():
        messagebox.showerror("Errore",
            "Questo programma deve essere eseguito come amministratore.\n\n"
            "Clicca con il tasto destro e scegli: 'Esegui come amministratore'.")
        return
        
    # ----------------------------
    # Avvio del loop principale dell'interfaccia grafica
    app = HyperVApp()
    app.mainloop()
    
if __name__ == '__main__':
    main()