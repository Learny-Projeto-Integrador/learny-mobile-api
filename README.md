# learny-mobile-api

API REST do projeto **Learny** — plataforma educacional gamificada para crianças. Esta API atende tanto o aplicativo mobile (Expo/React Native) quanto o dashboard web (Next.js) destinado aos pais/responsáveis.

## Stack

- **Python 3.11+** com **Flask** e **Flask-RESTful**
- **MongoDB** via **Flask-PyMongo** (driver `pymongo`)
- **Flask-JWT-Extended** para autenticação por token
- **Marshmallow** + **flask-marshmallow** para validação e serialização
- **Gunicorn** como WSGI server em produção
- **pytest** + **mongomock** para a suíte de testes
- **GitHub Actions** para CI; deploy em **Render**

## Pré-requisitos

- Python 3.11 ou 3.12
- Acesso a um cluster MongoDB (local ou Atlas)
- `pip` atualizado

## Setup local

```bash
# 1. Clone o repositório
git clone <url-do-repo>
cd learny-mobile-api

# 2. Crie e ative o ambiente virtual
python -m venv venv

# Windows
venv\Scripts\activate
# macOS/Linux
source venv/bin/activate

# 3. Instale as dependências
pip install -r requirements.txt          # produção
pip install -r requirements-dev.txt      # produção + testes

# 4. Configure o arquivo .env (veja a próxima seção)

# 5. Rode a aplicação
python run.py
```

A API sobe por padrão em `http://0.0.0.0:5000`.

## Variáveis de ambiente

Crie um arquivo `.env` na raiz do projeto com as variáveis abaixo:

| Variável         | Descrição                                                    | Obrigatória |
|------------------|--------------------------------------------------------------|-------------|
| `DB_USER`        | Usuário do MongoDB Atlas                                     | Não (1)     |
| `DB_PASSWORD`    | Senha do MongoDB Atlas                                       | Não (1)     |
| `DB_HOST`        | Host do cluster Atlas (ex.: `cluster0.abcde.mongodb.net`)    | Não (1)     |
| `DB_NAME`        | Nome do banco a ser usado                                    | Sim         |
| `JWT_SECRET_KEY` | Chave secreta para assinar tokens JWT                        | Sim         |

(1) Se `DB_USER` e `DB_PASSWORD` não forem definidos, a API tenta conectar em `mongodb://localhost:27017/<DB_NAME>` (útil para desenvolvimento local).

Exemplo de `.env`:

```env
DB_USER=meu_usuario
DB_PASSWORD=minha_senha
DB_HOST=cluster0.abcde.mongodb.net
DB_NAME=learny
JWT_SECRET_KEY=troque-este-valor-em-producao
```

## Estrutura do projeto

```
learny-mobile-api/
├── api/
│   ├── __init__.py          # Inicialização do Flask, JWT, Mongo e CORS
│   ├── models/              # Dataclasses (Parent, Child, Progress, ...)
│   ├── resources/           # Rotas Flask-RESTful (HTTP)
│   ├── schemas/             # Schemas Marshmallow (validação/serialização)
│   ├── services/            # Regras de negócio + acesso ao MongoDB
│   └── utils/               # Utilitários (validate_data, ...)
├── tests/                   # Suíte pytest (94 testes, 79% de cobertura)
├── .github/workflows/ci.yml # Pipeline CI/CD (GitHub Actions)
├── pytest.ini               # Configuração do pytest
├── requirements.txt         # Dependências de produção
├── requirements-dev.txt     # Dependências de teste
├── run.py                   # Entry point
└── README.md
```

## Endpoints da API

Todos os endpoints autenticados exigem o header `Authorization: Bearer <token>`. O token é obtido via `POST /auth/login`.

### Autenticação

| Método | Rota          | Descrição                                        | Auth |
|--------|---------------|--------------------------------------------------|------|
| POST   | `/auth/login` | Autentica responsável ou criança e retorna o JWT | Não  |

### Responsáveis (parents)

