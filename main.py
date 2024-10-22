import sys
from PyQt5.QtCore import QThread, pyqtSignal
from PyQt5.QtWidgets import QApplication, QMainWindow, QHeaderView
from PyQt5.QtCore import QPropertyAnimation, QEasingCurve
from PyQt5 import QtCore, QtWidgets
from PyQt5.uic import loadUi
from conexao import Comunication

class DataLoaderThread(QThread):
    data_loaded = pyqtSignal(list)

    def __init__(self, base_dados):
        super().__init__()
        self.base_dados = base_dados

    def run(self):
        try:
            data = self.base_dados.select_transacoes("")
            self.data_loaded.emit(data)
        except Exception as e:
            print(f"Erro ao carregar dados: {e}")

class telaprincipal(QMainWindow):
    def __init__(self):
        super(telaprincipal, self).__init__()
        loadUi('hugoteste.ui', self)
        self.show()
        
        self.bt_coluna.clicked.connect(self.mover_coluna)

        self.base_dados = Comunication()
        self.data_loader_thread = DataLoaderThread(self.base_dados)
        self.data_loader_thread.data_loaded.connect(self.update_table)

        self.gripSize = 10
        self.grip = QtWidgets.QSizeGrip(self)
        self.grip.resize(self.gripSize, self.gripSize)

        # Buttons
        self.bt_base.clicked.connect(self.mostrar_transacao)
        self.bt_add.clicked.connect(self.adicionar_transacao)
        self.bt_excluir.clicked.connect(self.excluir_transacao)
        self.bt_atualizar.clicked.connect(self.atualizar_transacao)
        self.bt_refrescar.clicked.connect(self.refrescar_transacao)
        self.bt_buscaralt.clicked.connect(self.buscar_por_nome_alterar)
        self.bt_buscarDELETE.clicked.connect(self.buscar_por_nome_excluir)

        self.bt_minimizar.clicked.connect(self.minimizar)
        self.bt_fechar.clicked.connect(lambda: self.close())
        self.bt_coluna.clicked.connect(self.mover_coluna)
        self.bt_telacheia.clicked.connect(self.telacheia)

        self.frame_superior.mouseMoveEvent = self.mover_janela

        self.bt_base.clicked.connect(lambda: self.stackedWidget.setCurrentWidget(self.page_dados))
        self.bt_add.clicked.connect(lambda: self.stackedWidget.setCurrentWidget(self.page_add))
        self.bt_excluir.clicked.connect(lambda: self.stackedWidget.setCurrentWidget(self.page_excluir))
        self.bt_atualizar.clicked.connect(lambda: self.stackedWidget.setCurrentWidget(self.page_atualizar))
        self.bt_ajuste.clicked.connect(lambda: self.stackedWidget.setCurrentWidget(self.page_ajuste))

        self.tabela_dados.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.tabela_excluir.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

    def control_bt_minimizar(self):
        self.showMinimized()

    def control_bt_normal(self):
        self.showNormal()

    def resizeEvent(self, event):
        rect = self.rect()
        if hasattr(self, 'grip'):  # Verifica se 'grip' foi inicializado
            self.grip.move(rect.right() - self.gripSize, rect.bottom() - self.gripSize)

    def mousePressEvent(self, event):
        self.clickPosition = event.globalPos()

    def mover_janela(self, event):
        if not self.isMaximized():
            if event.buttons() == QtCore.Qt.LeftButton:
                self.move(self.pos() + event.globalPos() - self.clickPosition)
                self.clickPosition = event.globalPos()
                event.accept()
        if event.globalPos().y() <= 10:
            self.showMaximized()
        else:
            self.showNormal()

    def mover_coluna(self):
        width = self.frame_controlo.width()
        normal = 0
        extender = 200 if width == 0 else normal
        self.animacao = QPropertyAnimation(self.frame_controlo, b'minimumWidth')
        self.animacao.setDuration(300)
        self.animacao.setStartValue(width)
        self.animacao.setEndValue(extender)
        self.animacao.setEasingCurve(QEasingCurve.InOutQuart)
        self.animacao.start()

    def mostrar_transacao(self):
        self.data_loader_thread.start()

    def update_table(self, dados):
        i = len(dados)
        self.tabela_dados.setRowCount(i)
        tablerow = 0
        for row in dados:
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
