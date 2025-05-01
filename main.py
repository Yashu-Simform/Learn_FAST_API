from fastapi import FastAPI, Body, Query, Response, status, Form, File, UploadFile, HTTPException
from fastapi.responses import JSONResponse
from models import BankClient
from typing import Annotated
import json
from query_params import Transaction
from models import UserBase, UserRegistration, UserRegistrationResponse

bank_clients = []

app = FastAPI()

@app.get('/')
def root():
    return {"message": "Hello!"}    

@app.get('/record/{record_num: int}')
def get_record(record_num: int) -> Response:
    print(bank_clients)
    data = get_bank_client_data()
    if record_num >= len(data):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Record Not Found!")
        # return JSONResponse(content={"data": 'Record Not Found!'}, status_code=status.HTTP_404_NOT_FOUND)
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

@app.post('/user/register/')
def user_register(user_data: Annotated[UserRegistration, Body()]) -> UserRegistrationResponse:
    return user_data

@app.post('/profile/img/upload')
def upload_profile_img(profile_image: Annotated[bytes, File()]):
    with open('app_images/userimg.png', 'wb') as f:
        f.write(profile_image)
    return JSONResponse(content={"data": f"File {len(profile_image)} uploaded successfully!"}, status_code=status.HTTP_200_OK)


@app.post('/records/file/upload')
def upload_records_file(records_file: UploadFile):
    with open('app_images/records.json', 'wb') as f:
        f.write(records_file.file.read())
    return JSONResponse(content={"data": f"Flie {records_file.filename} uploaded successfully!"}, status_code=status.HTTP_200_OK)

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