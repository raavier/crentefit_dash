import pandas as pd
import re
import streamlit as st
#import plotly.express as px
#import plotly.graph_objects as go
#from transform_data import DataProcessor, readTransformgsheet
#from tabs import tab1, tab2, tab3, tab4, tab5, tab6
import numpy as np
import plotly.express as px

data = """
Semana 1 - 05/08 à 11/08

5x
Cássio - 90 + 60 + 30 + 60 + [50]
Fernanda A. - 72 + 47 + 47 + 36 + [54]
Fernanda S. - 30 + 35 + 35
Fernanda W. - 70 + 89 + [64] + 80 + 80 
Gabi - 75 + 69 + [62] + 63 + 52
Luciano - 70+34+47+49+121+[30]
Marina - 60 + 60 + [34] + 60 + 41
Pedro Augusto - [30] + 47 + 32 + 32 + 60 + 30
Samuel - 80 +70 + 40 + [48] + 52 + 36

4x
Amanda M. - 50 + 60 + [54] + 60 + 40
Caio - 60 + 62 + 38 + [84]
David - [42] + 36 + 35 + 33
João Marcos - 60 + 60 + 50 + 60 + [40]
Lívia - 60 + 54 + [40] + 31 + 49
Mairon - 38
Naama - 46+ [31] + 50 +35
Mary - 47+ 73+78+64
   
3x
Amanda G. - [88] + 32 + 34 + 36
André - 32 + [85] + 95
Bianca - 43 + 39 + 62
Brenda -
Camila - 31
Guilherme - 41 + 45
Hamilton - [98] + 46 + 41
Patrícia -
Ravier - [129] + 39 + 42
Talita - 64 + 57 + 60 + [53]
Rebeca - 32 + 40 + 62 

2x
Anna - 33
Carol - [85] + 95
João Vitor -
Julia - 53 + 41 
Keren - 25+
Leandro - 34
Thaís - 56 + [31]

Semana 2 - 12/08 à 18/08

5x
Cássio - 60 + 73 + 60 + 60 +[43]
Fernanda A. - 54 + 34 +40 + 34 + [51]
Fernanda S. - 40 + 60 + 45 + 35 + 30 + [46]
Fernanda W. - 82 + 68 + 46 + 86 + 93 + [137]
Gabi - 76 + [87] + 75 + 33 + 32
Luciano - 45 + 30 + 41 + 31 + [34]
Marina - 60 + 73 + 60 + 60 +[64]
Pedro Augusto - 30 + 56 + 30 + 30 + 30 + [30]
Samuel - 96 + 77 + 62 + 86 + 103 + [137]
Tiago Lang - 100 + 75+ 115+ [121]

4x
Amanda M. - 32 + 60 + 30
Caio - 40 + 37 + 43 + [68]
David - [45] + 42 + 30 + 48
João Marcos - 60 + 60 + 30 + 30
Lívia - 40 + 60+ 60 + [60]+ 60
Mairon - 30 + [60]
Mary - 85 + 76 + [101] + 50+ 58
Naama - 51 + 35 + 49

3x
Amanda G. -
André - 58 + [111] + 90
Bianca - [46] +
Brenda -
Camila - 38
Guilherme - [28] + 48+ 30
Hamilton - 44 + 36 + [74]
Patrícia - 60 + 61 + 55
Ravier - [90] + 42 + 30
Rebeca - 62 + 85
Talita - 31 + 66 + [35]

2x
Anna - 44 + 34
Carol - [111] + 90
João Vitor -
Julia - 42 + 51
Keren -
Leandro -
Thaís - 47 + 59

Semana 3 - 19/08 à 25/08

5x
Cássio - 60 + 60 + 60 + 60 + [43]
Fernanda A. - 31 + 47 +[60]+ 46 + 49
Fernanda S. - 40 + 33 + 35 + 35 + [30]
Fernanda W. - 85 + 82 + 92 + 84 + 80
Gabi - 55 + [117] + 90 + 32 + 49
Luciano - 33+62+38+40+[54]
Marina - 60 + 60 + 60 + 60 + 60 + [40]
Pedro Augusto - [90] + 66 + 63 + 35 + 57
Samuel - [220] + 54 + 62 + 60 + 37
Tiago Lang - 101 +70 +73 +95 +90 +[35]

4x
Amanda M. - 75 + 50 + 30 + 67
Caio - 50 + 43 + 36 + [102]
David - 73 + [44] + 62 + 64 + 57
João Marcos - 75 + 30 + 50 + 67 + 30
Lívia - 50+ 60+ 70+ [40]+ 80
Mairon - [61]
Mary - 82 + [83] +78 + 53 + 60
Naama - 50 + 43 + 31

3x
Amanda G. -
André - 66 + [116] + 120
Bianca - 36
Brenda -
Camila - 31
Guilherme - 32 + [21] + 30
Hamilton - 41 + [74]
Patrícia - 45 + 73
Ravier - [116] + 90 + 35
Rebeca - 49 + 52+ 52
Talita - 82

2x
Anna - [40] + 32
Carol - [116] + 120
João Vitor -
Julia - 51
Keren - 20 +
Leandro - 35 +32
Thaís - 0

Semana 4 - 26/08 à 01/09

5x
Cássio - 60 + 60 + 60 + 37 + [57]
Fernanda A. - 43 + 61 + 40 + 88 + [ 40]
Fernanda S. - 35
Fernanda W. - 86 + 126 + [123] + 73 + 66
Gabi - 45 + 38 + 31 + 34 + [120]
Luciano - 30 + 56 + 30 + 30 + 32 + [34]
Marina - 60 + 60 + 60 + 60 + [37]
Pedro Augusto - 42 + 30 + 58 + 57 + [90]
Samuel - 100 + 170 + [123] + 74 + 130 + 80 + 110
Tiago Lang - 

4x
Amanda M. - 70 + 70 + 70 + 70 + [40]
Caio - 36 + 31 + 36 + [78]
David - [42] + 55 + 30 + 71
João Marcos - 70 + 70 + 55 + 70 + 70 + [40]
Lívia - 70 + [45] + 70 + 60 + 70 + 60
Mairon - 30 + 32 + [270]
Mary - 85 + [86] + 33
Naama - 46 + [35]

3x
Amanda G. - 55 + 58 + [49] + 57
André - 43 + [115] + 38
Bianca - 39 + [50]
Camila - [30] + 31 + 32
Guilherme - [33]
Hamilton - [95] + 48 + 46
Patrícia - 58 + 47 + 37 + [50]
Ravier - [128] + 46 + 32
Rebeca - 60 + 50
Talita - 63 + [40] + 58

2x
Anna - 33
Carol - [115] + 38
João Vitor - 92 + 77 + 40
Julia - 36 + 57
Keren - [44] + 28 + 53
Leandro - 33 + [36]
Thaís - [41]
"""
# Split the data by "Semana" to handle multiple weeks
semana_blocks = re.split(r'Semana (\d+) -', data)

