# test_google_connection.py
import sys
from dotenv import load_dotenv

# Load local environment variables
load_dotenv()

print("==================================================")
print("INICIANDO TESTE ISOLADO DE INTEGRAÇÃO GOOGLE SHEETS")
print("==================================================")

try:
    from services.sheets_service import test_google_connection, DATA_SOURCE_STATUS
    
    print("\n[INFO] Executando rotina de teste de conexão...")
    success, message = test_google_connection()
    
    print("\n---------------- RESULTADO DO TESTE ----------------")
    if success:
        print("[OK] Autenticado com sucesso no Google Sheets")
        print(f"[OK] Planilha encontrada: '{DATA_SOURCE_STATUS['spreadsheet_name']}'")
        print("[OK] Aba CAB encontrada")
        print("[OK] Dados carregados")
        print(f"[OK] Quantidade de registros carregados: {DATA_SOURCE_STATUS['total_rows']}")
        print(f"[OK] Quantidade de colunas encontradas: {DATA_SOURCE_STATUS['total_cols']}")
        print(f"[OK] Schema estrutural das primeiras 5 colunas: {DATA_SOURCE_STATUS['first_cols']}")
        print("\n[SUCESSO] Integração com Google Sheets totalmente homologada e operacional!")
        sys.exit(0)
    else:
        print(f"[ERRO] Falha na Conexão: {message}")
        print("\nDiagnóstico de Variáveis:")
        diag = DATA_SOURCE_STATUS["env_diagnostics"]
        print(f"  - E-mail da Service Account encontrado? {'SIM' if diag['email_ok'] else 'NÃO'}")
        print(f"  - Chave Privada encontrada? {'SIM' if diag['key_ok'] else 'NÃO'}")
        print(f"  - Chave formatada no padrão PEM correto? {'SIM' if diag['key_structure_ok'] else 'NÃO'}")
        print(f"  - Chave possui tamanho válido? {'SIM ('+str(diag['key_length'])+' bytes)' if diag['key_length'] > 0 else 'NÃO'}")
        print(f"  - Spreadsheet ID encontrado? {'SIM' if diag['id_ok'] else 'NÃO'}")
        print("\n[ERRO] A conexão falhou. Por favor, revise as credenciais no arquivo .env conforme as mensagens acima.")
        sys.exit(1)
        
except ImportError as e:
    print(f"[ERRO] Erro Crítico de Importação: {e}")
    print("Certifique-se de possuir gspread, google-auth e as dependências instaladas via 'py -m pip install -r requirements.txt'")
    sys.exit(1)
except Exception as e:
    print(f"[ERRO] Erro Inesperado durante o teste: {e}")
    sys.exit(1)
