from pydantic import BaseModel, Field, computed_field
from fastapi import FastAPI, Path, Query, HTTPException
from typing import Annotated,Optional 
import json

def load_data():
    with open('data.json', 'r') as f:
        data = json.load(f)
    return data

def save_data(data):
    with open('patients.json', 'w') as f:
        json.dump(data, f)

app = FastAPI()

class User(BaseModel):
    username: Annotated[str, Field(..., description="Unique username of the user")]
    password: Annotated[str, Field(..., description="User's hashed password")]
    current_money: Annotated[float, Field(0.0, ge=0, description="Current balance in the account")]
    collateral_value: Annotated[float, Field(0.0, ge=0, description="Collateral value for loans or credit")]




@app.get("/check_balance/{username}")
def check_balance(username: str):
    data = load_data()
    if username in data:
        return {"username" : username , "Balance" : data[username]["current_money"]}
    
    else:
        raise HTTPException(status_code = 404 , detail="no user found")
    
#------------------------------------------------------------------------------
    
@app.post("/withdraw/{username}/{amount}")
def withdraw(username: str, amount: int):
    data = load_data()
    if username not in data:
        raise HTTPException(status_code=404 , detail="user not found")
    elif amount > data[username]["current_money"]:
        raise HTTPException(status_code=404 , detail="not sufficient balance")
    
    balance = data[username]["current_money"]
    balance = balance - amount
    data[username]["current_money"] = balance
    save_data(data)
    return {"Remaining Balance" : data[username]["current_money"]}

@app.post("/create_account")
def create(user: User):
    data = load_data()
    if user.username in data:
        raise HTTPException(status_code="400", detail="user already exits")
    
    
    data[user.username] = user.model_dump(exclude=["username"])
    save_data(data)

    return {"message": "Account created successfully"}   





@app.get("/")
def about():
    return {"messgae" : "hello world"}