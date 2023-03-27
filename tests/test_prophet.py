import pandas
from prophet import Prophet
from pandas import read_csv
from pandas import to_datetime
from pandas import DataFrame
from matplotlib import pyplot
from sklearn.metrics import mean_absolute_error
from sklearn.metrics import accuracy_score

# Monthly Car Sales Dataset(CSV)
CSV_URL = 'https://raw.githubusercontent.com/jbrownlee/Datasets/master/monthly-car-sales.csv'


def test_time_series_plot():
    """
    데이터 시각화
    :return:
    """
    df = read_csv(CSV_URL, header=0)
    df.plot()
    pyplot.show()


def print_predict_columns():
    """

    :return:
    """
    print(Prophet().predict().columns)


def test_prophet_forecasting(year: str):
    """
    :param: year
    :return:
    """
    df = read_csv(CSV_URL, header=0)

    # 컬럼명 변경
    df.columns = ['ds', 'y']

    # 데이터 타입 변경
    df['ds'] = to_datetime(df['ds'])

    # 모델 생성
    model = Prophet()

    # 모델 학습
    model.fit(df)

    future = list()
    # 년월 데이터셋 생성
    for i in range(1, 13):
        date = f'{year}-%02d' % i
        future.append([date])
    future = DataFrame(future)
    future.columns = ['ds']
    future['ds'] = to_datetime(future['ds'])

    # 예측
    forecast = model.predict(future)
    print(forecast.columns.values)

    # predict()
    # yhat : 예측
    # yhat_lower, yhat_upper : 불확실성 구간
    print(forecast[['ds', 'yhat', 'yhat_lower', 'yhat_upper']].head())
    model.plot(forecast)
    pyplot.show()


def test_prophet_manual_forecasting():
    """
    :param: year
    :return:
    """
    df = read_csv(CSV_URL, header=0)

    # 컬럼명 변경
    df.columns = ['ds', 'y']

    # 데이터 타입 변경
    df['ds'] = to_datetime(df['ds'])

    # 테스트 데이터 세트 생성, 지난 12개월 제거
    train = df.drop(df.index[-12:])
    print(train.tail())

    # 모델 생성
    model = Prophet()

    # 모델 학습
    model.fit(train)

    future = list()
    # 년월 데이터 셋 생성
    for i in range(1, 13):
        date = '1968-%02d' % i
        future.append([date])
    future = DataFrame(future)
    future.columns = ['ds']
    future['ds'] = to_datetime(future['ds'])

    # 예측
    forecast = model.predict(future)

    # 절대 오차 평균 계산(MAE)
    # 12월의 기대값과 예측값 사이의 MAE 계산
    y_true = df['y'][-12:].values  # 1968-01 ~ 1968-12 실제값
    y_pred = forecast['yhat'].values  # 예측값

    # mae print
    mae = mean_absolute_error(y_true, y_pred)
    print('MAE: %.3f' % mae)

    # 예상 플롯 vs 실제
    pyplot.plot(y_true, label='Actual')
    pyplot.plot(y_pred, label='Predicted')
    pyplot.legend()
    pyplot.show()


def test_prophet_manual_forecasting_2():
    """

    :return:
    """
    df = read_csv(CSV_URL, header=0)
    df.columns = ['ds', 'y']
    df['ds'] = to_datetime(df['ds'])
    df['yhat'] = 0
    df['yhat_lower'] = 0
    df['yhat_upper'] = 0

    print(df)

    # 모델 생성
    model = Prophet()

    # 모델 학습
    model.fit(df)

    # 년월 데이터 셋 생성
    future = list()
    for i in range(1, 13):
        date = f'1969-%02d' % i
        future.append([date])
    future = DataFrame(future)
    future.columns = ['ds']
    future['ds'] = to_datetime(future['ds'])

    forecast = model.predict(future)
    forecast['y'] = 0

    # 예측된 dataframe과 합치기
    ndf = pandas.concat([df, forecast[['ds', 'y', 'yhat', 'yhat_lower', 'yhat_upper']]])
    print(df)
    print(ndf)


if __name__ == '__main__':
    # 시계열 플롯 테스트
    # test_time_series_plot()

    # Make an In-Sample Forecast(표본 내 예측 만들기)
    # test_prophet_forecasting("1968")

    # Make an Out-Of-Sample Forecast(표본 외 예측 만들기)
    # test_prophet_forecasting("1969")

    # Manually Evaluate Forecast Model(수동 으로 예측 모델 평가)
    # test_prophet_manual_forecasting()
    test_prophet_manual_forecasting_2()

