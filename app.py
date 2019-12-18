from datetime import datetime, timedelta
from flask import Flask, render_template, request, flash, redirect, session, abort
from flask_bootstrap import Bootstrap
import requests
import json
import time
from alpha_vantage.timeseries import TimeSeries

app = Flask(__name__)
Bootstrap(app)

ethicalInvestingStocksArray = ['AAPL', 'MSFT', 'ADBE']
growthInvestingStocksArray = ['FIT', 'GPRO', 'NVDA']
indexInvestingStocksArray = ['FB', 'AMZN', 'HMC']
qualityInvestingStocksArray = ['JPM', 'WMT', 'BBY']
valueInvestingStocksArray = ['TSLA', 'TWTR', 'GOOG']

companyName= {'AAPL':'Apple Inc.', 'MSFT':'Microsoft Corporation', 'ADBE':'Adobe Inc', 'FIT':'Fitbit Inc', 'GPRO':'Go-GoPro Inc', 'NVDA':'NVIDIA Corporation', 'FB':'Facebook, Inc.', 'AMZN':'Amazon.com, Inc.', 'HMC':'Honda Motor Co Ltd', 'JPM':'JPMorgan Chase & Co.', 'WMT':'Walmart Inc', 'BBY':'Best Buy Co Inc', 'TSLA':'Tesla Inc', 'TWTR':'Twitter Inc', 'GOOG':'Alphabet Inc'}

