# Copyright 2020 gRPC authors.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import asyncio
import logging
import grpc
from generated import account_pb2
from generated import account_pb2_grpc
from common.utils import generateRandomId
from .db import AccountDB

accountDB = AccountDB()

class Account(account_pb2_grpc.AccountServicer):
    async def GetAccountById(self, request: account_pb2.AccountRequestById, context: grpc.aio.ServicerContext) -> account_pb2.AccountResponse:
        account = accountDB.getAccountById(request.userId)
        if account is False:
            context.set_code(grpc.StatusCode.NOT_FOUND)
            context.set_details("Account not found or error occured.")
            return account_pb2.AccountResponse()
        return account_pb2.AccountResponse(
            userId=str(account.id),
            firstname=account.first_name,
            lastname=account.last_name,
            country_id=int(account.country_id),
            address=account.address,
            email=account.email,
            password=account.password,
            user_type_id=int(account.user_type_id)
        )

    async def GetAccountByEmail(self, request: account_pb2.AccountRequestByEmail, context: grpc.aio.ServicerContext) -> account_pb2.AccountResponse:
        account = accountDB.getAccountByEmail(request.email)
        if account is False:
            context.set_code(grpc.StatusCode.NOT_FOUND)
            context.set_details("Account not found or error occured.")
            return account_pb2.AccountResponse()
        return account_pb2.AccountResponse(
            userId=str(account.id),
            firstname=account.first_name,
            lastname=account.last_name,
            country_id=int(account.country_id),
            address=account.address,
            email=account.email,
            password=account.password,
            user_type_id=int(account.user_type_id)
        )
    async def CreateAccount(self, request: account_pb2.CreateAccountRequest, context: grpc.aio.ServicerContext) -> account_pb2.AccountResponse:
        # Check if the email already exists
        existing_account = accountDB.getAccountByEmail(request.email)
        if existing_account:
            context.set_code(grpc.StatusCode.ALREADY_EXISTS)
            context.set_details("Email is already in use.")
        return account_pb2.AccountResponse()
        newUserId = generateRandomId()  # Generate a new user ID
        # Insert the account data into the database
        account = accountDB.createAccount(
            (
                newUserId,               # accountId
                request.firstname,        # firstName
                request.lastname,         # lastName
                request.email,            # email
                request.password,         # password
                request.country_id,          # country_id
                request.address,          # address
                request.user_type_id              # user_type_id
            )
        )
        if account is False:
            context.set_code(grpc.StatusCode.INTERNAL)
            context.set_details("Account creation failed. Please try another username.")
            return account_pb2.AccountResponse()
        
        # Return the created account ID
        return account_pb2.AccountResponse(userId=newUserId)


    async def UpdateAccount(self, request: account_pb2.UpdateAccountRequest, context: grpc.aio.ServicerContext) -> account_pb2.AccountResponse:
        updated = accountDB.updateAccount(
            request.userId,
            {
                "firstname": request.firstname,
                "lastname": request.lastname,
                "country_id": request.country_id,
                "address": request.address,
                "password": request.password,
            }
        )
        if not updated:
            context.set_code(grpc.StatusCode.NOT_FOUND)
            context.set_details("Account not found for update or error occurred.")
            return account_pb2.AccountResponse()
        return account_pb2.AccountResponse(userId=request.userId)


    async def DeleteAccount(self, request: account_pb2.AccountRequestById, context: grpc.aio.ServicerContext) -> account_pb2.AccountResponse:
        deleted = accountDB.deleteAccount(request.userId)
        if not deleted:
            context.set_code(grpc.StatusCode.NOT_FOUND)
            context.set_details("Account not found for deletion or error occured.")
        return account_pb2.AccountResponse()

async def serve() -> None:
    server = grpc.aio.server()
    account_pb2_grpc.add_AccountServicer_to_server(Account(), server)
    listen_addr = "[::]:50051"
    server.add_insecure_port(listen_addr)
    logging.info("Starting server on %s", listen_addr)
    await server.start()
    await server.wait_for_termination()

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    asyncio.run(serve())
