# fastapi
from fastapi import APIRouter

# utils
from datetime import date
import json
import httpx

# models/schema
from schemas import ConversionResult

# currency list, conversion, historical data retrieval are supported by FIXER.io 
# Its several sets of API endpoints are used to get currency list, convert any amount from one currency 
# to another alongside with the historical data.

# 'fixer.io' related variable to reach their API endpoints
API_KEY = "af28058d25e64951e7069abe2e910df3"
BASE_URL = "http://data.fixer.io/api/" 
CURRENCY_LIST_PATH = "latest?access_key=" 
CURRENCY_CONVERTER_PATH ="convert?access_key="


# router instance to hook up 3 endponints 
# and attaching 'prefix' and 'tags' for the endpoints
router = APIRouter(
    prefix="/api/v1/currency",
    tags=["Currency Coversion Endpoints"],
)

# 3 APIs end points
@router.get('/')
async def supported_currencies_list():
    """
    Returns real-time exchange 'rates' data for all available or a specific set of currencies.
    From 'rates' data, supported currencies can be extracted.
    """

    # preparing url to reach fixer.io endpoint to get available currency list they support
    currency_list_fetch_url = BASE_URL + CURRENCY_LIST_PATH + API_KEY    

    async with httpx.AsyncClient() as client:

        resp = await client.get(currency_list_fetch_url)
        response_dict = resp.json()

        # only interested in 'rates' that holds up all the currency list we need
        currency_list = response_dict["rates"]
        
        return {
            'supported_currency_list': currency_list
        }

@router.get('/convert')
async def convert_currency(from_currency: str, to_currency: str, amount: float):
    """
    In order to convert currencies, we have to use FIXER.io's API's convert endpoint, append the 'from' and 'to' parameters 
    and set them to your preferred 'amount' that is need to be converted.
    """

    
    # preparing url to reach fixer.io's conversion endpoint
    currency_converter_url = BASE_URL + CURRENCY_CONVERTER_PATH + API_KEY

    if from_currency and to_currency and amount:
        # before reaching 'fixer.io' conversion endpoint, appending from,to and amount
        currency_converter_url += f'&from={from_currency}&to={to_currency}&amount={amount}'


    async with httpx.AsyncClient() as client:

        resp = await client.get(currency_converter_url)
        response_dict = resp.json()
        
        result = response_dict["success"]

        if not result:
            return response_dict
        
        # 'response_dict' has several nested objects (e.g. query, info both have nested objects)
        query_items = response_dict["query"]
        info_items = response_dict["info"]

        # storing the values in a pydantic model(i.e. ConversionResult)        
        conversion_result = ConversionResult(
            from_currency= query_items['from'], 
            to_currency= query_items['to'],
            query_amount= query_items['amount'],
            timestamp= info_items['timestamp'],
            rate= info_items['rate'],
            coversion_rate = response_dict["result"]
        )

        return conversion_result

@router.get('/get-historical-data')
async def get_historical_data(query_date: date, base_currency: str):
    """
    Historical rates are available for most currencies. We can query the Fixer API 
    for historical rates by appending a date (format YYYY-MM-DD) to the base URL with a 'base' currency.
    """
    if query_date and base_currency:
        # preparing url to reach fixer.io endpoint to get hostorical-data for a base currency
        historical_data_url = BASE_URL + str(query_date) + '?access_key=' + API_KEY
        historical_data_url += f'&base={base_currency}'

    async with httpx.AsyncClient() as client:
        resp = await client.get(historical_data_url)
        response_dict = resp.json()
        return response_dict