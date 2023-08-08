from Services.db import *

query1 = """
      create temporary table temp1 as
              select Symbol,TradeDate,
              sum((  CASE WHEN Units < 0
                     THEN 0
                     ELSE abs(Units)
                     END ) ) as buyQty ,
              sum((  CASE WHEN Units > 0
                     THEN 0
                     ELSE abs(Units)
                     END ) ) as sellQty ,
              sum((  CASE WHEN Units < 0
                     THEN 0
                     ELSE abs(Units)
                     END ) * Ltp) as buyAmt ,
              sum((  CASE WHEN Units > 0
                     THEN 0
                     ELSE abs(Units)
                     END ) * Ltp) as sellAmt
              from tradesEQ
              where Client_id = %s and TradeDate < CURRENT_DATE
          group by TradeDate,Symbol;
                """

query2 = """
      create temporary table temp2 as select
           Symbol,tradeDate,buyqty,sellQty,buyAmt,sellAmt,
           CASE WHEN buyqty = 0 THEN 0 ELSE buyamt/buyqty END AS buyAvg,
           CASE WHEN sellQty = 0 THEN 0 ELSE sellAmt / sellQty END AS sellAvg,
           buyqty-sellQty as netqty,
           case when buyqty > sellQty then sellqty else buyqty end as IntradayQty
           from temp1;
       """

query3 = """
        create temporary table temp3 as
               select Symbol,tradeDate,
               buyAvg * intradayQty as IBAmt,
               sellAvg * intradayQty as ISAmt,
               case when buyqty > sellQty then buyAvg * netQty else 0 end
               as DBAmt,
               case when buyqty > sellQty then 0 else sellAvg * netQty end
               as DsAmt
               from temp2;
         """

query4 = """
        create temporary table temp4 as
           select Symbol,
           abs(SUM(IBamt)) as IBAmt,
           abs(SUM(ISamt)) as ISAmt,
           abs(SUM(DBamt)) as DBAmt,
           abs(SUM(DSamt)) as DSAmt
           from temp3 group by Symbol;
                   """

query5 = """
      create temporary table temp_exp as
           select
           sum(i_buy)  as intraday_buy ,
           sum(i_sell) as intraday_sell ,
           sum(d_buy) as delivery_buy ,
           sum(d_sell) as delivery_sell
           from Expense_Master;
	   """

query6 = """
    CREATE temporary TABLE temp_symbolexp AS
        SELECT
            a.Symbol,
            ((a.IBamt * (b.intraday_buy / 10000000)) +
            (a.ISamt * (b.intraday_sell / 10000000)) +
            (a.DSamt * (b.delivery_sell / 10000000)) +
            (a.DBamt * (b.delivery_buy / 10000000))) AS Expense
        FROM
            temp4 a,temp_exp b;
        """

query7 = '''
        create temporary table fo_expense as 
            select 
                Symbol,
                Expiry,
                SUM(TOC) as Expense
            from tradesFO 
            where Client_id = %s and Symbol = %s and Expiry = %s
            group by Symbol;
        '''
query8 = """
        select 
            a.Symbol,a.Expiry,
            case when a.Symbol = b.Symbol then (a.Expense + b.Expense) else a.expense end as Expense 
        from fo_expense a left join temp_symbolexp b  on a.Symbol = b.Symbol
        """


def expense_calculation(client_id,symbol, expiry):
    cursor = mydb.cursor()
    cursor.execute("drop temporary table if exists temp1")
    cursor.execute("drop temporary table if exists temp2")
    cursor.execute("drop temporary table if exists temp3")
    cursor.execute("drop temporary table if exists temp4")
    cursor.execute("drop temporary table if exists temp_exp")
    cursor.execute("drop temporary table if exists temp_symbolexp")
    cursor.execute("drop temporary table if exists fo_expense")

    cursor.execute(query1,[client_id])
    cursor.execute(query2)
    cursor.execute(query3)
    cursor.execute(query4)
    cursor.execute(query5)
    cursor.execute(query6)
    cursor.execute(query7,(client_id,symbol,expiry))
    cursor.execute(query8)
    expense = cursor.fetchone()
    print("expense",cursor.fetchall())
    cursor.close()
    expenseValue = expense[2]
    return expenseValue

