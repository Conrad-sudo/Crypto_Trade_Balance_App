from tkinter import *
from pandastable import Table
import main

#Create a dispatcher with function objects in them
dispatcher={'coinbase': main.get_coinbase, 'kraken':main.get_kraken, 'ftx':main.get_ftx, 'bitfinex':main.get_bitfinex, 'totals':main.get_total }
window_dispatcher={}
table_dispatcher={}


def get_main():
    df=main.get_ftx()['df']['main']
    acc_window=Tk()
    acc_window.title('FTX Main Account')
    frame = Frame(acc_window)
    frame.grid(row=0, column=0)
    # create a table
    table = Table(frame, dataframe=df, height=40)
    table.show()


def get_btc():
    df=main.get_ftx()['df']['btc']
    acc_window=Tk()
    acc_window.title('FTX BTC Account')
    frame = Frame(acc_window)
    frame.grid(row=0, column=0)
    # create a table
    table = Table(frame, dataframe=df, height=40)
    table.show()


def get_eth():
    df=main.get_ftx()['df']['eth']
    acc_window=Tk()
    acc_window.title('FTX ETH Account')
    frame = Frame(acc_window)
    frame.grid(row=0, column=0)
    # create a table
    table = Table(frame, dataframe=df, height=40)
    table.show()


def get_sol():
    df=main.get_ftx()['df']['sol']
    acc_window=Tk()
    acc_window.title('FTX SOL Account')
    frame = Frame(acc_window)
    frame.grid(row=0, column=0)
    # create a table
    table = Table(frame, dataframe=df, height=40)
    table.show()


def get_tether():
    df=main.get_ftx()['df']['tether']
    acc_window=Tk()
    acc_window.title('FTX Tether Account')
    frame = Frame(acc_window)
    frame.grid(row=0, column=0)
    # create a table
    table = Table(frame, dataframe=df, height=40)
    table.show()


def get_yedek():
    df=main.get_ftx()['df']['yedek']
    acc_window=Tk()
    acc_window.title('FTX Yedek Account')
    frame = Frame(acc_window)
    frame.grid(row=0, column=0)
    # create a table
    table = Table(frame, dataframe=df, height=40)
    table.show()



def ftx_handler():
    main_button = Button(window_dispatcher['ftx'], text='Get Main', width=13, height=2, bg='green',font=('Arial', 10, 'bold'), command=get_main).grid(row=0, column=1)
    btc_button = Button(window_dispatcher['ftx'], text='Get BTC', width=13, height=2, bg='green',font=('Arial', 10, 'bold'), command=get_btc).grid(row=0, column=2)
    eth_button = Button(window_dispatcher['ftx'], text='Get ETH', width=13, height=2, bg='green',font=('Arial', 10, 'bold'),command=get_eth).grid(row=1, column=1)
    sol_button = Button(window_dispatcher['ftx'], text='Get SOL', width=13, height=2, bg='green',font=('Arial', 10, 'bold'), command=get_sol).grid(row=1, column=2)
    tether_button = Button(window_dispatcher['ftx'], text='Get Tether', width=13, height=2, bg='green',font=('Arial', 10, 'bold'),command=get_tether).grid(row=2, column=1)
    yedek_button = Button(window_dispatcher['ftx'], text='Get Yedek', width=13, height=2, bg='green',font=('Arial', 10, 'bold'),command=get_yedek).grid(row=2, column=2)
    orders_button = Button(window_dispatcher['ftx'], text='Get Filled Orders Excel', width=27, height=2, bg='blue',font=('Arial', 10, 'bold'),command=main.get_filled_orders_excel).grid(row=3, column=0)



def update():

    aralik= delay*60000
    for account in table_dispatcher:

        if account=='ftx':
            table_dispatcher[account].model.df = dispatcher[account]()['df']['totals']

        else:
            table_dispatcher[account].model.df=dispatcher[account]()['df']

        table_dispatcher[account].redraw()

    print('Tables updated')
    root.after(aralik,update)