# Initialize lists to store the dataframe columns
names = []
semanas = []
types = []
minutes = []
selected_aerobics = []

# Iterate through the blocks to handle each week separately
for i in range(1, len(semana_blocks), 2):
    semana = semana_blocks[i]
    block = semana_blocks[i + 1]
    lines = block.split('\n')

    # Initialize variables
    current_type = None

    # Iterate through the lines
    for line in lines:
        line = line.strip()
        if line.endswith('x'):
            current_type = line
        elif '-' in line:
            parts = line.split(' - ')
            if len(parts) == 2:  # Ensure there are exactly two parts to unpack
                name, minute_data = parts
                minute_data = minute_data.split('+')
                for minute in minute_data:
                    minute = minute.strip()
                    if minute:
                        selected_aerobic = bool(re.search(r'\[\d+\]', minute))
                        minute_value = int(re.search(r'\d+', minute).group())
                        names.append(name)
                        semanas.append(semana)
                        types.append(current_type)
                        minutes.append(minute_value)
                        selected_aerobics.append(selected_aerobic)

# Create the dataframe
df = pd.DataFrame({
    'name': names,
    'semana': semanas,
    'type': types,
    'minutes': minutes,
    'selected_aerobic': selected_aerobics
})

distinct_semanas_geral = int(df['semana'].max())

