# 🏦 CRUD com PyMongo - Guia Interativo

## 🚀 Introdução
Bem-vindo ao **CRUD com PyMongo!** Aqui você aprenderá a criar, ler, atualizar e excluir dados de forma dinâmica utilizando o **MongoDB** com Python. 📌

> 🎯 **Objetivo**: Cadastrar **gerentes** e **clientes** automaticamente, segmentá-los e gerar relatórios interativos!

---

## 🔧 Configuração Inicial
Antes de começar, certifique-se de:
✅ Ter o **MongoDB** instalado e rodando.  
✅ Instalar a biblioteca PyMongo:
```bash
pip install pymongo
```
✅ Criar a conexão com o banco:
```python
import pymongo as pm
import datetime as dt

conexao = pm.MongoClient("mongodb://localhost:27017/")
db = conexao["banco"]

collection_gerente = db["gerentes"]
collection_cliente = db["clientes"]
```
📌 **Agora estamos prontos para CRUD!**

---

## 📜 Dependências do Projeto
Para garantir que todas as bibliotecas necessárias sejam instaladas corretamente, utilize um arquivo `requirements.txt`.  
Crie um arquivo chamado `requirements.txt` e adicione o seguinte conteúdo:

```
pymongo
```

Agora, no terminal, execute:
```bash
pip install -r requirements.txt
```
Isso instalará automaticamente todas as dependências necessárias! ✅

---

## 🏗️ Operações CRUD

### 🔹 1. Criar um Gerente
```python
def cadastrarGerente(nome: str, agencia: str, segmento: str) -> dict | None:
    gerente_inserido = collection_gerente.insert_one(
        {
            "nome": nome,
            "agencia": agencia,
            "segmento": segmento,
            "clientes": []
        }
    ).inserted_id
    return gerente_inserido
```
✅ **Uso:**
```python
cadastrarGerente("Carlos Silva", "SP-001", "Exclusive")
```
📝 **Explicação:** Cadastra um novo gerente na base de dados.

---

### 🔹 2. Definir Segmento Financeiro
```python
def definir_segmento(renda):
    if renda <= 6999.99:
        return "Varejo"
    elif 7000 <= renda <= 29999:
        return "Exclusive"
    elif 30000 <= renda <= 99999:
        return "Premium"
    else:
        return "Classe A"
```
✅ **Uso:**
```python
print(definir_segmento(15000))  # Saída: Exclusive
```
💡 **Dica:** Segmentar clientes é essencial para oferecer atendimento personalizado!

---

### 🔹 3. Encontrar um Gerente Ideal
```python
def pegarGerente(estado: str, renda: int) -> dict | None:
    segmento = definir_segmento(renda)
    gerentes = list(collection_gerente.find(
        {"$or": [{"agencia": estado},
                  {"agencia": "Geral"}],
         "segmento": segmento,
         }))
    
    gerentes.sort(key=lambda g: len(g["clientes"]))
    
    return gerentes[0] if gerentes else None
```
✅ **Uso:**
```python
pegarGerente("SP-001", 12000)
```
🎯 **Objetivo:** Encontrar o gerente com menos clientes no mesmo segmento do cliente.

![Gerente e Cliente](https://cdn-icons-png.flaticon.com/512/1256/1256650.png)

---

### 🔹 4. Cadastrar um Cliente
```python
def inserirCliente(nome: str, cpf: str, renda: float, estado: str, nascimento: dt.datetime) -> dict | None:
    segmento = definir_segmento(renda)
    gerente = pegarGerente(estado, renda)

    if not gerente:
        return None  # Nenhum gerente disponível

    cliente_inserido = collection_cliente.insert_one(
        {
            "nome": nome,
            "cpf": cpf,
            "renda": renda,
            "estado": estado,
            "dataNascimento": nascimento,
            "dataCadastro": dt.datetime.now(),
            "segmento": segmento,
            "gerente": gerente["nome"]
        }
    ).inserted_id

    collection_gerente.update_one(
        {"_id": gerente["_id"]},
        {"$addToSet": {"clientes": cliente_inserido}}
    )
    return cliente_inserido
```
✅ **Uso:**
```python
inserirCliente("Ana Souza", "123.456.789-00", 8500, "SP-001", dt.datetime(1990, 5, 12))
```
📌 **Agora temos um novo cliente no sistema!**

---

### 📊 5. Relatório de Gerente
```python
def relatorioGerente(nome_gerente):
    gerente = collection_gerente.find_one({"nome": nome_gerente})
    if not gerente:
        return "Gerente não encontrado."
    
    for cliente_id in gerente["clientes"]:
        cliente = collection_cliente.find_one({"_id": cliente_id})
        print(f"{cliente['nome']} - CPF: {cliente['cpf']} - Estado: {cliente['estado']} - Renda: R$ {cliente['renda']:.2f}")
```
✅ **Uso:**
```python
relatorioGerente("Carlos Silva")
```
📈 **Gera um relatório de clientes vinculados a um gerente.**


---

### 📊 6. Relatório por Segmento
```python
def relatorioSegmento():
    segmentos = collection_gerente.distinct("segmento")
    for i in segmentos:
        print(f"Segmento: {i}")
        for cliente in collection_cliente.find({"segmento": i}):
            print(
                f"{cliente['nome']} - CPF: {cliente['cpf']} - Estado: {cliente['estado']} - Renda: R$ {cliente['renda']:.2f} - Gerente: {cliente['gerente']}"
            )
```
✅ **Uso:**
```python
relatorioSegmento()
```
📊 **Mostra todos os clientes separados por segmento financeiro.**

---

## 🎯 Conclusão
✅ Agora você domina o CRUD com **PyMongo**! 🏆  
📌 Você pode expandir este sistema adicionando autenticação, dashboards gráficos e muito mais! 🚀

👨‍💻 **Agora é sua vez! Implemente e personalize este projeto!**

