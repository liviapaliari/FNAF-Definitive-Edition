from PyQt5.QtWidgets import QMainWindow, QApplication, QLabel, QPushButton, QLineEdit
from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent
from PyQt5.QtCore import QUrl, QTimer
from PyQt5 import uic, QtGui
from random import randint
import sys
import os

class Menu(QMainWindow):
    def __init__(self):
        super(Menu, self).__init__()
        uic.loadUi("screen_ui/Menu.ui", self)

        # Define Widgets
        self.background = self.findChild(QLabel, "lb_background")
        self.btn_forca = self.findChild(QPushButton, "btn_forca")
        self.btn_velha = self.findChild(QPushButton, "btn_velha")
        self.btn_jokenpo = self.findChild(QPushButton, "btn_jokenpo")
        self.btn_sair = self.findChild(QPushButton, "btn_sair")

        # Button Functions
        self.btn_forca.clicked.connect(self.abrir_forca)
        self.btn_velha.clicked.connect(self.abrir_velha)
        self.btn_jokenpo.clicked.connect(self.abrir_jokenpo)
        self.btn_sair.clicked.connect(self.sair)

        # Music Player
        self.player = QMediaPlayer()
        self.musica_menu()

        # Show the App
        self.show()

    # Functions
    def musica_menu(self):
        arquivo = os.path.join(os.getcwd(), "audio/fnaf_1.mp3")
        url = QUrl.fromLocalFile(arquivo)
        conteudo = QMediaContent(url)
        self.player.setMedia(conteudo)
        self.player.play()

    def abrir_forca(self):
        self.player.stop()
        self.forca = Forca()
        self.forca.show()
        self.hide()

    def abrir_velha(self):
        self.player.stop()
        self.velha = Velha()
        self.velha.show()
        self.hide()

    def abrir_jokenpo(self):
        self.player.stop()
        self.jokenpo = Jokenpo()
        self.jokenpo.show()
        self.hide()

    def sair(self):
        self.close()

