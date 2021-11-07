import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

#Configurando páginas

st.set_page_config(page_title= "Dashboard Análise Mutual",layout= "centered")

st.markdown("<h1 style='text-align: center; color: pink;'>Mutual Invest</h1>", unsafe_allow_html=True)

st.image("https://mutual.club/assets/social/facebook_quero-investir.png", width=200)


#Carrgando o dataset
@st.cache
def load_dataset(nome_arquivo):
    df =  pd.read_csv(f"{nome_arquivo}.csv", sep=";")
    return df

df = load_dataset("MutualClientsTransform")

#KPI`s

# Campo de Idade
df_age = df['age'].unique()
list_select_age = np.sort(df_age)
interval_age= st.sidebar.select_slider(label='Selecione o intervalo de idade',
options= list_select_age)

#Campo de Meses de Trabalho
df_months_job = df["monthsInTheJob"].unique()
list_select_age = np.sort(df_months_job)
interval_job= st.sidebar.select_slider(label='Selecione o intervalo de tempo de trabalho',
options= list_select_age)

left_column, middle_columns, right_column = st.columns(3)
with middle_columns:
    df_age = df[(df['age'] >= interval_age)].mean()
    st.subheader(f"Mean of Ages")
    st.write(f'{df_age["age"].mean():.1f} anos')
with left_column:
    df_months_job = df[(df["monthsInTheJob"] >= interval_job)].mean()
    st.subheader('Mean Months in the Job')
    st.write(f'{df_months_job["monthsInTheJob"].mean():.1f} meses')
with right_column:
    if interval_job >=0 or interval_age >=15:
        df_concat_age = df[(df['age'] >= interval_age)]
        df_concat_months_job = df[(df["monthsInTheJob"] >= interval_job)]
        df_income = pd.concat([df_concat_age,df_concat_months_job], join='inner')
        st.subheader('Mean Personal Net Income')
        st.write(f"R$ {float(df_income[['personalNetIncome']].mean()):.2f}")
st.markdown('---')

#Show de Dataset
c1, c2, c3, c4 = st.columns((3, 3, 3, 1))
dataset_show = st.sidebar.checkbox("Mostrar Dataset")
if dataset_show:
    c3.subheader("Dataset")
    c3.write(df)
# Show categories of dataset
c1.subheader("features Categóricas")
c1.write(df.select_dtypes(include="object").columns)
c2.subheader("features Númericas")
c2.write(df.select_dtypes(include=['int64', 'float64']).columns)
st.markdown('---')

#Variables
category = st.sidebar.selectbox('Selecione uma categoria',df.select_dtypes(include="object").columns)
numeric = st.sidebar.selectbox('Selecione uma variável quantitativa',df.select_dtypes(include=['int64', 'float64']).columns)

#Display Graphics
if category in'gender':
    st.subheader(f'Gráfico de Barra {category}')
    x = df['gender'].value_counts()
    ax = sns.barplot(x= x.index, y=x.values, data=df)
    ax.set(xlabel=f'{category}', ylabel='Count')
    st.pyplot(plt)
    plt.clf()
else:
    st.subheader(f'Gráfico de Barra {category}')
    x= df[f'{category}'].value_counts().index
    y = df[f'{category}'].value_counts().values
    sns.barplot(x=x,y=y)
    st.pyplot(plt)
    plt.clf()

#Numeric 
if 'BAD' not in numeric:
    st.subheader(f'Histograma {numeric}')
    sns.histplot(data=df, x=f'{numeric}')
    st.pyplot(plt)
    plt.clf()
else:
    st.subheader(f'Histograma {numeric}')
    x= df[f'{numeric}'].value_counts().index
    y = df[f'{numeric}'].value_counts().values
    sns.barplot(x=x,y=y)
    st.pyplot(plt)
    plt.clf()    

#Display Graphics in comparison with column BAD
choice = st.sidebar.selectbox('Selecione uma categoria para comparação', ['gender', 'maritalStatus', 'residenceType'])

# function to obtain labels
def obtain_labels(nome_coluna, df=df):
    data = df[['BAD', nome_coluna]]
    data.dropna(inplace=True)
    group_0 = data[(data['BAD']==0)].value_counts()
    group_1 = data[(data['BAD']==1)].value_counts()    
    length = len(group_0)
    y1= [group_0.values[i] for i in range(0,length,1)]
    y2= [group_1.values[i] for i in range(0,length,1)]
    list_features = data[nome_coluna].unique()
    x= [i for i in list_features]
    return x,y1,y2

#gender x BAD
if choice in 'gender':
    x,y1,y2 = obtain_labels(choice)
    plt.bar(x,y1, label='Clientes Não Inadimplentes',width=0.4, align='edge')
    plt.bar(x,y2, label='Clientes Inadimplentes', width=-0.4 ,align='edge')
    plt.legend()
    plt.title("Gráfico de Sexo e Tipo de Cliente")
    st.pyplot(plt)
#maritalStatus x BAD
if choice in 'maritalStatus':
    x,y1,y2 = obtain_labels(choice)
    plt.bar(x,y1, label='Clientes Não Inadimplentes',width=0.4, align='edge')
    plt.bar(x,y2, label='Clientes Inadimplentes', width=-0.4 ,align='edge')
    plt.legend()
    plt.title("Gráfico de Estado Civil e Tipo de Cliente")
    st.pyplot(plt)
#residencetype x BAD
if choice in 'residenceType':
    x,y1,y2 = obtain_labels(choice)
    plt.bar(x,y1, label='Clientes Não Inadimplentes',width=0.4, align='edge')
    plt.bar(x,y2, label='Clientes Inadimplentes', width=-0.4 ,align='edge')
    plt.legend()
    plt.title("Gráfico de tipo de residência e Tipo de Cliente")
    st.pyplot(plt)