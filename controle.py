from PyQt6 import uic,QtWidgets #Biblioteca para utilizar o Qt Designer
import mysql.connector #Biblioteca para utilizar o MySQL
from reportlab.pdfgen import canvas #Biblioteca para gerar pdf de um arquivo

num_id = 0 #variável global criada para edição de dados

#Conexão com meu Banco de Dados.
banco = mysql.connector.connect(
    host="localhost",
    user="root",
    passwd="",
    database="cadastro_produtos"
)
#Função para mostrar os dados na tela de edição
def editar_dados():
    global num_id
    linha = lista_de_produtos.tableWidget.currentRow()

    cursor = banco.cursor()
    cursor.execute("SELECT id FROM produtos")
    dados_lidos = cursor.fetchall()
    valor_id = dados_lidos[linha][0]
    cursor.execute("SELECT * FROM produtos WHERE id=" + str(valor_id))
    produto = cursor.fetchall()
    tela_editar.show()

    num_id = valor_id

    tela_editar.lineEdit.setText(str(produto[0][0]))
    tela_editar.lineEdit_2.setText(str(produto[0][1]))
    tela_editar.lineEdit_3.setText(str(produto[0][2]))
    tela_editar.lineEdit_4.setText(str(produto[0][3]))
    tela_editar.lineEdit_5.setText(str(produto[0][4]))
    banco.commit()

#Salvando dados editados e mostrando na tela assim que salvar
def salvar_dados_editados():
    global num_id
    nome = tela_editar.lineEdit_2.text()
    codigo = tela_editar.lineEdit_3.text()
    valor = tela_editar.lineEdit_4.text()
    categoria = tela_editar.lineEdit_5.text()

    #atualizar os dados no banco de dados
    cursor = banco.cursor()
    cursor.execute("UPDATE produtos SET nome = '{}',codigo = '{}',valor = '{}',categoria = '{}' WHERE id = {}".format(nome,codigo,valor,categoria,num_id))
    # atualizar as janelas
    tela_editar.close()
    lista_de_produtos.close()
    chama_segunda_tela()
    banco.commit()

#Função para excluir dados do banco
def excluir_dados():
    linha = lista_de_produtos.tableWidget.currentRow()
    lista_de_produtos.tableWidget.removeRow(linha)

    cursor = banco.cursor()
    cursor.execute("SELECT id FROM produtos")
    dados_lidos = cursor.fetchall()
    valor_id = dados_lidos[linha][0]
    cursor.execute("DELETE FROM produtos WHERE id="+str(valor_id))
    banco.commit()

#Função para gerar PDF do banco de dados
def gerar_pdf():
    cursor = banco.cursor()
    comando_SQL = "SELECT * FROM produtos"
    cursor.execute(comando_SQL)
    dados_lidos = cursor.fetchall()
    y = 0
    pdf = canvas.Canvas("cadastro_produtos.pdf") #onde salvar arquivo pdf
    pdf.setFont("Times-Bold",25)
    pdf.drawString(175,800,"Produtos Cadastrados")# Título e posicionamento do mesmo
    pdf.setFont("Times-Bold",12)

    pdf.drawString(10,750,"ID")
    pdf.drawString(60,750,"NOME")
    pdf.drawString(300,750,"CÓDIGO")
    pdf.drawString(370,750,"VALOR")
    pdf.drawString(450,750,"CATEGORIA")

    for i in range(0,len(dados_lidos)):
        y = y + 50
        pdf.drawString(10,750 - y, str(dados_lidos[i][0]))
        pdf.drawString(60,750 -y, str(dados_lidos[i][1]))
        pdf.drawString(300, 750 -y, str(dados_lidos[i][2]))
        pdf.drawString(370, 750 -y, str(dados_lidos[i][3]))
        pdf.drawString(450, 750 -y, str(dados_lidos[i][4]))

    pdf.save()
    print("PDF FOI GERADO COM SUCESSO")

#Função para capturar informação adicionada no sistema de cadastro.
def funcao_principal():
    linha1 = formulario.lineEdit.text()
    linha2 = formulario.lineEdit_2.text()
    linha3 = formulario.lineEdit_3.text()

#Criação das categorias que serão adicionadas no Banco de Dados.
    categoria = ""

    if formulario.radioButton.isChecked():
        print("Categoria Som e Imagem foi selecionado")
        categoria = "Som e Imagem"
    elif formulario.radioButton_2.isChecked():
        print("Categoria Informática foi selecionado")
        categoria = "Informática"
    else:
        print("Categoria Automotivo foi selecionado")
        categoria = "Automotivo"
#Informa produto e categoria cadastrados.
    print("Nome:",linha1)
    print("Código:",linha2)
    print("Valor:",linha3)
#Incersão de informação no Banco de Dados
    cursor = banco.cursor()
    comando_SQL = "INSERT INTO produtos (nome,codigo,valor,categoria) VALUES (%s,%s,%s,%s)"
    dados = (str(linha1),str(linha2),str(linha3),categoria)
    cursor.execute(comando_SQL,dados)
    banco.commit()
#Limpar formulário após cadastro do produto
    formulario.lineEdit.setText("")
    formulario.lineEdit_2.setText("")
    formulario.lineEdit_3.setText("")

#mostrando a segunda tela
def chama_segunda_tela():
    lista_de_produtos.show()

    cursor = banco.cursor()
    comando_SQL = "Select * From produtos"
    cursor.execute(comando_SQL)
    dados_lidos = cursor.fetchall()

    lista_de_produtos.tableWidget.setRowCount(len(dados_lidos))
    lista_de_produtos.tableWidget.setColumnCount(5)

    for i in range(0, len(dados_lidos)):
        for j in range(0,5):
            lista_de_produtos.tableWidget.setItem(i,j,QtWidgets.QTableWidgetItem(str(dados_lidos[i][j])))


#Carregar tela para cadastro dos produtos..
app=QtWidgets.QApplication([])
formulario=uic.loadUi('formulario.ui')
lista_de_produtos=uic.loadUi('formulario2.ui')
tela_editar=uic.loadUi("alterar.ui")
formulario.pushButton.clicked.connect(funcao_principal)
formulario.pushButton_2.clicked.connect(chama_segunda_tela)#Botão para chamar a função segunda tela
lista_de_produtos.pushButton.clicked.connect(gerar_pdf) #Botão para chamar função gerar pdf
lista_de_produtos.pushButton_2.clicked.connect(excluir_dados)
lista_de_produtos.pushButton_3.clicked.connect(editar_dados)
tela_editar.pushButton.clicked.connect(salvar_dados_editados)

formulario.show()
app.exec()