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
Cássio - 90 + 60 + 30 + 60 +[50]
Fernanda A. - 72 + 47 + 47 + 36 +[54] 
Fernanda S. - 30 + 35 
Fernanda W. - 70 + 89 + [64] + 80 + 80 
Gabi - 75 + 69 + [62] + 63 + 52
Luciano - 70+34+47+49+121
Marina - 60 + 60 + [34] + 60 + 41
Pedro Augusto - [30] + 47 + 32 + 32 + 60 + 30
Samuel - 80 +70 + 40 + [48] + 52 + 36

4x
Amanda M. - 50 + 60 + [54] + 60 + 40
Caio - 60 + 62 + 38 + [84]
David - [42] + 36 + 35 + 33
João Marcos - 60 + 60 + 50 + 60 + [40]
Lívia - 60 + 54 + [40] + 31
Mairon - 38
Naama - 46+ [31] + 50 +35
Mary - 47+ 73+78+64
   
3x
Amanda G. - 88 + 32 + 34
André - 32 + [85] + 95
Bianca - 43 + 39 + 62
Brenda -
Camila - 31
Guilherme - 41 + 45
Hamilton - [98] + 46 + 41
Patrícia -
Ravier - [129] + 39 + 42
Talita - 64 + 57 + 60 + [53]

2x
Anna - 33
Carol - [85] + 95
João Vitor -
Julia - 53 + 41 
Keren - 25+
Leandro - 34
Rebeca -32+40+62 
Thaís - 56 + [31]



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
# Group by name, semana, and type, then count and sum as requested using pandas
result = df.groupby(["name", "semana", "type"]).agg(
    sum_minutes=("minutes", "sum"),
    count_minutes=("minutes", "count"),
    sum_selected_aerobic_minutes=("minutes", lambda x: x[df.loc[x.index, "selected_aerobic"]].sum())
).reset_index()


# Assuming 'result' is a pandas DataFrame and 'type' is a column in it
result['type_num'] = result['type'].str.replace('x', '').astype(int)
result['points_week'] = np.where(result['count_minutes'] >= result['type_num'], 3, 0)

df_ranking = result.groupby(['name', 'type']).agg(
    total_minutes_week=('sum_minutes','sum'),
    total_points_week=('points_week', 'sum'),
    total_sum_selected_aerobic_minutes=('sum_selected_aerobic_minutes', 'sum')
).reset_index()

def rank_type(df_type):
    df_type = df_type.sort_values(by=['total_points_week', 'total_sum_selected_aerobic_minutes'], ascending=[False, False])
    df_type['rank'] = df_type[['total_points_week', 'total_sum_selected_aerobic_minutes']].apply(tuple, axis=1).rank(method='min', ascending=False).astype(int)
    return df_type

# Apply the ranking function to each group
ranked_dfs = [rank_type(group) for _, group in df_ranking.groupby('type')]

# Merge all the ranked DataFrames back into a single DataFrame
df_ranked = pd.concat(ranked_dfs).reset_index(drop=True)

# Sort the final DataFrame by type and rank
df_ranked = df_ranked.sort_values(by=['type', 'rank']).reset_index(drop=True)

#print(result)
#print(df_ranked)



st.set_page_config(page_title="Crente Fit 2.0",layout="wide")

st.title("🏖 Incentivo mútuo ao cuidado com o corpo que Deus nos deu")
#st.subheader("Uma experiência sem plástico")
st.markdown("###")

#sidebar
#st.sidebar.image("material/img/logo.png")
st.sidebar.title("CRENTE FIT 2.0")
st.sidebar.header("Escolha seus filtros: ")

#FILTROS
#Tipo de Modalidade
tipoModalidade = st.sidebar.multiselect("Escolha a modalidade: ",sorted(result["type"].unique()))
if not tipoModalidade:
    df_result2 = result.copy()
    df_rank2 = df_ranked.copy()
else:
    df_result2 = result[result["type"].isin(tipoModalidade)]
    df_rank2 = df_ranked[df_ranked["type"].isin(tipoModalidade)]

#Tipo de Nome
nomeCrente = st.sidebar.multiselect("Escolha o Crente: ",sorted(df_result2["name"].unique()))
if not nomeCrente:
    df_result3 = df_result2.copy()
    df_rank3 = df_rank2.copy()
else:
    df_result3 = df_result2[df_result2["name"].isin(nomeCrente)]
    df_rank3 = df_rank2[df_rank2["name"].isin(nomeCrente)]


if not tipoModalidade and not nomeCrente:
    filtered_result_df = result
    filtered_rank_df = df_ranked
elif not nomeCrente:
    filtered_result_df = result[result["type"].isin(tipoModalidade)]
    filtered_rank_df = df_ranked[df_ranked["type"].isin(tipoModalidade)]
elif not tipoModalidade:
    filtered_result_df = result[result["name"].isin(nomeCrente)]
    filtered_rank_df = df_ranked[df_ranked["name"].isin(nomeCrente)]
else:
    filtered_result_df = df_result3[df_result3["type"].isin(tipoModalidade) & df_result3["name"].isin(nomeCrente)]
    filtered_rank_df = df_rank3[df_rank3["type"].isin(tipoModalidade) & df_rank3["name"].isin(nomeCrente)]


filtered_rank_df = filtered_rank_df.rename(columns={
    "name": "Nome",
    "type": "Modalidade",
    "total_minutes_week": "Soma Minutos na Semana",
    "total_points_week": "Pontos Semana",
    "total_sum_selected_aerobic_minutes": "Aerobico para Desempate",
    "rank": "Rank"
})

filtered_result_df = filtered_result_df.rename(columns={
    "name": "Nome",
    "type": "Modalidade",
    "sum_minutes": "Soma de Minutos",
    "count_minutes": "Quantidade de Atividades Registradas na Semana",
    "points_week": "Pontos Semana",
    "sum_selected_aerobic_minutes": "Aerobico para Desempate"
})
    
filtered_result_df = filtered_result_df.drop(columns=['type_num'])


#st.write(filtered_result_df)
#st.write(filtered_rank_df)
selected_columns_df = filtered_rank_df[["Nome", "Pontos Semana", "Aerobico para Desempate", "Rank", "Modalidade"]]

with st.container():
    st.subheader('Minutos exercitados por Crente:')
    fig = px.bar(filtered_result_df, x='Nome', color="Modalidade",y="Soma de Minutos",
        labels={'Nome': '', "Modalidade": 'Modalidade', 'count':''},
        category_orders={'Modalidade': sorted(filtered_result_df['Modalidade'].unique())}) 
    st.plotly_chart(fig, use_container_width=True)
    st.markdown("---")   

with st.container():
    col1, col2,col3, col4 = st.columns([1,1,1,1])
    with col1:
        st.subheader('Modalidade 2x:')
        st.table(selected_columns_df[selected_columns_df['Modalidade'] == '2x'].drop(columns=["Modalidade"]))
    with col2:
        st.subheader('Modalidade 3x:')
        st.table(selected_columns_df[selected_columns_df['Modalidade'] == '3x'].drop(columns=["Modalidade"]))
    with col3:
        st.subheader('Modalidade 4x:')
        st.table(selected_columns_df[selected_columns_df['Modalidade'] == '4x'].drop(columns=["Modalidade"]))
    with col4:
        st.subheader('Modalidade 5x:')
        st.table(selected_columns_df[selected_columns_df['Modalidade'] == '5x'].drop(columns=["Modalidade"]))
    st.markdown("---")        
