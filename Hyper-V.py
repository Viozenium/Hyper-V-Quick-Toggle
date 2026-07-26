"""Entry point di compatibilità: esegue il package hyperv_toggle.

Mantiene funzionante l'invocazione `python Hyper-V.py` (e il file .spec di PyInstaller) dopo la riorganizzazione del codice in moduli separati per responsabilità (system, theme, ui) sotto hyperv_toggle/.
"""

from hyperv_toggle.__main__ import main

if __name__ == "__main__":
    main()