class Forca(QMainWindow):
    def __init__(self):
        super(Forca, self).__init__()
        uic.loadUi("screen_ui/Forca.ui", self)

        # Define Widgets Forca
        self.background = self.findChild(QLabel, "lb_background")
        self.lb_letras = self.findChild(QLabel, "lb_letras")
        self.lb_dica = self.findChild(QLabel, "lb_dica")
        self.lb_palavra = self.findChild(QLabel, "lb_palavra")
        self.lb_vidas = self.findChild(QLabel, "lb_vidas")
        self.btn_menu = self.findChild(QPushButton, "btn_forcaMenu")
        self.btn_enviar = self.findChild(QPushButton, "btn_enviar")
        self.txt_letra = self.findChild(QLineEdit, "txt_letra")

        # Button Functions
        self.btn_menu.clicked.connect(self.abrir_menu)
        self.btn_enviar.clicked.connect(self.enviar)

        # Programação Back-End
        lista_palavras = ["MARFIM", "BARTENDER", "PELICANO", "CANDELABRO", "CIRIGUELA", "DESFIBRILADOR"]
        lista_dicas = ["Cor", "Profissão", "Animal", "Objeto", "Fruta", "Saúde"]
        self.forca = []
        self.letras_usadas = []
        self.vidas = 5

        aleatorio = randint(0, len(lista_palavras) - 1)
        self.palavra_atual = lista_palavras[aleatorio]

        for letra in range(len(self.palavra_atual)):
            self.forca.append("_")
            self.lb_palavra.setText("_ " * len(self.palavra_atual))

        # Music Player
        self.player = QMediaPlayer()
        self.player_cortina = QMediaPlayer()
        self.musica_forca("audio/fnaf_2.mp3")

        self.lb_dica.setText(lista_dicas[aleatorio])
        self.lb_vidas.setText(str(self.vidas))

        self.txt_letra.setFocus()

    def enviar(self):
        letra = self.txt_letra.text().upper().strip()
        texto = ""
        letras = ""
        if letra == self.palavra_atual:
            self.venceu()

        if letra != "" and len(letra) == 1:
            if letra not in self.letras_usadas:
                self.letras_usadas.append(letra)

            for contador in range(len(self.letras_usadas)):
                letras += self.letras_usadas[contador]

            for index, letrinha in enumerate(self.palavra_atual):
                if letrinha == letra:
                    self.forca[index] = letra

            for letrinha in self.forca:
                texto += str(letrinha) + " "

            if letra not in self.palavra_atual:
                self.musica_cortina()
                self.vidas -= 1

            self.lb_palavra.setText(texto)
            self.lb_vidas.setText(str(self.vidas))
            self.lb_letras.setText(letras)
            self.mudar_background()
        self.txt_letra.setText("")
        self.txt_letra.setFocus()
        self.verificar_palavra()

    def verificar_palavra(self):
        palavra_digitada = ""

        for contador in range(len(self.forca)):
            palavra_digitada += self.forca[contador]

        if palavra_digitada == self.palavra_atual:
            self.venceu()

    def venceu(self):
        uic.loadUi("screen_ui/F_Venceu.ui", self)
        self.musica_forca("audio/6am_bells.mp3")
        self.btn_vnovamente = self.findChild(QPushButton, "btn_fvenceuNovamente")
        self.btn_vmenu = self.findChild(QPushButton, "btn_fvenceuMenu")
        self.btn_vnovamente.clicked.connect(menu.abrir_forca)
        self.btn_vmenu.clicked.connect(self.abrir_menu)

    def mudar_background(self):
        if self.vidas == 4:
            self.background.setPixmap(QtGui.QPixmap("screen/forca_2.png"))
        elif self.vidas == 3:
            self.background.setPixmap(QtGui.QPixmap("screen/forca_3.png"))
        elif self.vidas == 2:
            self.background.setPixmap(QtGui.QPixmap("screen/forca_4.png"))
        elif self.vidas == 1:
            self.background.setPixmap(QtGui.QPixmap("screen/forca_5.png"))
        elif self.vidas == 0:
            uic.loadUi("screen_ui/F_Perdeu.ui", self)
            self.musica_forca("audio/jumpscare_foxy.mp3")
            self.btn_pnovamente = self.findChild(QPushButton, "btn_fperdeuNovamente")
            self.btn_pmenu = self.findChild(QPushButton, "btn_fperdeuMenu")
            self.btn_pnovamente.clicked.connect(menu.abrir_forca)
            self.btn_pmenu.clicked.connect(self.abrir_menu)

    def keyPressEvent(self, event):
        self.enviar()

    def musica_forca(self, caminho):
        arquivo = os.path.join(os.getcwd(), caminho)
        url = QUrl.fromLocalFile(arquivo)
        conteudo = QMediaContent(url)
        self.player.setMedia(conteudo)
        self.player.play()

    def musica_cortina(self):
        arquivo = os.path.join(os.getcwd(), "audio/curtains_closing.mp3")
        url = QUrl.fromLocalFile(arquivo)
        conteudo = QMediaContent(url)
        self.player_cortina.setMedia(conteudo)
        self.player_cortina.play()

    def abrir_menu(self):
        self.player.stop()
        menu.musica_menu()
        menu.show()
        self.close()

