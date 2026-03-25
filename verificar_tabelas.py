from google.cloud import bigquery
from config import get_client

print("🔍 Verificando tabelas de referência esperadas pelo código...")

# Tabelas que o código está tentando consultar
tabelas_esperadas = [
    'Servico',
    'operador',
    'AreaOperacional',
    'AreaGeograficaOperacao',
    'TipoSistema',
    'TipoVeiculo',
    'ParametroFuncional',
    'GrupamentoBRS',
    'Oficio'
]

try:
    client = get_client()

    # Query para listar todas as tabelas
    query = '''
    SELECT table_name
    FROM `rj-smtr-dev.CGR_Cadastro_Sistema_RIO.__TABLES__`
    ORDER BY table_name
    '''

    df = client.query(query).to_dataframe()
    tabelas_existentes = df['table_name'].tolist()

    print(f"📊 Tabelas encontradas no dataset: {len(tabelas_existentes)}")
    print(f"🎯 Tabelas esperadas pelo código: {len(tabelas_esperadas)}")

    print("\n🔍 Verificação:")

    tabelas_encontradas = []
    tabelas_faltando = []

    for tabela in tabelas_esperadas:
        if tabela in tabelas_existentes:
            tabelas_encontradas.append(tabela)
            print(f"  ✅ {tabela} - ENCONTRADA")
        else:
            tabelas_faltando.append(tabela)
            print(f"  ❌ {tabela} - FALTANDO")

    print(f"\n📈 Resumo:")
    print(f"  ✅ Encontradas: {len(tabelas_encontradas)}")
    print(f"  ❌ Faltando: {len(tabelas_faltando)}")

    if tabelas_faltando:
        print(f"  📋 Tabelas faltando: {tabelas_faltando}")
        print(f"\n💡 Solução: Criar essas tabelas no BigQuery ou ajustar o código para usar os nomes corretos.")

    print(f"\n📋 Todas as tabelas existentes: {sorted(tabelas_existentes)}")

except Exception as e:
    print(f"❌ Erro: {e}")
    import traceback
    traceback.print_exc()