import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from sv_ttk import set_theme
import ctypes
import subprocess

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

def set_hyperV(stato):
    try:
        #cmd = f'bcdedit /set hypervisorlaunchtype {stato}'
        #subprocess.run(["powershell", "-Command", cmd], check=True, creationflags=subprocess.CREATE_NO_WINDOW)
        
        subprocess.run(
            ["bcdedit", "/set", "hypervisorlaunchtype", stato],
            check=True,
            capture_output=True,
            creationflags=subprocess.CREATE_NO_WINDOW
        )
        
        messagebox.showinfo("Successo", f"Hyper-V portato a stato {stato}.\nRiavvia il PC per applicare la modifica.")
    
    except subprocess.CalledProcessError as e:
        messagebox.showerror("Errore", e.stderr.decode(errors="ignore"))
    except Exception as e:
        messagebox.showerror("Errore", str(e))

def reboot():
    try:
        subprocess.run(["shutdown", "/r", "/t", "0"], check=True, creationflags=subprocess.CREATE_NO_WINDOW)
    except Exception as e:
        messagebox.showerror("Errore", str(e))

def status():
    try:
        cmd = f'bcdedit /enum | findstr hypervisorlaunchtype'
        result = subprocess.run(["powershell", "-Command", cmd], capture_output=True, text=True, check=True, creationflags=subprocess.CREATE_NO_WINDOW)
        stato_attuale = result.stdout.strip()
        if(STATO_OFF in stato_attuale):
                messagebox.showinfo("Successo", f" Stato attuale: \"OFF\"")
        else:
            messagebox.showinfo("Successo", f" Stato attuale \"ON\"")
    except subprocess.CalledProcessError:
        messagebox.showerror("Errore", "Errore nell'esecuzione del comando.")
    except Exception as e:
        messagebox.showerror("Errore", str(e))

def main():
    
    # --------------------------------------------------------
    # Controllo privilegi di amministratore
    
    if not is_admin():
        messagebox.showerror("Errore",
            "Questo programma deve essere eseguito come amministratore.\n\n"
            "Clicca con il tasto destro e scegli: 'Esegui come amministratore'.")
        return
        
    # ----------------------------
    # Label informativa
    
    root = tk.Tk()
    root.title("HyperV")
    root.geometry("400x275")
    root.minsize(380, 225)
    
    set_theme("dark")
    
    # ----------------------------
    # Creazione della finestra principale dell'applicazione
    
    ttk.Label(root, text="Opzioni disponibili:").pack(pady=10)

    # ----------------------------
    # Pulsanti per selezionare le varie opzioni
    
    ttk.Button(root, text=f"Accendi HyperV ({STATO_ON})", width=25,
            command=lambda: set_hyperV(STATO_ON)).pack(pady=5)

    ttk.Button(root, text=f"Spegni HyperV ({STATO_OFF})", width=25,
            command=lambda: set_hyperV(STATO_OFF)).pack(pady=5)

    ttk.Button(root, text=f"Riavvia il PC", width=25,
            command=reboot).pack(pady=5)

    ttk.Button(root, text=f"Verifica HyperV", width=25,
            command=status).pack(pady=5)

    ttk.Button(root, text="Esci", width=25,
            command=root.destroy).pack(pady=5)

    # ----------------------------
    # Avvio del loop principale dell'interfaccia grafica

    root.mainloop()
    
if __name__ == '__main__':
    main()