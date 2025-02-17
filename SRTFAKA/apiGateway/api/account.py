from fastapi import APIRouter, Depends, Form, HTTPException
from ..models import AccountCreation, AccountUpdate, AccountResponse
from ..auth import getCurrentUser
from google.protobuf.json_format import MessageToDict
from ..gRPCHandler import getAccountById, updateAccount, deleteAccount, createAccount
from ..utils import hashPassword

MINIMUM_WALLET_AMOUNT = 5.00

account = APIRouter()

@account.get("/accounts/")
async def get_account(currentUser: AccountResponse = Depends(getCurrentUser)):
    account = await getAccountById(currentUser.userId)
    return {"message": "Account retrieved", "data": MessageToDict(account)}

@account.post("/accounts/create") 
async def create_account(name: str = Form, username: str = Form, password: str = Form): 
    accountObj = AccountCreation(name=name, username=username, password=hashPassword(password)) 
    newAccount = await createAccount(accountObj) 
    if newAccount is None:
        raise HTTPException(status_code=500, detail="Error occured")
    return {"message": "Account created", "data": MessageToDict(newAccount)}

@account.put("/accounts/")
async def update_account(account: AccountUpdate, currentUser: AccountResponse = Depends(getCurrentUser)):
    if currentUser.password != account.password:
        account.password = hashPassword(account.password)
    updatedAccount = await updateAccount(currentUser.userId, account)
    if updatedAccount is None:
        raise HTTPException(status_code=500, detail="Error occured")
    return {"message": "Account updated", "data": MessageToDict(updatedAccount)}

@account.delete("/accounts/")
async def delete_account(currentUser: AccountResponse = Depends(getCurrentUser)):
    deletedAccount = await deleteAccount(currentUser.userId)
    if deletedAccount is None:
        raise HTTPException(status_code=500, detail="Error occured")
    return {"message": "Account deleted successfully"}