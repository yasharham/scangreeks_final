# import pandas as pd
#
# from Services.bhavcopy import get_previous_bhavcopy
#
# import os,traceback
# from datetime import datetime,timedelta,date
# from Services.db import *
# import csv
# # from Services.bhavcopy import *
# from Settings.api_responses import response
# from Utils.configReader import readConfigFile
# # from API.Controller.V1.EOD_margin import margin
#
# loc = os.getcwd().split('ScanGreeks')
# fo_csv_file = os.path.join(loc[0],"ScanGreeks/Download/Bhavcopy/fo_bhav.csv")
# cm_file = os.path.join(loc[0],"ScanGreeks/Download/Bhavcopy/cm_bhav.csv")
#
# data = readConfigFile()
# Holidays = data[1]
# current_date = date.today()
# prev_date = (date.today() - timedelta(days=1))
#
# while prev_date.weekday() in [5, 6] or prev_date.strftime("%Y-%m-%d") in Holidays:
#     prev_date -= timedelta(days=1)
#
# previous_date = prev_date.strftime("%Y-%m-%d")
# today = current_date.strftime("%Y-%m-%d")
#
#
# def bhavcopy_FO():
#     try:
#         cursor = mydb.cursor()
#         bhavFO = pd.read_csv(fo_csv_file, index_col=0)
#         insert_query = '''
#                                INSERT INTO Bhavcopy_FO values (%s,%s,%s,%s,%s,%s)
#                                '''
#         print(bhavFO.columns)
#         for index, row in bhavFO.iterrows():
#             date_obj = datetime.strptime(row['EXPIRY_DT'], "%d-%b-%Y")
#             expiry = date_obj.strftime("%Y-%m-%d")
#
#             date_obj1 = datetime.strptime(row['TIMESTAMP'], "%d-%b-%Y")
#             date = date_obj1.strftime("%Y-%m-%d")
#
#             values = (row['SYMBOL'], expiry, row['STRIKE_PR'], row['OPTION_TYP'], row['CLOSE'], date)
#             cursor.execute(insert_query, values)
#             mydb.commit()
#         cursor.close()
#
#         #     # Modify the INSERT statement according to your table structure
#         #     query1 = ''' select TradeID from tradesFO where TradeId = %s and TradeDate = %s'''
#         #     value = (row['TradeId'], row['Date'])
#         #     cursor.execute(query1, value)
#         #     data = cursor.fetchone()
#         #     if not data:
#         #         print(row['TradeId'])
#         #         insert_query = '''
#         #                        INSERT INTO tradesFO
#         #                            (`Client_id`,`TradeId`, `TradeDate`, `Token`, `Instrument_Type`, `Symbol`, `Expiry`, `Strike`, `Option_Type`,
#         #                            `Units`, `Ltp`, `Tradeamount`, `AssetToken`, `Lotsize`, `Premium`, `TOC`, `TorM`)
#         #                            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
#         #                                  '''
#         #
#         #         values = (
#         #             'A2021', row['TradeId'], row['Date'], row['Token'], row['Instrument_Type'], row['Symbol'],
#         #             row['Expiry'],
#         #             row['Strike'], row['Option_Type'], row['Units'], row['Ltp'], row['Tradeamount'], row['AssetToken'],
#         #             row['Lotsize'], row['Premium'], row['TOC'], row['TorM'])
#         #         cursor.execute(insert_query, values)
#         #         mydb.commit()
#
#     #     '''Get Today Date'''
#     #
#     #     closing_rate_data = {}
#     #
#     #     '''
#     #     Reads CSV file of bhavcopy
#     #     and add values to temp_table db
#     #     '''
#     #
#     #     with open(fo_csv_file, 'r') as csvfile:
#     #         reader = csv.DictReader(csvfile)
#     #         for row in reader:
#     #             symbol = row["SYMBOL"]
#     #             expiry = row["EXPIRY_DT"]
#     #             formatted_date = datetime.strptime(expiry, "%d-%b-%Y")
#     #             expiry_date = formatted_date.strftime("%Y-%m-%d")
#     #             strike = float(row["STRIKE_PR"])
#     #             option_type = row["OPTION_TYP"]
#     #             if option_type == "XX":
#     #                 option_type = "  "
#     #             date_today = row["TIMESTAMP"]
#     #             closing_rate = float(row["CLOSE"])
#     #
#     #             key = (symbol, expiry_date, strike, option_type, date_today)
#     #             closing_rate_data[key] = closing_rate
#     #
#     #
#     #
#     #         temp_table_bhavFO.insert_many([
#     #             {
#     #                 'symbol': symbol,
#     #                 'expiry': expiry,
#     #                 'strike': strike,
#     #                 'option_type': option_type,
#     #                 'date': date_today,
#     #                 'closing_rate': closing_rate
#     #             }
#     #             for key, closing_rate in closing_rate_data.items()
#     #             for symbol, expiry, strike, option_type, date_today in [key]
#     #         ])
#     except:
#         print(traceback.print_exc())
#
# bhavcopy_FO()
#
# # def bhavcopy_EQ():
# #     try:
# #         temp_table_bhavEQ = tradeData["temp_table_bhavEQ"]
# #         temp_table_bhavEQ.drop()
# #         closing_rate_data = {}
# #         with open(cm_file, 'r') as csvfile:
# #             reader = csv.DictReader(csvfile)
# #             for row in reader:
# #                 symbol = row["SYMBOL"]
# #                 date_today = row["TIMESTAMP"]
# #                 closing_rate = float(row["CLOSE"])
# #                 key = (symbol, date_today)
# #                 closing_rate_data[key] = closing_rate
# #             temp_table_bhavEQ.insert_many([
# #                 {
# #                     'symbol': symbol,
# #                     'date': date_today,
# #                     'closing_rate': closing_rate
# #                 }
# #
# #                 for key, closing_rate in closing_rate_data.items()
# #                 for symbol, date_today in [key]
# #             ])
# #     except:
# #         print(traceback.print_exc())
#
# #
# # def previous_open(date):
# #     try:
# #         prev_open = list(position_Data.aggregate([
# #             {'$match':
# #                  {'Date': date}
# #              },
# #
# #             # left join from bhavcopy temp_table to add CLOSING_RATE by matching symbol,expiry,optiontype,strike
# #
# #             {
# #                 '$lookup': {
# #                     "from": "temp_table_bhavFO",
# #                     "let": {
# #                         'local_field1': "$Symbol",
# #                         'local_field2': "$Expiry",
# #                         'local_field3': "$OptionType",
# #                         'local_field4': "$Strike"
# #                     },
# #
# #                     "pipeline": [
# #                         {
# #                             "$match": {
# #                                 "$expr": {
# #                                     "$and": [
# #                                         {"$eq": ["$symbol", "$$local_field1"]},
# #                                         {"$eq": ["$expiry", "$$local_field2"]},
# #                                         {"$eq": ["$option_type", "$$local_field3"]},
# #                                         {"$eq": ["$strike", "$$local_field4"]}
# #                                     ]
# #                                 }
# #                             }
# #                         }
# #                     ],
# #                     'as': 'closing_rate'
# #                 }
# #             },
# #             {"$unwind": "$closing_rate"},
# #             {
# #                 "$set": {
# #                     "prev_closing_rate": "$closing_Rate",
# #                     "closing_Rate": "$closing_rate.closing_rate",
# #                     "Date": today
# #                 }
# #             },
# #             {
# #                 "$unset": "closing_rate"
# #             }
# #         ]))
# #         print("prev_open", len(prev_open))
# #         return prev_open
# #     except:
# #         print(traceback.print_exc())
# #
# #
# # def closing_position():
# #     try:
# #         openPosition = list(tradesFO.aggregate([
# #             # get extradesFO's today documents
# #
# #             {'$match':
# #                  {'Date': today}
# #              },
# #
# #             {"$group": {
# #                 "_id": {
# #                     # "client": "",
# #                     "symbol": "$Symbol",
# #                     "token": "$Token",
# #                     "expiry": "$Expiry",
# #                     "instrument": "$Instrument_Type",
# #                     "optionType": "$Option_Type",
# #                     "strike": "$Strike"
# #                 },
# #                 "netQty": {"$sum": "$Units"},
# #                 "premium": {"$sum": "$Premium"}
# #             }},
# #
# #             # left join from bhavcopy temp_table to add CLOSING_RATE by matching symbol,expiry,optiontype,strike
# #
# #             {
# #                 '$lookup': {
# #                     "from": "temp_table_bhavFO",
# #                     "let": {
# #                         'local_field1': "$_id.symbol",
# #                         'local_field2': "$_id.expiry",
# #                         'local_field3': "$_id.optionType",
# #                         'local_field4': "$_id.strike"
# #                     },
# #
# #                     "pipeline": [
# #                         {
# #                             "$match": {
# #                                 "$expr": {
# #                                     "$and": [
# #                                         {"$eq": ["$symbol", "$$local_field1"]},
# #                                         {"$eq": ["$expiry", "$$local_field2"]},
# #                                         {"$eq": ["$option_type", "$$local_field3"]},
# #                                         {"$eq": ["$strike", "$$local_field4"]}
# #                                     ]
# #                                 }
# #                             }
# #                         }
# #                     ],
# #                     'as': 'closing_rate'
# #                 }
# #             },
# #             {"$unwind": "$closing_rate"},
# #
# #             {
# #                 "$project":
# #                     {
# #                         "_id": 0,
# #                         "Instrument_Type": "$_id.instrument",
# #                         "premium": 1,
# #                         "client": "Client_03",
# #                         'token': "$_id.token",
# #                         "Symbol": "$_id.symbol",
# #                         "Expiry": "$_id.expiry",
# #                         "OptionType": "$_id.optionType",
# #                         "Strike": "$_id.strike",
# #                         "closing_Rate": "$closing_rate.closing_rate",
# #                         "Date": today,
# #                         # "Date": prev_date.strftime("%Y-%m-%d"), # change when today
# #                         "netQty": 1,
# #                     }
# #             }
# #         ]))
# #         print("openPosition ln ", len(openPosition))
# #
# #         prev_open = previous_open(previous_date)
# #
# #         # if token in prev open and today open matches it merge qty
# #
# #         for i in prev_open:
# #             flag = False
# #             for j in openPosition:
# #                 if (i['token'] == j['token']):
# #                     j['netQty'] += i['netQty']
# #                     j['premium'] += i['premium']
# #                     print("position updaated :", i['token'])
# #                     flag = True
# #                     break
# #             if (flag == False):
# #                 del i["_id"]
# #                 openPosition.append(i)
# #         print("openPosition ln 2 ", len(openPosition))
# #
# #         if openPosition:
# #             position_Data.insert_many(openPosition)
# #     except:
# #         print(traceback.print_exc())
# #
# #
# # def billFO_generation():
# #     try:
# #         fnoPosition = list(tradesFO.aggregate([
# #             # get tradesFO's today documents
# #
# #             {'$match':
# #                  {'Date': today}
# #              },
# #
# #             # add field buyqty,sellqty,buyrate,sellrate
# #
# #             {"$addFields": {
# #                 "BuyQty": {"$cond": [{'$gte': ["$Units", 0]}, '$Units', 0]},
# #                 "SellQty": {"$cond": [{'$lte': ["$Units", 0]}, '$Units', 0]},
# #                 "BuyRate": {"$cond": [{'$gte': ["$Units", 0]}, '$Ltp', 0]},
# #                 "SellRate": {"$cond": [{'$lte': ["$Units", 0]}, '$Ltp', 0]}
# #             }},
# #
# #             # Groupby symbol,expiry,date,optionType,strike for BUYQTY,BUYRATE,SELLQTY,SELLRATE
# #
# #             {"$group": {
# #                 "_id": {
# #                     "symbol": "$Symbol",
# #                     "expiry": "$Expiry",
# #                     'token': "$Token",
# #                     "optionType": "$Option_Type",
# #                     "strike": "$Strike"
# #                 },
# #                 "Instrument_Type": {"$first": "$Instrument_Type"},
# #                 "BuyQty": {"$sum": "$BuyQty"},
# #                 "BuyRate": {"$avg": "$BuyRate"},
# #                 "SellQty": {"$sum": "$SellQty"},
# #                 "SellRate": {"$avg": "$SellRate"},
# #                 "Expense": {"$sum": "$TOC"}
# #             }},
# #
# #             # add field I_type
# #
# #             {
# #                 '$addFields': {
# #                     'I_type': {
# #                         '$cond': {
# #                             'if': {
# #                                 '$or': [
# #                                     {'$eq': ['$Instrument_Type', 'OPTIDX']},
# #                                     {'$eq': ['$Instrument_Type', 'OPTSTK']}
# #                                 ]
# #                             },
# #                             'then': 'option',
# #                             'else': 'future'
# #                         }
# #                     }
# #                 }
# #             },
# #
# #             # add field BuyAmount,SellAmount
# #
# #             {"$addFields": {
# #                 "BuyAmount": {"$multiply": ["$BuyQty", "$BuyRate"]},
# #                 "SellAmount": {"$multiply": ["$SellQty", "$SellRate"]},
# #                 "Segment": "NSE_FNO",
# #
# #             }},
# #
# #             # ................................................Today_closing_rate......................
# #
# #             {
# #                 '$lookup': {
# #                     'from': "temp_table",
# #                     'let': {
# #                         'symbol': '$_id.symbol',
# #                         'expiry': '$_id.expiry',
# #                         'strike': '$_id.strike',
# #                         'option_type': '$_id.optionType',
# #                     },
# #                     'pipeline': [
# #                         {
# #                             '$match': {
# #                                 '$expr': {
# #                                     '$and': [
# #                                         {'$eq': ['$symbol', '$$symbol']},  # from [foreign,local(let)]
# #                                         {'$eq': ['$expiry', '$$expiry']},
# #                                         {'$eq': ['$strike', '$$strike']},
# #                                         {'$eq': ['$option_type', '$$option_type']},
# #
# #                                     ]
# #                                 }
# #                             }
# #                         },
# #
# #                     ],
# #                     'as': 'closing_rate_today'
# #                 }
# #             },
# #             {'$unwind': '$closing_rate_today'},
# #
# #             {"$addFields": {
# #                 "OpenQty": 0,
# #                 'OpenRate': 0,
# #                 "NetQty": {"$add": ["$BuyQty", "$SellQty"]},
# #                 "NetAmount": {"$subtract": [{"$add": ["$BuyAmount", "$SellAmount"]}, "$Expense"]}
# #                 # "NetAmount": {"$add": ["$BuyAmount", "$SellAmount"]},
# #             }},
# #
# #             {"$project": {
# #                 "_id": 0,
# #                 "Symbol": "$_id.symbol",
# #                 "Segment": 1,
# #                 "I_type": 1,
# #                 "OpenQty": 1,
# #                 "OpenRate": 1,
# #                 "ClosingRate": "$closing_rate_today.closing_rate",
# #                 "BuyQty": 1,
# #                 "SellQty": 1,
# #                 "BuyRate": 1,
# #                 "SellRate": 1,
# #                 "BuyAmount": 1,
# #                 "SellAmount": 1,
# #                 "NetAmount": 1,
# #                 "NetQty": 1,
# #                 "Expiry": "$_id.expiry",
# #                 "Token": "$_id.token",
# #                 "Date": today,
# #                 "Strike": "$_id.strike",
# #                 "Option_Type": "$_id.optionType",
# #                 'Expense': 1
# #             }}
# #         ]))
# #
# #         prev_open = previous_open(previous_date)
# #
# #         # Carry forword if token in prev open and today open matches then merge qty
# #         for i in prev_open:
# #             flag = False
# #             for j in fnoPosition:
# #                 if i['token'] == j['Token']:
# #                     if j['I_type'] == "future":
# #                         j['OpenQty'] = i['netQty']  # adds openqty
# #                         j['OpenRate'] = i['prev_closing_rate']  # openrate
# #                         j["NetQty"] = j["NetQty"] + i['netQty']
# #                         j['NetAmount'] = j['NetAmount'] + (i['netQty'] * i['prev_closing_rate'])
# #                         print("position updaated :", i['token'])
# #                         flag = True
# #
# #             if (flag == False):
# #                 if '_id' in i:
# #                     print(i['_id'])
# #                     del i["_id"]
# #                 x = {"Symbol": i['Symbol'],
# #                      "Segment": "NSE_FNO",
# #                      "OpenQty": i['netQty'],
# #                      "OpenRate": i['prev_closing_rate'],
# #                      "ClosingRate": i['closing_Rate'],
# #                      "Expense": i["Expense"],
# #                      "BuyQty": 0,
# #                      "SellQty": 0,
# #                      "BuyRate": 0,
# #                      "SellRate": 0,
# #                      "BuyAmount": 0,
# #                      "SellAmount": 0,
# #                      'Token': i['token'],
# #                      "NetAmount": i['netQty'] * i['closing_Rate'],
# #                      "NetQty": i['netQty'],
# #                      "Expiry": i['Expiry'],
# #                      "Date": today,
# #                      "Strike": i['Strike'],
# #                      "Option_Type": i['OptionType'],
# #                      }
# #                 if i['Instrument_Type'] in ['OPTIDX', 'OPTSTK']:
# #                     x.update({'I_type': "option"})
# #                 elif i['Instrument_Type'] in ['FUTIDX', 'FUTSTK']:
# #                     x.update({'I_type': "future"})
# #                 fnoPosition.append(x)
# #
# #         print("final bill ln ", len(fnoPosition))
# #
# #         if fnoPosition:
# #             FNO_Bills.insert_many(fnoPosition)
# #     except:
# #         print(traceback.print_exc())
# #
# #
# # def billFO_Posting():
# #     try:
# #         billData = list(FNO_Bills.aggregate([
# #             {
# #                 "$match": {"Date":today}
# #             },
# #             {
# #                 "$group": {
# #                     "_id": "client_id",
# #                     "BillAmount": {"$sum": "$NetAmount"}
# #                 }
# #             },
# #             {
# #                 "$project":
# #                     {
# #                         "_id": 0,
# #                         "Client_Id": "Client_03",
# #                         "Date": "2023-07-20",
# #                         "Segment": "NSE_FNO",
# #                         "Debit": {"$cond": [{"$lt": ["$BillAmount", 0]}]},
# #                         "Credit": {"$cond": [{"$gt": ["$BillAmount", 0]}]}
# #                     }
# #             }
# #         ]))
# #         BillPosting.insert_many(billData)
# #     except:
# #         print(traceback.print_exc())
# #
# #
# # def billEQ_generation():
# #     try:
# #         EqPosition = list(tradesEQ.aggregate([
# #             {"$addFields": {
# #                 "BuyQty": {"$cond": [{'$gte': ["$Units", 0]}, '$Units', 0]},
# #                 "SellQty": {"$cond": [{'$lte': ["$Units", 0]}, '$Units', 0]},
# #                 "BuyRate": {"$cond": [{'$gte': ["$Units", 0]}, '$Ltp', 0]},
# #                 "SellRate": {"$cond": [{'$lte': ["$Units", 0]}, '$Ltp', 0]}
# #             }},
# #
# #             {"$group": {
# #                 "_id": {
# #                     "symbol": "$Symbol",
# #                     "date": "$Date",
# #                 },
# #
# #                 "BuyQty": {"$sum": "$BuyQty"},
# #                 "BuyRate": {"$avg": "$BuyRate"},
# #                 "SellQty": {"$sum": "$SellQty"},
# #                 "SellRate": {"$avg": "$SellRate"}
# #             }},
# #
# #             {"$addFields": {
# #                 "BuyAmount": {"$multiply": ["$BuyQty", "$BuyRate"]},
# #                 "SellAmount": {"$multiply": ["$SellQty", "$SellRate"]}
# #             }},
# #
# #             {"$addFields": {
# #                 "NetQty": {"$add": ["$BuyQty", "$SellQty"]},
# #                 "NetAmount": {"$add": ["$BuyAmount", "$SellAmount"]},
# #                 "Segment": "NSE_CM",
# #             }},
# #
# #             # left join from prev table(position Table) - symbol,expiry,strike,option_type,prev_date
# #             {
# #                 '$lookup': {
# #                     'from': "temp_table_EQ",
# #                     "localField": "_id.symbol",
# #                     "foreignField": "symbol",
# #                     "as": "newData"
# #                 }},
# #             {'$unwind': '$newData'},
# #
# #             {"$project": {
# #                 "_id": 0,
# #                 "Symbol": "$_id.symbol",
# #                 "Segment": 1,
# #                 "BuyQty": 1,
# #                 "SellQty": 1,
# #                 "BuyRate": 1,
# #                 "SellRate": 1,
# #                 "BuyAmount": 1,
# #                 "SellAmount": 1,
# #                 "NetAmount": 1,
# #                 "NetQty": 1,
# #                 "ClosingRate": "$newData.closing_rate",
# #                 "Date": "$_id.date"
# #             }}
# #         ]))
# #         if EqPosition:
# #             EQ_Bills.insert_many(EqPosition)
# #     except:
# #         print(traceback.print_exc())
# #
# #
# # def billEQ_Posting():
# #     try:
# #         billData = list(EQ_Bills.aggregate([
# #             {
# #                 "$match": {"Date": today}
# #             },
# #             {
# #                 "$group": {
# #                     "_id": "client_id",
# #                     "BillAmount": {"$sum": "$NetAmount"}
# #                 }
# #             },
# #             {
# #                 "$project":
# #                     {
# #                         "_id": 0,
# #                         "Client_Id": "Client_03",
# #                         "Date": today,
# #                         "Segment": "NSE_CM",
# #                         "Debit": {"$cond": [{"$lt": ["$BillAmount", 0]}]},
# #                         "Credit": {"$cond": [{"$gt": ["$BillAmount", 0]}]}
# #                     }
# #             }
# #         ]))
# #         BillPosting.insert_many(billData)
# #     except:
# #         print(traceback.print_exc())
# #
# #
# # def margin_Posting():
# #     margin()
# #
# # print("EOD Started.....................")
# #
# # def EODProcess():
# #     get_previous_bhavcopy()
# #     bhavcopy_FO()
# #     bhavcopy_EQ()
# #     previous_open(previous_date)
# #     closing_position()
# #     billFO_generation()
# #     billFO_Posting()
# #     billEQ_generation()
# #     margin_Posting()
# #     response1 = response[200]
# #     response1['message'] = "EOD Process Completed"
# #     return response1
# #
# # print("EOD Complete.....................")
#
#
#
#
# # eodSpanfile()
# # parseSpan_margin()
# # parseSpan_calSpred()
# # parseSpan_spread()
#
# # EODspanMargin = getSpanMargin()
#
#
