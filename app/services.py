from datetime import datetime

from app.data import (
    historico_interrupcoes,
    mapeamento_zonas,
    regions,
)


def obter_regiao(region_id):
    if region_id not in regions:
        raise ValueError("Região não encontrada.")

    return regions[region_id]



def gerar_proximo_id_interrupcao():
    return max(
        (
            interrupcao["id"]
            for interrupcao in historico_interrupcoes
        ),
        default=0,
    ) + 1



def gerar_proximo_id_interrupcao():
    return max(
        (
            interrupcao["id"]
            for interrupcao in historico_interrupcoes
        ),
        default=0,
    ) + 1



def registrar_interrupcao(region_id):
    regiao = obter_regiao(region_id)

    if not regiao["has_power"]:
        raise ValueError(
            "A região já possui uma interrupção ativa."
        )

    interrupcao = {
        "id": gerar_proximo_id_interrupcao(),
        "region_id": region_id,
        "name": regiao["name"],
        "zone": regiao["zone"],
        "started_at": datetime.now(),
        "restored_at": None,
        "status": "sem_energia",
    }

    regiao["has_power"] = False
    historico_interrupcoes.append(interrupcao)

    return interrupcao



def registrar_interrupcoes_por_zona(zone):
    if zone not in mapeamento_zonas.values():
        raise ValueError("Zona inexistente.")

    interrupcoes_criadas = []

    for region_id, dados in regions.items():
        if dados["zone"] == zone and dados["has_power"]:
            interrupcao = registrar_interrupcao(region_id)

            interrupcoes_criadas.append(interrupcao)

    return interrupcoes_criadas



def restabelecer_energia(region_id):
    regiao = obter_regiao(region_id)

    if regiao["has_power"]:
        raise ValueError(
            "A região já está com energia."
        )

    interrupcao_ativa = None

    for interrupcao in reversed(historico_interrupcoes):
        if (
            interrupcao["region_id"] == region_id
            and interrupcao["status"] == "sem_energia"
        ):
            interrupcao_ativa = interrupcao
            break

    if interrupcao_ativa is None:
        raise RuntimeError(
            "Inconsistência: região sem energia sem interrupção ativa."
        )

    interrupcao_ativa["restored_at"] = datetime.now()
    interrupcao_ativa["status"] = "restabelecida"

    regiao["has_power"] = True

    return interrupcao_ativa



def listar_regioes():
    return list(regions.values())



def listar_historico():
    return list(historico_interrupcoes)



def filtrar_historico(
    region_id=None,
    zone=None,
    status=None,
    day=None,
    month=None,
    year=None,
):
    resultados = []

    for interrupcao in historico_interrupcoes:
        inicio = interrupcao["started_at"]

        if (
            region_id is not None
            and interrupcao["region_id"] != region_id
        ):
            continue

        if (
            zone is not None
            and interrupcao["zone"] != zone
        ):
            continue

        if (
            status is not None
            and interrupcao["status"] != status
        ):
            continue

        if day is not None and inicio.day != day:
            continue

        if month is not None and inicio.month != month:
            continue

        if year is not None and inicio.year != year:
            continue

        resultados.append(interrupcao)

    return resultados



def calcular_duracao(interrupcao):
    fim = interrupcao["restored_at"]

    if fim is None:
        fim = datetime.now()

    return fim - interrupcao["started_at"]


