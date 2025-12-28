import tkinter as tk
from tkinter import ttk, messagebox
from sv_ttk import set_theme
import ctypes
import subprocess
import sys

__version__ = "1.0.3"
__app_name__ = "Hyper-V Quick Toggle"
__author__ = "Mizu"

# ----------------------
# Costanti
STATO_ON = "auto"
STATO_OFF = "off"

# ----------------------
# Funzioni di sistema

def is_admin():
    """Verifica se l'app è eseguita come amministratore"""
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False

def run_command(cmd_list):
    """Esegue comandi di sistema con gestione"""
    try:
        result = subprocess.run(cmd_list, capture_output=True, text=True, check=True, creationflags=subprocess.CREATE_NO_WINDOW)
        return result.stdout.strip()
    except subprocess.CalledProcessError as e:
        raise RuntimeError(f"Errore comando {cmd_list}: {e.stderr.strip()}")
    except Exception as e:
        raise RuntimeError(str(e))

class HyperVApp(tk.Tk):
    
    def __init__(self):
        super().__init__()
        self.title(__app_name__)
        self.geometry("400x300")
        self.minsize(380, 250)
        set_theme("dark")

        self.status_label = ttk.Label(self, text="Stato non verificato", font=('Helvetica', 10, 'bold'),foreground="gray")
        self.status_label.pack(pady=10)
        
        self.create_widgets()
        self.update_status()

    def create_widgets(self):
        """Crea la finestra con i pulsanti principali"""
        ttk.Label(self, text="Gestione Hyper-V", font=('Helvetica', 12, 'bold')).pack(pady=10)
        self.btn_on = ttk.Button(self, text=f"Attiva Hyper-V ({STATO_ON})", width=25, command=lambda: self.set_hyperV(STATO_ON))
        self.btn_on.pack(pady=5)
        self.btn_off = ttk.Button(self, text=f"Disattiva Hyper-V ({STATO_OFF})", width=25,command=lambda: self.set_hyperV(STATO_OFF))
        self.btn_off.pack(pady=5)
        self.btn_on.state(["disabled"])
        self.btn_off.state(["disabled"])
        ttk.Button(self, text="Riavvia PC", width=25, command=self.reboot).pack(pady=5)
        ttk.Button(self, text="Aggiorna stato", width=25, command=self.update_status).pack(pady=5)
        ttk.Button(self, text="Esci", width=25, command=self.destroy).pack(pady=5)
        
    def update_status(self):
        """Aggiorna lo stato visibile nell'interfaccia"""
        try:
            output = run_command(["bcdedit"])
            for line in output.splitlines():
                if "hypervisorlaunchtype" in line.lower():
                    stato = line.split()[-1].lower()
                    self.status_label.config(text=f"Stato corrente: {stato.upper()}", foreground="green" if stato == "auto" else "orange")
                    
                    if stato == STATO_ON:
                        self.btn_on.state(["disabled"])
                        self.btn_off.state(["!disabled"])
                    elif stato == STATO_OFF:
                        self.btn_off.state(["disabled"])
                        self.btn_on.state(["!disabled"])
                    return
                
            self.status_label.config(text="Stato non rilevabile", foreground="red")
            
        except Exception as e:
            self.status_label.config(text="Errore nella verifica", foreground="red")
            messagebox.showerror("Errore", str(e))

    def set_hyperV(self, stato):
        """Modifica lo stato di Hyper-V con conferma utente"""
        if not messagebox.askyesno("Conferma azione", f"Confermi di voler impostare Hyper-V a '{stato}'?\n"
                                   "L'applicazione richiede un riavvio per completare l'operazione."):
            self.after(300, self.update_status)
            return
            
        try:
            run_command(["bcdedit", "/set", "hypervisorlaunchtype", stato])
            self.status_label.config(text=f"Stato impostato: {stato.upper()}", foreground="blue")
            messagebox.showinfo("Successo", f"Hyper-V impostato su '{stato}'.\n"
                                "Riavvia il PC per completare l'operazione.")
        except Exception as e:
            messagebox.showerror("Errore", str(e))
        finally:
            self.after(300, self.update_status)

    def reboot(self):
        """Riavvia il sistema con conferma utente"""
        if not messagebox.askyesno("Conferma riavvio", "Confermi il riavvio del sistema per completare le modifiche?"):
            return
            
        try:
            run_command(["shutdown", "/r", "/t", "0"])
        except Exception as e:
            messagebox.showerror("Errore", f"Non è stato possibile avviare il riavvio: {str(e)}")

def main():
    """Funzione principale con controllo privilegi"""
    if not is_admin():
        messagebox.showerror("Privilegi insufficienti", "L'applicazione deve essere eseguita come amministratore.")
        sys.exit(1)
    
    app = HyperVApp()
    app.mainloop()

if __name__ == "__main__":
    main()
