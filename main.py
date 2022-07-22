'''' Collection of functions to retrieve balance informaiton from various exchanges'''

import pandas as pd
import ccxt as cx

# Help for deploying web app: https://devcenter.heroku.com/articles/procfile
#github.com
#https://stackoverflow.com/questions/71101031/telegram-bot-doesnt-run-on-heroku
#https://towardsdatascience.com/how-to-deploy-a-telegram-bot-using-heroku-for-free-9436f89575d2
#git_url= ' https://git.heroku.com/damp-oasis-98426.git'



def counter(account_book,totals_book):
    for pair in account_book:
        if pair in totals_book:
            totals_book[pair] += account_book[pair]
        elif pair not in totals_book:
            totals_book.update({pair: account_book[pair]})

    return totals_book



def get_dataframe(book):

    for pair in book:
        book[pair]=[book[pair]]

    return book



# get balances of Coinbase wallets
def get_coinbase():

    coinbase_book={}
    key = '092ee44fa1ac029b9cbc2cd48b8fc29a'
    secret = 'fixJ49IzJJsHNkpdwNx/qNpdI6rCyuCVXM8TGlE0frLyidoszSKtS8luUm1mqqknD2gxsPV7cwbRm9N14uPqFQ=='
    passphrase = 'zz0uurpv3v'

    coinbase = cx.coinbasepro({
        "apiKey": key,
        "secret": secret,
        "password": passphrase,
        "enableRateLimit": True
    })


    wallets=coinbase.fetch_balance()['info']

    for wallet in wallets:
        if float(wallet['balance']) > 0.1:
            coinbase_book.update({wallet['currency']:float(wallet['balance'])})

    coinbase_df= pd.DataFrame(get_dataframe(coinbase_book))


    return {'df':coinbase_df, 'book':coinbase_book}




def get_ftx_accounts(subaccount):
    api_key = '4Bp2e4xpNNJV63V2uWM9rUNvu4Qf-eRCWFJfUWht'
    api_sec = '8F5aMKZkgB8Nr7pH_ED8Hqa8VDRUNl39yNg9IVHY'

    if subaccount != 'main':
        # fetch the subaccount
        ftx_subaccount = cx.ftx({
            'apiKey': api_key,
            'secret': api_sec,
            'enableRateLimit': True,
            'headers': {'FTX-SUBACCOUNT': subaccount},  # uncomment line if using subaccount
        })

    elif subaccount == 'main':
        # fetch the subaccount
        ftx_subaccount = cx.ftx({
            'apiKey': api_key,
            'secret': api_sec,
            'enableRateLimit': True,
            # 'headers': {'FTX-SUBACCOUNT': subaccount},  # uncomment line if using subaccount
        })

    # get the baances of all coins in the account
    balances = ftx_subaccount.fetch_balance()

    return balances['info']['result']





# get balances of FTX wallets WORKING
def get_ftx():

    #Declare books for all accounts
    main_book = {}
    btc_book = {}
    eth_book = {}
    sol_book = {}
    tether_book = {}
    yedek_book = {}
    #Total book
    totals_book = {}


    # Seperate the accounts
    main_account = get_ftx_accounts('main')
    btc_account = get_ftx_accounts('BTC')
    eth_account = get_ftx_accounts('ETH')
    sol_account = get_ftx_accounts('SOL')
    tether_account = get_ftx_accounts('Tether')
    yedek_account = get_ftx_accounts('Yedek')


    #Seperate the accounts into their respective bboks
    for wallet in main_account:
        if wallet['total'] != 0:
            main_book.update({wallet['coin']: wallet['total']})

    for wallet in btc_account:
        if wallet['total'] != 0:
            btc_book.update({wallet['coin']: wallet['total']})

    for wallet in eth_account:
        if wallet['total'] != 0:
            eth_book.update({wallet['coin']: wallet['total']})

    for wallet in sol_account:
        if wallet['total'] != 0:
            sol_book.update({wallet['coin']: wallet['total']})

    for wallet in tether_account:
        if wallet['total'] != 0:
            tether_book.update({wallet['coin']: wallet['total']})

    for wallet in yedek_account:
        if wallet['total'] != 0:
            yedek_book.update({wallet['coin']: wallet['total']})

    #Add the totals
    totals_book = counter(account_book=main_book, totals_book=totals_book)
    totals_book = counter(account_book=btc_book, totals_book=totals_book)
    totals_book = counter(account_book=eth_book, totals_book=totals_book)
    totals_book = counter(account_book=sol_book, totals_book=totals_book)
    totals_book = counter(account_book=tether_book, totals_book=totals_book)
    totals_book = counter(account_book=yedek_book, totals_book=totals_book)

    #Make dataframes of all the books
    main_df=pd.DataFrame(get_dataframe(main_book))
    btc_df=pd.DataFrame(get_dataframe(btc_book))
    eth_df=pd.DataFrame(get_dataframe(eth_book))
    sol_df=pd.DataFrame(get_dataframe(sol_book))
    tether_df=pd.DataFrame(get_dataframe(tether_book))
    yedek_df=pd.DataFrame(get_dataframe(yedek_book))
    totals_df=pd.DataFrame(get_dataframe(totals_book))

    ftx_df={'main':main_df,'btc':btc_df, 'eth':eth_df,'sol':sol_df,'tether':tether_df,'yedek':yedek_df, 'totals':totals_df}

    ftx_book={'main':main_book,'btc':btc_book, 'eth':eth_book,'sol':sol_book,'tether':tether_book,'yedek':yedek_book, 'totals':totals_book}

    return {'book':ftx_book,'df':ftx_df}




