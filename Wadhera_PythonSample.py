
## Sidhant Wadhera
## Python Code Sample

# This sample reads in data from the City of Chicago that
# provides COVID-19 information by zip code and week. I
# clean and reshape the data in order to estimate and
# plot two time series forecasts for the next six weeks
# of cases. Code created for a project in Data and Programming
# for Public Policy II, taken in Autumn 2020. 

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import statsmodels.tsa.api as smt

def read_chicago_data(id, cols_to_keep):
    url = f'https://data.cityofchicago.org/resource/{id}.csv'
    df = pd.read_csv(url, usecols=cols_to_keep)
    return(df)

def log_column(var_name):
    covid_byZIP[f'log_{var_name}'] = np.log(covid_byZIP[f'{var_name}_weekly'] + 1)

def ts_maker(indexvar, frequency, var, df):
    '''
    This function takes dates and values from a dataframe and makes them into a single
    time series. This time series will be used for the analysis.
    '''
    start_date = df.loc[0, indexvar]
    end_date   = df.loc[len(df) - 1, indexvar]
    index      = pd.date_range(start=start_date,
                               end=end_date,
                               freq=frequency)
    data=list(df[var])
    temp=pd.Series(data, index)
    return(temp)

def ts_forecaster(tseries, fperiods):
    '''
    This function takes a time series, and the number of forecast periods,
    and returns the forecasted values for two different models:
        - Simple Exponential Smoothing
        - Holt Winters
    '''
    # Simple Exponential Smoothing
    ses          = smt.SimpleExpSmoothing(tseries).fit(optimized = True)
    print(ses.summary())
    ses_fcast    = ses.forecast(fperiods)
    # Holt Winters
    hw           = smt.Holt(tseries).fit(optimized = True)
    print(hw.summary())
    hw_fcast     = hw.forecast(fperiods)
    # Combine forecasts into a Pandas Data Frame
    data = {'simple_exp_smoothing': ses_fcast,
            'holt_winters' : hw_fcast}
    forecasts = pd.concat(data, axis = 1)
    return(forecasts)

def forecast_plotter(tseries, sname, fcasts, xlab, ylab, title, fname):
    '''
    This function takes a time series with the original data values, and
    plots it along with the simple exponential smoothing, holt-winters
    forecasts. It also saves the plot as a png.
    '''
    plt.figure(figsize = (10,5))
    plt.plot(tseries, 'k-', label = sname)
    plt.plot(fcasts['simple_exp_smoothing'], 'b-',
             label = 'Simple Exponential Smoothing')
    plt.plot(fcasts['holt_winters'], 'r-',
             label = 'Holt - Winters')
    plt.xlabel(xlab)
    plt.ylabel(ylab)
    plt.title(title)
    plt.legend(loc = 'best')
    plt.savefig(fname)

## Data Cleaning
covid_byZIP = read_chicago_data(id="yhhz-zm2v",
                                cols_to_keep=['zip_code', 'week_start', 'cases_weekly', 'case_rate_weekly',
                                              'tests_weekly', 'test_rate_weekly', 'percent_tested_positive_weekly',
                                              'deaths_weekly', 'death_rate_weekly'])

covid_byZIP['week_start'] = covid_byZIP['week_start'].str.slice(0,10)
covid_byZIP = covid_byZIP[covid_byZIP['zip_code'] != 'Unknown'].reset_index().drop(columns=['index'], axis=1)
covid_byZIP['zip_code'] = covid_byZIP['zip_code'].astype(float)

for str in ['cases', 'tests', 'deaths']:
    log_column(str)

covid_byZIP.rename(columns={'zip_code':'zipcode', 'cases_weekly':'cases',
                            'tests_weekly':'tests', 'deaths_weekly':'deaths'}, inplace=True)

covid_tot = covid_byZIP.groupby(by ='week_start').sum().reset_index()

weeklycases_ts  = ts_maker('week_start', 'W', 'cases', covid_tot)

## Time Series Forecasting
weeklycases_forecast  = ts_forecaster(weeklycases_ts, 6)

## Time Series Plotting
forecast_plotter(tseries=weeklycases_ts, sname='Weekly Cases',
                 fcasts=weeklycases_forecast, xlab='Time',
                 ylab='COVID-19 Cases', title='Forecasting COVID-19 Cases in Chicago',
                 fname='weekly_cases_forecast.png')
