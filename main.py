'''' Collection of functions to retrieve balance informaiton from various exchanges'''

import pandas as pd
import ccxt as cx





def counter(account_book,totals_book):
    for pair in account_book:
        if pair in totals_book:
            totals_book[pair] += account_book[pair]
        elif pair not in totals_book:
            totals_book.update({pair: account_book[pair]})

    return totals_book


#Return a dictionary in a dataframe format
def get_dataframe(book):

    for pair in book:
        book[pair]=[book[pair]]

    return book



# get balances of Coinbase wallets
def get_coinbase():

    coinbase_book={}
    key = '<Your_key>'
    secret = '<Your_secret>'
    passphrase = '<Your_passphrase>'

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
    api_key = '<Your_key>'
    api_sec = '<Your_secret>'

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





# get balances of FTX wallets 
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
    api_key = 'Your_key'
    api_sec = '<Your_secret>'

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

    api_key='Your_key'
    api_sec='Your_secret'
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
   



    with pd.ExcelWriter('Account_Balances.xlsx') as writer:
        kraken_df.to_excel(writer,sheet_name='Kraken',index=False)
        coinbase_df.to_excel(writer,sheet_name='Coinbase',index=False)
        bitfinex_df.to_excel(writer,sheet_name='Bitfinex',index=False)
        ftx_main.to_excel(writer,sheet_name='FTX Main',index=False)
        ftx_totals.to_excel(writer,sheet_name='FTX Total',index=False)
        totals_df.to_excel(writer,sheet_name='Total Accounts',index=False)