print(distinct_semanas_geral)
# Group by name, semana, and type, then count and sum as requested using pandas
result = df.groupby(["name", "semana", "type"]).agg(
    sum_minutes=("minutes", "sum"),
    count_minutes=("minutes", "count"),
    sum_selected_aerobic_minutes=("minutes", lambda x: x[df.loc[x.index, "selected_aerobic"]].sum())
    
).reset_index()




# Assuming 'result' is a pandas DataFrame and 'type' is a column in it

result['type_num'] = result['type'].str.replace('x', '').astype(int)
result['points_week'] = np.where(result['count_minutes'] > 0,np.where(result['count_minutes'] >= result['type_num'], 3, 1),0)

df_ranking_semana = result.groupby(['name', 'type','semana']).agg(
    total_minutes_week=('sum_minutes','sum'),
    total_points_week=('points_week', 'sum'),
    total_sum_selected_aerobic_minutes=('sum_selected_aerobic_minutes', 'sum'),
    distinct_semana_count=("semana", "nunique")
).reset_index()

df_ranking_semana["adjusted_sum_selected_aerobic_minutes"] = (df_ranking_semana["total_sum_selected_aerobic_minutes"] / distinct_semanas_geral)
print(df_ranking_semana)
df_ranking = result.groupby(['name', 'type',]).agg(
    total_minutes_week=('sum_minutes','sum'),
    total_points_week=('points_week', 'sum'),
    total_sum_selected_aerobic_minutes=('sum_selected_aerobic_minutes', 'sum'),
    distinct_semana_count=("semana", "nunique")
).reset_index()

df_ranking["adjusted_sum_selected_aerobic_minutes"] = (df_ranking["total_sum_selected_aerobic_minutes"] / distinct_semanas_geral)

def rank_type(df_type):
    df_type = df_type.sort_values(by=['total_points_week', 'adjusted_sum_selected_aerobic_minutes'], ascending=[False, False])
    df_type['rank'] = df_type[['total_points_week', 'adjusted_sum_selected_aerobic_minutes']].apply(tuple, axis=1).rank(method='min', ascending=False).astype(int)
    return df_type

# Apply the ranking function to each group
ranked_dfs = [rank_type(group) for _, group in df_ranking.groupby('type')]

# Merge all the ranked DataFrames back into a single DataFrame
df_ranked = pd.concat(ranked_dfs).reset_index(drop=True)

# Sort the final DataFrame by type and rank
df_ranked = df_ranked.sort_values(by=['type', 'rank']).reset_index(drop=True)

#print(result)
#print(df_ranked)

print(df_ranked)

st.set_page_config(page_title="Crente Fit 2.0",layout="wide")

st.title("🏖 Incentivo mútuo ao cuidado com o corpo que Deus nos deu")
#st.subheader("Uma experiência sem plástico")
st.markdown("###")

#sidebar
#st.sidebar.image("material/img/logo.png")
st.sidebar.title("CRENTE FIT 2.0")
st.sidebar.header("Escolha seus filtros: ")

tipoModalidade = st.sidebar.multiselect("Escolha a modalidade: ", sorted(result["type"].unique()))
if not tipoModalidade:
    df_result2 = result.copy()
    df_rank2 = df_ranked.copy()
else:
    df_result2 = result[result["type"].isin(tipoModalidade)]
    df_rank2 = df_ranked[df_ranked["type"].isin(tipoModalidade)]

# Tipo de Nome
nomeCrente = st.sidebar.multiselect("Escolha o Crente: ", sorted(df_result2["name"].unique()))
if not nomeCrente:
    df_result3 = df_result2.copy()
    df_rank3 = df_rank2.copy()
else:
    df_result3 = df_result2[df_result2["name"].isin(nomeCrente)]
    df_rank3 = df_rank2[df_rank2["name"].isin(nomeCrente)]

# Tipo de Semana
tipoSemana = st.sidebar.multiselect("Escolha a Semana: ", sorted(result["semana"].unique()))
if not tipoSemana:
    df_result4 = df_result3.copy()
else:
    df_result4 = df_result3[df_result3["semana"].isin(tipoSemana)]
    

# Condicionais finais
if not tipoModalidade and not nomeCrente and not tipoSemana:
    filtered_result_df = result
    filtered_rank_df = df_ranked
