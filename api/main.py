import json

import requests
from fastapi import APIRouter
from starlette.responses import JSONResponse

router = APIRouter()

headers = {
    'Content-Type': 'application/json',
    'Access-Control-Request-Headers': '*',
    'api-key': 'quzesCE7eY3nLKg6NRxlA66T2HVXTm45IZ9PseU54OTLXNMCUy86dTSI3LER4WxM'
}
payload = json.dumps({
    "collection": "Shop",
    "database": "ReviewX",
    "dataSource": "ReviewApi-Cluster"
})


@router.get("/merchants/")
async def get_merchants(merchant_name: str):
    url = "https://data.mongodb-api.com/app/data-bonin/endpoint/data/beta/action/find"
    new_payload = payload.update({"projection": {"_id": 1}})
    print(payload)
    response = requests.request("POST", url, headers=new_payload, data=payload)
    print(response.text)
    return JSONResponse(response.text)


@router.get("/merchants/{merchant_url/")
async def get_reviews(merchant_name: str):
    url = "https://data.mongodb-api.com/app/data-bonin/endpoint/data/beta/action/find"

    response = requests.request("POST", url, headers=headers, data=payload)
    print(response.text)
    return JSONResponse(response.text)