| Método | Rota                                       | Descrição                                                  | Auth |
|--------|--------------------------------------------|------------------------------------------------------------|------|
| GET    | `/parents`                                 | Retorna os dados do responsável autenticado                | Sim  |
| POST   | `/parents`                                 | Cadastra um novo responsável                               | Não  |
| PUT    | `/parents`                                 | Atualiza os dados do responsável autenticado               | Sim  |
| DELETE | `/parents`                                 | Exclui a conta do responsável autenticado                  | Sim  |
| GET    | `/parents/children`                        | Lista todos os filhos do responsável                       | Sim  |
| POST   | `/parents/children`                        | Cadastra um novo filho (com progresso inicial)             | Sim  |
| GET    | `/parents/child/<id>`                      | Retorna os dados de um filho específico                    | Sim  |
| PUT    | `/parents/child/<id>`                      | Atualiza os dados de um filho                              | Sim  |
| DELETE | `/parents/child/<id>`                      | Remove um filho da conta do responsável                    | Sim  |
| GET    | `/parents/child/<id>/activity`             | Retorna o histórico de atividades de um filho              | Sim  |
| POST   | `/parents/child/<id>/notifications`        | Envia uma notificação para um filho                        | Sim  |
| GET    | `/parents/child/selected`                  | Retorna o filho atualmente selecionado + seu progresso     | Sim  |

### Crianças (children)

| Método | Rota                              | Descrição                                                  | Auth |
|--------|-----------------------------------|------------------------------------------------------------|------|
| GET    | `/child`                          | Retorna os dados da criança autenticada                    | Sim  |
| PUT    | `/child`                          | Atualiza os dados da criança autenticada                   | Sim  |
| GET    | `/child/progress`                 | Retorna o progresso da criança autenticada                 | Sim  |
| PUT    | `/child/progress`                 | Atualiza pontos, moedas, streak ou outros campos           | Sim  |
| PUT    | `/child/progress/complete-phase`  | Marca uma fase como concluída e atualiza progresso         | Sim  |
| GET    | `/child/notifications`            | Lista as notificações da criança                           | Sim  |
| GET    | `/children/ranking`               | Retorna o ranking global das crianças por pontuação        | Sim  |

### Jogo (game)

| Método | Rota                       | Descrição                                                  | Auth |
|--------|----------------------------|------------------------------------------------------------|------|
| GET    | `/game/worlds`             | Lista todos os mundos disponíveis                          | Sim  |
| GET    | `/game/worlds/<code>`      | Retorna detalhes de um mundo + módulos + fases             | Sim  |
| GET    | `/game/characters`         | Lista todos os personagens disponíveis                     | Sim  |

## Testes

A suíte usa **pytest** com **mongomock** para simular o MongoDB, sem depender de instância real.

```bash
# Roda todos os testes com relatório de cobertura
pytest

# Apenas um arquivo específico
pytest tests/test_login_service.py

# Apenas um teste
pytest tests/test_parent_service.py::TestRegisterParent::test_creates_parent
```

A configuração está em `pytest.ini`. O relatório de cobertura é gerado em `coverage.xml` (consumido pelo CI) e exibido no terminal.

**Cobertura atual**: 94 testes / 79% das linhas.

## CI/CD

O pipeline (`.github/workflows/ci.yml`) executa em todo push e pull request para `main` e `develop`:

1. **Lint / sintaxe**: `python -m compileall api tests`
2. **Testes**: `pytest --cov=api --cov-report=xml --cov-report=term`
3. **Matriz**: Python 3.11 e 3.12
4. **Cache** das dependências via `actions/setup-python`
5. **Deploy** (apenas em push para `main`): dispara o *deploy hook* do Render via `curl`

### Configurar deploy no Render

1. No GitHub → Settings → Secrets and variables → Actions, adicione o secret `RENDER_DEPLOY_HOOK_URL`.
2. A URL pode ser obtida em: Render → seu serviço → Settings → Deploy Hook.
3. A cada merge em `main`, o pipeline aciona o deploy automaticamente.

## Convenções

- **Commits**: [Conventional Commits](https://www.conventionalcommits.org/) (`feat:`, `fix:`, `ci:`, `test:`, `refactor:`, ...).
- **Branches**: `main` (produção), `develop` (integração), feature branches a partir de `develop`.
- **Estilo**: PEP 8.
