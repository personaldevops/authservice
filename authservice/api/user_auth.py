from appservicecore.api_service import app
from fastapi import Response
from abstractions.mongo_abstractions.mongo_query_builder import MongoQueryBuilder
from abstractions.mongo_abstractions.operations import MongoColumn, MongoFilter, MongoFindFilter, MongoUpdateFilter
from abstractions.enums.mongo import MongoPredicates, MongoActions, MongoColumnSelection, MongoSortOrder
from pydantic import BaseModel



class UserSignUp(BaseModel):
    email: str
    password: str
    first_name: str
    last_name: str


class UserSignIn(BaseModel):
    email: str
    password: str


@app.get("/auth")
async def auth_main():
    return {"message":"Authservice running on port 7171"}
@app.post("/auth/account-signup")
async def signup_user(data: UserSignUp, response: Response):
    email = data.email
    password = data.password
    first_name = data.first_name
    last_name = data.last_name
    query_filter = MongoFilter(attribute='email', predicate=MongoPredicates.EqualTo, value=email)
    query = MongoFindFilter()
    query.add_filter(filter=query_filter)
    db_find = MongoQueryBuilder(schema='authorization', collection='signup_info', action=MongoActions.Find,
                                filters=query).execute_query()
    if len(db_find) > 0:
        response.status_code = 401
        return {'Message': 'User already registered'}
    db_entry = {"email": email, "password": password, "first_name": first_name, "last_name": last_name}
    MongoQueryBuilder(schema='authorization', collection='signup_info', action=MongoActions.Insert,
                      data=db_entry).execute_query()
    response.status_code = 200
    return {'Message': 'User successfully registered'}


@app.post("/auth/account-signin")
async def signin_user(data: UserSignIn, response: Response):
    email = data.email
    password = data.password
    query_filter = MongoFilter(attribute='email', predicate=MongoPredicates.EqualTo, value=email)
    query = MongoFindFilter()
    query.add_filter(filter=query_filter)
    db_find = MongoQueryBuilder(schema='authorization', collection='signup_info', action=MongoActions.Find,
                                filters=query).execute_query()
    if len(db_find) < 1:
        response.status_code = 402
        return {'Message': 'User does not exist'}
    if db_find[0]['password'] == password:
        response.status_code = 200
        return {'Message': db_find[0]}
    else:
        response.status_code = 403
        return {'Message': 'Wrong password or email entered.'}
