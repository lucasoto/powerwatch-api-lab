# PowerWatch API

API REST desenvolvida com **Python** e **FastAPI** para simular o monitoramento de interrupções de energia em diferentes regiões da cidade de São Paulo.

> Projeto em desenvolvimento, criado com foco em estudo de APIs, organização de código e fundamentos de backend.

## Funcionalidades

* Consulta de regiões e estado atual da energia
* Registro de interrupções por região
* Registro de interrupções por zona
* Consulta de interrupções e histórico
* Filtros por região, zona, status e data
* Restabelecimento de uma interrupção
* Estatísticas básicas das ocorrências
* Tratamento de erros com códigos HTTP adequados

## Tecnologias

* Python 3.14
* FastAPI
* Pydantic
* Uvicorn

## Estrutura

```text
app/
├── __init__.py
├── main.py       # Rotas FastAPI
├── schemas.py    # Modelos de entrada com Pydantic
├── services.py   # Regras de negócio
├── data.py       # Dados temporários em memória
└── cli.py        # Interface CLI desenvolvida na fase inicial
```

## Como executar

Instale as dependências:

```bash
python -m pip install -r requirements.txt
```

Inicie a API na raiz do projeto:

```bash
fastapi dev app/main.py
```

A documentação interativa estará disponível em:

```text
http://127.0.0.1:8000/docs
```

## Principais endpoints

| Método | Endpoint               | Descrição                                |
| ------ | ---------------------- | ---------------------------------------- |
| GET    | `/health`              | Verifica o funcionamento da API          |
| GET    | `/regions`             | Lista as regiões                         |
| GET    | `/regions/{region_id}` | Consulta uma região                      |
| POST   | `/outages`             | Registra uma interrupção                 |
| POST   | `/outages/by-zone`     | Registra interrupções em uma zona        |
| GET    | `/outages`             | Lista ou filtra interrupções             |
| GET    | `/outages/{outage_id}` | Consulta uma interrupção                 |
| PATCH  | `/outages/{outage_id}` | Marca uma interrupção como restabelecida |
| GET    | `/stats`               | Exibe estatísticas das interrupções      |

## Estado atual

Nesta versão, os dados são mantidos **em memória** e são perdidos quando a aplicação é reiniciada.

Próximas etapas planejadas incluem testes automatizados, validações mais completas e persistência com banco de dados.

## Objetivo

O PowerWatch faz parte do meu processo de aprendizado em desenvolvimento backend, partindo de uma aplicação Python em terminal até uma API REST organizada em camadas.
