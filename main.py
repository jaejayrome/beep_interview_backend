from fastapi import FastAPI
from country import json_string, total_search_results, get_all_currencies, get_specific_currency
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/countries")
async def get_countries(): 
    return json_string

@app.get("/countries/{search_params}")
async def get_countries(search_params: str):
    return total_search_results(query = search_params)


@app.get("/currencies")
async def get_currencies(): 
    return {'currencies': get_all_currencies()}

@app.get("/currencies/{search_params}")
async def get_specific_currencies(search_params: str): 
    return {'result': get_specific_currency(query = search_params)}
