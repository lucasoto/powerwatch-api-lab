import os

from datetime import datetime
from pprint import pprint


historico_interrupcoes = []

mapeamento_zonas = {
    1: "Zona Norte",
    2: "Zona Sul",
    3: "Zona Leste",
    4: "Zona Oeste",
    5: "Centro",
}


regions = {
    1: {
        "name": "Sé",
        "zone": "Centro",
        "has_power": True,
    },
    2: {
        "name": "Santana",
        "zone": "Zona Norte",
        "has_power": True,
    },
    3: {
        "name": "Tucuruvi",
        "zone": "Zona Norte",
        "has_power": True,
    },
    4: {
        "name": "Vila Mariana",
        "zone": "Zona Sul",
        "has_power": True,
    },
    5: {
        "name": "Santo Amaro",
        "zone": "Zona Sul",
        "has_power": True,
    },
    6: {
        "name": "Itaquera",
        "zone": "Zona Leste",
        "has_power": True,
    },
    7: {
        "name": "Tatuapé",
        "zone": "Zona Leste",
        "has_power": True,
    },
    8: {
        "name": "Pinheiros",
        "zone": "Zona Oeste",
        "has_power": True,
    },
    9: {
        "name": "Lapa",
        "zone": "Zona Oeste",
        "has_power": True,
    },
    10: {
        "name": "Butantã",
        "zone": "Zona Oeste",
        "has_power": True,
    },
}


def limpar_tela():
    """Limpa o terminal de forma compatível com Windows, Linux e macOS."""
    if os.name == "nt":
        os.system("cls")
    else:
        os.system("clear")


def menu_usuario():
    while True:
        print("-" * 50)
        print("Menu de dados de energia".center(50, "-"))
        print("-" * 50)

        print(
            """
    1 - Consultar interrupções
    2 - Cadastrar interrupções
    3 - Atualizar situação de energia
    4 - Consultar histórico de interrupções
    5 - Sair do sistema
            """
        )

        try:
            opcao = int(input("Digite a opção desejada [1 - 5]: "))

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
                    print("\nDigite uma opção válida entre 1 e 5!\n")

            if opcao != 5:
                input("\n\n...Pressione ENTER para voltar ao menu... \n\n")
                limpar_tela()

        except ValueError:
            print("\nErro: Você deve digitar um número inteiro válido!\n")


# Opção 1 - Consultar estado atual de energia
def situacao_energia():
    for region in regions.values():
        if region["has_power"]:
            print(f"Energia estável em {region['name']} - {region['zone']}")
        else:
            print(f"Falta de energia em {region['name']} - {region['zone']}")


# Opção 2 - Cadastrar uma queda de energia
def cadastrar_interrupcoes():
    try:
        opcao = int(
            input(
                "\nDeseja selecionar por ID ou ZONA? "
                "[1 - ID], [2 - ZONA] "
            )
        )

        match opcao:
            case 1:
                print("Mapa de regiões".center(50, "-"))
                pprint(regions)
                print("-" * 50)

                id_escolhido = int(
                    input(
                        "\nDigite o ID correspondente ao local que deseja "
                        "cadastrar interrupção: "
                    )
                )

                if id_escolhido not in regions:
                    print("\nErro: ID não encontrado no sistema!")
                    return

                if not regions[id_escolhido]["has_power"]:
                    print(
                        "\nAviso: Já há um registro de queda de energia para "
                        f"o local '{regions[id_escolhido]['name']}'!"
                    )
                    return

                regions[id_escolhido]["has_power"] = False
                registrar_evento(id_escolhido, "sem_energia")

                print(f"\nSucesso! Interrupção cadastrada para {id_escolhido}:")
                pprint(regions[id_escolhido])

            case 2:
                print("Zonas da cidade".center(50, "-"))
                pprint(mapeamento_zonas)

                zona_escolhida = int(
                    input("\nDigite o número correspondente à ZONA: ")
                )

                if zona_escolhida not in mapeamento_zonas:
                    print("Zona inexistente. Digite um número válido!")
                    return

                nome_zona = mapeamento_zonas[zona_escolhida]
                houve_novo_registro = False

                for id_regiao, dados in regions.items():
                    if dados["zone"] == nome_zona and dados["has_power"]:
                        dados["has_power"] = False
                        registrar_evento(id_regiao, "sem_energia")
                        houve_novo_registro = True

                        print(
                            f"Interrupção registrada em "
                            f"{dados['name']} - {dados['zone']}"
                        )

                if not houve_novo_registro:
                    print(
                        f"\nTodas as regiões de {nome_zona} "
                        "já estão sem energia."
                    )

            case _:
                print("Digite uma opção válida!")

    except ValueError:
        print("\nDigite apenas números inteiros válidos.")


