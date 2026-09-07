import os

from pprint import pprint

from datetime import datetime

historico_interrupcoes = []

def limpar_tela():
    """Limpa o terminal de forma compatível com Windows, Linux e Mac."""
    if os.name == 'nt':
        os.system('cls')  # Comando para Windows
    else:
        os.system('clear') # Linux e MAC

## Consultar interrupções

regions = {
    1: {
        "name": "Sé",
        "zone": "Centro",
        "has_power": True
    },
    2: {
        "name": "Santana",
        "zone": "Zona Norte",
        "has_power": True
    },
    3: {
        "name": "Tucuruvi",
        "zone": "Zona Norte",
        "has_power": True
    },
    4: {
        "name": "Vila Mariana",
        "zone": "Zona Sul",
        "has_power": True
    },
    5: {
        "name": "Santo Amaro",
        "zone": "Zona Sul",
        "has_power": True
    },
    6: {
        "name": "Itaquera",
        "zone": "Zona Leste",
        "has_power": True
    },
    7: {
        "name": "Tatuapé",
        "zone": "Zona Leste",
        "has_power": True
    },
    8: {
        "name": "Pinheiros",
        "zone": "Zona Oeste",
        "has_power": True
    },
    9: {
        "name": "Lapa",
        "zone": "Zona Oeste",
        "has_power": True
    },
    10: {
        "name": "Butantã",
        "zone": "Zona Oeste",
        "has_power": True
    }
}

def menu_usuario():

    while True:
        print('-' * 50)
        print('Menu de dados de energia'.center(50, '-'))
        print('-' * 50)

        print("""
    1 - Consultar Interrupções\n
    2 - Cadastrar Interrupções\n
    3 - Atualizar situção de energia\n
    4 - Consultar histórico de interrupções\n
    5 - Sair do sistema
        """)

        try:
            opcao = int(input('Digite a opção desejada [1 - 5]: '))
        
            match opcao:
                case 1:
                    print("\nConsultando interrupções...\n")
                    situacao_energia()
                case 2:
                    cadastrar_interrupcoes()
                case 3:
                    atualizar_situacao_de_energia()
                case 4:
                    consultar_historico()
                case 5:
                    print("\nSistema encerrado. Até logo!\n")
                    break
                case _: 
                    print('\nDigite uma opção válida entre 1 e 5!\n')
                    
            input('\n\n...Pressione ENTER para voltar ao menu... \n\n')
            limpar_tela()
                    
        except ValueError:
            print('\nErro: Você deve digitar um número inteiro válido!\n')
        except:
            print('Houve um erro desconhecido!')


## Check se há energia 
def situacao_energia(): ## Opção 1

    for region in regions.values():
        if region["has_power"] is True:
            print(f"Energia estável em {region['name']} - {region['zone']}")
        elif region["has_power"] is False:
            print(f"Falta de energia em {region['name']} - {region['zone']}")

## Cadastrar uma queda de energia num local
def cadastrar_interrupcoes(): ## Opção 2

    mapeamento_zonas = {
        1 : "Zona Norte",
        2 : "Zona Sul",
        3 : "Zona Leste",
        4 : "Zona Oeste",
        5 : "Centro"
    }

    try:
        opcao = int(input('\nDeseja selecionar por ID ou ZONA? [1 - ID], [2 - ZONA] '))
        match opcao:
            case 1:
                print('Mapa de regiões'.center(50, '-'))
                pprint(regions)
                print('-' * 50)

                id_escolhido = int(input('\nDigite o ID correspondente ao local que deseja cadastrar interrupção: '))

                if id_escolhido in regions:
                    if not regions[id_escolhido]['has_power']:
                        print(f"\nAviso: Já há um registro de queda de energia para o local '{regions[id_escolhido]['name']}'!")
                    else:
                        regions[id_escolhido]['has_power'] = False
                        registrar_evento(id_escolhido, "sem_energia") # Registra a mudança
                        print(f"\nSucesso! Interrupção cadastrada para {id_escolhido}:")
                        pprint(regions[id_escolhido])
                else:
                    print('\nErro: ID não encontrado no sistema!')

            case 2:
                print('Zonas da cidade'.center(50, '-'))
                pprint(mapeamento_zonas)

                zona_escolhida = int(input('\nDigite o número correspondente a ZONA: '))

                if zona_escolhida in mapeamento_zonas:
                    nome_zona = mapeamento_zonas[zona_escolhida]

                    for i, dados in regions.items():
                        if dados['zone'] == nome_zona:
                            if dados["has_power"]:
                                dados['has_power'] = False
                                registrar_evento(i, "sem_energia")

                                print(f'Interrupção registrada em {regions[i]}')
                else:
                    print('Zona Inexistente, Digite um número válido!')

            case _:
                print('Digite uma opção válida!')

    except Exception as erro:
        print(f'Ocorreu um erro no sistema: {erro}')

