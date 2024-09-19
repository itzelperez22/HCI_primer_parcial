import uvicorn.config
from ventana_ui import *
import main
import uvicorn
from threading import Thread
import signal
from python_event_bus import EventBus

signal.signal(signal.SIGINT, signal.SIG_DFL)

window = None

class MainWindow(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self, *args, **kwargs):
        QtWidgets.QMainWindow.__init__(self, *args, **kwargs)
        self.setupUi(self)
        self.label.setText("Haz clic en el botón")
        self.pushButton.setText("Presióname")
        self.pushButton.clicked.connect(self.actualizar)

    def actualizar(self):
        self.label.setText("¡Acabas de hacer clic en el botón!")
        EventBus.call("QT5_say", "Presionaste el boton en QT")#Se llama al EventBus para anunciar al servidor que el botón fue presionado

@EventBus.on("websocket_say")
def WSConnect(message):
    global window
    window.label.setText(message)

def run_api(): #En esta función hacemos que el servidor de la ventana sea el mismo que usamos en main
    config = uvicorn.Config(main.app, host="127.0.0.1", port=8000)
    server = uvicorn.Server(config)
    server.run()

def run_QT5():
    global window
    app = QtWidgets.QApplication([])
    window = MainWindow()
    window.show()
    app.exec_()

if __name__ == "__main__":
    apiThread = Thread(target=run_api)
    apiThread.start()
    run_QT5()
    apiThread.join()