@app.route('/getData', methods=['POST'])
def processRequest():
    # investmentAmount = request.form['investment_value']
    # investmentStrategies = request.form.getlist('strategy')
    investmentAmount = request.form['amount']
    investmentStrategies = request.form.getlist('strategies')
    amountInvestedPerStrategy = int(investmentAmount) / len(
        investmentStrategies)

    finalStockDistribution = {}
    overallPortfolio = []

    for strategy in investmentStrategies:
        if strategy == "Ethical Investing":
            StockDistribution, Portfolio = getInvestments(
                strategy, amountInvestedPerStrategy,
                ethicalInvestingStocksArray)
            finalStockDistribution['Ethical Investing'] = StockDistribution
            overallPortfolio.append(Portfolio)
            time.sleep(60)
        elif strategy == "Growth Investing":
            StockDistribution, Portfolio = getInvestments(
                strategy, amountInvestedPerStrategy,
                growthInvestingStocksArray)
            finalStockDistribution['Growth Investing'] = StockDistribution
            overallPortfolio.append(Portfolio)
            time.sleep(60)
        elif strategy == "Index Investing":
            StockDistribution, Portfolio = getInvestments(
                strategy, amountInvestedPerStrategy, indexInvestingStocksArray)
            finalStockDistribution['Index Investing'] = StockDistribution
            overallPortfolio.append(Portfolio)
            time.sleep(60)
        elif strategy == "Quality Investing":
            StockDistribution, Portfolio = getInvestments(
                strategy, amountInvestedPerStrategy,
                qualityInvestingStocksArray)
            finalStockDistribution['Quality Investing'] = StockDistribution
            overallPortfolio.append(Portfolio)
            time.sleep(60)
        elif strategy == "Value Investing":
            StockDistribution, Portfolio = getInvestments(
                strategy, amountInvestedPerStrategy, valueInvestingStocksArray)
            finalStockDistribution['Value Investing'] = StockDistribution
            overallPortfolio.append(Portfolio)
            # time.sleep(60)
        else:
            print("Invalid Strategy")
    finalStockDistribution['amountDistribution'] = [amountInvestedPerStrategy * 0.5, amountInvestedPerStrategy * 0.3, amountInvestedPerStrategy * 0.2 ]
    # print(finalStockDistribution)
    # print(overallPortfolio)

    s1Data = finalStockDistribution[investmentStrategies[0]]
    temp = {'strategyCount': len(investmentStrategies),
            'companyName1': s1Data[0][0],
            'companyName2': s1Data[1][0],
            'companyName3': s1Data[2][0],
            'companySymbol1': s1Data[0][1],
            'companySymbol2': s1Data[1][1],
            'companySymbol3': s1Data[2][1],
            'stockPrice1': s1Data[0][3],
            'stockPrice2': s1Data[1][3],
            'stockPrice3': s1Data[2][3],
            'dateCompany1': s1Data[0][2],
            'dateCompany2': s1Data[1][2],
            'dateCompany3': s1Data[2][2],
            'strategy1': investmentStrategies[0],
            'suggestionAmount1': finalStockDistribution['amountDistribution'][0],
            'suggestionAmount2': finalStockDistribution['amountDistribution'][1],
            'suggestionAmount3': finalStockDistribution['amountDistribution'][2]};

    graphData = {'c1d1d': overallPortfolio[0][0][1][0][0],
    'c1d2d': overallPortfolio[0][0][1][1][0],
    'c1d3d': overallPortfolio[0][0][1][2][0],
    'c1d4d': overallPortfolio[0][0][1][3][0],
    'c1d5d': overallPortfolio[0][0][1][4][0],
    'c1d1p': overallPortfolio[0][0][1][0][1],
    'c1d2p': overallPortfolio[0][0][1][1][1],
    'c1d3p': overallPortfolio[0][0][1][2][1],
    'c1d4p': overallPortfolio[0][0][1][3][1],
    'c1d5p': overallPortfolio[0][0][1][4][1],
    'c2d1d': overallPortfolio[0][1][1][0][0],
    'c2d2d': overallPortfolio[0][1][1][1][0],
    'c2d3d': overallPortfolio[0][1][1][2][0],
    'c2d4d': overallPortfolio[0][1][1][3][0],
    'c2d5d': overallPortfolio[0][1][1][4][0],
    'c2d1p': overallPortfolio[0][1][1][0][1],
    'c2d2p': overallPortfolio[0][1][1][1][1],
    'c2d3p': overallPortfolio[0][1][1][2][1],
    'c2d4p': overallPortfolio[0][1][1][3][1],
    'c2d5p': overallPortfolio[0][1][1][4][1],
    'c3d1d': overallPortfolio[0][2][1][0][0],
    'c3d2d': overallPortfolio[0][2][1][1][0],
    'c3d3d': overallPortfolio[0][2][1][2][0],
    'c3d4d': overallPortfolio[0][2][1][3][0],
    'c3d5d': overallPortfolio[0][2][1][4][0],
    'c3d1p': overallPortfolio[0][2][1][0][1],
    'c3d2p': overallPortfolio[0][2][1][1][1],
    'c3d3p': overallPortfolio[0][2][1][2][1],
    'c3d4p': overallPortfolio[0][2][1][3][1],
    'c3d5p': overallPortfolio[0][2][1][4][1]
    };
    graphTemp = json.dumps(graphData)
    newGraph = json.loads(graphTemp)
    if len(investmentStrategies) > 1:
        temp['strategy2'] = investmentStrategies[1]
        s2Data = finalStockDistribution[investmentStrategies[1]]
        temp['companyName4'] = s2Data[0][0]
        temp['companyName5'] = s2Data[1][0]
        temp['companyName6'] = s2Data[2][0]
        temp['companySymbol4'] = s2Data[0][1]
        temp['companySymbol5'] = s2Data[1][1]
        temp['companySymbol6'] = s2Data[2][1]
        temp['stockPrice4'] = s2Data[0][3]
        temp['stockPrice5'] = s2Data[1][3]
        temp['stockPrice6'] = s2Data[2][3]
        temp['dateCompany4'] = s2Data[0][2]
        temp['dateCompany5'] = s2Data[1][2]
        temp['dateCompany6'] = s2Data[2][2]
        temp = json.dumps(temp)
        newTemp = json.loads(temp)
        print(overallPortfolio)
        print(overallPortfolio[1])
        graphData2 = {'c4d1d': overallPortfolio[1][0][1][0][0],
                     'c4d2d': overallPortfolio[1][0][1][1][0],
                     'c4d3d': overallPortfolio[1][0][1][2][0],
                     'c4d4d': overallPortfolio[1][0][1][3][0],
                     'c4d5d': overallPortfolio[1][0][1][4][0],
                     'c4d1p': overallPortfolio[1][0][1][0][1],
                     'c4d2p': overallPortfolio[1][0][1][1][1],
                     'c4d3p': overallPortfolio[1][0][1][2][1],
                     'c4d4p': overallPortfolio[1][0][1][3][1],
                     'c4d5p': overallPortfolio[1][0][1][4][1],

                     'c5d1d': overallPortfolio[1][1][1][0][0],
                     'c5d2d': overallPortfolio[1][1][1][1][0],
                     'c5d3d': overallPortfolio[1][1][1][2][0],
                     'c5d4d': overallPortfolio[1][1][1][3][0],
                     'c5d5d': overallPortfolio[1][1][1][4][0],
                     'c5d1p': overallPortfolio[1][1][1][0][1],
                     'c5d2p': overallPortfolio[1][1][1][1][1],
                     'c5d3p': overallPortfolio[1][1][1][2][1],
                     'c5d4p': overallPortfolio[1][1][1][3][1],
                     'c5d5p': overallPortfolio[1][1][1][4][1],

                     'c6d1d': overallPortfolio[1][2][1][0][0],
                     'c6d2d': overallPortfolio[1][2][1][1][0],
                     'c6d3d': overallPortfolio[1][2][1][2][0],
                     'c6d4d': overallPortfolio[1][2][1][3][0],
                     'c6d5d': overallPortfolio[1][2][1][4][0],
                     'c6d1p': overallPortfolio[1][2][1][0][1],
                     'c6d2p': overallPortfolio[1][2][1][1][1],
                     'c6d3p': overallPortfolio[1][2][1][2][1],
                     'c6d4p': overallPortfolio[1][2][1][3][1],
                     'c6d5p': overallPortfolio[1][2][1][4][1]
                     };
        graphTemp2 = json.dumps(graphData2)
        newGraph2 = json.loads(graphTemp2)
        newTemp['newGraph'] = newGraph;
        newTemp['newGraph2'] = newGraph2;
        return render_template("resultTwo.html", **newTemp )

    temp = json.dumps(temp)
    newTemp = json.loads(temp)

    newTemp['newGraph'] = newGraph
    return render_template("resultOne.html", **newTemp)


def getInvestments(investmentStrategy, amount, stockSymbolList):
    stockDistribution = []
    stockPortfolio = []

    print(stockSymbolList)
    for stockSymbol in stockSymbolList:
        name = companyName[stockSymbol]
        try:
            ts = TimeSeries(key='UZS4X61DRGCV60CX')
            data, meta_data = ts.get_daily_adjusted(stockSymbol)

        except requests.exceptions.RequestException as e:
            print(e)
        portfolio = []
        if meta_data:
            i = 0
            for date in data:
                if i < 5:
                    strDate = date.replace('-', ',')
                    dList = strDate.split(',')
                    dList[1] = str(int(dList[1]) - 1)
                    strDate = ','.join(dList)
                    print(strDate)

                    portfolio.append(
                        [strDate, data[date]['5. adjusted close']])
                    if i == 0:
                        stockDistribution.append([name, stockSymbol, date, data[date]['5. adjusted close']])
                    i = i + 1
                else:
                    break
            stockPortfolio.append([name, portfolio])
        else:
            print("Invalid Symbol")
    return stockDistribution, stockPortfolio

@app.route("/")
def home():
    return render_template("mainHomePage.html", **locals())