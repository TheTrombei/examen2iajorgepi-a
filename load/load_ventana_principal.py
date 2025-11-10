# load/load_ventana_principal.py
from PyQt5 import QtWidgets, uic
from .load_ventana_modelos_basicos import Load_ventana_modelos_basicos
from .load_ventana_modelos_langchain import Load_ventana_modelos_langchain

class Load_ventana_principal(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi("interfaces/ventana_principal.ui", self)
        self.showMaximized()

        # Conectar acciones del menú
        self.actionbasicos.triggered.connect(self.abrirventanabasico)
        self.actionlangchain_2.triggered.connect(self.abrirventanalangchain)
        self.actionsalir.triggered.connect(self.cerrarVentana)

    def abrirventanabasico(self):
        self.basicos = Load_ventana_modelos_basicos()
        self.basicos.show()
        # Centrar el diálogo sobre la ventana principal
        self.basicos.move(
            self.geometry().center() - self.basicos.rect().center()
        )

    def abrirventanalangchain(self):
        self.basicos = Load_ventana_modelos_langchain()
        self.basicos.show()
        # Centrar el diálogo sobre la ventana principal
        self.basicos.move(
            self.geometry().center() - self.basicos.rect().center()
        )


    def cerrarVentana(self):
        self.close()