## Atualizar de False para True no estado de energia
def atualizar_situacao_de_energia(): ## Opção 3
    print('-' * 50)
    print('Regiões para ser atualizadas'.center(50, '-'))
    print('-' * 50)

    regions_temp = {} #Dicionário temporário para consultar se o ID digitado é um dos que se podem alterar
    for chave, dados in regions.items():
        if not dados['has_power']:
            pprint(f"{chave}: {dados}")
            regions_temp[chave] = dados

    if not regions_temp:
        print('\nTodas as regiões estão atualizadas. Não há o que atualizar!\n')
        return

    try:
        id_para_atualizacao = int(input('\nDigite o ID da região que deseja atualizar: '))

        if id_para_atualizacao not in regions_temp:
            print('\nID não encontrado! Digite um ID válido.')
        else:
            regions[id_para_atualizacao]['has_power'] = True
            registrar_evento(id_para_atualizacao, "restabelecida") ## Registra a mudança
            print(f'\nSituação atualizada para {regions[id_para_atualizacao]}')

    except ValueError:
        print('\nDigite apenas um número inteiro válido.')







def registrar_evento(id_regiao, status):
    if status == "sem_energia":
        historico_interrupcoes.append({
            "region_id": id_regiao,
            "name": regions[id_regiao]["name"],
            "zone": regions[id_regiao]["zone"],
            "started_at": datetime.now(),
            "restored_at": None,
            "status": "sem_energia"
        })

    elif status == "restabelecida":
        for interrupcao in reversed(historico_interrupcoes):
            if (interrupcao["region_id"] == id_regiao and interrupcao["status"] == "sem_energia"):

                interrupcao["restored_at"] = datetime.now()
                interrupcao["status"] = "restabelecida"
                break


def consultar_historico():
    if not historico_interrupcoes:
        print("\nNenhuma interrupção registrada no histórico.")
        return

    print("\nHistórico de interrupções\n")

    for interrupcao in historico_interrupcoes:
        print("-" * 50)
        print(f"ID da região: {interrupcao['region_id']}")
        print(f"Região: {interrupcao['name']}")
        print(f"Zona: {interrupcao['zone']}")
        print(f"Status: {interrupcao['status']}")

        print(
            f"Início: {formatar_data(interrupcao['started_at'])}"
        )

        if interrupcao["restored_at"] is None:
            print("Restabelecimento: ainda sem energia")
        else:
            print(
                f"Restabelecimento: "
                f"{formatar_data(interrupcao['restored_at'])}"
            )


def formatar_data(data):
    meses = {
        1: "janeiro",
        2: "fevereiro",
        3: "março",
        4: "abril",
        5: "maio",
        6: "junho",
        7: "julho",
        8: "agosto",
        9: "setembro",
        10: "outubro",
        11: "novembro",
        12: "dezembro"
    }

    return (
        f"{data.day} de {meses[data.month]} de {data.year} "
        f"às {data.hour:02d}:{data.minute:02d}"
    )







menu_usuario()










