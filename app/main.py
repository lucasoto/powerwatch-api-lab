from fastapi import FastAPI, HTTPException, status

from app.schemas import (
    OutageCreate,
    OutageUpdate,
    OutageZoneCreate,
)

from app.services import (
    calcular_estatisticas,
    filtrar_historico,
    listar_historico,
    listar_regioes,
    obter_interrupcao,
    obter_regiao,
    registrar_interrupcao,
    registrar_interrupcoes_por_zona,
    restabelecer_interrupcao,
)


app = FastAPI(
    title="PowerWatch API",
    version="0.1.0",
)


@app.get("/health")
def health():
    return {"status": "ok"}


@app.get("/regions")
def get_regions():
    return listar_regioes()


@app.get("/regions/{region_id}")
def get_region(region_id: int):
    try:
        return obter_regiao(region_id)

    except ValueError as erro:
        raise HTTPException(
            status_code=404,
            detail=str(erro),
        )

@app.post("/outages", status_code=status.HTTP_201_CREATED)
def create_outage(outage: OutageCreate):
    try:
        obter_regiao(outage.region_id)

    except ValueError as erro:
        raise HTTPException(
            status_code=404,
            detail=str(erro),
        )

    try:
        return registrar_interrupcao(outage.region_id)

    except ValueError as erro:
        raise HTTPException(
            status_code=409,
            detail=str(erro),
        )

@app.get("/outages")
def get_outages(
    region_id: int | None = None,
    zone: str | None = None,
    status: str | None = None,
    day: int | None = None,
    month: int | None = None,
    year: int | None = None,
):
    return filtrar_historico(
        region_id=region_id,
        zone=zone,
        status=status,
        day=day,
        month=month,
        year=year,
    )

@app.get("/outages/{outage_id}")
def get_outage(outage_id: int):
    try:
        return obter_interrupcao(outage_id)

    except ValueError as erro:
        raise HTTPException(
            status_code=404,
            detail=str(erro),
        )

@app.patch("/outages/{outage_id}")
def update_outage(
    outage_id: int,
    outage: OutageUpdate,
):
    try:
        obter_interrupcao(outage_id)

    except ValueError as erro:
        raise HTTPException(
            status_code=404,
            detail=str(erro),
        )

    try:
        return restabelecer_interrupcao(outage_id)

    except ValueError as erro:
        raise HTTPException(
            status_code=409,
            detail=str(erro),
        )

@app.get("/stats")
def get_stats():
    return calcular_estatisticas()

@app.post(
    "/outages/by-zone",
    status_code=status.HTTP_201_CREATED,
)
def create_outages_by_zone(outage: OutageZoneCreate):
    try:
        interrupcoes = registrar_interrupcoes_por_zona(
            outage.zone
        )

    except ValueError as erro:
        raise HTTPException(
            status_code=404,
            detail=str(erro),
        )

    if not interrupcoes:
        raise HTTPException(
            status_code=409,
            detail="Todas as regiões dessa zona já estão sem energia.",
        )

    return interrupcoes
