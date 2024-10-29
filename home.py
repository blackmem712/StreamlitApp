import streamlit as st
import plotly.express as px
import pandas as pd
from datetime import datetime

# Configuração da Página
st.set_page_config(page_title="Meu Site Streamlit", layout="wide")

# Função para carregar o CSS global
def carregar_css():
    st.markdown("""
        <style>
        /* Cabeçalho */
        .header {
            text-align: center;
            background-color: #4CAF50;
            color: white;
            padding: 20px;
            border-radius: 8px;
            margin-bottom: 30px;
        }
        .header h1 {
            font-size: 36px;
            margin: 0;
        }
        .header h3 {
            font-size: 20px;
            margin: 5px 0 0 0;
            font-weight: 300;
        }

        /* Filtros */
        .filter-section {
            background-color: #f9f9f9;
            padding: 20px;
            border-radius: 8px;
            margin-bottom: 20px;
        }

        /* Títulos de Seções */
        .section-title {
            font-size: 24px;
            color: #4CAF50;
            margin: 0;
            font-weight: 600;
        }

        /* Tabela */
        .stDataFrame {
            border: 1px solid #ddd;
            border-radius: 8px;
        }

        /* Rodapé */
        .footer {
            text-align: center;
            font-size: 14px;
            color: #777;
            margin-top: 30px;
        }
        </style>
    """, unsafe_allow_html=True)

# Função para exibir o cabeçalho
def exibir_cabecalho():
    st.markdown("""
        <div class="header">
            <h1>Dashboard de Faturamento</h1>
            <h3>Análise de dados de vendas por data, categoria e cidade</h3>
        </div>
    """, unsafe_allow_html=True)

# Função para exibir os filtros de seleção de dados
def exibir_filtros(dados):
    st.markdown('<div class="filter-section">', unsafe_allow_html=True)
    st.write("### Selecione o intervalo de datas e filtros:")
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        data_inicio = st.date_input("Data Início", value=dados['Order Date'].min(), min_value=dados['Order Date'].min(), max_value=dados['Order Date'].max())
        data_fim = st.date_input("Data Fim", value=dados['Order Date'].max(), min_value=dados['Order Date'].min(), max_value=dados['Order Date'].max())
    
    with col2:
        categorias_disponiveis = dados['Category'].unique()
        cidades_disponiveis = dados['Purchase Address'].unique()
        categorias_selecionadas = st.multiselect("Categoria de Compra", options=categorias_disponiveis)
        cidades_selecionadas = st.multiselect("Capital de Estado", options=cidades_disponiveis)
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    return data_inicio, data_fim, categorias_selecionadas, cidades_selecionadas

# Função para exibir o gráfico de barras
def exibir_grafico_barras(dados_filtrados):
    st.markdown('<p class="section-title">Faturamento por Capital de Estado</p>', unsafe_allow_html=True)
    if not dados_filtrados.empty:
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
    else:
        st.warning("Nenhum dado encontrado para o intervalo de datas selecionado.")

# Função para exibir o gráfico de linhas
def exibir_grafico_linhas(dados_filtrados):
    st.markdown('<p class="section-title">Evolução do Faturamento Mensal por Categoria</p>', unsafe_allow_html=True)
    if not dados_filtrados.empty:
        dados_filtrados['Mes'] = dados_filtrados['Order Date'].dt.to_period('M')
        dados_agrupados = dados_filtrados.groupby(['Mes', 'Category'])['Price Each'].sum().reset_index()
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

def exibir_grafico_pizza(dados_filtrados):
    st.markdown('<p class="section-title">Proporção do Faturamento por Categoria</p>', unsafe_allow_html=True)
    if not dados_filtrados.empty:
        dados_categoria = dados_filtrados.groupby('Category')['Price Each'].sum().reset_index()
        fig = px.pie(dados_categoria, 
                     names='Category', 
                     values='Price Each', 
                     title='Proporção de Faturamento por Categoria')
        fig.update_traces(textposition='inside', textinfo='percent+label')
        st.plotly_chart(fig, use_container_width=True)


