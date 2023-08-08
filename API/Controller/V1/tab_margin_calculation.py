import traceback
import numpy as np
import datatable as dt
from Services.api_services import *



def margincalculation(option,future):
    print(option)
    print(future)
    # print("f",future)
    spanTableTW = np.zeros((20000,40),dtype=object)
    j = 0

    for i in option:
        scn = span[int(i["Token"]) - 35000, :]
        # print('scn',scn)
        expo = Ael[int(i["Token"]) - 35000]

        instrumentType=contract_fo[int(i["Token"]) - 35000, 5]
        futureToken = contract_fo[int(i["Token"]) - 35000, 9]

        fltr = contract_eq[np.where(contract_eq[:, 2] == futureToken)]
        # global FPrice
        if fltr.size != 0:
            FPrice = fltr[0][18]

        if (instrumentType in ['OPTIDX']):
            FPrice = idxbhav[int(futureToken) - 26000, 3]

        PFQ = 0
        NFQ = 0
        PCD = 0
        NCD = 0

        # global iexpoM
        if (i["Option_Type"] in ['CE','PE'] ):
            iexpoM = 0.0 if (i["Units"] > 0) else expo[5] / 100.0 * abs(i['Units']) * FPrice
            # print(FPrice,'FPrice',expo[5],i[2],iexpoM)



        spanTableTW[j, :26] = [i["Option_Type"],scn[10] * i["Units"], scn[11] * i["Units"], scn[12] * i["Units"],scn[13] * i["Units"], scn[14] * i["Units"],
                                     scn[15] * i["Units"], scn[16] * i["Units"], scn[17] * i["Units"],scn[18] * i["Units"], scn[19] * i["Units"],
                                     scn[20] * i["Units"], scn[21] * i["Units"], scn[22] * i["Units"],scn[23] * i["Units"], scn[24] * i["Units"],
                                     scn[25] * i["Units"],scn[26] * i["Units"], scn[9],
                                     iexpoM,i["Premium"], PFQ, NFQ,PCD, NCD , i["Symbol"]]
        j += 1


        # print("main.spanTableTW",main.spanTableTW)

    if future:
        future = future[0]
        # print("fut",future)
        futureqty = int(future['Units'])
        # print("futureqty",future['Units'])
        if futureqty !=0:
            ftoken = int(future["Token"])
            eqtoken=contract_fo[ftoken-35000,9]

            # eqtoken = int(tab.leEQToken.text())

            scn = span[ftoken - 35000, :]
            expo = Ael[ftoken - 35000]

            PFQ = 0
            NFQ = 0
            PCD = 0
            NCD = 0

            try:
                FPrice = idxbhav[eqtoken - 26000, 3]
            except:
                fltr = contract_eq[np.where(contract_eq[:, 2] == eqtoken)]
                FPrice = fltr[0][18]
            # print("futureqty", futureqty)

            iexpoM = expo[5] / 100.0 * abs(futureqty) * FPrice
            if (futureqty > 0):
                PFQ = futureqty
            else:
                NFQ = abs(futureqty)

            spanTableTW[j, :26] = [0, scn[10] * futureqty, scn[11] * futureqty, scn[12] * futureqty,
                                        scn[13] * futureqty,
                                        scn[14] * futureqty,
                                        scn[15] * futureqty, scn[16] * futureqty, scn[17] * futureqty,
                                        scn[18] * futureqty, scn[19] * futureqty,
                                        scn[20] * futureqty, scn[21] * futureqty, scn[22] * futureqty,
                                        scn[23] * futureqty, scn[24] * futureqty,
                                        scn[25] * futureqty, scn[26] * futureqty, scn[9],
                                        iexpoM,future['Premium'], PFQ, NFQ, PCD, NCD, future['Symbol']]

            j += 1


    #########
    # print(tab.symbol)
    # with open('d:/span.csv', 'w') as f:
    #     for i in range(j):
    #         a = ''
    #         for w in range(main.spanTableTW.shape[1]):
    #             x = main.spanTableTW[i, w]
    #             a = a + str(x) + ','
    #         f.write(a + '\n')
    #         # print(a)
    # f.close()




    df3 = dt.Frame(spanTableTW[:j,
                   [25,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,19,20,21,22,23,24]],
                   names=['sym','scn1', 'scn2', 'scn3', 'scn4', 'scn5', 'scn6',
                          'scn7', 'scn8', 'scn9', 'scn10', 'scn11', 'scn12', 'scn13', 'scn14', 'scn15', 'scn16',
                          'Cdelta', 'iexpoM', 'netpremium','PFQ', 'NFQ','PCD', 'NCD'])





    df3[1:] = dt.float64
    df3[0] = dt.str64


    df3[:, dt.update(PCD=dt.ifelse(dt.f.Cdelta > 0, dt.f.Cdelta, 0.0))]
    df3[:, dt.update(NCD=dt.ifelse(dt.f.Cdelta > 0, 0.0, -dt.f.Cdelta))]

    # with open('d:/df3.csv', 'w') as f:
    #     for i in range(df3.shape[0]):
    #         a = ''
    #         for j in range(df3.shape[1]):
    #             x = df3[i,j]
    #             a = a + str(x) + ','
    #         f.write(a + '\n')
    #         # print(a)
    # f.close()


    x1 = df3[:, dt.sum(dt.f[1:]), dt.by('sym')]





    x1[:, 'FSQ'] = 0.0    # col no 24
    x1[:, 'CDSQ'] = 0.0   # col no 25
    x1[:, 'spreadChrg'] = 0.0   # col no 26
    x1[:, 'spreadBeni'] = 0.0   # col no 27
    x1[:, 'maxVal'] = 0.0   # col no 28
    x1[:, 'spanMargin'] = 0.0   # col no 29


    x1[:, dt.update(FSQ=dt.ifelse(dt.f.PFQ > dt.f.NFQ, dt.f.NFQ, dt.f.PFQ))]
    x1[:, dt.update(CDSQ=dt.ifelse(dt.f.PCD > dt.f.NCD, dt.f.NCD, dt.f.PCD))]
    x1[:, dt.update(maxVal=dt.rowmax(dt.f[1:16]))]
    x1[:, dt.update(spanMargin=dt.f[28] - dt.f[19])]
    x1[:, dt.update(index=range(x1.nrows))]

    # print("x1",x1)
    # with open('d:/x1.csv', 'w') as f:
    #     for i in range(x1.shape[0]):
    #         a = ''
    #         for j in range(x1.shape[1]):
    #             x = x1[i,j]
    #             a = a + str(x) + ','
    #         f.write(a + '\n')
    #         # print(a)
    # f.close()


    x2=x1[:,[30,0,18,19,24,25,26,27,28,29]]



    # for i in range(x2.nrows):
    #
    #     if (x2[i, 4] != 0 or x2[i, 5] != 0):
    #         fsq = x2[i, 4]
    #         cdsq = x2[i, 5]
    #         data = main.calspread[np.where(main.calspread[:, 1] == tab.symbol)]
    #
    #         ael = data[0][2]
    #         fprice = data[0][3]
    #         calsc = data[0][0]
    #
    #         bvalue = fsq * 2 / 3 * ael/100 * fprice
    #         sprdC = cdsq * calsc
    #         x2[i, dt.update(spanMargin=dt.f[9] + sprdC)]
    #
    #
    #         x2[i, dt.update(iexpoM=dt.f[2] - bvalue)]

    # with open('d:/x2.csv', 'w') as f:
    #     for i in range(x2.shape[0]):
    #         a = ''
    #         for j in range(x2.shape[1]):
    #             x = x2[i, j]
    #             a = a + str(x) + ','
    #         f.write(a + '\n')
            # print(a)
    # f.close()
    # print(x2)
    # x2.to_csv("margin.csv")
    x2[:, dt.update(spanMargin=dt.ifelse(dt.f.spanMargin > 0, dt.f.spanMargin, 0.0))]
    x2[:,dt.update(Total_Margin=dt.f[9] + dt.f[2])]
    # x2.to_csv("margin1.csv")
    # print(f"expo_margin:{x2[0,2]},span_margin':{x2[0, 9]}, total_margin:{x2[0, 10]}")
    return {'expo_margin':x2[0,2], 'span_margin':x2[0,9], "total_margin":x2[0,10]}



