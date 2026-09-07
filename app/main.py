from pprint import pprint

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
        "has_power": False
    },
    10: {
        "name": "Butantã",
        "zone": "Zona Oeste",
        "has_power": False
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
                    print("\nConsultando histórico...\n")
                case 5:
                    print("\nSistema encerrado. Até logo!\n")
                    break
                case _: 
                    print('\nDigite uma opção válida entre 1 e 5!\n')
                    
            input('\n\n...Pressione ENTER para voltar ao menu... \n\n')
                    
        except ValueError:
            print('\nErro: Você deve digitar um número inteiro válido!\n')
        except:
            print('Houve um erro desconhecido!')


## Check se há energia 
def situacao_energia():
    for region in regions.values():
        if region["has_power"] is True:
            print(f"Energia estável em {region['name']} - {region['zone']}")
        elif region["has_power"] is False:
            print(f"Falta de energia em {region['name']} - {region['zone']}")

## Cadastrar uma queda de energia num local
def cadastrar_interrupcoes():

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
                            dados['has_power'] = False  # Altera diretamente
                            print(f'Interrupção registrada em {regions[i]}')
                else:
                    print('Zona Inexistente, Digite um número válido!')

            case _:
                print('Digite uma opção válida!')

    except Exception as erro:
        print(f'Ocorreu um erro no sistema: {erro}')



def atualizar_situacao_de_energia():
    print('-' * 50)
    print('Regiões para ser atualizadas'.center(50, '-'))
    print('-' * 50)

    regions_temp = {} #Dicionário temporário para consultar se o ID digitado é um dos que podem alterar
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
            print(f'Situação atualizada para {regions[id_para_atualizacao]}')

    except ValueError:
        print('\nDigite apenas um número inteiro válido.')






menu_usuario()










