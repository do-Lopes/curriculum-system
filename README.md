# Sistema de Gerenciamento de Currículos

Este é um sistema web desenvolvido com Django para gerenciamento de currículos, permitindo cadastro, edição, visualização e remoção de dados curriculares.

## 📋 Pré-requisitos

- Docker
- Docker Compose
- Git

## 🎯 Principais Funcionalidades

- Gerenciamento de currículos (criação, atualização, visualização, exclusão)
- Interface administrativa Django
- Sistema de autenticação

## 🚀 Começando

### 1. Clone o repositório

```bash
git clone https://github.com/do-Lopes/curriculum-system.git
cd curriculum-system
```

### 2. Configuração do Ambiente

Crie um arquivo `.env` na raiz do projeto:

```plaintext
DJANGO_SUPERUSER_USERNAME=admin
DJANGO_SUPERUSER_PASSWORD=sua_senha_segura
DJANGO_SUPERUSER_EMAIL=seu_email@exemplo.com
```

### 3. Construa e Execute o Projeto

```bash
# Primeira vez: com --build
docker-compose up --build

# Durante desenvolvimento normal: sem --build
docker-compose up

# Caso faça alterações nas configs: com --build novamente
docker-compose up --build
```

### 4. Acesse o Sistema

Após a inicialização, acesse:
- Painel Admin: http://localhost:8000/admin
- Home do site: http://localhost:8000/dashboard
- Página de registro: http://localhost:8000/authors/register/
- Página de login: http://localhost:8000/authors/login/

Use as credenciais definidas no arquivo `.env` para fazer login apenas na página de admnistração. Crie novas credenciais para restante do sistema.

## 📦 Estrutura do Projeto

```plaintext
.
├── base_static/                    # Base para arquivos CSS
│   └── global/
│       └── css/
│           └── styles.css        
├── base_templates/                 # Templates HTML do site
│   global/
│       └── partials/
│       └── base.html
├── utils/
│   ├── djang_curriculums_admin.py
│   ├── django_forms.py
│   └── verify_datetime.py
├── authors/                        # App de gerenciamento de autores
│   ├── forms/
│   ├── tests/
│   ├── templates/
│   │   └── authors/
│   │       └── partials/
│   │       └── pages/
│   ├── models.py
│   ├── views.py
│   └── urls.py
├── curriculum/                     # App de gerenciamento de currículos
│   ├── templates/  
│   │   └── curriculums/
│   │       └── partials/
│   │       └── pages/        
│   ├── models.py
│   ├── views.py
│   └── urls.py
└── project/                        # Configurações principais do projeto
    ├── settings.py
    ├── urls.py
    └── wsgi.py
```

## 🛠️ Comandos Úteis

### Gerenciamento do Docker

```bash
# Parar os containers
docker-compose down

# Visualizar logs
docker-compose logs
```

### Comandos Django

```bash
# Criar migrações
python manage.py makemigrations

# Aplicar migrações
python manage.py migrate

# Criar superusuário
python manage.py createsuperuser
```
