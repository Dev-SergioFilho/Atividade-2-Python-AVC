import pandas as pd
import matplotlib.pyplot as plt
import sqlite3

# Passo 1: Preparação e limpeza dos dados
# Carrega o arquivo CSV
dados = pd.read_csv("Atividade2.csv")

# Renomeia as colunas para português para facilitar a compreensão
dados.rename(columns={
    'id': 'ID',
    'gender': 'Genero',
    'age': 'Idade',
    'hypertension': 'Hipertensao',
    'heart_disease': 'Doenca_Cardiaca',
    'ever_married': 'Ja_Casou',
    'work_type': 'Tipo_Trabalho',
    'Residence_type': 'Tipo_Residencia',
    'avg_glucose_level': 'Nivel_Medio_Glicose',
    'bmi': 'IMC',
    'smoking_status': 'Status_Tabagismo',
    'stroke': 'AVC'
}, inplace=True)

# Traduz os valores da coluna de tabagismo
dados["Status_Tabagismo"] = dados["Status_Tabagismo"].replace({
    "never smoked": "Nunca fumou",
    "formerly smoked": "Ex-fumante",
    "smokes": "Fumante",
    "Unknown": "Desconhecido"
})

print("Analise Inicial:")
print(f"Total de registros: {dados.shape[0]}")
print(f"Total de caracteristicas: {dados.shape[1]}\n")

print("Dados ausentes antes do tratamento:")
print(dados.isnull().sum().to_string())

# Trata os dados ausentes preenchendo o IMC vazio com a média da coluna
dados["IMC"] = dados["IMC"].fillna(dados["IMC"].mean())

print("\nDados ausentes apos o tratamento:")
print(dados.isnull().sum().to_string())


# Passo 2: Análise dos dados
# Filtra e separa os pacientes em dois grupos
sem_avc = dados[dados["AVC"] == 0]
com_avc = dados[dados["AVC"] == 1]

print("\nContagem de pacientes:")
print(f"Sem AVC: {len(sem_avc)}")
print(f"Com AVC: {len(com_avc)}")

print("\nMedias comparativas (Sem AVC vs Com AVC):")
medias = dados.groupby("AVC")[["Idade", "Hipertensao", "Doenca_Cardiaca", "Nivel_Medio_Glicose", "IMC"]].mean().round(2)
print(medias.to_string())

print("\nTabagismo nos pacientes com AVC:")
print(com_avc["Status_Tabagismo"].value_counts().to_string())


# Passo 3: Visualização dos dados
# Grafico 1: Distribuicao das idades (Obrigatório)
plt.figure(figsize=(8, 5))
plt.hist(com_avc["Idade"], bins=20, color="#3a7fb8", edgecolor="black")
plt.title("Distribuicao de Idades - Pacientes com AVC")
plt.xlabel("Idade (anos)")
plt.ylabel("Frequencia")
plt.savefig("grafico1_idades.png")
plt.close()

# Grafico 2: Comparacao de IMC entre grupos (Obrigatório)
media_imc_sem = sem_avc["IMC"].mean()
media_imc_com = com_avc["IMC"].mean()

plt.figure(figsize=(8, 5))
barras_imc = plt.bar(["Sem AVC", "Com AVC"], [media_imc_sem, media_imc_com], color=["#2ca02c", "#ffbf00"])
plt.title("Comparacao do IMC Medio entre Pacientes com e sem AVC")
plt.ylabel("IMC Medio")
plt.ylim(0, 40)

# Adiciona o valor numerico no topo de cada barra
for barra in barras_imc:
    altura = barra.get_height()
    plt.text(barra.get_x() + barra.get_width()/2, altura + 0.5, f"{altura:.2f}", ha='center', va='bottom', fontweight='bold')

plt.savefig("grafico2_imc.png")
plt.close()

# Grafico 3: Analise livre (Hipertensao em pacientes com AVC)
hipertensao_avc = com_avc["Hipertensao"].replace({0: "Sem Hipertensao", 1: "Com Hipertensao"}).value_counts()
plt.figure(figsize=(8, 5))
barras_hip = plt.bar(hipertensao_avc.index, hipertensao_avc.values, color=["#2ca02c", "#ffbf00"])
plt.title("Pacientes com AVC: Relacao com Hipertensao")
plt.ylabel("Quantidade de Pacientes")

# Adiciona o valor numerico no topo de cada barra
for barra in barras_hip:
    altura = barra.get_height()
    plt.text(barra.get_x() + barra.get_width()/2, altura + 1, f"{altura}", ha='center', va='bottom', fontweight='bold')

plt.savefig("grafico3_hipertensao.png")
plt.close()


# Passo 4: Persistencia dos dados (SQLite)
# Cria o banco de dados e salva o DataFrame tratado como uma tabela chamada "pacientes"
conn = sqlite3.connect("dados_saude.db")
dados.to_sql("pacientes", conn, if_exists="replace", index=False)
cursor = conn.cursor()

print("\nResultados das Consultas SQLite:")

# 1. Consulta: Quantidade total de registros armazenados
cursor.execute("SELECT COUNT(*) FROM pacientes")
total_registros = cursor.fetchone()[0]
print(f"1. Quantidade total de registros: {total_registros}")

# 2. Consulta: Pacientes com registro de AVC
cursor.execute("SELECT COUNT(*) FROM pacientes WHERE AVC = 1")
total_avc = cursor.fetchone()[0]
print(f"2. Pacientes com registro de AVC: {total_avc}")

# 3. Consulta da equipe: Pacientes com AVC e Hipertensao simultaneamente
cursor.execute("SELECT COUNT(*) FROM pacientes WHERE AVC = 1 AND Hipertensao = 1")
avc_e_hipertensao = cursor.fetchone()[0]
print(f"3. Consulta da equipe (AVC e Hipertensao): {avc_e_hipertensao}")

# Fecha a conexao com o banco de dados
conn.close()