import json
from datetime import datetime

import numpy
import pandas
from dateutil.relativedelta import relativedelta
from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from fastapi_versioning import version
from pandas import read_csv, to_datetime, DataFrame
from prophet import Prophet
from sklearn.metrics import mean_absolute_error
from sklearn.metrics import mean_squared_error
from sklearn.metrics import mean_absolute_percentage_error
from sklearn.metrics import mean_squared_log_error

from src.common.utils import templates

router = APIRouter(prefix='/forecasting')


@router.get('/test-api', summary="TEST 예측 테스트 API")
@version(1)
async def get_sample_csv():
    """
    예측 샘플 데이터
    return
    """
    df = read_csv('https://raw.githubusercontent.com/jbrownlee/Datasets/master/monthly-car-sales.csv', header=0)
    return {'values': df.values}


@router.get('/view/car-sales', response_class=HTMLResponse, summary="예측 데이터 시각화")
@version(1)
async def get_view_car_sales(request: Request):
    """
    monthly-car-sales.csv 데이터 시각화
    """
    df = read_csv('https://raw.githubusercontent.com/jbrownlee/Datasets/master/monthly-car-sales.csv', header=0)
    df.columns = ['ds', 'y']
    df['ds'] = to_datetime(df['ds'])

    # 모델 생성
    model = Prophet()

    # 모델 학습
    model.fit(df)

    # 년월 데이터 셋 생성
    future = list()
    date = datetime.strptime("1968-01", '%Y-%m')

    for i in range(1, 24):
        future.append([date])
        date = date + relativedelta(months=1)
    future = DataFrame(future)
    future.columns = ['ds']
    future['ds'] = to_datetime(future['ds'])

    # 예측
    forecast = model.predict(future)

    # 절대 오차 평균 계산(MAE)
    # 12월의 기대값과 예측값 사이의 MAE 계산
    y_true = df['y'][-12:].values  # 1968-01 ~ 1968-12 실제값
    y_pred = forecast['yhat'][-12:].values  # 1969-01 ~ 1969-12 예측값
    mae = mean_absolute_error(y_true, y_pred)
    mse = mean_squared_error(y_true, y_pred)
    rmse = numpy.sqrt(mse)
    msle = mean_squared_log_error(y_true, y_pred)
    mape = mean_absolute_percentage_error(y_true, y_pred)
    mpe = MPE(y_true, y_pred)

    # ndf = pandas.concat([df, forecast[['ds', 'y', 'yhat', 'yhat_lower', 'yhat_upper']]])
    ndf = pandas.merge(df, forecast[['ds', 'yhat', 'yhat_lower', 'yhat_upper']], how='outer', on='ds')
    ndf.fillna(0, inplace=True)  # NaN 값 채우기

    # 날짜 형변환(년-월)
    ndf['str_ds'] = ndf['ds'].dt.strftime('%Y-%m')

    result = {
        'request': request,
        'label': ndf['str_ds'].values.tolist(),
        'y': ndf['y'].values.tolist(),
        'yhat': ndf['yhat'].values.tolist(),
        'yhat_lower': ndf['yhat_lower'].values.tolist(),
        'yhat_upper': ndf['yhat_upper'].values.tolist(),
        'mae': mae,
        'mse': mse,
        'rmse': rmse,
        'msle': msle,
        'mape': mape,
        'mpe': mpe,
        'data': ndf[['str_ds', 'y', 'yhat', 'yhat_lower', 'yhat_upper']].values.tolist()
    }

    return templates().TemplateResponse("/forecasting/car-sales.html", result)


def MPE(y_test, y_pred):
    return numpy.mean((y_test - y_pred) / y_test) * 100

