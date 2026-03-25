# =============================================================
# db.py — Operações com BigQuery
# Dataset: CGR_Cadastro_Sistema_RIO
# =============================================================

import uuid
from datetime import datetime, timezone

import pandas as pd
from google.cloud import bigquery

from config import get_client, PROJECT_ID, DATASET_ID


def ref(table: str) -> str:
    """Retorna referência completa da tabela para uso em queries."""
    return f"`{PROJECT_ID}.{DATASET_ID}.{table}`"


def _query_df(sql: str) -> pd.DataFrame:
    """Executa query e retorna DataFrame. Retorna vazio em caso de erro."""
    try:
        return get_client().query(sql).to_dataframe()
    except Exception:
        return pd.DataFrame()


# ------------------------------------------------------------------
# LOADERS — tabelas de referência para dropdowns
# ------------------------------------------------------------------

def carregar_servicos() -> pd.DataFrame:
    df = _query_df(f"""
        SELECT servicoID, Prefixo, descricao
        FROM {ref('Servico')}
        ORDER BY descricao
    """)
    if df.empty:
        return df
    df["label"] = df["Prefixo"].fillna("").str.strip() + " — " + df["descricao"].str.strip()
    return df[["servicoID", "label"]].rename(columns={"servicoID": "id"})


def carregar_operadores() -> pd.DataFrame:
    df = _query_df(f"""
        SELECT operadorID, nomeFantasia
        FROM {ref('operador')}
        ORDER BY nomeFantasia
    """)
    if df.empty:
        return df
    return df.rename(columns={"operadorID": "id", "nomeFantasia": "label"})


def carregar_areas_operacionais() -> pd.DataFrame:
    df = _query_df(f"""
        SELECT areaOperacionalID, descricao
        FROM {ref('AreaOperacional')}
        ORDER BY descricao
    """)
    if df.empty:
        return df
    return df.rename(columns={"areaOperacionalID": "id", "descricao": "label"})


def carregar_areas_geograficas() -> pd.DataFrame:
    df = _query_df(f"""
        SELECT areaGeograficaOperacaoID, area
        FROM {ref('AreaGeograficaOperacao')}
        ORDER BY area
    """)
    if df.empty:
        return df
    return df.rename(columns={"areaGeograficaOperacaoID": "id", "area": "label"})


def carregar_tipos_sistema() -> pd.DataFrame:
    df = _query_df(f"""
        SELECT tipoSistemaID, descricao
        FROM {ref('TipoSistema')}
        ORDER BY descricao
    """)
    if df.empty:
        return df
    return df.rename(columns={"tipoSistemaID": "id", "descricao": "label"})


def carregar_tipos_veiculo() -> pd.DataFrame:
    df = _query_df(f"""
        SELECT tipoVeiculoID, descricao
        FROM {ref('TipoVeiculo')}
        ORDER BY descricao
    """)
    if df.empty:
        return df
    return df.rename(columns={"tipoVeiculoID": "id", "descricao": "label"})


def carregar_parametros() -> pd.DataFrame:
    df = _query_df(f"""
        SELECT parametroFuncionalID, parametro
        FROM {ref('ParametroFuncional')}
        ORDER BY parametro
    """)
    if df.empty:
        return df
    return df.rename(columns={"parametroFuncionalID": "id", "parametro": "label"})


def carregar_grupamentos() -> pd.DataFrame:
    df = _query_df(f"""
        SELECT grupamentoBRSID, CAST(descricao AS STRING) AS descricao
        FROM {ref('GrupamentoBRS')}
        ORDER BY descricao
    """)
    if df.empty:
        return df
    return df.rename(columns={"grupamentoBRSID": "id", "descricao": "label"})


def carregar_oficios() -> pd.DataFrame:
    df = _query_df(f"""
        SELECT oficioID,
               CONCAT(CAST(numeroOficio AS STRING), ' — ', IFNULL(assunto,'')) AS label
        FROM {ref('Oficio')}
        ORDER BY numeroOficio DESC
    """)
    if df.empty:
        return df
    return df.rename(columns={"oficioID": "id"})


# Função genérica para montar dict {label -> id} usado nos selectboxes
def opcoes(df: pd.DataFrame) -> dict:
    """Converte DataFrame {id, label} em dict {label: id} para st.selectbox."""
    if df.empty:
        return {}
    return dict(zip(df["label"], df["id"]))


# ------------------------------------------------------------------
# INSERÇÃO — tabela Linha
# ------------------------------------------------------------------

