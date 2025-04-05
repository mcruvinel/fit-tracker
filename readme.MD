# Workouts Tracker 🏋️‍♂️🚴‍♀️

Este é um projeto fullstack para acompanhar e visualizar treinos esportivos a partir de arquivos `.FIT` (formato comum de dispositivos Garmin, por exemplo). Ele permite o upload de treinos, armazenamento dos dados em banco de dados, visualização dos treinos em lista e detalhes, além da exibição de gráficos com métricas de desempenho.

## ✨ Funcionalidades

- Upload de arquivos `.FIT`
- Extração dos dados de treino (tempo, distância, frequência cardíaca, etc.)
- Armazenamento dos dados em um banco de dados relacional
- API RESTful para acessar os treinos
- Frontend em React com gráficos interativos
- Visualização em lista e detalhes de cada treino

---

## ⚙️ Tecnologias

- **Backend**: [FastAPI](https://fastapi.tiangolo.com/)
- **Frontend**: [React](https://reactjs.org/) com [Vite](https://vitejs.dev/)
- **Banco de Dados**: SQLite (local) | Suporte para PostgreSQL
- **ORM**: SQLModel
- **Gráficos**: Recharts (no frontend)
- **Parser `.fit`**: [`fitparse`](https://github.com/dtcooper/python-fitparse)

---

## 🚀 Como rodar localmente

### Pré-requisitos

- Python 3.11+
- Node.js 18+
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

### 3. Configure o frontend (React + Vite)

Abra outro terminal:

```bash
cd frontend
npm install
npm run dev
```

O frontend estará disponível em: [http://localhost:5173](http://localhost:5173)

---

## 📂 Estrutura do Projeto

```
workouts-tracker/
│
├── backend/              # Backend com FastAPI
│   ├── app/
│   │   ├── api/          # Rotas da API
│   │   ├── models/       # Modelos do banco de dados
│   │   ├── services/     # Lógica de negócio e utilitários
│   │   └── main.py       # Ponto de entrada do backend
│   └── requirements.txt
│
├── frontend/             # Frontend com React e Vite
│   ├── src/
│   │   ├── components/   # Componentes reutilizáveis
│   │   ├── pages/        # Páginas da aplicação
│   │   └── App.tsx
│   └── package.json
│
└── README.md             # Este arquivo
```

---

## 🔧 Melhorias Futuras

- Autenticação de usuários
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