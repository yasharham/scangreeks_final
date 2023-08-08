import datetime
import os
import shutil
import traceback
import pandas as pd

from API.Controller.V1.expense_calculation import expense_calculation
from Middleware.authenticate import decode_access_token
from Services.db import *
from Settings.api_responses import response
from API.Controller.V1.tab_margin_calculation import *

def tradesFO_upload(file):
    try:
        cursor = mydb.cursor()
        date = datetime.date.today().strftime("%d%m%y")
        path = '/home/arham001/Yash/ScanGreeks/Download/Tradefiles'

        with open(f"{(os.path.join(path, f'FO_{date}.csv'))}", "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        tradesFO = pd.read_csv(f"{(os.path.join(path, f'FO_{date}.csv'))}", index_col=0)

        for index, row in tradesFO.iterrows():
            # Modify the INSERT statement according to your table structure
            query1 = ''' select TradeID from tradesFO where TradeId = %s and TradeDate = %s'''
            value = (row['TradeId'], row['Date'])
            cursor.execute(query1, value)
            data = cursor.fetchone()
            if not data:
                print(row['TradeId'])
                insert_query = '''
                        INSERT INTO tradesFO 
                            (`Client_id`,`TradeId`, `TradeDate`, `Token`, `Instrument_Type`, `Symbol`, `Expiry`, `Strike`, `Option_Type`, 
                            `Units`, `Ltp`, `Tradeamount`, `AssetToken`, `Lotsize`, `Premium`, `TOC`, `TorM`)
                            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                                  '''

                values = (
                'A2021', row['TradeId'], row['Date'], row['Token'], row['Instrument_Type'], row['Symbol'], row['Expiry'],
                row['Strike'], row['Option_Type'], row['Units'], row['Ltp'], row['Tradeamount'], row['AssetToken'],
                row['Lotsize'], row['Premium'], row['TOC'], row['TorM'])
                cursor.execute(insert_query, values)
                mydb.commit()
            else:
                pass
        cursor.close()
        return {"filename": f"successfully upload {file.filename}"}
    except:
        print(traceback.print_exc())

def tradesEQ_upload(file):
    try:
        cursor = mydb.cursor()
        date = datetime.date.today().strftime("%d%m%y")
        path = '/home/arham001/Yash/ScanGreeks/Download/Tradefiles'

        with open(f"{(os.path.join(path, f'EQ_{date}.csv'))}", "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        tradesEQ = pd.read_csv(f"{(os.path.join(path, f'EQ_{date}.csv'))}", index_col=0)

        for index, row in tradesEQ.iterrows():
            query1 = ''' select TradeID from tradesEQ where TradeId = %s and TradeDate = %s'''
            value = (row['TradeId'], row['Date'])
            cursor.execute(query1, value)
            data = cursor.fetchone()
            if not data:
                print(data)
                insert_EQ_query = '''
                            INSERT INTO tradesEQ (`Client_id`, `TradeId`, `TradeDate`, `Token`, `Symbol`, `Units`, `Ltp`, `Tradeamount`, `TorM`, `BS`)
                            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s);
                                  '''
                values = (
                'A2021', row['TradeId'], row['Date'], row['Token'], row['Symbol'], row['Units'], row['Ltp'], row['Tradeamount'],
                row['TorM'], row['BS'])
                cursor.execute(insert_EQ_query, values)
                mydb.commit()
            else:
                pass
        cursor.close()
        return {"filename": f"successfully upload {file.filename}"}
    except:
        print(traceback.print_exc())


def get_tab(authToken):
    try:
        try:
            user = decode_access_token(authToken)
            client_id = user.username
        except:
            return response[401]
        print(client_id)
        cursor = mydb.cursor()
        date = datetime.date.today().strftime("%Y-%m-%d")
        # date ="2023-06-29"
        # client_id = "A2021"
        tabQuery = ''' select DISTINCT Symbol,Expiry from tradesFO where Expiry >= %s and Client_id = %s'''
        cursor.execute(tabQuery,[date,client_id])
        tabdata = cursor.fetchall()
        tabList = []
        for i in tabdata:
          date1 = datetime.datetime.strptime(i[1],"%Y-%m-%d")
          expirydate= date1.strftime("%d%b%Y").upper()
          tabList.append(i[0]+'_'+expirydate)
        response[200]['data'] = tabList
        return response[200]
    except:
        print(f"getTabData", traceback.print_exc())
        return response[500]


def getTabData(id,authToken):
    try:
        try:
            user = decode_access_token(authToken)
            client_id = user.username
        except:
            return response[401]
        cursor = mydb.cursor()
        data1 = id.split("_")
        symbol = data1[0]
        date_obj = datetime.datetime.strptime(data1[1], "%d%b%Y")
        expiry = date_obj.strftime("%Y-%m-%d")

        queryOption = '''
                    select 
                        Symbol,
                        Expiry,
                        Token,
                        SUM(Units) as Units,
                        SUM(Tradeamount) as Tradeamount,
                        SUM(Premium) as Premium,
                        AssetToken,
                        AVG(Ltp) as LTP,
                        Strike,
                        Option_Type,
                        case when SUM(Units) > 0 then (SUM(Tradeamount)/SUM(Units)) else 0 end as avg_price
                    from tradesFO where Client_id = %s  and Symbol = %s and Expiry = %s and Instrument_Type IN ('OPTSTK', 'OPTIDX')
                    group by Token, AssetToken, Option_Type, Strike;
                 '''
        queryFuture = '''
                       select 
                        Symbol,
                        Expiry,
                        Token,
                        SUM(Units) as Units,
                        SUM(Premium) as Premium,
                        case when SUM(Units) > 0 then (SUM(Tradeamount)/SUM(Units)) else 0 end as LTP
                    from tradesFO where Client_id = %s  and Symbol = %s and Expiry = %s and Instrument_Type IN ("FUTSTK", "FUTIDX")
                    group by Token  
                        '''

        queryEquity = '''
                   select 
                        Symbol,
                        Token,
                        SUM(Units) as Units,
                        SUM(Tradeamount) as Tradeamount,
                        case when SUM(Units) > 0 then (SUM(Tradeamount)/SUM(Units)) else 0 end as avg_price
                        from tradesEQ where Client_id = %s  and Symbol = %s
                        group by Token  
                                '''

        ############################## Option Data #############################

        cursor.execute(queryOption,(client_id,symbol,expiry))
        column_names = [column[0] for column in cursor.description]
        data = cursor.fetchall()
        optionData = []

        for i in data:
            x = {}
            for k,j in enumerate(column_names):
                if j == 'Units':
                    x.update({j:int(i[k])})
                else:
                    x.update({j:i[k]})
            optionData.append(x)

        ############################### Future Data #############################
        cursor.execute(queryFuture,(client_id,symbol,expiry))
        column_names_future = [column[0] for column in cursor.description]
        data = cursor.fetchall()
        futData = []

        for i in data:
            x = {}
            for k,j in enumerate(column_names_future):
                if j == 'Units':
                    x.update({j: int(i[k])})
                else:
                    x.update({j: i[k]})
            futData.append(x)

        ############################### Equity Data #############################
        cursor.execute(queryEquity,(client_id,symbol))
        column_names_equity = [column[0] for column in cursor.description]
        data = cursor.fetchall()
        equData = []

        for i in data:
            x = {}
            for k,j in enumerate(column_names_equity):
                if j == 'Units':
                    x.update({j: int(i[k])})
                else:
                    x.update({j: i[k]})
            equData.append(x)

        getMarginData = margincalculation(optionData, futData)
        expense = expense_calculation(client_id,symbol, expiry)
        response[200]['data'] = {"optionData": optionData,"futData":futData, "equData":equData,"getMarginData": getMarginData ,'totalExpense': expense}
        return response[200]
    except:
        print(f"getTabData_{id}", traceback.print_exc())
        return response[500]
