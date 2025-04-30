from fastapi import FastAPI, Body, Query
from models import BankClient
from typing import Annotated
import json
from query_params import Transaction

bank_clients = []

app = FastAPI()

@app.get('/')
def root():
    return {"message": "Hello!"}    

@app.get('/record/{record_num}')
def get_record(record_num: int):
    print(bank_clients)
    print(bank_clients)
    data = get_bank_client_data()
    if record_num >= len(data):
        return {'status': 404, 'message': 'Record Not Found!'}
    return data[record_num]

@app.post('/create/client/')
def create_client(client: BankClient, account_type: Annotated[str, Body()]):
    bank_clients.append(client)
    print(bank_clients)
    print('Account_type: ',account_type)
    add_client_data(client)
    return client


@app.get('/transaction')
def get_transaction(t: Annotated[Transaction, Query()]):
    return {'status': 200, 'data': t.model_dump()}


# File operations related to data storage
def add_client_data(client: BankClient, file_path = './bank_clients.json'):
    with open(file_path, 'r+') as f:
        data = client.model_dump_json()

        loaded_data = json.load(f)

        loaded_data['bank_clients'].append(data)

        f.seek(0)
        json.dump(loaded_data, f, indent=4)

def get_bank_client_data(file_path = './bank_clients.json') -> list[BankClient]:
    with open(file_path, 'r') as f:
        # data = f.read()
        data = json.load(f)
        print(data)
        return data['bank_clients']