# get balances for Kraken
def get_kraken():
    kraken_book={}
    api_key = 'VmzxajcbR3OM/OCbqgHov2ZaYanw9JZO0GT3Lg/9ij3fvfGLT00a4bqk'
    api_sec = 'eLHOhfhfGk2C3wKJEskNNgNP/9G09xRmHiAMh126GLMoLrWfV8ZGapQY8eKAsDzxZUZ1h07oOw9DIqWAi9Bhyg=='

    kraken = cx.kraken({
        'apiKey': api_key,
        'secret': api_sec,
        'verbose': False,  # switch it to False if you don't want the HTTP log
    })

    wallets = kraken.fetch_balance()['info']['result']

    for pair in wallets:
        if float(wallets[pair]) !=0:
            #Add Exceptions for XRP and XLM
            if 'XXRP'==pair or 'XXLM'==pair:
                mock_pair = pair.replace('X', '')
                mock_pair.strip()
                new_pair=f'X{mock_pair}'
                kraken_book.update({new_pair: float(wallets[pair])})
            else:
                kraken_book.update({pair:float(wallets[pair])})

    kraken_df=pd.DataFrame(get_dataframe(kraken_book))
    return {'df':kraken_df, 'book':kraken_book}




# get balances for bitfinex
def get_bitfinex():

    api_key='I7lJkJ9KCTcBrooN3BrwvIakcMQXeaaIxb7Qu7vSgIj'
    api_sec='VwrmePApuQlW9dCbiefGpK7RrWTJmjdsK9anPoIAVf9'
    bitfinex_book = {}

    bitfinex = cx.bitfinex({
        'apiKey': api_key,
        'secret': api_sec,
    })

    wallets = bitfinex.fetch_balance()['info']

    for wallet in wallets:
        if float(wallet['amount']) !=0:
            if wallet['currency']=='ust':
                bitfinex_book.update({wallet['currency'].upper().replace('T','DT'): float(wallet['amount'])})
            else:
                bitfinex_book.update({wallet['currency'].upper(): float(wallet['amount'])})

    bitfinex_df= pd.DataFrame(get_dataframe(bitfinex_book))
    return {'df':bitfinex_df, 'book':bitfinex_book}



#Calculates the total balance of each coin from all accounts
def get_total():

    kraken_book = get_kraken()['book']
    ftx_book = get_ftx()['book']
    coinbase_book = get_coinbase()['book']
    bitfinex_book = get_bitfinex()['book']
    totals_book={}

    #Get the totals of all accounts
    totals_book= counter(account_book=kraken_book,totals_book=totals_book)
    totals_book=counter(account_book=coinbase_book,totals_book=totals_book)
    totals_book=counter(account_book=bitfinex_book,totals_book=totals_book)
    totals_book=counter(account_book=ftx_book['totals'],totals_book=totals_book)

    # Create a dataframe
    totals_df=pd.DataFrame(get_dataframe(totals_book))

    return {'df':totals_df, 'book':totals_book}



def get_difference(current_total, prev_total):

    difference = {}

    for coin_1 in current_total:
        for coin_2 in prev_total:
            if coin_1 == coin_2:
                difference.update({coin_1: current_total[coin_1] - prev_total[coin_2]})






#Export all balance info to an excel file
def get_excel():
    kraken_df = get_kraken()['df']
    coinbase_df = get_coinbase()['df']
    bitfinex_df = get_bitfinex()['df']
    totals_df=get_total()['df']

    ftx_main = get_ftx()['df']['main']
    ftx_btc = get_ftx()['df']['btc']
    ftx_eth = get_ftx()['df']['eth']
    ftx_sol = get_ftx()['df']['sol']
    ftx_tether = get_ftx()['df']['tether']
    ftx_yedek = get_ftx()['df']['yedek']
    ftx_totals = get_ftx()['df']['totals']



    with pd.ExcelWriter('Account_Balances.xlsx') as writer:
        kraken_df.to_excel(writer,sheet_name='Kraken',index=False)
        coinbase_df.to_excel(writer,sheet_name='Coinbase',index=False)
        bitfinex_df.to_excel(writer,sheet_name='Bitfinex',index=False)
        ftx_main.to_excel(writer,sheet_name='FTX Main',index=False)
        ftx_btc.to_excel(writer,sheet_name='FTX BTC',index=False)
        ftx_eth.to_excel(writer,sheet_name='FTX ETH',index=False)
        ftx_sol.to_excel(writer,sheet_name='FTX SOL',index=False)
        ftx_tether.to_excel(writer,sheet_name='FTX Tether',index=False)
        ftx_yedek.to_excel(writer,sheet_name='FTX Yedek',index=False)
        ftx_totals.to_excel(writer,sheet_name='FTX Total',index=False)
        totals_df.to_excel(writer,sheet_name='Total Accounts',index=False)



