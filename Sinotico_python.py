
import serial
import pymysql
from builtins import print
from datetime import datetime


# ---------------------------Variaveis Global----------------------------------------------------#

indice_1 = "temperatura"
indice_2 = "nivel"
indice_3 = "vazao"
indice_4 = "pressao"
rg = '0123456789'
condicao = True
Intervalo = 0.1
Tempo_Anterior = 0


#Tenta comunicação  inicial com Arduino
try:
    ser = serial.Serial(port='COM3', baudrate=9600,timeout='1')
    flag = 1
except:
    print("Não há comunicação serial, tente novamente")
    flag = 0    
    while(flag == 0):
        try:
            ser = serial.Serial(port='COM3', baudrate=9600)
            flag = 1        
        except:
            print("Reconnecte o dispositivo...") #Tenta comunicação inicial com Servidor
                try:
                    conn = pymysql.connect(host='localhost', user='root', password='', db='cadastro')
                    ql1 = conn.cursor()  # Inserir o TimeStamp e demais variaveis    
                    sql1_1 = conn.cursor()  # consulta tempo    
                    sql2_2 = conn.cursor()  # consulta temperatura    
                    sql3_3 = conn.cursor()  # consulta nivel    
                    sql4_4 = conn.cursor()  # consutla vazao    
                    sql5_5 = conn.cursor()  # consulta pressao    
                    flag2 = 1
                except:
                    flag2 = 0    
                    print("Não foi possivel se conectar ao banco de dados, restart o servidor.")
    while (flag2 == 0):
        try:
            conn = pymysql.connect(host='localhost', user='root', password='', db='cadastro')
            sql1 = conn.cursor()  # Inserir o TimeStamp e demais variaveis            
            sql1_1 = conn.cursor()  # consulta tempo            
            sql2_2 = conn.cursor()  # consulta temperatura            
            sql3_3 = conn.cursor()  # consulta nivel            
            sql4_4 = conn.cursor()  # consutla vazao            
            sql5_5 = conn.cursor()  # consulta pressao            
            flag2 = 1        
         except:
            print("Não foi possivel se conectar ao banco de dados, restart o servidor.")
            
            
while (True):
    now = str(datetime.now())
    palavra = ser.readline(40)
    teste = str('\_r\_n').replace("_", "")
    teste_2 = ("_'_").replace('_', "")
    texto = str(palavra).replace(teste, " ").replace('b', "").replace(teste_2,'') # valor deixa de existir apos o print    
    texto_Apenas = str(palavra).replace(teste, " ").replace('b', "").replace(teste_2, '')
    if indice_1 in texto_Apenas:
        temp = texto_Apenas
        for i in range(len(temp)):
            if temp[i] not in rg:
                temp = temp.replace(temp[i], " ")
                valor_temperatura = (temp).replace(" ", "")
                temperatura = valor_temperatura
    if indice_2 in texto_Apenas:
        niv = texto_Apenas
        for i in range(len(niv)):
            if niv[i] not in rg:
                niv = niv.replace(niv[i], " ")
                valor_nivel = (niv).replace(" ", "")
                nivel = valor_nivel
    if indice_3 in texto_Apenas:
        vaz = texto_Apenas
        for i in range(len(vaz)):
            if vaz[i] not in rg:
                vaz = vaz.replace(vaz[i], " ")
                valor_vazao = (vaz).replace(" ", "")
                vazao = valor_vazao
    if indice_4 in texto_Apenas:
        pres = texto_Apenas
        for i in range(len(pres)):
            if pres[i] not in rg:
                pres = pres.replace(pres[i], " ")
                valor_pressao = (pres).replace(" ", "")
                pressao = valor_pressao
    #Controle de tempo    
    now = str(datetime.now())
    Tempo_Segundo = datetime.now()
    Tempo_Atual = Tempo_Segundo.second
    Controle_Tempo = (Tempo_Atual - Tempo_Anterior)
    if (Controle_Tempo &lt; Intervalo):
        Tempo_Anterior = Tempo_Segundo.second
    if (Controle_Tempo &gt; Intervalo):
        Tempo_Anterior = Tempo_Segundo.second
        TimeStamp = datetime.utcnow().strftime('%Y-%m-%d  %H:%M:%S')
        try:
            sql1.execute('INSERT INTO `arduino` (data,temperatura,nivel,vazao,pressao) values( "' + TimeStamp + '",'+valor_temperatura+','+valor_nivel+','+valor_vazao+','+valor_pressao+')')
            sql1_1.execute('SELECT `data`  FROM `arduino` Order by `data` DESC LIMIT 1')
            sql2_2.execute('SELECT `temperatura`  FROM `arduino` Order by `data` DESC LIMIT 1')
            sql3_3.execute('SELECT `nivel`  FROM `arduino` Order by `data` DESC LIMIT 1')
            sql4_4.execute('SELECT `vazao`  FROM `arduino` Order by `data` DESC LIMIT 1')
            sql5_5.execute('SELECT `pressao`  FROM `arduino` Order by `data` DESC LIMIT 1')
            Data = sql1_1.fetchall()
            Temperatura = sql2_2.fetchall()
            Nivel = sql3_3.fetchall()
            Vazao = sql4_4.fetchall()
            Pressao = sql5_5.fetchall()
            print(str(Data).replace(',)', "").replace("((", ""))
            print("Valor de Temperatura: " + str(Temperatura).replace(',)', "").replace("((", ""))
            print("Valor de Nivel: " + str(Nivel).replace(',)', "").replace("((", ""))
            print("Valor de Vazao: " + str(Vazao).replace(',)', "").replace("((", ""))
            print("Valor de Pressao: " + str(Pressao).replace(',)', "").replace("((", ""))
        except:
            try:
                conn = pymysql.connect(host='localhost', user='root', password='', db='cadastro')
                sql1 = conn.cursor()  # Inserir o TimeStamp e demais variaveis                
                sql1_1 = conn.cursor()  # consulta tempo                
                sql2_2 = conn.cursor()  # consulta temperatura                
                sql3_3 = conn.cursor()  # consulta nivel                
                sql4_4 = conn.cursor()  # consutla vazao                
                sql5_5 = conn.cursor()  # consulta pressao            
            except:
                print("Erro na consulta, tentando se reconectar o Servidor")