# Opção 3 - Atualizar de False para True no estado de energia
def atualizar_situacao_de_energia():
    print("-" * 50)
    print("Regiões para serem atualizadas".center(50, "-"))
    print("-" * 50)

    regions_temp = {}

    for chave, dados in regions.items():
        if not dados["has_power"]:
            print(f"{chave}: {dados}")
            regions_temp[chave] = dados

    if not regions_temp:
        print("\nTodas as regiões estão atualizadas. Não há o que atualizar!\n")
        return

    try:
        id_para_atualizacao = int(
            input("\nDigite o ID da região que deseja atualizar: ")
        )

        if id_para_atualizacao not in regions_temp:
            print("\nID não encontrado! Digite um ID válido.")
            return

        regions[id_para_atualizacao]["has_power"] = True
        registrar_evento(id_para_atualizacao, "restabelecida")

        print(
            f"\nSituação atualizada para "
            f"{regions[id_para_atualizacao]['name']} - "
            f"{regions[id_para_atualizacao]['zone']}"
        )

    except ValueError:
        print("\nDigite apenas um número inteiro válido.")


def registrar_evento(id_regiao, status):
    """Cria ou encerra uma ocorrência no histórico."""
    if status == "sem_energia":
        historico_interrupcoes.append(
            {
                "region_id": id_regiao,
                "name": regions[id_regiao]["name"],
                "zone": regions[id_regiao]["zone"],
                "started_at": datetime.now(),
                "restored_at": None,
                "status": "sem_energia",
            }
        )

    elif status == "restabelecida":
        for interrupcao in reversed(historico_interrupcoes):
            if (
                interrupcao["region_id"] == id_regiao
                and interrupcao["status"] == "sem_energia"
            ):
                interrupcao["restored_at"] = datetime.now()
                interrupcao["status"] = "restabelecida"
                break


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
        12: "dezembro",
    }

    return (
        f"{data.day} de {meses[data.month]} de {data.year} "
        f"às {data.hour:02d}:{data.minute:02d}"
    )


def calcular_duracao(interrupcao):
    """Retorna a duração da interrupção como timedelta."""
    fim = interrupcao["restored_at"]

    if fim is None:
        fim = datetime.now()

    return fim - interrupcao["started_at"]


def formatar_duracao(duracao):
    """Transforma um timedelta em uma duração legível."""
    segundos_totais = max(0, int(duracao.total_seconds()))

    dias, resto = divmod(segundos_totais, 86400)
    horas, resto = divmod(resto, 3600)
    minutos, segundos = divmod(resto, 60)

    partes = []

    if dias:
        partes.append(f"{dias} dia(s)")
    if horas:
        partes.append(f"{horas} hora(s)")
    if minutos:
        partes.append(f"{minutos} minuto(s)")

    if not partes:
        partes.append(f"{segundos} segundo(s)")

    return ", ".join(partes)


def exibir_historico(interrupcoes):
    """Exibe as ocorrências recebidas."""
    if not interrupcoes:
        print("\nNenhuma interrupção encontrada para essa consulta.")
        return

    print(f"\n{len(interrupcoes)} ocorrência(s) encontrada(s).\n")

    for interrupcao in interrupcoes:
        print("-" * 60)
        print(f"ID da região: {interrupcao['region_id']}")
        print(f"Região: {interrupcao['name']}")
        print(f"Zona: {interrupcao['zone']}")

        if interrupcao["status"] == "sem_energia":
            print("Status: Sem energia")
        else:
            print("Status: Restabelecida")

        print(f"Início: {formatar_data(interrupcao['started_at'])}")

        if interrupcao["restored_at"] is None:
            print("Restabelecimento: ainda sem energia")
            print(
                "Duração até o momento: "
                f"{formatar_duracao(calcular_duracao(interrupcao))}"
            )
        else:
            print(
                "Restabelecimento: "
                f"{formatar_data(interrupcao['restored_at'])}"
            )
            print(
                "Duração: "
                f"{formatar_duracao(calcular_duracao(interrupcao))}"
            )

    print("-" * 60)


