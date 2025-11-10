# main_gui.py
import sys
import os
from PyQt5 import QtWidgets

# --- RUTA ABSOLUTA AL DIRECTORIO DEL PROYECTO ---
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(BASE_DIR)

from load.load_ventana_principal import Load_ventana_principal

def main():
    app = QtWidgets.QApplication(sys.argv)
    ventana = Load_ventana_principal()
    ventana.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()