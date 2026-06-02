# Dashboard Executivo de Impacto Social - Instituto Bold & ADM

Este repositório contém o **Dashboard Executivo Premium** desenvolvido em parceria entre o **Instituto Bold** e a **ADM (Archer Daniels Midland)**. 

O foco central deste produto é demonstrar **Impacto Social, Diversidade, Inclusão e Empregabilidade** dos jovens formados pela Jornada CAB, servindo como uma ferramenta estratégica de storytelling de dados para patrocinadores, conselheiros e executivos.

---

## 🎨 Identidade Visual & Design System
O visual foi inspirado em relatórios executivos de grandes consultorias estratégicas (McKinsey, Deloitte, Bain) e utiliza a seguinte paleta de cores institucional:
- **Roxo Instituto Bold:** `#522f8b` (Cor primária e destaques de aprovação)
- **Dourado Instituto Bold:** `#fb9e21` (Cor de realce para indicadores D&I)
- **Azul ADM:** `#004B87` (Cor secundária corporativa)
- **Tipografia:** Importada do Google Fonts (*Outfit*), com visualização de cards glassmorphism, sombras premium e micro-animações interativas.

---

## 📂 Estrutura do Projeto

```
c:\Users\Admin\Documents\ESTUDOS\dash_adm\
├── app.py                      # Página de Boas-Vindas e Portal Principal
├── assets/                     # Recursos visuais e marcas
│   ├── logos/
│   │   ├── instituto_bold.png
│   │   └── adm.png
│   └── favicon/
│       └── favicon.png
├── pages/                      # Páginas específicas da aplicação Streamlit
│   ├── 01_visao_geral.py       # KPIs Executivos, Mapa Territorial e Funil
│   ├── 02_perfil_demografico.py # Idade, Etnia, Gênero e Renda Familiar
│   ├── 03_impacto_social.py    # Índices D&I e Indicadores ESG Compostos
│   ├── 04_empregabilidade.py   # Empregabilidade e Dados Comportamentais (Jornada)
│   ├── 05_consulta_individual.py # Busca Avançada e Ficha Completa do Aluno
│   └── 06_perfil_aprovados.py  # Análise exclusiva dos candidatos selecionados
├── services/
│   └── sheets_service.py       # Autenticação Google Sheets & Fallback
├── styles/
│   └── custom.css              # Estilização CSS premium e Responsividade
├── utils/
│   ├── metrics.py              # Cálculo de KPIs e Métricas D&I
│   ├── charts.py               # Design de gráficos corporativos no Plotly
│   ├── insights.py             # Gerador dinâmico de insights executivos
│   ├── interface.py            # Componentes reutilizáveis (Sidebar, CSS)
│   └── pdf_service.py          # Gerador de relatórios PDF com ReportLab
├── requirements.txt            # Dependências de bibliotecas Python
└── README.md                   # Documentação do projeto
```

---

## ⚙️ Configuração de Dados (Google Sheets)

O dashboard consome dados em tempo real de uma planilha Google Sheets (aba `CAB`). A autenticação é realizada via **Service Account do Google**.

### 1. Variáveis de Ambiente Necessárias
As credenciais devem ser fornecidas sem hardcode no código pelas seguintes chaves:
- `GOOGLE_SERVICE_ACCOUNT_EMAIL`: E-mail da Service Account criada no Google Cloud.
- `GOOGLE_PRIVATE_KEY`: Chave privada da Service Account (formato PEM).
- `GOOGLE_SPREADSHEET_ID`: O ID da sua planilha Google Sheets (exibido na URL da planilha).

### 2. Rodando Localmente (.env)
Crie um arquivo chamado `.env` na raiz do seu projeto local:
```env
GOOGLE_SERVICE_ACCOUNT_EMAIL=seu-email-service-account@projeto.iam.gserviceaccount.com
GOOGLE_PRIVATE_KEY="-----BEGIN PRIVATE KEY-----\nMIIEvgIBADANBgkqhkiG9w0BAQEFAASCBKgwggSkAgEAAoIBAQ..."
GOOGLE_SPREADSHEET_ID=sua_planilha_id_aqui
```

