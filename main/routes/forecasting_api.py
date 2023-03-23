import json
from fastapi import APIRouter
from fastapi_versioning import version
from pandas import read_csv

router = APIRouter(prefix='/forecasting')


@router.get('/sample-csv', summary="예측 테스트 API")
@version(1)
async def get_sample_csv():
    """
    예측 테스트 API
    return
    """
    df = read_csv('https://raw.githubusercontent.com/jbrownlee/Datasets/master/monthly-car-sales.csv', header=0)
    return {'values': df.values}
