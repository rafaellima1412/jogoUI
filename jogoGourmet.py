import sys
from PyQt5 import QtCore
from PyQt5 import QtWidgets
from PyQt5.QtGui import QBrush, QIcon, QImage, QPalette, QPixmap
from PyQt5.QtWidgets import QInputDialog, QMainWindow, QApplication, QPushButton, QLineEdit, QMessageBox
from PyQt5.QtCore import QDir, QSize
from decideprato import DecidePrato

class App(QMainWindow):

    def __init__(self, root):
        super().__init__()
        self.title = 'Jogo Gourmet'
        self.left = 100
        self.top = 100
        self.width = 400
        self.height = 140
        self.arvoredecisao = root
        self.initUI()

    def procura_resposta(self):
        resposta = self.arvoredecisao
        #Aqui a arvore de desição tenta advinhar o prato ela tbm avalia se o no ainda estar no começo
        while not resposta.inicio():
            #aqui precisa fazer melhoria para não inserir  vazio
            buttonReply = QMessageBox.question(self, 'O prato que você pensou é', resposta.data , QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
            if buttonReply == QMessageBox.Yes:
                resposta = resposta.left
            else:
                resposta = resposta.right
        return resposta

    def acertou(self):
        dlg = QMessageBox(self)
        dlg.setWindowTitle("Yes!")
        dlg.setText("Acertei novamente!!")
        button = dlg.exec()
        if button == QMessageBox.Ok:
            print("OK!")

        
    def jogar_de_novo(self):       
        buttonReply = QMessageBox.question(self, 'UHUuu!', " Ainda que jogar?", 
        QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if buttonReply == QMessageBox.Yes:
            return True   
        else:
            return False      

    
    def nova_comida(self, guess):
        novoPrato, ok = QInputDialog().getText(self, "pergunta",
                                     "Qual é o nome da comida? ", QLineEdit.Normal,
                                     QDir().home().dirName())
        try:
            if ok and novoPrato:   
                    novoTipo, ok = QInputDialog().getText(self, "pergunta",
                                        "Qual é o tipo de comida? ", QLineEdit.Normal,
                                        QDir().home().dirName())

            if ok and novoTipo:
                    return (novoPrato, novoTipo)
        except:
            print('não escreveu nada então voce gosta de pudim doce!!')
            return ('pudim ', 'doce')

    
    def adiciona_comida(self, arvoredecisao, comida, tipo):
        arvoredecisao.right = DecidePrato(arvoredecisao.data)
        arvoredecisao.left = DecidePrato(comida)
        arvoredecisao.data = tipo
        
    
    def initUI(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)
        #icone
        self.setWindowIcon(QIcon("ico.png"))
        #imagem png
        oImage = QImage("ico.png")
        sImage = oImage.scaled(QSize(400,140))
        palette = QPalette()
        palette.setBrush(10, QBrush(sImage))
        # esse 10 acima é a propriedade Window role, veja o manual da Qt
        self.setPalette(palette)

        #create label
        self.label = QtWidgets.QLabel('Pense em um prato e divirta-se!', self)
        self.label.setStyleSheet("background-color: rgb(33, 33, 33, 0.2);"
                                    "border-color: rgb(18, 18, 18);"
                                        "color: rgb(255, 255, 255);"
                            "font: bold italic 16pt 'Times New Roman';")
        self.label.setGeometry(QtCore.QRect(80, 0, 290, 80))

        # Create a button in the window
        self.button = QPushButton('Começar', self)
        self.button.setStyleSheet("background-color: rgb(210,105,30, 0.5);"
                                    "border-color: rgb(139,69,19);"
                                        "color: rgb(255, 255, 255);"
                            "font: bold italic 16pt 'Times New Roman';")
        self.button.move(160,80)

        # connect button to function on_click
        self.button.clicked.connect(self.on_click)
        self.show()
   
    def on_click(self):
        playAgain = True
        while playAgain:
            resposta = self.procura_resposta()
            acertou = QMessageBox.question(self, 'Então o prato que você pensou é', resposta.data , QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
            if acertou  == QMessageBox.Yes:
                self.acertou()
                # melhoria para saber se usuario quer jogar de novo
                playAgain = self.jogar_de_novo()
                continue
            (comida, tipo) = self.nova_comida(resposta)
            if not resposta.inicio():
                continue
            self.adiciona_comida(resposta, comida, tipo)
            # melhoria para saber se usuario quer jogar de novo
            playAgain = self.jogar_de_novo()  
        

if __name__ == '__main__':
    inicio = DecidePrato("Massa", DecidePrato("Lasanha"),
                         DecidePrato("Bolo de Chocolate"))
    app = QApplication(sys.argv)
    ex = App(inicio)
    sys.exit(app.exec_())