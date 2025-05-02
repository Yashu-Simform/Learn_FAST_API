from fastapi import FastAPI, Body, Query, Response, status, Form, File, UploadFile, HTTPException, Path, Depends
from fastapi.responses import JSONResponse
from models import BankClient, BankClientUpdate
from typing import Annotated
import json
from query_params import Transaction
from models import UserBase, UserRegistration, UserRegistrationResponse
from fastapi.encoders import jsonable_encoder
from enum import Enum

bank_clients = []

app = FastAPI()

class AppTags(Enum):
    bank = "bank",
    client = "client"

@app.get('/')
def root():
    return {"message": "Hello!"}    

@app.get('/record/{record_num: int}', tags=[AppTags.bank])
def get_record(record_num: int) -> Response:
    print(bank_clients)
    data = get_bank_client_data()
    if record_num >= len(data):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Record Not Found!")
        # return JSONResponse(content={"data": 'Record Not Found!'}, status_code=status.HTTP_404_NOT_FOUND)
    return data[record_num]

@app.post('/create/client/', tags=[AppTags.bank])
def create_client(client: BankClient, account_type: Annotated[str, Body()]):
    bank_clients.append(client)
    print(bank_clients)
    print('Account_type: ',account_type)
    add_client_data(client)
    return client

@app.put('/update/client/{client_id}', tags=[AppTags.bank])
def update_client(client_id: Annotated[int, Path()], client_data: BankClientUpdate):
    print('APi called!')
    data = get_bank_client_data()
    print(data)
    if client_id >= len(data):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Record Not Found!")
    
    old_data = data[client_id]
    new_data = client_data.model_dump(exclude_unset=True)
    updated_data = old_data.model_copy(update=new_data)
    print(updated_data.model_dump())
    return JSONResponse(content={"data": "Data Updated Successfully!"}, status_code=status.HTTP_200_OK)
    # add_client_data(updated_data)


@app.get('/transaction', tags=[AppTags.bank])
def get_transaction(t: Annotated[Transaction, Query()]):
    return {'status': 200, 'data': t.model_dump()}

@app.post('/user/register/', tags=[AppTags.client])
def user_register(user_data: Annotated[UserRegistration, Body()]) -> UserRegistrationResponse:
    return user_data

@app.post(
    '/profile/img/upload', 
    tags=[AppTags.client],
    description="This field is for uplodaing the profile image by the users.",
    summary="Allows the user to upload the profile image.",
    response_description="File Uploaded"
    )
def upload_profile_img(profile_image: Annotated[bytes, File()]):
    with open('app_images/userimg.png', 'wb') as f:
        f.write(profile_image)
    return JSONResponse(content={"data": f"File {len(profile_image)} uploaded successfully!"}, status_code=status.HTTP_200_OK)


@app.post('/records/file/upload', tags=[AppTags.client])
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
        bank_clients_array = [BankClient(**json.loads(obj)) for obj in data["bank_clients"]]
        return bank_clients_array
    

from db_connections import DBConnection

db_inst = DBConnection()
db_inst.connect()