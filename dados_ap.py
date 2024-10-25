import pandas as pd

tabela = pd.read_csv("sales_data_example.csv")

####### Mostrar as primeiras linhas do arquivo csv

#print(tabela.head())

######## Verificar se há valores nulos  
valor_nulo = tabela.isnull().sum()

#print(valor_nulo)

###### conferir os tipos de dados em cada coluna
tipos_dados = tabela.dtypes

#print(tipos_dados)
 

####### Converter a coluna 'Order Date' para o tipo datetime

tabela['Order Date'] = pd.to_datetime(tabela['Order Date'])


####### Verificar se há linhas duplicadas
duplicatas = tabela.duplicated().sum()

#print(duplicatas)




###### Verificar se há valores negativos ou iguais a zero nas colunas 'Quantity Ordered' e 'Price Each'

verificar_QO = tabela[tabela['Quantity Ordered'] <= 0]
verificar_PE= tabela[tabela['Price Each'] <= 0]

#print(verificar_PE,verificar_QO)

#####Obter valores únicos da coluna 'Category'
categorias_unicas = tabela['Category'].unique().tolist()

######Exibir os valores únicos

#print(categorias_unicas)

##### Obter valores únicos da coluna 'Product'
#produtos_unicos = tabela['Product'].unique().tolist()

#### Exibir os valores únicos
#print(produtos_unicos)

# Obter valores únicos da coluna 'Purchase Address'
enderecos_unicos = tabela['Purchase Address'].unique().tolist()

# Exibir os valores únicos
#print(enderecos_unicos)

# Remove o número e a palavra "Street" da coluna 'Purchase Address'
tabela['Purchase Address'] = tabela['Purchase Address'].str.replace(r'\d+\s*', '', regex=True)  # Remove números, o (\d+) remove digitos 0 a 9, 

tabela['Purchase Address'] = tabela['Purchase Address'].str.replace(r'\bStreet\b', '', regex=True)  # Remove a palavra "Street", o(\b delimita a palavra como unica, e não pertencente a outra)

# Remove espaços em branco que podem ter sido deixados

tabela['Purchase Address'] = tabela['Purchase Address'].str.strip()

# Salvar o DataFrame modificado em um novo arquivo CSV
tabela.to_csv('novos_dados.csv', index=False)


tabela_nova = pd.read_csv("novos_dados.csv")

enderecos_unicos = tabela_nova['Purchase Address'].unique().tolist()

print(enderecos_unicos)