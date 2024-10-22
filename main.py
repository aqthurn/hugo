import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QCheckBox, QComboBox, QPushButton, QLineEdit, QTableWidget, QTableWidgetItem, QHeaderView
from PyQt5.QtCore import QPropertyAnimation, QEasingCurve
from PyQt5 import QtCore, QtWidgets
from PyQt5.uic import loadUi
from conexao import Comunication


class telaprincipal(QMainWindow):
    def __init__(self):
        super(telaprincipal, self).__init__()
        loadUi('hugoteste.ui', self)
        self.show()
        
        self.bt_coluna.clicked.connect(self.mover_coluna)

        self.base_dados = Comunication()

        self.gripSize = 10
        self.grip = QtWidgets.QSizeGrip(self)
        self.grip.resize(self.gripSize, self.gripSize)


    #BOTOES GERAIS

        self.bt_base.clicked.connect(self.mostrar_transacao)
        self.bt_add.clicked.connect(self.adicionar_transacao)
        self.bt_excluir.clicked.connect(self.excluir_transacao)
        self.bt_atualizar.clicked.connect(self.atualizar_transacao)
        self.bt_refrescar.clicked.connect(self.refrescar_transacao)
        self.bt_buscaralt.clicked.connect(self.buscar_por_nome_alterar)
        self.bt_buscarDELETE.clicked.connect(self.buscar_por_nome_excluir)

#BOTOES BARRA SUPERIOR

        self.bt_minimizar.clicked.connect(self.minimizar)
        self.bt_fechar.clicked.connect(lambda: self.close)
        self.bt_coluna.clicked.connect(self.mover_coluna)
        self.bt_telacheia.clicked.connect(self.telacheia)

#opacidade barra de titulo da janela

        #self.setWindowOpacity(0.9)
        #self.setWindowFlags(QtCore.Qt.FramelessWindowHint)
        #self.setAttribute(QtCore.Qt.WA_TranslucentBackground)

#size grip
        
        #mover janela

        self.frame_superior.mouseMoveEvent = self.mover_janela

#conectar botoes

        self.bt_base.clicked.connect(lambda: self.stackedWidget.setCurrentWidget(self.page_dados))
        self.bt_add.clicked.connect(lambda: self.stackedWidget.setCurrentWidget(self.page_add))
        self.bt_excluir.clicked.connect(lambda: self.stackedWidget.setCurrentWidget(self.page_excluir))
        self.bt_atualizar.clicked.connect(lambda: self.stackedWidget.setCurrentWidget(self.page_atualizar))
        self.bt_ajuste.clicked.connect(lambda: self.stackedWidget.setCurrentWidget(self.page_ajuste))
#tabelas

        self.tabela_dados.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.tabela_excluir.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

    def control_bt_minimizar(self):
        self.showMinimized()

    def control_bt_normal(self):
        self.showNormal()
        

#size grip
    def resizeEvent(self, event):
     rect = self.rect()
     if hasattr(self, 'grip'):  # Verifica se 'grip' foi inicializado
        self.grip.move(rect.right() - self.gripSize, rect.bottom() - self.gripSize)



#mover janela
    def mousePressEvent(self, event):
                self.clickPosition = event.globalPos()

    def mover_janela(self, event):
        if self.isMaximized() == False:
          if event.buttons() == QtCore.Qt.LeftButton:
                self.move(self.pos() + event.globalPos() - self.clickPosition)
                self.clickPosition = event.globalPos()
                event.accept()
        if event.globalPos().y() <=10:
             self.showMaximized()

        else:
             self.showNormal()

#mover coluna
    def mover_coluna(self):
         if True:
           width = self.frame_controlo.width()
           normal = 0
           if width==0:
                extender = 200
           else:
                extender = normal
           self.animacao = QPropertyAnimation(self.frame_controlo, b'minimumWidth')
           self.animacao.setDuration(300)
           self.animacao.setStartValue(width)
           self.animacao.setEndValue(extender)
           self.animacao.setEasingCurve(QtCore.QEasingCurve.InOutQuart)
           self.animacao.start()

    def mostrar_dados(self):
         dados = self.base_dados.mostrar_dados()
         i = len(dados)
         self.tabela_dados.setRowCount(i)
         tablerow = 0
         for row in dados:
              self.Id = row[0]
              self.tabela_dados.setItem(tablerow, 0, QtWidgets.QTableWidgetItem(row[1]))
              self.tabela_dados.setItem(tablerow, 1, QtWidgets.QTableWidgetItem(row[2]))
              self.tabela_dados.setItem(tablerow, 2, QtWidgets.QTableWidgetItem(row[3]))
              self.tabela_dados.setItem(tablerow, 3, QtWidgets.QTableWidgetItem(row[4]))
              self.tabela_dados.setItem(tablerow, 4, QtWidgets.QTableWidgetItem(row[5]))
              tablerow += 1
             





try:
    app = QApplication(sys.argv)
    mi_app = telaprincipal()
    mi_app.show()
    sys.exit(app.exec_())
except Exception as e:
    print(f"Erro: {e}")



    