def escolher_regiao_filtro():
    """Mostra todas as regiões e retorna um ID válido."""
    print("\nRegiões:")

    for region_id, dados in regions.items():
        print(f"{region_id} - {dados['name']} ({dados['zone']})")

    while True:
        try:
            escolha = int(input("\nDigite o ID da região: "))

            if escolha in regions:
                return escolha

            print("\nRegião inexistente.")

        except ValueError:
            print("\nDigite apenas números.")


def escolher_zona_filtro():
    """Seleciona uma zona e, opcionalmente, uma região dentro dela."""
    print("\nZonas:")

    for numero, zona in mapeamento_zonas.items():
        print(f"{numero} - {zona}")

    while True:
        try:
            numero_zona = int(input("\nDigite a zona desejada: "))

            if numero_zona in mapeamento_zonas:
                zona_escolhida = mapeamento_zonas[numero_zona]
                break

            print("\nZona inexistente.")

        except ValueError:
            print("\nDigite apenas números.")

    regioes_da_zona = {}

    for region_id, dados in regions.items():
        if dados["zone"] == zona_escolhida:
            regioes_da_zona[region_id] = dados

    print(f"\nRegiões de {zona_escolhida}:")
    print("0 - Toda a zona")

    for region_id, dados in regioes_da_zona.items():
        print(f"{region_id} - {dados['name']}")

    while True:
        try:
            escolha = int(
                input("\nEscolha uma região ou 0 para toda a zona: ")
            )

            if escolha == 0:
                return zona_escolhida, None

            if escolha in regioes_da_zona:
                return zona_escolhida, escolha

            print("\nRegião inválida para essa zona.")

        except ValueError:
            print("\nDigite apenas números.")


def escolher_status_filtro():
    """Retorna None ou um status válido para o filtro."""
    while True:
        print(
            """
Status:
0 - Todos
1 - Sem energia
2 - Restabelecida
            """
        )

        try:
            escolha = int(input("Escolha o status: "))

            if escolha == 0:
                return None
            if escolha == 1:
                return "sem_energia"
            if escolha == 2:
                return "restabelecida"

            print("\nStatus inválido.")

        except ValueError:
            print("\nDigite apenas números.")


def pedir_numero_opcional(mensagem, minimo=None, maximo=None):
    """Lê um inteiro opcional. ENTER significa ignorar o filtro."""
    while True:
        valor = input(mensagem).strip()

        if valor == "":
            return None

        try:
            numero = int(valor)

            if minimo is not None and numero < minimo:
                print(f"Digite um valor maior ou igual a {minimo}.")
                continue

            if maximo is not None and numero > maximo:
                print(f"Digite um valor menor ou igual a {maximo}.")
                continue

            return numero

        except ValueError:
            print("Digite um número inteiro ou pressione ENTER para ignorar.")


def solicitar_filtros_historico():
    """Coleta os filtros do histórico de forma hierárquica e intuitiva."""
    region_id = None
    zone = None

    while True:
        print(
            """
Como deseja filtrar a localização?

1 - Por região
2 - Por zona
3 - Todas as regiões
            """
        )

        try:
            tipo_local = int(input("Escolha uma opção [1 - 3]: "))

            if tipo_local == 1:
                region_id = escolher_regiao_filtro()
                break

            if tipo_local == 2:
                zone, region_id = escolher_zona_filtro()
                break

            if tipo_local == 3:
                break

            print("\nDigite uma opção válida entre 1 e 3.")

        except ValueError:
            print("\nDigite apenas números.")

    status = escolher_status_filtro()

    day = None
    month = None
    year = None

    while True:
        resposta = input("\nDeseja filtrar também por data? [S/N]: ").strip().lower()

        if resposta in ("n", "nao", "não"):
            break

        if resposta in ("s", "sim"):
            print(
                "\nInforme somente os campos desejados. "
                "Pressione ENTER para ignorar um campo."
            )
            day = pedir_numero_opcional("Dia: ", 1, 31)
            month = pedir_numero_opcional("Mês: ", 1, 12)
            year = pedir_numero_opcional("Ano: ", 1)
            break

        print("Digite S para sim ou N para não.")

    return {
        "region_id": region_id,
        "zone": zone,
        "status": status,
        "day": day,
        "month": month,
        "year": year,
    }


