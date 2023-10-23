from PyQt5.QtWidgets import QWidget, QLabel, QPushButton

class TextDisplay(QWidget):
    """
    Text Display widget
    """
    def __init__(self,text, *args, **kwargs):
        super().__init__()
        self.label = QLabel(self)
        self.label.setWordWrap(True)
        self.label.setText(text)
        return None
    
    def setTextDsiplay(self, txt):
        """
        Modify the text in the label
        """
        self.label.setText(txt)
        self.label.adjustSize()
        return None

class CustomButton(QWidget):
    """
    Buttin widget
    """
    def __init__(self,name,func, *args, **kwargs):
        super().__init__()
        self.button= QPushButton(name, self)
        self.button.setCheckable(False)
        self.button.clicked.connect(func)
    