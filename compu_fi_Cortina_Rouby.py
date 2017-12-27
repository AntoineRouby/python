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

std = datax.to_returns().rolling(57).std()
inv_std=1/std
inv_std_weights=inv_std.div(inv_std.sum(axis=1),axis=0)

s_custom_weighting = bt.Strategy('Custom weighting', 
                       [bt.algos.RunMonthly(),
                       bt.algos.SelectAll(),
                       bt.algos.WeighTarget(inv_std_weights),
                       bt.algos.Rebalance()])

b_custom_weighting = bt.Backtest(s_custom_weighting, datax)
result3 = bt.run(b_custom_weighting, b_equal_weights, b_spy)
result3.plot()
result3.set_riskfree_rate(riskfree_rate)
result3.display()
###on ne bat pas non plus le marché en utilisant une stratégie d'allocation  
###qui suit l'inverse de l'écart type 
################################################################################
################################################################################

std_weights=std.div(std.sum(axis=1),axis=0)


our_strat = bt.Strategy('our_strategy', 
                       [bt.algos.RunMonthly(),
                       bt.algos.SelectAll(),
                       bt.algos.WeighTarget(std_weights),
                       bt.algos.Rebalance()])
b_newstrat = bt.Backtest(our_strat, datax)
result3 = bt.run(b_newstrat,b_spy)
result3.plot()
result3.set_riskfree_rate(riskfree_rate)
result3.display()

# En définissant les poids de chacun de nos actifs en fonction de l'écart type des rendements 
# flottants de chacune de nos 5 actions, on obtient un rendement de prés de 30%, lorsque le marché 
# obtient 39%. 
# On observe une forte baisse de notre portefeuille  aux alentours de fin 2012 - début 2013
# Le SP 500 fait lui aussi une baisse à cette époque là mais elle est nettement moins significative
# que par rapport à notre portefeuille. Le titre provoquant cette baisse doit être nettement moins 
# fortement pondérée dans l'indice SP 500 que dans notre portefeuille.

##### Testons notre stratégie sur la période du 1er janvier 2016 au 26 décembre 2017 #####

data_spy_test = bt.get('spy', start='2016-01-01',end='2017-01-01')
s_spy_test = bt.Strategy('S&P 500 only', 
                       [bt.algos.RunMonthly(),
                       bt.algos.SelectThese(['spy']),
                       bt.algos.WeighEqually(),
                       bt.algos.Rebalance()])
b_spy_test = bt.Backtest(s_spy, data_spy_test)

res=bt.run(b_spy_test)

equity_list_test= ['AAPL','IBM','NKE','GM','MCD']
wiki_equity_list_test = []
for ticker in equity_list_test:
    wiki_equity_list_test.append('WIKI/' + ticker)
data_test = quandl.get(wiki_equity_list_test, start_date = '2015-10-01',end_date='2017-01-01', column_index = 4)

std_test = data_test.to_returns().rolling(57).std()
std_weights_test=std_test.div(std_test.sum(axis=1),axis=0)

our_strat_test = bt.Strategy('our_strategy_test', 
                       [bt.algos.RunMonthly(),
                       bt.algos.SelectAll(),
                       bt.algos.WeighTarget(std_weights_test),
                       bt.algos.Rebalance()])
b_newstrat_test = bt.Backtest(our_strat_test, data_test)

result_test=bt.run(b_newstrat_test,b_spy_test)
result_test.plot()
result_test.set_riskfree_rate(riskfree_rate)
result_test.display()


# On oublie pas de décaller les dates de data_test 3 mois auparavant étant donné que notre stratégie se base 
# sur des poids pour chacun des actifs qui dépendent de l'écart type des rendements floattants sur 3 mois en arrière 
# de nos 5 actions. 
# On ne bat toujours pas le marché mais la stratégie est fonctionelle. Globalement, on remarque 
# que notre portefeuille suit grossièrement les évolutions du marché, ce qui est logique puisque les titres
# que nous avons sélectionné sont partie intégrantes de l'indice SP500. 
# Nous ne battons pas l'indice SP500 car ce dernier est beaucoup plus diversifié que notre portefeuille.
# On a même pu observer qu'une forte baisse de notre portefeuille n'entrainait qu'une baisse plus légère du SP 500.
# A l'intérieur de l'indice SP 500 si une des 5 actions que nous avons choisi chute, alors les autres actions 
# qui composent l'indice SP500 "absorberont" beaucoup mieux la chute que les 4 actions restantes de notre portefeuille
