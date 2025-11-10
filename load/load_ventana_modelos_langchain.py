from PyQt5 import QtWidgets, uic, QtCore
from PyQt5.QtCore import QPropertyAnimation, QRunnable, QThreadPool, pyqtSignal, QObject
from modelos.llmchain import ModeloLLMChain

class Signals(QObject):
    finished = pyqtSignal(str)
    error = pyqtSignal(str)

class Worker(QRunnable):
    def __init__(self, model, prompt):
        super().__init__()
        self.model = model
        self.prompt = prompt
        self.signals = Signals()

    def run(self):
        try:
            respuesta = self.model.generar(self.prompt)
            self.signals.finished.emit(respuesta)
        except Exception as e:
            self.signals.error.emit(str(e))

class Load_ventana_modelos_langchain(QtWidgets.QDialog):
    def __init__(self):
        super().__init__()
        uic.loadUi("interfaces/ventana_modelos_langchain.ui", self)
        self.setWindowFlag(QtCore.Qt.FramelessWindowHint)
        self.setWindowOpacity(1)

        self.boton_cerrar.clicked.connect(lambda: self.close())
        self.frame_superior.mouseMoveEvent = self.mover_ventana
        self.boton_menu.clicked.connect(self.mover_menu)
        self.boton_llm_chain.clicked.connect(self._ir_a_llm_chain)
        self.boton_enviar.clicked.connect(self.ejecutar_llm_chain)

        self._llm_chain_model = None
        self.threadpool = QThreadPool()

    def _ir_a_llm_chain(self):
        i_llm_chain = self.stackedWidget.indexOf(self.page_llm_chain)
        self.stackedWidget.setCurrentIndex(i_llm_chain)

    def ejecutar_llm_chain(self):
        prompt = self.imput_prompt.text().strip()
        if not prompt:
            QtWidgets.QMessageBox.warning(self, "Aviso", "Escribe un prompt primero.")
            return

        self._bloquear_boton(self.boton_enviar, "Procesando...")

        if self._llm_chain_model is None:
            try:
                self._llm_chain_model = ModeloLLMChain(model="gemini-2.5-flash")
            except Exception as e:
                QtWidgets.QMessageBox.critical(self, "Error", f"No se pudo cargar el modelo:\n{e}")
                self._desbloquear_boton(self.boton_enviar)
                return

        worker = Worker(self._llm_chain_model, prompt)
        worker.signals.finished.connect(self.mostrar_respuesta)
        worker.signals.error.connect(self.mostrar_error)
        self.threadpool.start(worker)

    def mostrar_respuesta(self, texto):
        self.output_response.setPlainText(texto)
        self._desbloquear_boton(self.boton_enviar)

    def mostrar_error(self, texto):
        self.output_response.setPlainText(f"Error: {texto}")
        self._desbloquear_boton(self.boton_enviar)

    def _bloquear_boton(self, btn, texto="Procesando..."):
        if btn:
            btn.setEnabled(False)
            btn.setText(texto)

    def _desbloquear_boton(self, btn):
        if btn:
            btn.setEnabled(True)
            btn.setText("Enviar")

    def mousePressEvent(self, event):
        self.clickPosition = event.globalPos()

    def mover_ventana(self, event):
        if not self.isMaximized():
            if event.buttons() == QtCore.Qt.LeftButton:
                self.move(self.pos() + event.globalPos() - self.clickPosition)
                self.clickPosition = event.globalPos()
                event.accept()
        if event.globalPos().y() <= 20:
            self.showMaximized()
        else:
            self.showNormal()

    def mover_menu(self):
        width = self.frame_lateral.width()
        normal = 0
        if width == 0:
            extender = 200
            self.boton_menu.setText("Menú")
        else:
            extender = normal
            self.boton_menu.setText("")
        self.animacion = QtCore.QPropertyAnimation(self.frame_lateral, b"minimumWidth")
        self.animacion.setDuration(300)
        self.animacion.setStartValue(width)
        self.animacion.setEndValue(extender)
        self.animacion.setEasingCurve(QtCore.QEasingCurve.InOutQuart)
        self.animacion.start()
        self.animacionb = QPropertyAnimation(self.boton_menu, b"minimumWidth")
        self.animacionb.setStartValue(width)
        self.animacionb.setEndValue(extender)
        self.animacionb.setEasingCurve(QtCore.QEasingCurve.InOutQuart)
        self.animacionb.start()