class Velha(QMainWindow):
    def __init__(self):
        super(Velha, self).__init__()
        uic.loadUi("screen_ui/Velha.ui", self)

        # Define Widgets
        self.lb_usuario = self.findChild(QLabel, "lb_usuario")
        self.lb_computador = self.findChild(QLabel, "lb_computador")
        self.btn_menu = self.findChild(QPushButton, "btn_velhaMenu")
        self.btn_reset = self.findChild(QPushButton, "btn_velhaReset")
        self.btn_1x1 = self.findChild(QPushButton, "btn_1x1")
        self.btn_1x2 = self.findChild(QPushButton, "btn_1x2")
        self.btn_1x3 = self.findChild(QPushButton, "btn_1x3")
        self.btn_2x1 = self.findChild(QPushButton, "btn_2x1")
        self.btn_2x2 = self.findChild(QPushButton, "btn_2x2")
        self.btn_2x3 = self.findChild(QPushButton, "btn_2x3")
        self.btn_3x1 = self.findChild(QPushButton, "btn_3x1")
        self.btn_3x2 = self.findChild(QPushButton, "btn_3x2")
        self.btn_3x3 = self.findChild(QPushButton, "btn_3x3")

        # Button Functions
        self.btn_menu.clicked.connect(self.abrir_menu)
        self.btn_reset.clicked.connect(self.reset)
        self.btn_1x1.clicked.connect(self.f1x1)
        self.btn_1x2.clicked.connect(self.f1x2)
        self.btn_1x3.clicked.connect(self.f1x3)
        self.btn_2x1.clicked.connect(self.f2x1)
        self.btn_2x2.clicked.connect(self.f2x2)
        self.btn_2x3.clicked.connect(self.f2x3)
        self.btn_3x1.clicked.connect(self.f3x1)
        self.btn_3x2.clicked.connect(self.f3x2)
        self.btn_3x3.clicked.connect(self.f3x3)

        # Programação Back-End
        self.lista_indisponiveis = []
        self.tabuleiro = [[0, 0, 0],
                          [0, 0, 0],
                          [0, 0, 0]]
        self.placar_usuario = 0
        self.placar_computador = 0

        # Music Player
        self.player = QMediaPlayer()
        self.musica_velha()

    def sortear_jogada(self):
        self.aleatorio = randint(0, 8)
        while True:
            if len(self.lista_indisponiveis) == 9:
                break
            elif self.aleatorio in self.lista_indisponiveis:
                self.aleatorio = randint(0, 8)
            else:
                self.jogada_pc()
                break

    def reset(self):
        self.lista_indisponiveis = []
        self.tabuleiro = [[0, 0, 0],
                          [0, 0, 0],
                          [0, 0, 0]]
        self.ativacao_botoes(True)

        self.btn_1x1.setStyleSheet("background-image: none; background-color: transparent;")
        self.btn_1x2.setStyleSheet("background-image: none; background-color: transparent;")
        self.btn_1x3.setStyleSheet("background-image: none; background-color: transparent;")
        self.btn_2x1.setStyleSheet("background-image: none; background-color: transparent;")
        self.btn_2x2.setStyleSheet("background-image: none; background-color: transparent;")
        self.btn_2x3.setStyleSheet("background-image: none; background-color: transparent;")
        self.btn_3x1.setStyleSheet("background-image: none; background-color: transparent;")
        self.btn_3x2.setStyleSheet("background-image: none; background-color: transparent;")
        self.btn_3x3.setStyleSheet("background-image: none; background-color: transparent;")

    def musica_velha(self):
        arquivo = os.path.join(os.getcwd(), "audio/fnaf_4.mp3")
        url = QUrl.fromLocalFile(arquivo)
        conteudo = QMediaContent(url)
        self.player.setMedia(conteudo)
        self.player.play()

    def f1x1(self):
        self.btn_1x1.setEnabled(False)
        self.tabuleiro[0][0] = 1
        self.lista_indisponiveis.append(0)
        self.btn_1x1.setStyleSheet("background-image: url(image/toy_gfreddy.png); background-color: transparent;")
        if self.verificar_jogada():
            self.sortear_jogada()

    def f1x2(self):
        self.btn_1x2.setEnabled(False)
        self.tabuleiro[0][1] = 1
        self.lista_indisponiveis.append(1)
        self.btn_1x2.setStyleSheet("background-image: url(image/toy_gfreddy.png); background-color: transparent;")
        if self.verificar_jogada():
            self.sortear_jogada()

    def f1x3(self):
        self.btn_1x3.setEnabled(False)
        self.tabuleiro[0][2] = 1
        self.lista_indisponiveis.append(2)
        self.btn_1x3.setStyleSheet("background-image: url(image/toy_gfreddy.png); background-color: transparent;")
        if self.verificar_jogada():
            self.sortear_jogada()

    def f2x1(self):
        self.btn_2x1.setEnabled(False)
        self.tabuleiro[1][0] = 1
        self.lista_indisponiveis.append(3)
        self.btn_2x1.setStyleSheet("background-image: url(image/toy_gfreddy.png); background-color: transparent;")
        if self.verificar_jogada():
            self.sortear_jogada()

    def f2x2(self):
        self.btn_2x2.setEnabled(False)
        self.tabuleiro[1][1] = 1
        self.lista_indisponiveis.append(4)
        self.btn_2x2.setStyleSheet("background-image: url(image/toy_gfreddy.png); background-color: transparent;")
        if self.verificar_jogada():
            self.sortear_jogada()

    def f2x3(self):
        self.btn_2x3.setEnabled(False)
        self.tabuleiro[1][2] = 1
        self.lista_indisponiveis.append(5)
        self.btn_2x3.setStyleSheet("background-image: url(image/toy_gfreddy.png); background-color: transparent;")
        if self.verificar_jogada():
            self.sortear_jogada()

    def f3x1(self):
        self.btn_3x1.setEnabled(False)
        self.tabuleiro[2][0] = 1
        self.lista_indisponiveis.append(6)
        self.btn_3x1.setStyleSheet("background-image: url(image/toy_gfreddy.png); background-color: transparent;")
        if self.verificar_jogada():
            self.sortear_jogada()

    def f3x2(self):
        self.btn_3x2.setEnabled(False)
        self.tabuleiro[2][1] = 1
        self.lista_indisponiveis.append(7)
        self.btn_3x2.setStyleSheet("background-image: url(image/toy_gfreddy.png); background-color: transparent;")
        if self.verificar_jogada():
            self.sortear_jogada()

    def f3x3(self):
        self.btn_3x3.setEnabled(False)
        self.tabuleiro[2][2] = 1
        self.lista_indisponiveis.append(8)
        self.btn_3x3.setStyleSheet("background-image: url(image/toy_gfreddy.png); background-color: transparent;")
        if self.verificar_jogada():
            self.sortear_jogada()

    def jogada_pc(self):
        if self.aleatorio == 0:
            self.btn_1x1.setEnabled(False)
            self.tabuleiro[0][0] = 2
            self.lista_indisponiveis.append(0)
            self.btn_1x1.setStyleSheet("background-image: url(image/toy_freddy.png); background-color: transparent;")
            self.verificar_jogada()

        elif self.aleatorio == 1:
            self.btn_1x2.setEnabled(False)
            self.tabuleiro[0][1] = 2
            self.lista_indisponiveis.append(1)
            self.btn_1x2.setStyleSheet("background-image: url(image/toy_freddy.png); background-color: transparent;")
            self.verificar_jogada()

        elif self.aleatorio == 2:
            self.btn_1x3.setEnabled(False)
            self.tabuleiro[0][2] = 2
            self.lista_indisponiveis.append(2)
            self.btn_1x3.setStyleSheet("background-image: url(image/toy_freddy.png); background-color: transparent;")
            self.verificar_jogada()

        elif self.aleatorio == 3:
            self.btn_2x1.setEnabled(False)
            self.tabuleiro[1][0] = 2
            self.lista_indisponiveis.append(3)
            self.btn_2x1.setStyleSheet("background-image: url(image/toy_freddy.png); background-color: transparent;")
            self.verificar_jogada()

        elif self.aleatorio == 4:
            self.btn_2x2.setEnabled(False)
            self.tabuleiro[1][1] = 2
            self.lista_indisponiveis.append(4)
            self.btn_2x2.setStyleSheet("background-image: url(image/toy_freddy.png); background-color: transparent;")
            self.verificar_jogada()

        elif self.aleatorio == 5:
            self.btn_2x3.setEnabled(False)
            self.tabuleiro[1][2] = 2
            self.lista_indisponiveis.append(5)
            self.btn_2x3.setStyleSheet("background-image: url(image/toy_freddy.png); background-color: transparent;")
            self.verificar_jogada()

        elif self.aleatorio == 6:
            self.btn_3x1.setEnabled(False)
            self.tabuleiro[2][0] = 2
            self.lista_indisponiveis.append(6)
            self.btn_3x1.setStyleSheet("background-image: url(image/toy_freddy.png); background-color: transparent;")
            self.verificar_jogada()

        elif self.aleatorio == 7:
            self.btn_3x2.setEnabled(False)
            self.tabuleiro[2][1] = 2
            self.lista_indisponiveis.append(7)
            self.btn_3x2.setStyleSheet("background-image: url(image/toy_freddy.png); background-color: transparent;")
            self.verificar_jogada()

        else:
            self.btn_3x3.setEnabled(False)
            self.tabuleiro[2][2] = 2
            self.lista_indisponiveis.append(8)
            self.btn_3x3.setStyleSheet("background-image: url(image/toy_freddy.png); background-color: transparent;")
            self.verificar_jogada()

    def verificar_jogada(self):
        linha_1 = self.tabuleiro[0]
        linha_2 = self.tabuleiro[1]
        linha_3 = self.tabuleiro[2]
        coluna_1 = [self.tabuleiro[0][0], self.tabuleiro[1][0], self.tabuleiro[2][0]]
        coluna_2 = [self.tabuleiro[0][1], self.tabuleiro[1][1], self.tabuleiro[2][1]]
        coluna_3 = [self.tabuleiro[0][2], self.tabuleiro[1][2], self.tabuleiro[2][2]]
        d1 = [self.tabuleiro[0][0], self.tabuleiro[1][1], self.tabuleiro[2][2]]
        d2 = [self.tabuleiro[2][0], self.tabuleiro[1][1], self.tabuleiro[0][2]]

        velha = [linha_1, linha_2, linha_3, coluna_1, coluna_2, coluna_3, d1, d2]
        for espaco in velha:
            if espaco == [1, 1, 1]:
                self.placar_usuario += 1
                self.lb_usuario.setText(str(self.placar_usuario))
                self.ativacao_botoes(False)
                return False
            elif espaco == [2, 2, 2]:
                self.placar_computador += 1
                self.lb_computador.setText(str(self.placar_computador))
                self.ativacao_botoes(False)
                return False
        return True

    def ativacao_botoes(self, condicao):
        # for coluna in range(3):
        #     for linha in range(3):
        #         botao = "btn_"
        #         botao += str(coluna + 1) + "x" + str(linha + 1)

        self.btn_1x1.setEnabled(condicao)
        self.btn_1x2.setEnabled(condicao)
        self.btn_1x3.setEnabled(condicao)
        self.btn_2x1.setEnabled(condicao)
        self.btn_2x2.setEnabled(condicao)
        self.btn_2x3.setEnabled(condicao)
        self.btn_3x1.setEnabled(condicao)
        self.btn_3x2.setEnabled(condicao)
        self.btn_3x3.setEnabled(condicao)

    def abrir_menu(self):
        self.player.stop()
        menu.musica_menu()
        menu.show()
        self.close()

