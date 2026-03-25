#!/usr/bin/env python3
"""
Diagnóstico das tabelas de referência
Execute este script para verificar se as tabelas existem e têm dados.
"""

from google.cloud import bigquery
from config import get_client

def main():
    print("🔍 DIAGNÓSTICO: Tabelas de referência no cadastro de linhas")
    print("=" * 60)

    # Tabelas que o código do app está tentando consultar
    tabelas_esperadas = {
        'Servico': 'Serviços (Prefixo + descrição)',
        'operador': 'Operadores (nomeFantasia)',
        'AreaOperacional': 'Áreas Operacionais',
        'AreaGeograficaOperacao': 'Áreas Geográficas',
        'TipoSistema': 'Tipos de Sistema',
        'TipoVeiculo': 'Tipos de Veículo',
        'ParametroFuncional': 'Parâmetros Funcionais',
        'GrupamentoBRS': 'Grupamentos BRS',
        'Oficio': 'Ofícios'
    }

    try:
        client = get_client()
        print("✅ Conexão com BigQuery estabelecida")

        # Query para listar todas as tabelas e contar linhas
        query = '''
        SELECT table_name, row_count
        FROM `rj-smtr-dev.CGR_Cadastro_Sistema_RIO.__TABLES__`
        ORDER BY table_name
        '''

        df = client.query(query).to_dataframe()
        tabelas_existentes = df.set_index('table_name')['row_count'].to_dict()

        print(f"\n📊 Dataset tem {len(tabelas_existentes)} tabelas")

        print("\n🔍 VERIFICAÇÃO DAS TABELAS ESPERADAS:")
        print("-" * 50)

        tabelas_ok = []
        tabelas_faltando = []
        tabelas_vazias = []

        for tabela, descricao in tabelas_esperadas.items():
            if tabela in tabelas_existentes:
                linhas = tabelas_existentes[tabela]
                if linhas > 0:
                    print(f"✅ {tabela} ({descricao}): {linhas} registros")
                    tabelas_ok.append(tabela)
                else:
                    print(f"⚠️  {tabela} ({descricao}): TABELA VAZIA")
                    tabelas_vazias.append(tabela)
            else:
                print(f"❌ {tabela} ({descricao}): TABELA NÃO EXISTE")
                tabelas_faltando.append(tabela)

        print("\n" + "=" * 60)
        print("📈 RESUMO:")
        print(f"✅ Tabelas OK (com dados): {len(tabelas_ok)}")
        print(f"⚠️  Tabelas vazias: {len(tabelas_vazias)}")
        print(f"❌ Tabelas faltando: {len(tabelas_faltando)}")

        if tabelas_faltando:
            print(f"\n💡 TABELAS QUE PRECISAM SER CRIADAS:")
            for tabela in tabelas_faltando:
                print(f"   - {tabela}")

        if tabelas_vazias:
            print(f"\n📝 TABELAS QUE PRECISAM SER POVOADAS:")
            for tabela in tabelas_vazias:
                print(f"   - {tabela}")

        print(f"\n📋 TODAS AS TABELAS EXISTENTES ({len(tabelas_existentes)}):")
        for tabela, linhas in sorted(tabelas_existentes.items()):
            status = "📈" if linhas > 0 else "📭"
            print(f"   {status} {tabela}: {linhas} linhas")

    except Exception as e:
        print(f"❌ ERRO: {e}")
        print("\n💡 POSSÍVEIS CAUSAS:")
        print("   - Credenciais ADC não configuradas")
        print("   - Projeto 'rj-smtr-dev' inacessível")
        print("   - Dataset 'CGR_Cadastro_Sistema_RIO' não existe")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()