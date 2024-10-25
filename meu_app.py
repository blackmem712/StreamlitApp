import streamlit as st
import plotly.express as px
import pandas as pd

st.set_page_config(page_title="Meu Site Streamlit",layout="wide")

st.title("Gráficos de Faturamento")
st.write("### Selecione o intervalo de datas:")

# Função que carrega os dados
@st.cache_data
def carregar_dados():
    tabela = pd.read_csv("novos_dados.csv")
    tabela['Order Date'] = pd.to_datetime(tabela['Order Date'])  # Converte a coluna de datas para datetime
    tabela['Price Each'] = tabela['Price Each'].astype(float)    # Converte preços para float
    return tabela

# Função para filtrar os dados com base na data de início e data de fim
def filtrar_data(dados, data_inicio, data_fim):
    data_inicio = pd.to_datetime(data_inicio)
    data_fim = pd.to_datetime(data_fim)
    return dados[(dados['Order Date'] >= data_inicio) & (dados['Order Date'] <= data_fim)]

# Função que carrega o gráfico de barras
def carregar_grafico_barras(dados_filtrados):
    if dados_filtrados.empty:
        st.warning("Nenhum dado encontrado para o intervalo de datas selecionado.")
        return
    fig = px.bar(
        dados_filtrados,
        x='Purchase Address',
        y='Price Each',
        color='Category',
        labels={'Price Each': 'Faturamento (R$)'},
        title="Faturamento por Capital de Estado",
        height=400
    )
    fig.update_layout(
        yaxis_tickprefix='R$',  
        yaxis_tickformat=',.2f',  
        xaxis_title="Endereço de Compra",
        yaxis_title="Faturamento (R$)",
        bargap=0.5  
    )
    st.plotly_chart(fig, use_container_width=True)

# Função que carrega o gráfico de linhas
def carregar_grafico_linhas(dados):
    dados['Mes'] = dados['Order Date'].dt.to_period('M')
    dados_agrupados = dados.groupby(['Mes', 'Category'])['Price Each'].sum().reset_index()
    dados_agrupados['Mes'] = dados_agrupados['Mes'].dt.to_timestamp()
    fig = px.line(dados_agrupados, 
                  x='Mes', 
                  y='Price Each', 
                  color='Category',  
                  labels={'Price Each': 'Faturamento (R$)', 'Mes': 'Mês'},
                  title="Evolução do Faturamento Mensal por Categoria")
    fig.update_layout(
        yaxis_tickprefix='R$',  
        yaxis_tickformat=',.2f',  
        xaxis_title="Mês",
        yaxis_title="Faturamento (R$)"
    )
    st.plotly_chart(fig, use_container_width=True)

 # Carrega os dados
dados = carregar_dados()

 

with st.container():
  
    col1, col_esp,col2 = st.columns([1.2,0.1 ,1]) # Define duas colunas, cada uma com 50% da largura

    with col1:
        # Carrega o gráfico de barras na primeira coluna
   
       col_data_inicio, col_data_fim, col_graph = st.columns([1, 1, 1])
       
       with col_data_inicio:
        
        data_inicio = st.date_input("Data Início", value=dados['Order Date'].min(), min_value=dados['Order Date'].min(), max_value=dados['Order Date'].max())
       
       with col_data_fim:
        data_fim = st.date_input("Data Fim", value=dados['Order Date'].max(), min_value=dados['Order Date'].min(), max_value=dados['Order Date'].max())
      
       if data_inicio > data_fim:
         st.error("Erro: A data de início não pode ser depois da data final.")

       else:
         dados_filtrados = filtrar_data(dados, data_inicio, data_fim) 
         carregar_grafico_barras(dados_filtrados) 

       if not dados_filtrados.empty:
         max_valor = dados_filtrados['Price Each'].max()
        

         

         
         
    with col_esp:
         st.write("")
            
    with col2:
     st.markdown("")
     st.markdown("")
     st.markdown("")
     st.markdown("")
     st.markdown("")
     st.markdown("")
     st.markdown("")
     st.markdown("")
     
     
    
     
     tabela_pivot = dados.pivot_table(
     index='Product',         # As linhas serão os produtos
     columns='Category',      # As colunas serão as categorias
     values='Price Each',     # Os valores serão o faturamento (Price Each)
     aggfunc='sum',           # Soma o faturamento para cada combinação
     fill_value=0             # Substitui valores ausentes por 0
     )
 
           # Exibir a tabela dinâmica no Streamlit
 
     st.write("###### Tabela de Faturamento por Produto e Categoria")
     st.markdown("")
     st.markdown("")
     st.dataframe(tabela_pivot.style.format("R${:,.2f}"))  # Formatar valores como monetários
  


carregar_grafico_linhas(dados)

   
