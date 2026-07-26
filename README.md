# Hyper-V Quick Toggle

## Italiano

Questa applicazione Python permette di visualizzare rapidamente lo stato di Hyper-V (attivato o disattivato) e di modificarlo con un semplice pulsante, senza dover digitare manualmente comandi PowerShell o bcdedit.

### Descrizione

L'applicazione verifica lo stato corrente di Hyper-V tramite `bcdedit` e consente di abilitarlo o disabilitarlo in modo semplice e visivo.
È pensata per chi ha la necessità di passare frequentemente tra Hyper-V attivo e disattivato, ad esempio per usare software incompatibili con l'hypervisor (emulatori, alcune VM, ecc.).

### Requisiti

1. Esecuzione con permessi di amministratore richiesti automaticamente all'avvio tramite prompt UAC.
2. Riavvio del computer dopo ogni cambio di stato per rendere effettiva l'impostazione.
3. Python 3.11 o superiore.

### Utilizzo

```bash
python Hyper-V.py
```

Oppure eseguire direttamente il file `.exe`.
All'avvio verrà richiesta automaticamente l'elevazione dei privilegi.

### Note

- Le modifiche vengono applicate tramite `bcdedit /set hypervisorlaunchtype`, non tramite PowerShell.
- In caso di errore durante la modifica, lo stato non viene alterato e viene mostrato un messaggio descrittivo.

### Sviluppo e test

```bash
pip install -e ".[dev]"
python -m pytest
```

### Motivazione

Questo progetto nasce dalla necessità di attivare e disattivare Hyper-V rapidamente, evitando di dover aprire un terminale e inserire manualmente i comandi ad ogni cambio.

---

## English

This Python application allows you to quickly view the status of Hyper-V (enabled or disabled) and change it with a simple button, without manually typing PowerShell or bcdedit commands.

### Description

The application checks the current Hyper-V status via `bcdedit` and allows you to enable or disable it through a clean graphical interface.
It is designed for users who frequently need to switch between Hyper-V being enabled or disabled, for example, to run software incompatible with the hypervisor (emulators, certain VMs, etc.).

### Requirements

1. Administrator privileges automatically requested at launch via UAC prompt.
2. A system restart after each status change to apply the new setting.
3. Python 3.11 or higher.

### Usage

```bash
python Hyper-V.py
```

Or run the `.exe` file directly (if available). Administrator elevation will be requested automatically on startup.

### Notes

- Changes are applied via `bcdedit /set hypervisorlaunchtype`, not via PowerShell.
- If an error occurs during the change, the state is left unaltered and a descriptive message is shown.

### Development & testing

```bash
pip install -e ".[dev]"
python -m pytest
```

### Motivation

This project was created to quickly enable and disable Hyper-V, avoiding the need to open a terminal and manually enter commands each time.

---

## Changelog

### v1.3.0

- **Refactoring architetturale**: il codice, prima in un unico file, è ora organizzato in un package `hyperv_toggle/` con separazione delle responsabilità (`system.py`, `theme.py`, `ui.py`, `constants.py`, `__main__.py`). `Hyper-V.py` resta come entry point di compatibilità.
- **Bug fix**: risolto il rilancio elevato (UAC) che falliva silenziosamente quando l'app veniva avviata da sorgente con `python Hyper-V.py`; il processo elevato partiva con working directory forzata su `System32` e non trovava più lo script. Ora viene passata esplicitamente la directory corretta a `ShellExecuteW`.
- Aggiunto script console `hyperv-toggle` in `pyproject.toml` per l'installazione via `pip install -e .`.
- **Test automatici**: aggiunta suite `pytest` (`tests/`) per il layer di sistema (`system.py`) e per la logica della UI (`ui.py`); eseguibile con `python -m pytest` dopo `pip install -e ".[dev]"`.

### v1.2.0

- **Threading**: tutte le operazioni di sistema (`bcdedit`, `shutdown`) vengono eseguite in thread separati, la UI non si congela più durante le operazioni.
- **Feedback visivo**: aggiunta progress bar indeterminata e messaggi di stato durante ogni operazione ("Lettura in corso...", "Impostazione in corso...", ecc.).
- **UAC robusta**: il relaunch con privilegi elevati ora verifica il valore di ritorno di `ShellExecuteW`; in caso di rifiuto o errore viene mostrato un messaggio chiaro all'utente.
- **Bug fix**: risolto blocco permanente della UI dopo il cambio di stato (progress bar infinita).
- **Bug fix**: risolto "Aggiorna stato" e "Riavvia PC" non selezionabili dopo un cambio di stato.
- Rimossa dipendenza da `sv-ttk`: il tema scuro è ora implementato con `ttk.Style` nativo.

### v1.1.0

- Refactoring generale del codice.
- Logica di lettura BCD estratta in funzione dedicata `get_hyperv_state()`.
- Aggiunta gestione `FileNotFoundError` in `run_command()`.
- Primo tentativo di auto-elevazione UAC tramite `ShellExecuteW`.
- Migliorato layout: separatori, padding uniforme, pulsanti a larghezza piena.
- Aggiunti type hint.
- Rimosso `after(300, update_status)` ridondante.
- I `messagebox` passano ora `parent=self`.

### v1.0.3

- Prima versione pubblica.
- Interfaccia grafica base con `tkinter` + `sv-ttk`.
- Lettura stato Hyper-V tramite `bcdedit`.
- Pulsanti Attiva / Disattiva / Riavvia.
