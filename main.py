import pymongo as pm
import datetime as dt

conexao = pm.MongoClient("mongodb://localhost:27017/")
db = conexao["banco"]

collection_gerente = db["gerentes"]
collection_cliente = db["clientes"]

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

def definir_segmento(renda):
    if renda <= 6999.99:
        return "Varejo"
    elif 7000 <= renda <= 29999:
        return "Exclusive"
    elif 30000 <= renda <= 99999:
        return "Premium"
    else:
        return "Classe A"

def pegarGerente(estado: str, renda: int) -> dict | None:

    segmento = definir_segmento(renda)
    gerentes = list(collection_gerente.find(
        {"$or":[{"agencia":estado},
                {"agencia":"Geral"}],
        "segmento": segmento,
        }))

    #Pega o gerente com menos clientes cadastrados
    gerentes.sort(key=lambda g: len(g["clientes"]))


    return gerentes[0]


def inserirCliente(nome: str, cpf: str, renda: float, estado:str, nascimento:dt.datetime) -> dict | None:
    segmento = definir_segmento(renda)
    gerente = pegarGerente(estado, renda)

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
        {"id": gerente["id"]},
        {"$addToSet": {"clientes": cliente_inserido}}
    )
    return cliente_inserido



def relatorioGerente(nome_gerente):
    def relatorioGerente(nome_gerente):
        gerente = collection_gerente.find_one({"nome": nome_gerente})
        if not gerente:
            return "Gerente não encontrado."

        for cliente_id in gerente["clientes"]:
            cliente = collection_cliente.find_one({"_id": cliente_id})
            print(
                f"{cliente['nome']} - CPF: {cliente['cpf']} - Estado: {cliente['estado']} - Renda: R$ {cliente['renda']:.2f}")

def relatorioSegmento():
    segmentos = collection_gerente.distinct("segmento")
    for i in segmentos:
        print(f"Segmento: {i}")
        for cliente in collection_cliente.find({"segmento": i}):
            print(
                f"{cliente['nome']} - CPF: {cliente['cpf']} - Estado: {cliente['estado']} - Renda: R$ {cliente['renda']:.2f} - Gerente: {cliente['gerente']}")
