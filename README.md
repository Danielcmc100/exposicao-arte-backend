# Exposição Arte Backend

Backend API para sistema de exposição de arte desenvolvido com FastAPI.

## Pré-requisitos

- uv (gerenciador de pacotes Python)

## Instalação

### 1. Instalar uv

Baixe e instale o uv seguindo a documentação oficial:
https://docs.astral.sh/uv/

### 2. Clonar o repositório
```bash
https://github.com/Danielcmc100/exposicao-arte-backend.git
```

### 3. Copie o arquivo de configuração
Crie um arquivo `.env` na raiz do projeto copiando o conteúdo do arquivo `.env.example`. Este arquivo contém as variáveis de ambiente necessárias para a aplicação.

```bash
cp .env.example .env
```


## Executar o projeto

Para rodar o servidor de desenvolvimento:

```bash
uv run fastapi dev src/app.py
```

O servidor estará disponível em `http://localhost:8000`

## Documentação da API

Acesse a documentação interativa da API em:
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

## Estrutura do projeto
```
src/
├── app.py              # Arquivo principal da aplicação
├── config.py            # Configurações gerais
├── database.py          # Conexão e funções do banco de dados
├── models/              # Modelos das entidades do sistema
│   └── ...
├── repositories/        # Funções de acesso ao banco de dados
│   └── ...
├── services/            # Rotas e lógica de negócio
│   └── ...
└── errors/              # Tratamento de erros personalizados
    └── ...

dockerfile               # Dockerfile para containerização
pyproject.toml           # Configuração do projeto Python
uv.lock                  # Lockfile do gerenciador uv
README.md                # Documentação do projeto
```

## Criando uma migração de banco de dados

Obs: antes de executar os comandos, certifique-se de que o banco de dados está configurado corretamente no arquivo `.env`. e que o seu modelo foi importado no arquivo `src/models/__init__.py`.

Para criar uma nova migração, use o comando:

```bash
uv run alembic revision --autogenerate -m "Descrição da migração"
```

Aplique as migrações pendentes com:

```bash
uv run alembic upgrade head
```

## Docker
Para construir e rodar o container Docker:
```bash
docker build -t exposicao-arte-backend .
docker run -p 8080:8080 exposicao-arte-backend
```