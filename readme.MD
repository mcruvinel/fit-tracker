# Workouts Tracker 🏋️‍♂️🚴‍♀️

Este é um projeto fullstack para acompanhar e visualizar treinos esportivos a partir de arquivos `.FIT` (formato comum de dispositivos Garmin, por exemplo). Ele permite o upload de treinos, armazenamento dos dados em banco de dados, visualização dos treinos em lista e detalhes, além da exibição de gráficos com métricas de desempenho.

## ✨ Funcionalidades

- Upload de arquivos `.FIT`
- Extração dos dados de treino (tempo, distância, frequência cardíaca, etc.)
- Armazenamento dos dados em um banco de dados relacional
- API RESTful para acessar os treinos
- Interface em Streamlit para upload, visualização e gráficos dos treinos

---

## ⚙️ Tecnologias

- **Backend**: [FastAPI](https://fastapi.tiangolo.com/)
- **Frontend**: [Streamlit](https://streamlit.io/)
- **Banco de Dados**: SQLite (local) | Suporte para PostgreSQL
- **ORM**: SQLModel
- **Gráficos**: Altair / Matplotlib / Plotly via Streamlit
- **Parser `.fit`**: [`fitparse`](https://github.com/dtcooper/python-fitparse)

---

## 🚀 Como rodar localmente

### Pré-requisitos

- Python 3.11+
- Git

### 1. Clone o repositório

```bash
git clone https://github.com/mcruvinel/workouts-tracker.git
cd workouts-tracker
```

### 2. Configure o backend (FastAPI)

```bash
cd backend
python -m venv venv
source venv/bin/activate  # ou .\venv\Scripts\activate no Windows

pip install -r requirements.txt

# Inicie o backend
uvicorn app.main:app --reload
```

A API estará disponível em: [http://localhost:8000](http://localhost:8000)  
Documentação interativa: [http://localhost:8000/docs](http://localhost:8000/docs)

### 3. Rode o frontend (Streamlit)

Em outro terminal:

```bash
cd frontend
streamlit run app.py
```

A interface estará disponível em: [http://localhost:8501](http://localhost:8501)

---

## 📂 Estrutura do Projeto

```
workouts-tracker/
│
├── backend/              # Backend com FastAPI
│   ├── app/
│   │   ├── api/
│   │   ├── models/
│   │   ├── services/
│   │   └── main.py
│   └── requirements.txt
│
├── frontend/             # Frontend com Streamlit
│   ├── app.py            # App principal do Streamlit
│   └── requirements.txt
│
└── README.md             # Este arquivo
```

---

## 🔧 Melhorias Futuras

- Busca e filtros por tipo de treino, data e métricas
- Exportação de dados e gráficos
- Suporte a arquivos `.gpx` e `.tcx`
- Análises avançadas (zonas de FC, tempo em zona, etc.)

---

## 📄 Licença

Este projeto está licenciado sob a [MIT License](LICENSE).

---

## 👤 Autor

Desenvolvido por [@mcruvinel](https://github.com/mcruvinel)