def inserir_linha(dados: dict) -> tuple[bool, str]:
    """Insere nova linha no BigQuery. Retorna (sucesso, mensagem)."""
    client = get_client()
    agora  = datetime.now(tz=timezone.utc).isoformat()

    row = {
        "linhaID":               str(uuid.uuid4()),
        "numeroLinha":           dados.get("numeroLinha", "").strip(),
        "dataCriacaoLinha":      str(dados["dataCriacaoLinha"]) if dados.get("dataCriacaoLinha") else None,
        "servico":               dados.get("servico") or None,
        "operador":              dados.get("operador") or None,
        "vista":                 dados.get("vista", "").strip() or None,
        "areaOperacional":       dados.get("areaOperacional") or None,
        "oficio":                dados.get("oficio") or None,
        "oficioprimeiroHistorico": dados.get("oficioprimeiroHistorico") or None,
        "oficioUltimaAlteracao": dados.get("oficioUltimaAlteracao") or None,
        "tipoSistema":           dados.get("tipoSistema") or None,
        "kmIDA":                 float(dados["kmIDA"]) if dados.get("kmIDA") else None,
        "kmVOLTA":               float(dados["kmVOLTA"]) if dados.get("kmVOLTA") else None,
        "areaGeografica":        dados.get("areaGeografica") or None,
        "classificacaoEspacial": dados.get("classificacaoEspacial", "").strip() or None,
        "parametro":             dados.get("parametro") or None,
        "grupamentoBRS":         int(dados["grupamentoBRS"]) if dados.get("grupamentoBRS") else None,
        "frotaTipoVeiculo":      dados.get("frotaTipoVeiculo") or None,
        "frotaUltimoOficio":     dados.get("frotaUltimoOficio") or None,
        "frotaDataOficio":       dados.get("frotaDataOficio") or None,
        "itinerarioIDA":         dados.get("itinerarioIDA", "").strip() or None,
        "itinerarioIdaOficio":   dados.get("itinerarioIdaOficio") or None,
        "itinerarioIdaData":     dados.get("itinerarioIdaData") or None,
        "itinerarioVOLTA":       dados.get("itinerarioVOLTA", "").strip() or None,
        "itinerarioVoltaOficio": dados.get("itinerarioVoltaOficio") or None,
        "itinerarioVoltaData":   dados.get("itinerarioVoltaData") or None,
        "observacao":            dados.get("observacao", "").strip() or None,
        "dataCadastro":          agora,
        "ultimaAtualizacao":     agora,
    }

    table_id = f"{PROJECT_ID}.{DATASET_ID}.Linha"
    errors   = client.insert_rows_json(table_id, [row])

    if errors:
        return False, f"Erro ao inserir: {errors[0]}"
    return True, f"Linha {row['numeroLinha']} cadastrada com sucesso!"


# ------------------------------------------------------------------
# CONSULTA — tabela Linha com JOINs
# ------------------------------------------------------------------

def consultar_linhas(
    numero: str = "",
    area_operacional_id: str = "",
    operador_id: str = "",
    tipo_sistema_id: str = "",
) -> pd.DataFrame:
    """Consulta linhas com filtros e retorna DataFrame enriquecido com JOINs."""
    client    = get_client()
    condicoes = ["1=1"]

    if numero.strip():
        condicoes.append(f"LOWER(l.numeroLinha) LIKE '%{numero.strip().lower()}%'")
    if area_operacional_id:
        condicoes.append(f"l.areaOperacional = '{area_operacional_id}'")
    if operador_id:
        condicoes.append(f"l.operador = '{operador_id}'")
    if tipo_sistema_id:
        condicoes.append(f"l.tipoSistema = '{tipo_sistema_id}'")

    where = " AND ".join(condicoes)

    query = f"""
        SELECT
            l.numeroLinha                                                       AS `Número`,
            l.vista                                                             AS `Vista`,
            s.descricao                                                         AS `Serviço`,
            op.nomeFantasia                                                     AS `Operador`,
            ao.descricao                                                        AS `Área Operacional`,
            ts.descricao                                                        AS `Tipo Sistema`,
            ag.area                                                             AS `Área Geográfica`,
            pf.parametro                                                        AS `Parâmetro`,
            tv.descricao                                                        AS `Tipo Veículo`,
            l.kmIDA                                                             AS `KM Ida`,
            l.kmVOLTA                                                           AS `KM Volta`,
            l.classificacaoEspacial                                             AS `Classif. Espacial`,
            FORMAT_DATE('%d/%m/%Y', l.dataCriacaoLinha)                        AS `Data Criação`,
            FORMAT_TIMESTAMP('%d/%m/%Y %H:%M', l.dataCadastro, 'America/Sao_Paulo') AS `Cadastrado em`
        FROM {ref('Linha')} l
        LEFT JOIN {ref('Servico')}                s  ON l.servico         = s.servicoID
        LEFT JOIN {ref('operador')}               op ON l.operador        = op.operadorID
        LEFT JOIN {ref('AreaOperacional')}        ao ON l.areaOperacional = ao.areaOperacionalID
        LEFT JOIN {ref('TipoSistema')}            ts ON l.tipoSistema     = ts.tipoSistemaID
        LEFT JOIN {ref('AreaGeograficaOperacao')} ag ON l.areaGeografica  = ag.areaGeograficaOperacaoID
        LEFT JOIN {ref('ParametroFuncional')}     pf ON l.parametro       = pf.parametroFuncionalID
        LEFT JOIN {ref('TipoVeiculo')}            tv ON l.frotaTipoVeiculo = tv.tipoVeiculoID
        WHERE {where}
        ORDER BY l.dataCadastro DESC
        LIMIT 500
    """

    try:
        return client.query(query).to_dataframe()
    except Exception as e:
        return pd.DataFrame({"Erro": [str(e)]})