elif not tipoModalidade and not nomeCrente:
    filtered_result_df = df_result4.copy()
    filtered_rank_df = df_ranked
elif not tipoModalidade and not tipoSemana:
    filtered_result_df = df_result3[df_result3["name"].isin(nomeCrente)]
    filtered_rank_df = df_rank3[df_rank3["name"].isin(nomeCrente)]
elif not nomeCrente and not tipoSemana:
    filtered_result_df = result[result["type"].isin(tipoModalidade)]
    filtered_rank_df = df_ranked[df_ranked["type"].isin(tipoModalidade)]
elif not tipoModalidade:
    filtered_result_df = df_result4[df_result4["name"].isin(nomeCrente)]
    filtered_rank_df = df_rank3[df_rank3["name"].isin(nomeCrente)]
elif not nomeCrente:
    filtered_result_df = df_result4[df_result4["type"].isin(tipoModalidade)]
    filtered_rank_df = df_rank3[df_rank3["type"].isin(tipoModalidade)]
elif not tipoSemana:
    filtered_result_df = df_result3[df_result3["type"].isin(tipoModalidade) & df_result3["name"].isin(nomeCrente)]
    filtered_rank_df = df_rank3[df_rank3["type"].isin(tipoModalidade) & df_rank3["name"].isin(nomeCrente)]
else:
    filtered_result_df = df_result4[df_result4["type"].isin(tipoModalidade) & df_result4["name"].isin(nomeCrente)]
    filtered_rank_df = df_rank3[df_rank3["type"].isin(tipoModalidade) & df_rank3["name"].isin(nomeCrente)]


filtered_rank_df = filtered_rank_df.rename(columns={
    "name": "Nome",
    "type": "Modalidade",
    "total_minutes_week": "Soma Minutos na Semana",
    "total_points_week": "Pontuação",
    "adjusted_sum_selected_aerobic_minutes": "Média Desempate (min)",
    "rank": "Rank"
})

filtered_result_df = filtered_result_df.rename(columns={
    "name": "Nome",
    "type": "Modalidade",
    "sum_minutes": "Soma de Minutos",
    "count_minutes": "Quantidade de Atividades Registradas na Semana",
    "points_week": "Pontuação",
    "adjusted_sum_selected_aerobic_minutes": "Média Desempate (min)"
})
    
filtered_result_df = filtered_result_df.drop(columns=['type_num'])
# Agrupar os dados por semana e modalidade para calcular o total de pessoas
total_pessoas_por_semana_modalidade = filtered_result_df.groupby(['semana', 'Modalidade']).size().reset_index(name='Total')

# Filtrar os dados para quem conseguiu 3 pontos, agrupando por semana e modalidade
pessoas_com_3_pontos_modalidade = filtered_result_df[filtered_result_df['Pontuação'] == 3].groupby(['semana', 'Modalidade']).size().reset_index(name='Conseguiu_3_Pontos')

# Juntar os dois DataFrames para calcular a porcentagem
df_aderencia_modalidade = pd.merge(total_pessoas_por_semana_modalidade, pessoas_com_3_pontos_modalidade, on=['semana', 'Modalidade'])

# Calcular a porcentagem de pessoas que conseguiram 3 pontos por modalidade
df_aderencia_modalidade['Porcentagem'] = (df_aderencia_modalidade['Conseguiu_3_Pontos'] / df_aderencia_modalidade['Total']) * 100

# Formatando a porcentagem para ter apenas uma casa decimal
df_aderencia_modalidade['Porcentagem'] = df_aderencia_modalidade['Porcentagem'].round(1)
df_aderencia_modalidade['semana'] = df_aderencia_modalidade['semana'].astype(str)