class Jokenpo(QMainWindow):
    def __init__(self):
        super(Jokenpo, self).__init__()
        uic.loadUi("screen_ui/Jokenpo.ui", self)

        # Define Widgets
        self.background = self.findChild(QLabel, "lb_background")
        self.lb_usuario = self.findChild(QLabel, "lb_usuario")
        self.lb_computador = self.findChild(QLabel, "lb_computador")
        self.lb_timer = self.findChild(QLabel, "lb_timer")
        self.lb_escolha = self.findChild(QLabel, "lb_escolha")
        self.btn_pedra = self.findChild(QPushButton, "btn_pedra")
        self.btn_papel = self.findChild(QPushButton, "btn_papel")
        self.btn_tesoura = self.findChild(QPushButton, "btn_tesoura")
        self.btn_menu = self.findChild(QPushButton, "btn_jokenpoMenu")
        self.btn_reset = self.findChild(QPushButton, "btn_jokenpoReset")

        # Button Functions
        self.btn_pedra.clicked.connect(self.pedra)
        self.btn_papel.clicked.connect(self.papel)
        self.btn_tesoura.clicked.connect(self.tesoura)
        self.btn_menu.clicked.connect(self.abrir_menu)
        self.btn_reset.clicked.connect(self.reset)

        # Programação Back-End
        self.usuario = 0
        self.computador = 0
        self.placar_user = 0
        self.placar_pc = 0

        self.lb_usuario.setText(str(self.placar_user))
        self.lb_computador.setText(str(self.placar_pc))

        # Music Player
        self.player = QMediaPlayer()
        self.musica_jokenpo("audio/watch_your_6.mp3")

        # Timer
        self.timer = QTimer()
        self.timer.timeout.connect(self.acabou_tempo)

        # Timer
        if not self.timer.isActive():
            self.timer.start(10000)
        else:
            self.timer.stop()

        # Show the App
        self.show()

    def acabou_tempo(self):
        self.timer.stop()
        if self.placar_user > self.placar_pc:
            uic.loadUi("screen_ui/Venceu.ui", self)
            self.musica_jokenpo("audio/freddys_jingle.mp3")
            self.btn_vnovamente = self.findChild(QPushButton, "btn_venceuNovamente")
            self.btn_vmenu = self.findChild(QPushButton, "btn_venceuMenu")
            self.btn_vnovamente.clicked.connect(menu.abrir_jokenpo)
            self.btn_vmenu.clicked.connect(self.abrir_menu)
        else:
            uic.loadUi("screen_ui/Perdeu.ui", self)
            self.btn_pnovamente = self.findChild(QPushButton, "btn_perdeuNovamente")
            self.btn_pmenu = self.findChild(QPushButton, "btn_perdeuMenu")
            self.btn_pnovamente.clicked.connect(menu.abrir_jokenpo)
            self.btn_pmenu.clicked.connect(self.abrir_menu)
            if self.placar_pc > self.placar_user:
                self.musica_jokenpo("audio/fnaf_3.mp3")
            else:
                self.e_background = self.findChild(QLabel, "lb_background")
                self.e_background.setPixmap(QtGui.QPixmap("screen/empate.png"))
                self.musica_jokenpo("audio/fnaf_sl.mp3")

    def sortear_jogada(self):
        self.computador = randint(3, 4)

        while True:
            if self.computador != self.usuario:
                break
            else:
                self.computador = randint(3, 5)

        if self.computador == 3:
            self.lb_escolha.setStyleSheet("background-image: url(image/freddy.png);")

        elif self.computador == 4:
            self.lb_escolha.setStyleSheet("background-image: url(image/bonnie.png);")

        else:
            self.lb_escolha.setStyleSheet("background-image: url(image/chica.png);")

    def pedra(self):
        self.usuario = 3
        self.sortear_jogada()
        self.verificar_jogada()

    def papel(self):
        self.usuario = 4
        self.sortear_jogada()
        self.verificar_jogada()

    def tesoura(self):
        self.usuario = 5
        self.sortear_jogada()
        self.verificar_jogada()

    def verificar_jogada(self):
        if self.usuario == 3 and self.computador == 5 or self.usuario == 4 and self.computador == 3 or self.usuario == 5 and self.computador == 4:
            self.placar_user += 1

        elif self.computador == 3 and self.usuario == 5 or self.computador == 4 and self.usuario == 3 or self.computador == 5 and self.usuario == 4:
            self.placar_pc += 1

        self.lb_usuario.setText(str(self.placar_user))
        self.lb_computador.setText(str(self.placar_pc))

    def reset(self):
        self.player.stop()
        self.musica_jokenpo("audio/watch_your_6.mp3")
        self.jokenpo = Jokenpo()
        self.jokenpo.show()
        self.hide()

    def musica_jokenpo(self, caminho):
        arquivo = os.path.join(os.getcwd(), caminho)
        url = QUrl.fromLocalFile(arquivo)
        conteudo = QMediaContent(url)
        self.player.setMedia(conteudo)
        self.player.play()

    def abrir_menu(self):
        self.player.stop()
        menu.musica_menu()
        self.close()
        menu.show()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    menu = Menu()
    app.exec()