def filtrar_historico(
    region_id=None,
    zone=None,
    status=None,
    day=None,
    month=None,
    year=None,
):
    """Retorna apenas as ocorrências que correspondem aos filtros."""
    resultados = []

    for interrupcao in historico_interrupcoes:
        inicio = interrupcao["started_at"]

        if region_id is not None and interrupcao["region_id"] != region_id:
            continue

        if zone is not None and interrupcao["zone"] != zone:
            continue

        if status is not None and interrupcao["status"] != status:
            continue

        if day is not None and inicio.day != day:
            continue

        if month is not None and inicio.month != month:
            continue

        if year is not None and inicio.year != year:
            continue

        resultados.append(interrupcao)

    return resultados


def exibir_estatisticas():
    """Calcula estatísticas simples com base no histórico atual."""
    if not historico_interrupcoes:
        print("\nNão há dados suficientes para gerar estatísticas.")
        return

    total = len(historico_interrupcoes)

    em_andamento = [
        interrupcao
        for interrupcao in historico_interrupcoes
        if interrupcao["status"] == "sem_energia"
    ]

    restabelecidas = [
        interrupcao
        for interrupcao in historico_interrupcoes
        if interrupcao["status"] == "restabelecida"
    ]

    contagem_regioes = {}
    contagem_zonas = {}

    for interrupcao in historico_interrupcoes:
        nome = interrupcao["name"]
        zona = interrupcao["zone"]

        contagem_regioes[nome] = contagem_regioes.get(nome, 0) + 1
        contagem_zonas[zona] = contagem_zonas.get(zona, 0) + 1

    regiao_mais_afetada = max(contagem_regioes, key=contagem_regioes.get)
    zona_mais_afetada = max(contagem_zonas, key=contagem_zonas.get)

    print("\n" + "=" * 60)
    print("ESTATÍSTICAS DO HISTÓRICO".center(60))
    print("=" * 60)

    print(f"Total de interrupções registradas: {total}")
    print(f"Interrupções em andamento: {len(em_andamento)}")
    print(f"Interrupções restabelecidas: {len(restabelecidas)}")
    print(
        f"Região com mais interrupções: {regiao_mais_afetada} "
        f"({contagem_regioes[regiao_mais_afetada]})"
    )
    print(
        f"Zona com mais interrupções: {zona_mais_afetada} "
        f"({contagem_zonas[zona_mais_afetada]})"
    )

    if restabelecidas:
        duracoes = [calcular_duracao(item) for item in restabelecidas]

        tempo_total = sum(duracoes, start=duracoes[0] - duracoes[0])
        tempo_medio = tempo_total / len(duracoes)

        maior_interrupcao = max(
            restabelecidas,
            key=calcular_duracao,
        )

        print(
            "Tempo total sem energia nas ocorrências encerradas: "
            f"{formatar_duracao(tempo_total)}"
        )
        print(
            "Duração média das interrupções encerradas: "
            f"{formatar_duracao(tempo_medio)}"
        )
        print(
            "Maior interrupção encerrada: "
            f"{maior_interrupcao['name']} - "
            f"{formatar_duracao(calcular_duracao(maior_interrupcao))}"
        )
    else:
        print(
            "Ainda não existem interrupções restabelecidas para calcular "
            "tempo total, média e maior duração."
        )

    print("=" * 60)


# Opção 4 - Histórico, filtros, duração e estatísticas
def consultar_historico():
    if not historico_interrupcoes:
        print("\nNenhuma interrupção registrada no histórico.")
        return

    while True:
        print("\n" + "-" * 50)
        print("Histórico de interrupções".center(50, "-"))
        print("-" * 50)

        print(
            """
    1 - Mostrar todo o histórico
    2 - Filtrar histórico
    3 - Exibir estatísticas
    4 - Voltar
            """
        )

        try:
            opcao = int(input("Escolha uma opção [1 - 4]: "))

            match opcao:
                case 1:
                    exibir_historico(historico_interrupcoes)

                case 2:
                    filtros = solicitar_filtros_historico()
                    resultados = filtrar_historico(**filtros)
                    exibir_historico(resultados)

                case 3:
                    exibir_estatisticas()

                case 4:
                    break

                case _:
                    print("\nDigite uma opção válida entre 1 e 4.")

            if opcao != 4:
                input("\nPressione ENTER para continuar...")
                limpar_tela()

        except ValueError:
            print("\nDigite apenas um número inteiro válido.")


if __name__ == "__main__":
    menu_usuario()
