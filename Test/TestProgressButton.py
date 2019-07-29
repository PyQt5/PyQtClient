from PyQt5.QtCore import QTimer
from PyQt5.QtWidgets import QWidget, QVBoxLayout

from Widgets.Buttons.ProgressButton import ProgressButton


class Window(QWidget):

    def __init__(self, *args, **kwargs):
        super(Window, self).__init__(*args, **kwargs)
        self.resize(246, 200)
        layout = QVBoxLayout(self, spacing=0)
        layout.setContentsMargins(0, 0, 0, 0)
        self.btn = ProgressButton('test',
                                  self, maximumHeight=36, minimumHeight=36, styleSheet='qproperty-circleColor: rgb(0, 255, 0);')
        layout.addWidget(self.btn)
    
        QTimer.singleShot(2000, lambda: self.btn.showWaiting(True))
 
        QTimer.singleShot(8000, lambda: self.btn.showWaiting(False))


if __name__ == '__main__':
    import sys
    from PyQt5.QtWidgets import QApplication
    app = QApplication(sys.argv)
    w = Window()
    w.show()
    sys.exit(app.exec_())