def get_account():

    message_label.configure(text='')
    choices=[]

    for account in accounts:
        if account.get() != '':
            choices.append(account.get() )

    #Create a new window
    if len(choices) !=0:
        #Create the table for each account
        for choice in choices:
            choice_acc_window = Tk()
            #Update the window dispatcher
            window_dispatcher.update({choice:choice_acc_window})

            if choice in dispatcher:
                if choice=='ftx':
                    df = dispatcher[choice]()['df']['totals']
                    ftx_handler()
                else:
                    # Call the fuction in the dispatcher
                    df = dispatcher[choice]()['df']

                choice_acc_window.title(choice.upper())
                # create a frame for the table
                frame = Frame(choice_acc_window)
                frame.grid(row=0, column=0)
                # create a table
                table = Table(frame, dataframe=df, height=40, width= 750)
                table_dispatcher.update({choice:table})
                table.show()


    try:
        global delay
        delay = int(interval.get())
        if len(choices)!=0:
            message_label.configure(text=f'Tablolar her {delay} dakika güncellenecek')
            update()
        else:
            message_label.configure(text=f'Hesab seçin')
    except ValueError:
        pass






root= Tk()
root.geometry('900x300')
root.title('Coin Counter')

root.resizable(True,True)
root.grid_columnconfigure(index=0,weight=1)
root.grid_columnconfigure(index=1,weight=1)
root.grid_columnconfigure(index=2,weight=1)
root.grid_columnconfigure(index=3,weight=1)


root.grid_rowconfigure(index=0,weight=1)
root.grid_rowconfigure(index=1,weight=1)
root.grid_rowconfigure(index=2,weight=1)
root.grid_rowconfigure(index=3,weight=1)
root.grid_rowconfigure(index=4,weight=1)
root.grid_rowconfigure(index=5,weight=1)
root.grid_rowconfigure(index=6,weight=1)




kraken=StringVar()
coinbase=StringVar()
ftx=StringVar()
bitfinex=StringVar()
totals=StringVar()

accounts= [kraken,coinbase,ftx,bitfinex,totals]



title= Label(root, text='Account', font=('Arial',25,'italic'), fg='red', ).grid(row=1,column=0,sticky='w', pady=(40,0), padx=10)


ftx_check=Checkbutton(root,variable=ftx, onvalue='ftx', offvalue='', text='FTX', width=12,font=('Arial',13,'bold')).grid(row=2,column=0,padx=(0,0.5))
coinbase_check=Checkbutton(root,variable=coinbase, onvalue='coinbase', offvalue='', text='Coinbase', width=12,font=('Arial',13,'bold')).grid(row=2,column=1,padx=(0,0.5))
kraken_check=Checkbutton(root,variable=kraken, onvalue='kraken', offvalue='', text='Kraken', width=12,font=('Arial',13,'bold')).grid(row=2,column=2,padx=(0,0.5))
bitfinex_check=Checkbutton(root,variable=bitfinex, onvalue='bitfinex', offvalue='', text='Bitfinex', width=12,font=('Arial',13,'bold')).grid(row=2,column=3,padx=(0,0.5))
totals_check=Checkbutton(root,variable=totals, onvalue='totals', offvalue='', text='Totals', width=12,font=('Arial',13,'bold')).grid(row=2,column=4,padx=(0,0.5))


title= Label(root, text='Güncelleme aralık (istemli)', font=('Arial',15,'bold'), fg='red', ).grid(row=4,column=0,sticky='w', pady=(0,0), padx=2)
interval=Entry(root,width= 20)
interval.place(relx= .4, rely= .62, anchor= CENTER,)

message_label= Label(root, text='', font=('Arial',12,'bold'), fg='red', )
message_label.grid(row=5,column=0,sticky='w', pady=(0,0), padx=2)



button=Button(root, text='Get account', width=10 ,height=2, bg='green', font=('Arial',10,'bold'),command=get_account).grid(row=6,column=0)
button=Button(root, text='Export to Excel', width=13 ,height=2, bg='blue',font=('Arial',10,'bold'),command=main.get_excel).grid(row=6,column=1)







root.mainloop()