# Tabela: Resumo por Categoria e Cidade
def exibir_resumo_categoria_cidade(dados_filtrados):
    st.markdown('<p class="section-title"> Faturamento por Categoria e Cidade</p>', unsafe_allow_html=True)
    resumo = dados_filtrados.groupby(['Category', 'Purchase Address'])['Price Each'].sum().reset_index()
    resumo = resumo.rename(columns={'Category': 'Categoria', 'Purchase Address': 'Cidade', 'Price Each': 'Total Faturamento (R$)'})
    st.dataframe(resumo.style.format({"Total Faturamento (R$)": "R${:,.2f}"}))

# Tabela: Produtos Mais Vendidos
def exibir_produtos_mais_vendidos(dados_filtrados):
    st.markdown('<p class="section-title">Produtos Mais Vendidos</p>', unsafe_allow_html=True)
    produtos_vendidos = dados_filtrados.groupby('Product').agg(
        Total_Unidades=('Quantity Ordered', 'sum'),
        Total_Faturamento=('Price Each', 'sum')
    ).reset_index()
    produtos_vendidos = produtos_vendidos.sort_values(by='Total_Unidades', ascending=False)
    st.dataframe(produtos_vendidos.style.format({"Total_Faturamento": "R${:,.2f}"}))


# Tabela: Desempenho Mensal por Categoria
def exibir_desempenho_mensal_categoria(dados_filtrados):
     st.markdown('<p class="section-title">Desempenho Mensal por Categoria</p>', unsafe_allow_html=True)
     dados_filtrados['Mes'] = dados_filtrados['Order Date'].dt.to_period('M')
     desempenho_mensal = dados_filtrados.groupby(['Mes', 'Category'])['Price Each'].sum().unstack().fillna(0)
    
     # Converter índice de período para o nome do mês
     desempenho_mensal.index = desempenho_mensal.index.to_timestamp()
     desempenho_mensal.index = desempenho_mensal.index.strftime('%B %Y')  # Converte para o nome do mês e ano

     st.dataframe(desempenho_mensal.style.format("R${:,.2f}"))

# Função para exibir o rodapé
def exibir_rodape():
    st.markdown("""
        <div class="footer">
            <p>Desenvolvido por [Seu Nome] - Todos os direitos reservados © 2024</p>
        </div>
    """, unsafe_allow_html=True)

# Função que carrega os dados
@st.cache_data
def carregar_dados():
    tabela = pd.read_csv("novos_dados.csv")
    tabela['Order Date'] = pd.to_datetime(tabela['Order Date'])
    tabela['Price Each'] = tabela['Price Each'].astype(float)
    return tabela


def filtrar_dados(dados, data_inicio, data_fim, categorias, cidades):
    data_inicio = datetime.combine(data_inicio, datetime.min.time())
    data_fim = datetime.combine(data_fim, datetime.max.time())
    
    dados_filtrados = dados[(dados['Order Date'] >= data_inicio) & (dados['Order Date'] <= data_fim)]
    
    if categorias:
        dados_filtrados = dados_filtrados[dados_filtrados['Category'].isin(categorias)]
    if cidades:
        dados_filtrados = dados_filtrados[dados_filtrados['Purchase Address'].isin(cidades)]
    
    return dados_filtrados


carregar_css()
exibir_cabecalho()


dados = carregar_dados()
data_inicio, data_fim, categorias_selecionadas, cidades_selecionadas = exibir_filtros(dados)


if data_inicio > data_fim:
    st.error("Erro: A data de início não pode ser depois da data final.")
else:
    dados_filtrados = filtrar_dados(dados, data_inicio, data_fim, categorias_selecionadas, cidades_selecionadas)
    exibir_grafico_barras(dados_filtrados)
    exibir_grafico_linhas(dados_filtrados)

    col1,copesp ,col2 = st.columns([1, 0.5, 1.2])
 
    with col1:
      exibir_grafico_pizza(dados_filtrados)
    with copesp:
        st.markdown("")
    with col2:
     exibir_desempenho_mensal_categoria(dados_filtrados)

    col1, col2 = st.columns([1, 1])

    with col1:
     exibir_produtos_mais_vendidos(dados_filtrados) 
    
   
    with col2:
     exibir_resumo_categoria_cidade(dados_filtrados)

# Exibir o rodapé
exibir_rodape()

