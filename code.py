#Importando as bibliotecas

import numpy as np
import datetime
from collections import Counter
import collections
import pandas as pd
import matplotlib
import matplotlib.pyplot as plt
import seaborn as sns
import re



#Lendo o arquivo e formantando a data e hora para string

ref_arquivo = open('conversa_bi.txt', "r", encoding='utf-8')
linha = ref_arquivo.readline()

list_datas = []
list_erros_formatacao = []
list_pessoas = []
list_msgs = []

while linha:
    linha = ref_arquivo.readline()
    try:
      date_time_obj = datetime.datetime.strptime(linha[1:17], '%d/%m/%y %H:%M:%S')
      list_datas.append(date_time_obj)
      msg = linha[20:]
      if(len(msg.split(':')) >= 2):
            list_pessoas.append(msg.split(':')[0])
            list_msgs.append(msg.split(':')[1])
    except ValueError:
      list_erros_formatacao.append('Não foi possível formatar')
ref_arquivo.close()




#Contando os participantes da conversa e qual participante envia mais mensangens (plotado em gráfico de barras horizontais)

dict_pessoas = dict(Counter(list_pessoas))
pessoas_df = pd.DataFrame(dict_pessoas.items(), columns=['Participantes', 'Quantidade Mensagens'])
pessoas_df = pessoas_df.sort_values(by=['Quantidade Mensagens'])
pessoas_df['Participantes'] = pessoas_df['Participantes'].replace(['\u202a+55\xa011\xa095765‑5550\u202c','\u202a+55\xa081\xa09957‑6999\u202c','\u202a+55\xa011\xa098793‑6843\u202c','\u202a+55\xa011\xa097301‑7387\u202c','\u202a+55\xa013\xa099785‑0435\u202c','\u202a+55\xa011\xa095980‑8745\u202c','\u202a+55\xa011\xa099122‑8956\u202c'],['Oliveira','Rosane','Laisla','Mirella','Lopes','Alexandre','Jean'])
print(pessoas_df)
pessoas_df.plot(kind='barh', x = 'Participantes', y = 'Quantidade Mensagens', figsize=(13,7), color=['#FF00FF', '#D2691E', '#ADFF2F', '#006400', '#000000', '#836FFF', '#D2691E', '#FF1493'])



#Palavras mais utilizadas (plotado em gráfico de barras horizontais)

palavras = []
f = list_msgs
for i in f:
  i = i.split()
  for a in i:
    palavras.append(a)
    if len(a) < 2:
     palavras.remove(a)
dict_palavras = dict(Counter(palavras).most_common(3))
print('Palavras mais utilizadas :', dict_palavras)

palavras_df = pd.DataFrame(dict_palavras.items(), columns=['Palavra', 'Quantidade'])
palavras_df = palavras_df.sort_values(by=['Quantidade'])
palavras_df.plot(kind='barh', x = 'Palavra', y = 'Quantidade', figsize=(20,7), color=['#FF0000', '#D8BFD8', '#FFD700', '#8B008B', '#9DAAA2'])



dia_da_semana = {
  0: "Domingo",
  1: "Segunda",
  2: "Terça",
  3: "Quarta",
  4: "Quinta",
  5: "Sexta",
  6: "Sábado"
 
}
list_horas = []
list_dia_semana = []
for data in list_datas:
    list_horas.append(data.time().hour) 
    list_dia_semana.append(dia_da_semana.get(data.weekday()))
    
#Contando dia da semana com maior frequencia de mensagens
dict_dia_semana = dict(Counter(list_dia_semana))

semana_df = pd.DataFrame(dict_dia_semana.items(), columns=['Dia Semana', 'Frequencia'])
semana_df.plot(kind='barh', x = 'Dia Semana', y='Frequencia', title='Frequencia de conversas por dia da semana', figsize=(20,7), color=['#FF0000'])

#Contando o horário de maior movimento no grupo
dict_horas = dict(Counter(list_horas))
horas_df = pd.DataFrame(dict_horas.items(), columns=['Hora', 'Frequencia'])
horas_df.plot(kind='bar', x = 'Hora', y='Frequencia', title='Frequencia de mensagens por horário',figsize=(20,8), color=['#000000'])

