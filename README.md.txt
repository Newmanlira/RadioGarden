# Rádio Garden Mundial (via Radio Browser)

Aplicação desenvolvida em Streamlit para visualização e exploração de rádios do mundo todo em um mapa interativo.  
Os dados são obtidos da API pública do Radio Browser, contendo informações atualizadas sobre estações, idiomas e países.

## Funcionalidades

- Visualização geográfica das estações em mapa interativo (Plotly + Mapbox)
- Filtros por país e idioma
- Exibição de metadados das rádios (bitrate, URL, estado, idioma)
- Tabela interativa com ordenação e pesquisa

## Estrutura do Projeto

projeto-radio-garden/
│
├── app/
│ └── radio_browser_dashboard.py
│
├── dags/
│ └── radio_garden_dag.py
│
├── data/
│ ├── raw/
│ ├── processed/
│ └── output/
│
├── requirements.txt
└── docker-compose.yml

bash
Copiar código

## Execução Local

1. Clonar o repositório
   ```bash
   git clone https://github.com/Newmanlira/RadioGarden.git
   cd RadioGarden
Criar ambiente virtual e instalar dependências

bash
Copiar código
python -m venv venv
venv\Scripts\activate  # Windows
pip install -r requirements.txt
Executar o aplicativo Streamlit

bash
Copiar código
streamlit run app/radio_browser_dashboard.py
Pipeline ETL (Airflow)
O projeto inclui um pipeline ETL implementado no Apache Airflow, composto pelas etapas:

Extract: coleta das estações via API do Radio Browser

Transform: limpeza e estruturação dos dados

Load: gravação dos dados transformados no diretório data/processed/ ou em um bucket MinIO (S3)

Cada execução é monitorada pela interface do Airflow, garantindo controle e rastreabilidade das tarefas.

Tecnologias Utilizadas
Categoria	Tecnologias
Backend	Python, Requests, Pandas
Frontend	Streamlit, Plotly Express
Orquestração	Apache Airflow
Armazenamento	MinIO (S3), CSV, Parquet
Infraestrutura	Docker, Docker Compose

Autor
Newman de Lira e Melo Neto
Engenheiro de Dados
E-mail: newmanliramelo@gmail.com
LinkedIn: linkedin.com/in/newmanlira
GitHub: github.com/Newmanlira