# Exibir o DataFrame resultante
#st.write(df_aderencia_modalidade)
#st.write(filtered_result_df)
#st.write(filtered_rank_df)
selected_columns_df = filtered_rank_df[["Rank", "Nome", "Pontuação", "Média Desempate (min)", "Modalidade"]].reset_index(drop=True)
#print(selected_columns_df[selected_columns_df['Modalidade'] == '2x'].drop(columns=["Modalidade"]))
print("filtered_result_df:",filtered_result_df)
df_weekly_sum = filtered_result_df.groupby(['semana', 'Modalidade'])['Soma de Minutos'].sum().reset_index()
df_weekly_sum['semana'] = df_weekly_sum['semana'].astype(str)
with st.container():
    col1, col2 = st.columns([1,1])
    with col1:
        #st.subheader('Aderência a Meta dos Crentes:')
        # Criar o gráfico de linhas categorizado por Modalidade
        fig = px.line(df_aderencia_modalidade,
            x='semana',
            y='Porcentagem',
            color='Modalidade',
            labels={'semana': 'Semana', 'Porcentagem': 'Porcentagem de Cumprimento de Metas (%)', 'Modalidade': 'Modalidade'},
            title="Os crentes estão cumprimdo suas metas?",
            markers=True,  # Adiciona marcadores nos pontos de dados
            text='Porcentagem')  # Adiciona os valores como labels"

        # Ajustar a posição dos labels para ficarem acima dos pontos
        fig.update_traces(textposition='top left')
        # Ajustar o layout para garantir que o eixo x mostre apenas valores inteiros
        fig.update_layout(
            xaxis=dict(
                tickmode='array',
                tickvals=[str(i) for i in sorted(df_aderencia_modalidade['semana'].astype(int).unique())],
            )
        )
        # Exibir o gráfico
        st.plotly_chart(fig)
    with col2:
        #st.subheader('Minutos exercitados por Semana:')
        # Criando o gráfico
        fig = px.line(df_weekly_sum,
                x='semana',
                y='Soma de Minutos',
                color='Modalidade',
                labels={'semana': 'Semana', 'Soma de Minutos': 'Minutos Somados', 'Modalidade': 'Modalidade'},
                title="Evolução dos Minutos Somados por Semana",
                category_orders={'semana': sorted(df_weekly_sum['semana'].unique(), key=int),
                                'Modalidade': sorted(filtered_result_df['Modalidade'].unique())},
                markers=True,
                text='Soma de Minutos')  # Adiciona marcadores nos pontos de dados
        # Ajustar o layout para garantir que o eixo x mostre apenas valores inteiros
        fig.update_layout(
            xaxis=dict(
                tickmode='array',
                tickvals=[str(i) for i in sorted(df_weekly_sum['semana'].astype(int).unique())],
            )
        )
        # Exibindo o gráfico
        fig.update_traces(textposition="top center")
        
        # Display the chart in Streamlit
        st.plotly_chart(fig, use_container_width=True)
st.markdown("---")  

with st.container():
    st.subheader('Minutos exercitados por Crente:')
    
    # Create the bar chart
    fig = px.bar(filtered_result_df, 
                 x='Nome', 
                 color="Modalidade", 
                 y="Soma de Minutos",
                 labels={'Nome': '', "Modalidade": 'Modalidade', 'Soma de Minutos':''},
                 category_orders={'Modalidade': sorted(filtered_result_df['Modalidade'].unique())},
                 text='Soma de Minutos')  # Add labels to each bar
    
    # Update layout to customize text appearance if needed
    fig.update_traces(textposition='auto')
    
    # Display the chart in Streamlit
    st.plotly_chart(fig, use_container_width=True)
    st.markdown("---")  

with st.container():
    col1, col2 = st.columns([1,1])
    with col1:
        st.subheader('Modalidade 2x:')
        st.dataframe(selected_columns_df[selected_columns_df['Modalidade'] == '2x'].drop(columns=["Modalidade"]),hide_index=True)
    with col2:
        st.subheader('Modalidade 3x:')
        st.dataframe(selected_columns_df[selected_columns_df['Modalidade'] == '3x'].drop(columns=["Modalidade"]),hide_index=True)
    st.markdown("---")    
with st.container():
    col3, col4 = st.columns([1,1])
    with col3:
        st.subheader('Modalidade 4x:')
        st.dataframe(selected_columns_df[selected_columns_df['Modalidade'] == '4x'].drop(columns=["Modalidade"]),hide_index=True)
    with col4:
        st.subheader('Modalidade 5x:')
        st.dataframe(selected_columns_df[selected_columns_df['Modalidade'] == '5x'].drop(columns=["Modalidade"]),hide_index=True)
    st.markdown("---")        