# get filled orders for the ftx SOl subaccount
def get_ftx_sol_orders():

    sol_order_book={'Order ID':[],'Market':[],'Type':[], 'Side':[],'Price':[],'Size':[], 'AvgFillPrice':[], 'Status':[], 'Order date':[]}

    api_key= 'jM3JLiq6uYd-vBC2zr17Y5vdzibatg92lCKXPaGU'
    api_sec= '2aXxPQ38x0qacwMkTNJxChIBQmdGL-an3I4XUIfb'

    c = cx.ftx({
        'apiKey': api_key,
        'secret': api_sec,
        'enableRateLimit': True,
        'headers': {'FTX-SUBACCOUNT': 'SOL'}, # uncomment line if using subaccount
    })


    orders=c.fetch_orders()

    for order in orders:
        entry= order['info']
        if entry['status']=='closed':
            sol_order_book['Order ID'].append(entry['id'])
            sol_order_book['Market'].append(entry['market'])
            sol_order_book['Type'].append(entry['type'])
            sol_order_book['Side'].append(entry['side'])
            sol_order_book['Price'].append(entry['price'])
            sol_order_book['Size'].append(entry['size'])
            sol_order_book['AvgFillPrice'].append(entry['avgFillPrice'])
            sol_order_book['Status'].append(entry['status'])
            sol_order_book['Order date'].append(entry['createdAt'])


    sol_order_df=pd.DataFrame(sol_order_book)

    return sol_order_df





# get filled orders for the ftx BTC subaccount
def get_ftx_btc_orders():

    btc_order_book={'Order ID':[],'Market':[],'Type':[], 'Side':[],'Price':[],'Size':[], 'AvgFillPrice':[], 'Status':[],'Order date':[]}

    api_key= 'jM3JLiq6uYd-vBC2zr17Y5vdzibatg92lCKXPaGU'
    api_sec= '2aXxPQ38x0qacwMkTNJxChIBQmdGL-an3I4XUIfb'

    c = cx.ftx({
        'apiKey': api_key,
        'secret': api_sec,
        'enableRateLimit': True,
        'headers': {'FTX-SUBACCOUNT': 'BTC'}, # uncomment line if using subaccount
    })


    orders=c.fetch_orders()

    for order in orders:
        entry= order['info']
        if entry['status']=='closed':
            btc_order_book['Order ID'].append(entry['id'])
            btc_order_book['Market'].append(entry['market'])
            btc_order_book['Type'].append(entry['type'])
            btc_order_book['Side'].append(entry['side'])
            btc_order_book['Price'].append(entry['price'])
            btc_order_book['Size'].append(entry['size'])
            btc_order_book['AvgFillPrice'].append(entry['avgFillPrice'])
            btc_order_book['Status'].append(entry['status'])
            btc_order_book['Order date'].append(entry['createdAt'])


    btc_order_df=pd.DataFrame(btc_order_book)

    return btc_order_df




# get filled orders for the ftx ETH subaccount
def get_ftx_eth_orders():

    eth_order_book={'Order ID':[],'Market':[],'Type':[], 'Side':[],'Price':[],'Size':[], 'AvgFillPrice':[], 'Status':[],'Order date':[]}

    api_key= 'jM3JLiq6uYd-vBC2zr17Y5vdzibatg92lCKXPaGU'
    api_sec= '2aXxPQ38x0qacwMkTNJxChIBQmdGL-an3I4XUIfb'

    c = cx.ftx({
        'apiKey': api_key,
        'secret': api_sec,
        'enableRateLimit': True,
        'headers': {'FTX-SUBACCOUNT': 'ETH'}, # uncomment line if using subaccount
    })


    orders=c.fetch_orders()

    for order in orders:
        entry= order['info']
        if entry['status']=='closed':
            eth_order_book['Order ID'].append(entry['id'])
            eth_order_book['Market'].append(entry['market'])
            eth_order_book['Type'].append(entry['type'])
            eth_order_book['Side'].append(entry['side'])
            eth_order_book['Price'].append(entry['price'])
            eth_order_book['Size'].append(entry['size'])
            eth_order_book['AvgFillPrice'].append(entry['avgFillPrice'])
            eth_order_book['Status'].append(entry['status'])
            eth_order_book['Order date'].append(entry['createdAt'])


    eth_order_df=pd.DataFrame(eth_order_book)

    return eth_order_df









#Export all order info to an excel file
def get_filled_orders_excel():
    sol_orders_df=get_ftx_sol_orders()
    btc_orders_df=get_ftx_btc_orders()
    eth_orders_df=get_ftx_eth_orders()

    with pd.ExcelWriter('Filled_Orders.xlsx') as writer:
        btc_orders_df.to_excel(writer,sheet_name='BTC Orders',index=False)
        eth_orders_df.to_excel(writer,sheet_name='ETH Orders',index=False)
        sol_orders_df.to_excel(writer,sheet_name='SOL Orders',index=False)
