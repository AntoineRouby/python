#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Wed Dec 13 14:59:25 2017

@author: cortinamatthieu
"""

import bt


##récupération du SP500 pour comparer nos stratégies au marché##
data_spy = bt.get('spy', start='2012-03-01',end='2014-01-01')
s_spy = bt.Strategy('S&P 500 only', 
                       [bt.algos.RunMonthly(),
                       bt.algos.SelectThese(['spy']),
                       bt.algos.WeighEqually(),
                       bt.algos.Rebalance()])
b_spy = bt.Backtest(s_spy, data_spy)
result = bt.run(b_spy)
result.plot()
###############################################################
###############################################################

####on récup le taux sans risque###
riskfree =  bt.get('IEF', start='2012-03-01',end='2014-01-01')
riskfree_rate = float(riskfree.calc_cagr())



import quandl
####on importe les données####

equity_list= ['AAPL','IBM','NKE','GM','MCD']
wiki_equity_list = []
for ticker in equity_list:
    wiki_equity_list.append('WIKI/' + ticker)
datax = quandl.get(wiki_equity_list, start_date = '2012-03-01',end_date='2014-01-01', column_index = 4)
print datax.head()
print datax.tail()
datax.dropna(axis=1, how='all', inplace=True)
datax.dropna(axis=0, how='all', inplace=True)

####on regarde ce que donne notre stratégie equal_weight de base####

s_equal_weights = bt.Strategy('Equal weights', 
                       [bt.algos.RunMonthly(),
                       bt.algos.SelectAll(),
                       bt.algos.WeighEqually(),
                       bt.algos.Rebalance()])
    
b_equal_weights = bt.Backtest(s_equal_weights, datax)
result2 = bt.run(b_equal_weights,b_spy)
result2.plot()

result2.set_riskfree_rate(riskfree_rate)
result2.display()
### on ne bat pas le marché et on remarque que notre rentabilité globale suit
### la retabilité du marché. Cependant les chocs positifs et négatifs sont plus bénéfiques au 
### marché qu'à notre portefeuille de 5 titres 

