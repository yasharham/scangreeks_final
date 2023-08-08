import traceback
from Services.db import *
from Middleware.authenticate import decode_access_token
from Settings.api_responses import *
from Utils.configReader import readConfigFile


Holidays = readConfigFile()


async def getTradeHistory(page,page_size,token):
    try:
        try:
            tokenData = decode_access_token(token)
            client_id = tokenData.username
        except:
            return response[401]
        cursor = mydb.cursor()
        cursor.execute('''select * from tradesFO where Client_id = %s''',(client_id,))
        column_names = [column[0] for column in cursor.description]
        data = cursor.fetchall()
        cursor.close()
        optionData = []

        for i in data:
            x = {}
            for k, j in enumerate(column_names):
                    x.update({j: i[k]})
            optionData.append(x)

        sortTrades = optionData[::-1]

        start_index = (page - 1) * page_size
        end_index = start_index + page_size

        paginated_trades = sortTrades[start_index:end_index]
        print("paginated_trades",len(paginated_trades))
        response[200]['data'] = paginated_trades
        return response[200]
    except:
        print("tardeHistory",traceback.print_exc())
        return response[500]

def getNetPosition(page,page_size,token):
    try:
        try:
            tokenData = decode_access_token(token)
            client_id = tokenData.username

        except:
            return response[401]

        query1 = '''
                select 
                    Token,Option_Type,Strike,Instrument_Type,Symbol,Expiry,
                    SUM(Units) as Units,
                    SUM(Tradeamount) as Tradeamount,
                    SUM(Premium) as Premium,
                    case when (SUM(Units)> 0) then SUM(Tradeamount)/SUM(Units)  else 0 end as LTP  
                    from tradesFO where Client_id = %s and  Instrument_Type in ('OPTIDX','OPTSTK') 
                    group by Token,Option_Type,Strike,Instrument_Type,Symbol,Expiry;
                '''
        cursor = mydb.cursor()
        cursor.execute(query1,(client_id,))
        data = cursor.fetchall()
        column_names = [column[0] for column in cursor.description]
        optionData=[]

        for i in data:
            x = {}
            for k, j in enumerate(column_names):
                x.update({j: i[k]})
            optionData.append(x)



        # start_index = (page - 1) * page_size
        # end_index = start_index + page_size
        #
        # paginated_trades = optionData[start_index:end_index]
        # print("optionData",len(optionData))


        response[200]['data'] = optionData
        return response[200]
    except:
        print("getNetPosition",traceback.print_exc())
        return response[500]


def getTradeHistoryfilter(token):
    try:
        tokenData = decode_access_token(token)
        client_id = tokenData.username

    except:
        return response[401]
    # data = list(tradesFO.find({}, {"_id": 0, "Instrument_Type": 0, "AssetToken": 0, "Lotsize": 0, "TOC": 0, "TorM": 0}))
    cursor = mydb.cursor()
    cursor.execute('''select distinct Symbol from tradesFO where Client_id = %s and Expiry >= current_date''',(client_id,))
    symbol_ex = cursor.fetchall()
    cursor.execute('''select distinct Expiry from tradesFO where Client_id = %s  and Expiry >= current_date''',(client_id,))
    expiry_ex = cursor.fetchall()
    cursor.execute('''select distinct Strike from tradesFO where Client_id = %s  and Expiry >= current_date''',(client_id,))
    strike_ex = cursor.fetchall()
    symbol = []
    expiry = []
    strike = []
    for i in symbol_ex:
        symbol.append(i[0])
    for i in expiry_ex:
        expiry.append(i[0])
    for i in strike_ex:
        strike.append(i[0])
    tabList = {"symbol": symbol, "expiry": expiry, "strike": strike}
    return tabList
