import pandas as pd
import csv
import random
import os

# --- 1. Configurações Iniciais ---

# Carregar a lista das 17 associações
try:
    # Ajuste o caminho se executar este script de um local diferente
    caminho_assoc_geo = os.path.join("data", "associacoes_geocoords.csv") 
    if not os.path.exists(caminho_assoc_geo) and os.path.basename(os.getcwd()) == "notebooks":
         # Tentativa de encontrar a partir da pasta notebooks
        caminho_assoc_geo = os.path.join("..", "data", "associacoes_geocoords.csv")

    df_associacoes = pd.read_csv(caminho_assoc_geo)
    lista_associacoes = df_associacoes[['Nome_Associacao', 'Localidade_Principal_Projeto']].to_dict('records')
    if len(lista_associacoes) != 17:
        print(f"Aviso: Esperava 17 associações, mas encontrei {len(lista_associacoes)} em '{caminho_assoc_geo}'.")
except FileNotFoundError:
    print(f"Erro: Arquivo 'associacoes_geocoords.csv' não encontrado no caminho esperado: {caminho_assoc_geo}")
    print("Por favor, certifique-se de que o arquivo existe ou ajuste o caminho.")
    exit()
except Exception as e:
    print(f"Erro ao ler 'associacoes_geocoords.csv': {e}")
    exit()


# Lista dos 35 produtos (conforme PDF do projeto)
lista_completa_produtos = [
    "Alface", "Mandioca", "Tomate", "Repolho", "Batata", "Cebola", "Couve", "Chuchu",
    "Morango", "Pimentão", "Brócolis", "Abóbora", "Berinjela", "Beterraba", "Pepino",
    "Cenoura", "Quiabo", "Agrião", "Jiló", "Gengibre", "Abacate", "Goiaba", "Banana",
    "Limão", "Tangerina", "Maracujá", "Manga", "Lichia", "Uva", "Atemóia",
    "Cajamanga", "Graviola", "Coco", "Pitaia", "Mamão"
]

# Sazonalidade base "inventada" para os produtos
# 1 = disponível, 0 = não disponível
# (Esta é uma simulação e pode ser ajustada conforme conhecimento local)
sazonalidade_base_produtos = {
    "Alface":       {"primavera": 1, "verao": 1, "outono": 1, "inverno": 1},
    "Mandioca":     {"primavera": 1, "verao": 1, "outono": 1, "inverno": 1}, # Colheita pode variar, mas raiz conserva
    "Tomate":       {"primavera": 1, "verao": 1, "outono": 1, "inverno": 0}, # Produção principal em épocas mais quentes/secas
    "Repolho":      {"primavera": 1, "verao": 0, "outono": 1, "inverno": 1}, # Prefere climas mais amenos
    "Batata":       {"primavera": 0, "verao": 0, "outono": 1, "inverno": 1}, # Safra de inverno no DF
    "Cebola":       {"primavera": 1, "verao": 1, "outono": 0, "inverno": 0}, # Bulbo, depende do ciclo
    "Couve":        {"primavera": 1, "verao": 1, "outono": 1, "inverno": 1},
    "Chuchu":       {"primavera": 1, "verao": 1, "outono": 1, "inverno": 0},
    "Morango":      {"primavera": 1, "verao": 0, "outono": 1, "inverno": 1}, # Clima ameno/frio
    "Pimentão":     {"primavera": 1, "verao": 1, "outono": 1, "inverno": 0},
    "Brócolis":     {"primavera": 0, "verao": 0, "outono": 1, "inverno": 1}, # Clima frio
    "Abóbora":      {"primavera": 1, "verao": 1, "outono": 1, "inverno": 1}, # Muitas variedades, boa disponibilidade
    "Berinjela":    {"primavera": 1, "verao": 1, "outono": 0, "inverno": 0},
    "Beterraba":    {"primavera": 1, "verao": 1, "outono": 1, "inverno": 1},
    "Pepino":       {"primavera": 1, "verao": 1, "outono": 1, "inverno": 0},
    "Cenoura":      {"primavera": 1, "verao": 1, "outono": 1, "inverno": 1},
    "Quiabo":       {"primavera": 1, "verao": 1, "outono": 0, "inverno": 0}, # Clima quente
    "Agrião":       {"primavera": 1, "verao": 0, "outono": 1, "inverno": 1}, # Prefere umidade e mais fresco
    "Jiló":         {"primavera": 1, "verao": 1, "outono": 1, "inverno": 0},
    "Gengibre":     {"primavera": 0, "verao": 1, "outono": 1, "inverno": 0}, # Colheita mais para o final do ciclo
    "Abacate":      {"primavera": 1, "verao": 0, "outono": 0, "inverno": 0}, # Variedades diferentes, mas pico primavera
    "Goiaba":       {"primavera": 0, "verao": 1, "outono": 1, "inverno": 0}, # Pico no verão/outono
    "Banana":       {"primavera": 1, "verao": 1, "outono": 1, "inverno": 1}, # Produção contínua
    "Limão":        {"primavera": 1, "verao": 1, "outono": 1, "inverno": 1}, # Várias safras
    "Tangerina":    {"primavera": 0, "verao": 0, "outono": 1, "inverno": 1}, # Outono/Inverno
    "Maracujá":     {"primavera": 1, "verao": 1, "outono": 1, "inverno": 0}, # Principalmente épocas quentes
    "Manga":        {"primavera": 1, "verao": 1, "outono": 0, "inverno": 0}, # Fim da primavera / Verão
    "Lichia":       {"primavera": 0, "verao": 1, "outono": 0, "inverno": 0}, # Safra curta no verão
    "Uva":          {"primavera": 0, "verao": 1, "outono": 0, "inverno": 0}, # Depende da variedade, DF mais verão
    "Atemóia":      {"primavera": 0, "verao": 0, "outono": 1, "inverno": 0}, # Outono
    "Cajamanga":    {"primavera": 1, "verao": 1, "outono": 0, "inverno": 0},
    "Graviola":     {"primavera": 1, "verao": 1, "outono": 1, "inverno": 0}, # Produção mais em épocas quentes
    "Coco":         {"primavera": 1, "verao": 1, "outono": 1, "inverno": 1}, # Coco verde o ano todo
    "Pitaia":       {"primavera": 0, "verao": 1, "outono": 1, "inverno": 0}, # Verão/Outono
    "Mamão":        {"primavera": 1, "verao": 1, "outono": 1, "inverno": 1}  # Produção contínua
}

# Associações com foco em orgânicos (para dar um viés na simulação)
# Nomes parciais para facilitar a correspondência
assoc_organicas_foco = ["Amista", "Rede Terra", "Asproc"]

# --- 2. Geração dos Dados Simulados ---
dados_simulados_produtos = []
cabecalho = [
    'nome_associacao', 'localidade_principal', 'nome_produto',
    'produto_organico', 'avaliacao_produto',
    'disponivel_primavera', 'disponivel_verao', 'disponivel_outono', 'disponivel_inverno'
]
dados_simulados_produtos.append(cabecalho)

for assoc_info in lista_associacoes:
    nome_assoc = assoc_info['Nome_Associacao']
    local_assoc = assoc_info['Localidade_Principal_Projeto']

    # Cada associação oferecerá entre 8 e 15 produtos diferentes da lista de 35
    num_produtos_para_vender = random.randint(8, 15)
    produtos_oferecidos = random.sample(lista_completa_produtos, num_produtos_para_vender)

    # Verifica se a associação tem foco em orgânicos
    is_assoc_organica_foco = any(foco in nome_assoc for foco in assoc_organicas_foco)

    for produto in produtos_oferecidos:
        # Determinar se o produto é orgânico
        if is_assoc_organica_foco:
            # Maior chance de ser orgânico se a associação tem esse foco
            produto_organico = 1 if random.random() < 0.75 else 0
        else:
            # Chance menor para as demais
            produto_organico = 1 if random.random() < 0.25 else 0

        # Avaliação simulada (entre 3 e 5)
        avaliacao = random.randint(3, 5)

        # Obter sazonalidade base
        sazonalidade = sazonalidade_base_produtos.get(produto, {
            "primavera": 0, "verao": 0, "outono": 0, "inverno": 0 # Default se produto não listado
        })

        dados_simulados_produtos.append([
            nome_assoc,
            local_assoc,
            produto,
            produto_organico,
            avaliacao,
            sazonalidade["primavera"],
            sazonalidade["verao"],
            sazonalidade["outono"],
            sazonalidade["inverno"]
        ])

# --- 3. Salvar o Novo CSV ---
# Ajuste o caminho de saída se necessário
caminho_saida_csv = os.path.join("data", "associacoes_produtos_simulado.csv")
if not os.path.exists("data") and os.path.basename(os.getcwd()) == "notebooks":
    # Tentativa de criar a partir da pasta notebooks
    caminho_saida_csv = os.path.join("..", "data", "associacoes_produtos_simulado.csv")
    os.makedirs(os.path.join("..", "data"), exist_ok=True)
elif not os.path.exists("data"):
     os.makedirs("data", exist_ok=True)


try:
    with open(caminho_saida_csv, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerows(dados_simulados_produtos)
    print(f"\nArquivo '{caminho_saida_csv}' gerado com sucesso!")
    print(f"Total de linhas de dados (sem cabeçalho): {len(dados_simulados_produtos) - 1}")
except IOError:
    print(f"Erro: Não foi possível escrever o arquivo em '{caminho_saida_csv}'. Verifique as permissões.")
except Exception as e:
    print(f"Ocorreu um erro inesperado ao salvar o CSV: {e}")