import os

from pprint import pprint

from app.data import mapeamento_zonas
from app.services import (
    calcular_duracao,
    calcular_estatisticas,
    filtrar_historico,
    listar_historico,
    listar_regioes,
    registrar_interrupcao,
    registrar_interrupcoes_por_zona,
    restabelecer_energia,
)


def limpar_tela():
    """Limpa o terminal de forma compatível com Windows, Linux e macOS."""
    if os.name == "nt":
        os.system("cls")
    else:
        os.system("clear")


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


def situacao_energia():
    """Opção 1 - Exibe o estado atual das regiões."""
    for region in listar_regioes():
        if region["has_power"]:
            print(
                f"Energia estável em {region['name']} - {region['zone']}"
            )
        else:
            print(
                f"Falta de energia em {region['name']} - {region['zone']}"
            )


def cadastrar_interrupcoes():
    """Opção 2 - Registra uma interrupção por região ou por zona."""
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
                for regiao in listar_regioes():
                    print(
                        f"{regiao['id']} - {regiao['name']} "
                        f"({regiao['zone']})"
                    )
                print("-" * 50)

                id_escolhido = int(
                    input(
                        "\nDigite o ID correspondente ao local que deseja "
                        "cadastrar interrupção: "
                    )
                )

                try:
                    interrupcao = registrar_interrupcao(id_escolhido)
                    print("\nSucesso! Interrupção cadastrada:")
                    pprint(interrupcao)

                except ValueError as erro:
                    print(f"\nErro: {erro}")

            case 2:
                print("Zonas da cidade".center(50, "-"))
                for numero, zona in mapeamento_zonas.items():
                    print(f"{numero} - {zona}")

                zona_escolhida = int(
                    input("\nDigite o número correspondente à ZONA: ")
                )

                if zona_escolhida not in mapeamento_zonas:
                    print("Zona inexistente. Digite um número válido!")
                    return

                nome_zona = mapeamento_zonas[zona_escolhida]

                try:
                    interrupcoes = registrar_interrupcoes_por_zona(nome_zona)

                    if not interrupcoes:
                        print(
                            f"\nTodas as regiões de {nome_zona} "
                            "já estão sem energia."
                        )
                        return

                    for interrupcao in interrupcoes:
                        print(
                            "Interrupção registrada em "
                            f"{interrupcao['name']} - {interrupcao['zone']} "
                            f"(ocorrência #{interrupcao['id']})"
                        )

                except ValueError as erro:
                    print(f"\nErro: {erro}")

            case _:
                print("Digite uma opção válida!")

    except ValueError:
        print("\nDigite apenas números inteiros válidos.")


def atualizar_situacao_de_energia():
    """Opção 3 - Restabelece a energia de uma região em interrupção."""
    print("-" * 50)
    print("Regiões para serem atualizadas".center(50, "-"))
    print("-" * 50)

    regioes_sem_energia = [
        regiao
        for regiao in listar_regioes()
        if not regiao["has_power"]
    ]

    if not regioes_sem_energia:
        print("\nTodas as regiões estão atualizadas. Não há o que atualizar!\n")
        return

    for regiao in regioes_sem_energia:
        print(
            f"{regiao['id']} - {regiao['name']} ({regiao['zone']})"
        )

    try:
        id_para_atualizacao = int(
            input("\nDigite o ID da região que deseja atualizar: ")
        )

        try:
            interrupcao = restabelecer_energia(id_para_atualizacao)
            print(
                f"\nEnergia restabelecida em {interrupcao['name']} - "
                f"{interrupcao['zone']} "
                f"(ocorrência #{interrupcao['id']})."
            )

        except (ValueError, RuntimeError) as erro:
            print(f"\nErro: {erro}")

    except ValueError:
        print("\nDigite apenas um número inteiro válido.")


def exibir_historico(interrupcoes):
    """Exibe as ocorrências recebidas."""
    if not interrupcoes:
        print("\nNenhuma interrupção encontrada para essa consulta.")
        return

    print(f"\n{len(interrupcoes)} ocorrência(s) encontrada(s).\n")

    for interrupcao in interrupcoes:
        print("-" * 60)
        print(f"ID da ocorrência: {interrupcao['id']}")
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
    regioes = listar_regioes()

    print("\nRegiões:")
    for regiao in regioes:
        print(
            f"{regiao['id']} - {regiao['name']} ({regiao['zone']})"
        )

    ids_validos = {regiao["id"] for regiao in regioes}

    while True:
        try:
            escolha = int(input("\nDigite o ID da região: "))

            if escolha in ids_validos:
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

    regioes_da_zona = [
        regiao
        for regiao in listar_regioes()
        if regiao["zone"] == zona_escolhida
    ]

    print(f"\nRegiões de {zona_escolhida}:")
    print("0 - Toda a zona")

    for regiao in regioes_da_zona:
        print(f"{regiao['id']} - {regiao['name']}")

    ids_validos = {regiao["id"] for regiao in regioes_da_zona}

    while True:
        try:
            escolha = int(
                input("\nEscolha uma região ou 0 para toda a zona: ")
            )

            if escolha == 0:
                return zona_escolhida, None

            if escolha in ids_validos:
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
    """Coleta filtros do histórico de forma hierárquica."""
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
        resposta = input(
            "\nDeseja filtrar também por data? [S/N]: "
        ).strip().lower()

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


def exibir_estatisticas():
    """Exibe as estatísticas calculadas pela camada de serviço."""
    estatisticas = calcular_estatisticas()

    if estatisticas["total"] == 0:
        print("\nNão há dados suficientes para gerar estatísticas.")
        return

    print("\n" + "=" * 60)
    print("ESTATÍSTICAS DO HISTÓRICO".center(60))
    print("=" * 60)

    print(
        "Total de interrupções registradas: "
        f"{estatisticas['total']}"
    )
    print(
        "Interrupções em andamento: "
        f"{estatisticas['em_andamento']}"
    )
    print(
        "Interrupções restabelecidas: "
        f"{estatisticas['restabelecidas']}"
    )
    print(
        "Região com mais interrupções: "
        f"{estatisticas['regiao_mais_afetada']} "
        f"({estatisticas['quantidade_regiao_mais_afetada']})"
    )
    print(
        "Zona com mais interrupções: "
        f"{estatisticas['zona_mais_afetada']} "
        f"({estatisticas['quantidade_zona_mais_afetada']})"
    )

    if estatisticas["restabelecidas"]:
        print(
            "Tempo total sem energia nas ocorrências encerradas: "
            f"{formatar_duracao(estatisticas['tempo_total'])}"
        )
        print(
            "Duração média das interrupções encerradas: "
            f"{formatar_duracao(estatisticas['tempo_medio'])}"
        )

        maior_interrupcao = estatisticas["maior_interrupcao"]
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


def consultar_historico():
    """Opção 4 - Histórico, filtros, duração e estatísticas."""
    if not listar_historico():
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
                    exibir_historico(listar_historico())

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
