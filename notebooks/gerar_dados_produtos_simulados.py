import pandas as pd
import csv
import random
import os


# xarregar a lista das 17 associações
try:
   
    caminho_assoc_geo = os.path.join("data", "associacoes_geocoords.csv") 
    if not os.path.exists(caminho_assoc_geo) and os.path.basename(os.getcwd()) == "notebooks":
         
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


# lista dos 35 olericulas
lista_completa_produtos = [
    "Alface", "Mandioca", "Tomate", "Repolho", "Batata", "Cebola", "Couve", "Chuchu",
    "Morango", "Pimentão", "Brócolis", "Abóbora", "Berinjela", "Beterraba", "Pepino",
    "Cenoura", "Quiabo", "Agrião", "Jiló", "Gengibre", "Abacate", "Goiaba", "Banana",
    "Limão", "Tangerina", "Maracujá", "Manga", "Lichia", "Uva", "Atemóia",
    "Cajamanga", "Graviola", "Coco", "Pitaia", "Mamão"
]


sazonalidade_base_produtos = {
    "Alface":       {"primavera": 1, "verao": 1, "outono": 1, "inverno": 1},
    "Mandioca":     {"primavera": 1, "verao": 1, "outono": 1, "inverno": 1}, 
    "Tomate":       {"primavera": 1, "verao": 1, "outono": 1, "inverno": 0}, 
    "Repolho":      {"primavera": 1, "verao": 0, "outono": 1, "inverno": 1}, 
    "Batata":       {"primavera": 0, "verao": 0, "outono": 1, "inverno": 1}, 
    "Cebola":       {"primavera": 1, "verao": 1, "outono": 0, "inverno": 0}, 
    "Couve":        {"primavera": 1, "verao": 1, "outono": 1, "inverno": 1},
    "Chuchu":       {"primavera": 1, "verao": 1, "outono": 1, "inverno": 0},
    "Morango":      {"primavera": 1, "verao": 0, "outono": 1, "inverno": 1}, 
    "Pimentão":     {"primavera": 1, "verao": 1, "outono": 1, "inverno": 0},
    "Brócolis":     {"primavera": 0, "verao": 0, "outono": 1, "inverno": 1}, 
    "Abóbora":      {"primavera": 1, "verao": 1, "outono": 1, "inverno": 1}, 
    "Berinjela":    {"primavera": 1, "verao": 1, "outono": 0, "inverno": 0},
    "Beterraba":    {"primavera": 1, "verao": 1, "outono": 1, "inverno": 1},
    "Pepino":       {"primavera": 1, "verao": 1, "outono": 1, "inverno": 0},
    "Cenoura":      {"primavera": 1, "verao": 1, "outono": 1, "inverno": 1},
    "Quiabo":       {"primavera": 1, "verao": 1, "outono": 0, "inverno": 0}, 
    "Agrião":       {"primavera": 1, "verao": 0, "outono": 1, "inverno": 1}, 
    "Jiló":         {"primavera": 1, "verao": 1, "outono": 1, "inverno": 0},
    "Gengibre":     {"primavera": 0, "verao": 1, "outono": 1, "inverno": 0}, 
    "Abacate":      {"primavera": 1, "verao": 0, "outono": 0, "inverno": 0}, 
    "Goiaba":       {"primavera": 0, "verao": 1, "outono": 1, "inverno": 0}, 
    "Banana":       {"primavera": 1, "verao": 1, "outono": 1, "inverno": 1}, 
    "Limão":        {"primavera": 1, "verao": 1, "outono": 1, "inverno": 1}, 
    "Tangerina":    {"primavera": 0, "verao": 0, "outono": 1, "inverno": 1},
    "Maracujá":     {"primavera": 1, "verao": 1, "outono": 1, "inverno": 0}, 
    "Manga":        {"primavera": 1, "verao": 1, "outono": 0, "inverno": 0}, 
    "Lichia":       {"primavera": 0, "verao": 1, "outono": 0, "inverno": 0}, 
    "Uva":          {"primavera": 0, "verao": 1, "outono": 0, "inverno": 0}, 
    "Atemóia":      {"primavera": 0, "verao": 0, "outono": 1, "inverno": 0}, 
    "Cajamanga":    {"primavera": 1, "verao": 1, "outono": 0, "inverno": 0},
    "Graviola":     {"primavera": 1, "verao": 1, "outono": 1, "inverno": 0}, 
    "Coco":         {"primavera": 1, "verao": 1, "outono": 1, "inverno": 1}, 
    "Pitaia":       {"primavera": 0, "verao": 1, "outono": 1, "inverno": 0}, 
    "Mamão":        {"primavera": 1, "verao": 1, "outono": 1, "inverno": 1}  
}


assoc_organicas_foco = ["Amista", "Rede Terra", "Asproc"]


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

    # associação oferecerá entre 8 e 15 produtos diferentes da lista
    num_produtos_para_vender = random.randint(8, 15)
    produtos_oferecidos = random.sample(lista_completa_produtos, num_produtos_para_vender)
   
    is_assoc_organica_foco = any(foco in nome_assoc for foco in assoc_organicas_foco)

    for produto in produtos_oferecidos:
        
        if is_assoc_organica_foco:
            
            produto_organico = 1 if random.random() < 0.75 else 0
        else:
            
            produto_organico = 1 if random.random() < 0.25 else 0
       
        avaliacao = random.randint(3, 5)
        
        sazonalidade = sazonalidade_base_produtos.get(produto, {
            "primavera": 0, "verao": 0, "outono": 0, "inverno": 0 
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


caminho_saida_csv = os.path.join("data", "associacoes_produtos_simulado.csv")
if not os.path.exists("data") and os.path.basename(os.getcwd()) == "notebooks":
    # Tenta de criar a partir da pasta notebooks
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