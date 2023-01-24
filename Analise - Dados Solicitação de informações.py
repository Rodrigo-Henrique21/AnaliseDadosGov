#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
import seaborn as sns 
import matplotlib
import matplotlib.pyplot as plt
get_ipython().run_line_magic('matplotlib', 'inline')
sns.set_style('darkgrid')
matplotlib.rcParams['font.size'] = 14
matplotlib.rcParams['figure.figsize'] = (9,5)
matplotlib.rcParams['figure.facecolor'] = '#00000000'


# In[2]:


file_name = "20230115_Pedidos_csv_2022.csv"
path = r"C:\Users\rhcorrea\OneDrive - Stefanini\Desktop\Python\Pandas\Treinamento_2\Base_de_dados"
path_complete = path+"\\"+file_name
columns = ["id_pedido","nr_pedido","competencia","orgao","status","data_solicitacao","pedido_feito",
           "justificativa","data_conclusao","status_respostas","status_solucao","evidencia","meio_de_comunicao","id_mensagem",
           "tipo_de_assunto","assunto_n1","assunto_n2","data_respota","resposta","conclusao_do_pedido","complemento"]


# In[3]:


pedidos = pd.read_csv(path_complete,sep = ";" , header = None ,encoding = "UTF-16 LE" )


# In[4]:


pedidos.columns


# In[5]:


for col_old,col_new in zip(pedidos.columns,columns):
    pedidos.rename(columns={col_old:col_new}, inplace=True)


# In[6]:


pedidos.index.name = "quantidade_pedidos"
pedidos.columns.name = "detalhes_do_pedido"


# In[7]:


pedidos.dtypes


# In[8]:


pedidos = pedidos.convert_dtypes(infer_objects=True)


# In[9]:


pedidos["data_solicitacao"] = pedidos["data_solicitacao"].str.replace("/","-")
pedidos["data_conclusao"] = pedidos["data_conclusao"].str.replace("/","-")
pedidos["data_respota"] = pedidos["data_respota"].str.replace("/","-")


# In[10]:


pedidos[["data_solicitacao","data_conclusao","data_respota"]] = pedidos[["data_solicitacao","data_conclusao","data_respota"]].apply(pd.to_datetime,format='%d-%m-%Y')


# In[11]:


pedidos.info()
#pedidos.dtypes


# In[12]:


pedidos["status"].describe()


# In[13]:


pedidos["assunto_n1"].describe()


# In[14]:


print(pedidos.isna().sum())


# In[15]:


pedidos.fillna(method = 'ffill', inplace = True)


# In[139]:


total_de_pedidos = pedidos["id_pedido"].count()
competencias = pedidos["competencia"].unique()
data_minima = pedidos["data_solicitacao"].min()
data_maxima = pedidos["data_solicitacao"].max()
meios_de_comunicacao = pedidos["meio_de_comunicao"].groupby(pedidos["meio_de_comunicao"]).count().sort_values(ascending = False)
tipos_de_assuntos = pedidos["tipo_de_assunto"].groupby(pedidos["tipo_de_assunto"]).count().sort_values(ascending = False)
quantidade_dias = abs((data_minima - data_maxima).days)
media_de_pedidos_data = total_de_pedidos/quantidade_dias
df_qtd_pedido = pedidos[["data_solicitacao","id_pedido"]]
quantidade_pedidos_mes = df_qtd_pedido[["id_pedido"]].groupby(df_qtd_pedido["data_solicitacao"].dt.month).count().sort_values(by="data_solicitacao",ascending = False)
quantidade_pedidos_dia = df_qtd_pedido[(df_qtd_pedido["data_solicitacao"].dt.quarter == 1) & (df_qtd_pedido["id_pedido"] > 0)].groupby("data_solicitacao").count().sort_values(by="id_pedido",ascending = False)
conclusao_do_pedido = pedidos[["conclusao_do_pedido","id_pedido"]].groupby("conclusao_do_pedido").count().sort_values(by = "id_pedido",ascending = False)


# In[17]:


total_de_pedidos


# In[18]:


competencias


# In[19]:


meios_de_comunicacao


# In[20]:


tipos_de_assuntos


# In[148]:


quantidade_pedidos_mes.index.name="index"
quantidade_pedidos_mes.columns.name=None
quantidade_pedidos_mes["mes"] = quantidade_pedidos_mes.index
x = quantidade_pedidos_mes["mes"]
y = quantidade_pedidos_mes["id_pedido"]
plt.barh(x,y)


# In[23]:


axes = quantidade_pedidos_dia.plot(figsize=(11,9), subplots=False,linewidth=1)


# In[95]:


conclusao_do_pedido


# In[54]:


plt.figure(figsize=(10,10))
plt.plot(pedidos[["data_conclusao","data_solicitacao"]])
plt.title("Comparação total de solicitações vs conclusao dos pedidos")
plt.xlabel("data")
plt.ylabel("Contagem")
plt.legend(["conclusao","solicitacao"], loc="upper center",bbox_to_anchor=(1.2,1))


# In[ ]:




