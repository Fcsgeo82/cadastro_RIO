from google.auth import default as google_auth_default
from google.cloud import bigquery

print("🔍 Verificando tabelas de referência no dataset CGR_Cadastro_Sistema_RIO...")

try:
    credentials, project_id = google_auth_default(scopes=['https://www.googleapis.com/auth/bigquery'])
    client = bigquery.Client(project='rj-smtr-dev', credentials=credentials)

    # Obter todas as tabelas do dataset
    dataset_ref = client.dataset('CGR_Cadastro_Sistema_RIO')
    tables = list(client.list_tables(dataset_ref))
    table_names = [t.table_id for t in tables]

    print(f"📊 Total de tabelas encontradas: {len(table_names)}")
    print(f"📋 Tabelas: {sorted(table_names)}")

    # Tabelas de referência esperadas pelo código
    tabelas_referencia = [
        'Servico', 'servico', 'servicos',
        'operador', 'operadores',
        'areaOperacional', 'areas_operacionais',
        'areaGeografica', 'areas_geograficas',
        'tipoSistema', 'tipos_sistema',
        'tipoVeiculo', 'tipos_veiculo', 'frotaTipoVeiculo',
        'parametro', 'parametros',
        'grupamentoBRS', 'grupamentos',
        'oficio', 'oficios'
    ]

    print("\n🔍 Verificando tabelas de referência:")
    tabelas_encontradas = []
    tabelas_com_dados = []

    for tabela in tabelas_referencia:
        if tabela in table_names:
            tabelas_encontradas.append(tabela)

            # Verificar se tem dados
            try:
                table_ref = dataset_ref.table(tabela)
                table = client.get_table(table_ref)
                if table.num_rows > 0:
                    tabelas_com_dados.append(f"{tabela} ({table.num_rows} linhas)")
                    print(f"  ✅ {tabela}: {table.num_rows} linhas")
                else:
                    print(f"  ⚠️  {tabela}: tabela vazia")
            except Exception as e:
                print(f"  ❌ {tabela}: erro ao acessar ({e})")

    print(f"\n📊 Resumo:")
    print(f"  🎯 Tabelas de referência encontradas: {len(tabelas_encontradas)}")
    print(f"  📈 Tabelas com dados: {len(tabelas_com_dados)}")

    if tabelas_com_dados:
        print(f"  📋 Com dados: {tabelas_com_dados}")

except Exception as e:
    print(f"❌ Erro: {e}")