### 3. Mecanismo de Contingência (Mock Data Fallback)
> [!NOTE]
> Se as credenciais do Google Sheets não estiverem configuradas ou se a conexão falhar, o dashboard **ativará automaticamente o Fallback de Alta Fidelidade**. 
> Ele gerará programaticamente **250 registros simulados** contendo exatamente os mesmos campos, comportamentos e distribuições regionais das áreas de atuação da ADM (Uberlândia-MG, Rondonópolis-MT, Catalão-GO, Paranaguá-PR, Sorocaba-SP, etc.). Isso permite que o dashboard seja visualizado **100% funcional imediatamente**.

---

## 📈 Fórmulas dos Indicadores ESG Compostos

Criamos métricas sofisticadas de impacto para apresentações institucionais:

### A. Índice de Inclusão (D&I)
Mede a representatividade geral na base. Calcula a porcentagem de candidatos aprovados que atendem a pelo menos uma dimensão de diversidade:
$$\text{Índice de Inclusão} = \frac{\text{Mulheres } \cup \text{ Minorias Étnicas (Preta/Parda/Indígena) } \cup \text{ Baixa Renda } \cup \text{ PCD}}{\text{Total de Participantes}}$$

### B. Índice de Vulnerabilidade Social
Identifica participantes em maior vulnerabilidade acumulada. É classificado como vulnerável o participante que atende cumulativamente a **pelo menos dois** dos seguintes critérios:
1. Renda Familiar de até 2 salários mínimos.
2. Desempregado ou sem experiência de trabalho prévia.
3. Baixa escolaridade formal (ensino médio público).

### C. Potencial de Transformação
Porcentagem de jovens aprovados em posições onde o programa representa a maior ponte de mudança de vida: desempregados ou em busca do primeiro emprego, oriundos de famílias de baixa renda e baixa escolaridade.

---

## 🚀 Como Executar o Projeto Localmente

1. Certifique-se de possuir o Python 3.10+ instalado no seu computador.
2. Clone ou copie a pasta do projeto para a sua máquina.
3. Instale as dependências executando:
   ```bash
   py -m pip install -r requirements.txt
   ```
4. Se quiser regenerar as imagens de marca e logo localmente, rode:
   ```bash
   py assets/generate_assets.py
   ```
5. Inicie o dashboard local executando:
   ```bash
   py -m streamlit run app.py
   ```
6. O Streamlit abrirá automaticamente a interface no seu navegador padrão (geralmente em `http://localhost:8501`).

---

## ☁️ Deploy no Streamlit Community Cloud

Para disponibilizar o dashboard publicamente para os diretores da ADM:
1. Suba o código do seu repositório para uma conta do GitHub.
2. Acesse o [Streamlit Community Cloud](https://share.streamlit.io/) e faça login com sua conta do GitHub.
3. Clique em **"New app"** e selecione o repositório, branch e o arquivo principal `app.py`.
4. Clique em **"Advanced Settings"**.
5. No campo **"Secrets"**, cole suas credenciais do Google Sheets no formato TOML:
   ```toml
   GOOGLE_SERVICE_ACCOUNT_EMAIL = "seu-email-service-account@projeto.iam.gserviceaccount.com"
   GOOGLE_PRIVATE_KEY = "-----BEGIN PRIVATE KEY-----\nMIIEvgIBADANBgkqhkiG9w0BAQEFAASCBKgwggSkAgEAAoIBAQ..."
   GOOGLE_SPREADSHEET_ID = "sua_planilha_id_aqui"
   ```
6. Clique em **"Deploy"**. Seu painel executivo estará online e totalmente operacional em poucos minutos!
