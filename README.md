# API de Tarefas - Flask

Uma API REST simples para gerenciamento de tarefas usando Flask e SQLite.

## Funcionalidades

- ✅ Criar tarefas
- ✅ Listar todas as tarefas
- ✅ Filtrar tarefas por status
- ✅ Buscar tarefa por ID
- ✅ Atualizar tarefa existente
- ✅ Excluir tarefa
- ✅ Validação de dados
- ✅ Banco de dados SQLite

## Pré-requisitos

- Python 3.7 ou superior
- pip (gerenciador de pacotes Python)

## Instalação e Execução

### Linux 

1. **Instalar Python e pip** (se não estiver instalado):
   ```bash
   sudo apt update
   sudo apt install python3 python3-pip python3-venv
   ```

2. **Criar e ativar ambiente virtual**:
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```

3. **Instalar dependências**:
   ```bash
   pip install flask
   ```

4. **Salvar o código** em um arquivo chamado `app.py`

5. **Executar a aplicação**:
   ```bash
   python3 app.py
   ```

### Windows

1. **Instalar Python**:
   - Baixe Python em https://python.org/downloads/
   - Durante a instalação, marque "Add Python to PATH"

2. **Abrir Command Prompt ou PowerShell**

3. **Criar e ativar ambiente virtual**:
   ```cmd
   python -m venv venv
   venv\Scripts\activate
   ```

4. **Instalar dependências**:
   ```cmd
   pip install flask
   ```

5. **Salvar o código** em um arquivo chamado `app.py`

6. **Executar a aplicação**:
   ```cmd
   python app.py
   ```

## Estrutura de Dados

### Tarefa
```json
{
  "id": 1,
  "titulo": "Minha tarefa",
  "descricao": "Descrição da tarefa",
  "status": "pendente",
  "data_vencimento": "2024-12-31"
}
```

### Status válidos:
- `pendente`
- `realizando`
- `concluída`

## Endpoints da API

### 1. Criar Tarefa
**POST** `/tarefas`

**Body:**
```json
{
  "titulo": "Estudar Python",
  "descricao": "Revisar conceitos de Flask",
  "status": "pendente",
  "data_vencimento": "2024-12-31"
}
```

**Resposta:**
```json
{
  "id": 1,
  "titulo": "Estudar Python",
  "descricao": "Revisar conceitos de Flask",
  "status": "pendente",
  "data_vencimento": "2024-12-31"
}
```

### 2. Listar Tarefas
**GET** `/tarefas`

**Parâmetros opcionais:**
- `status`: filtrar por status (pendente, realizando, concluída)

**Exemplos:**
```bash
# Listar todas as tarefas
curl http://localhost:5000/tarefas

# Filtrar por status
curl http://localhost:5000/tarefas?status=pendente
```

### 3. Buscar Tarefa por ID
**GET** `/tarefas/{id}`

**Exemplo:**
```bash
curl http://localhost:5000/tarefas/1
```

### 4. Atualizar Tarefa
**PUT** `/tarefas/{id}`

**Body:**
```json
{
  "titulo": "Estudar Python - Atualizado",
  "descricao": "Revisar conceitos de Flask e SQLite",
  "status": "realizando",
  "data_vencimento": "2024-12-31"
}
```

### 5. Excluir Tarefa
**DELETE** `/tarefas/{id}`

**Exemplo:**
```bash
curl -X DELETE http://localhost:5000/tarefas/1
```

## Testando a API

### Usando curl (Linux/Windows)

1. **Criar uma tarefa:**
   ```bash
   curl -X POST http://localhost:5000/tarefas \
     -H "Content-Type: application/json" \
     -d '{"titulo": "Minha primeira tarefa", "descricao": "Teste da API", "status": "pendente"}'
   ```

2. **Listar tarefas:**
   ```bash
   curl http://localhost:5000/tarefas
   ```

3. **Buscar tarefa específica:**
   ```bash
   curl http://localhost:5000/tarefas/1
   ```

### Usando Postman ou Insomnia

1. Importe a coleção com os endpoints listados acima
2. Configure a base URL como `http://localhost:5000`
3. Teste cada endpoint individualmente


## Códigos de Erro

- **400**: Dados inválidos (título/status obrigatórios, status inválido, data inválida)
- **404**: Tarefa não encontrada
- **500**: Erro interno do servidor

## Observações

- A API roda por padrão na porta 5000
- O banco de dados SQLite é criado automaticamente no primeiro uso
- O modo debug está habilitado para desenvolvimento
- Para uso em produção, desabilite o modo debug e configure um servidor WSGI

## Desativando o Ambiente Virtual

Quando terminar de usar a aplicação:

**Linux:**
```bash
deactivate
```

**Windows:**
```cmd
deactivate
```
