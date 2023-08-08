import os,traceback,zipfile,requests
from os import path
from datetime import datetime,timedelta,date
import lxml.etree as elementTree
import pandas as pd
from Services.api_services import contract_fo



yesterday = date.today()-timedelta(days=1)
Ymd_yesterday = yesterday.strftime("%Y%m%d")
Ymd_today = date.today().strftime("%Y%m%d")

loc1 = os.getcwd().split('Services')
downloadLoc = os.path.join(loc1[0],"Download/EODSpan")
today =date.today()


def eodSpanfile():
    url = 'https://archives.nseindia.com/archives/nsccl/span/nsccl.' + Ymd_today + '.s.zip'
    print(url)
    try:
        res = requests.get(url)
        span = path.join(downloadLoc, "spanfile.zip")
        with open(span, 'wb+') as f:
            f.write(res.content)
        f.close()

        zf = zipfile.ZipFile(span, 'r')
        zf.extractall(downloadLoc)
        os.remove(os.path.join(downloadLoc, "spanfile.zip"))
        zf.close()

        if path.isfile(path.join(downloadLoc, 'span.spn')):
            os.remove(path.join(downloadLoc, 'span.spn'))
        fname = path.join(downloadLoc, f"nsccl.{Ymd_yesterday}.s.spn")
        os.rename(fname, path.join(downloadLoc, 'span.spn'))
    except:
        print(traceback.print_exc())


def parseSpan_calSpred():
    try:
        tree = elementTree.parse (path.join(downloadLoc,"span.spn"))
        root = tree.getroot()
        spanCalSpred = path.join(downloadLoc, "calspred.csv")
        with open(spanCalSpred, 'w') as abcd:
            for decade in (root.iter("ccDef")):
                for i, year in enumerate(decade.findall("./dSpread")):
                    rb1 = str(year[0].text)
                    rb2 = str(year[2][1].text)
                    rb3 = str(year[3][0].text)
                    rb4 = str(year[3][1].text)
                    rb5 = str(year[4][1].text)

                    # print(str(year[0].text), str(year[2][1].text), str(year[3][0].text), str(year[3][1].text), str(year[4][1].text))
                    # abcd.write("%s,%s,%s,%s,%s\n" % (rb1, rb2, rb3, rb4, rb5))

        print("calspred created..........")
        abcd.close()
    except:
        print(traceback.print_exc())


def parseSpan_spread():
    try:
        tree = elementTree.parse (path.join(downloadLoc,"span.spn"))
        root = tree.getroot()
        spanSomr = path.join(downloadLoc, "somr.csv")
        with open(spanSomr, 'w') as abcd:
            for decade in (root.iter("ccDef")):
                # if(i>30):
                #     continue
                # print('ff',str(decade[0].text),str(decade.text))
                aa = str(decade[0].text)
                if aa.__contains__('NSETEST'):
                    pass
                else:
                    bb = str(decade[26][0][1][1].text)
                    abcd.write('%s,%s\n' % (aa, bb))
        print("somr created..........")
        abcd.close()
    except:
        print(traceback.print_exc())


def parseSpan_margin():
    try:
        tree = elementTree.parse(path.join(downloadLoc, "span.spn"))
        root = tree.getroot()
        spanSomr = path.join(downloadLoc, "span.csv")
        with open(spanSomr, 'w') as abcd:
            for decade in root.iter("futPf"):
                name = str(decade[1].text)
                if 'NIFTY' in name:
                    IT = "FUTIDX"
                else:
                    IT = "FUTSTK"

                for year in decade.findall("./fut"):
                    # print(name)
                    exp = year[1].text
                    ra_17 = year[2].text
                    ra_1 = year[12][1].text
                    ra_2 = year[12][2].text
                    ra_3 = year[12][3].text
                    ra_4 = year[12][4].text
                    ra_5 = year[12][5].text
                    ra_6 = year[12][6].text
                    ra_7 = year[12][7].text
                    ra_8 = year[12][8].text
                    ra_9 = year[12][9].text
                    ra_10 = year[12][10].text
                    ra_11 = year[12][11].text
                    ra_12 = year[12][12].text
                    ra_13 = year[12][13].text
                    ra_14 = year[12][14].text
                    ra_15 = year[12][15].text
                    ra_16 = year[12][16].text
                    ra_18 = year[12][17].text
                    OT = ("")
                    SP = ("")
                    abcd.write("%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s\n" % (
                        IT, name, exp, SP, OT, ra_17, ra_1, ra_2, ra_3, ra_4, ra_5, ra_6, ra_7, ra_8, ra_9, ra_10,
                        ra_11, ra_12, ra_13, ra_14, ra_15, ra_16, ra_18))



            for dec in root.iter("oopPf"):
                name = dec[1].text

                for ser in dec.iter("series"):
                    exp = ser[0].text
                    # IT = str(ser[10].tag)
                    if 'NIFTY' in name:
                        IT = "OPTIDX"
                    else:
                        IT = "OPTSTK"

                    for opt in ser.findall("opt"):
                        OT = opt[1].text
                        OT = OT + 'E'
                        SP = opt[2].text
                        # print(name, exp,OT,SP)

                        ara_17 = opt[3].text
                        ara_1 = opt[6][1].text
                        ara_2 = opt[6][2].text
                        ara_3 = opt[6][3].text
                        ara_4 = opt[6][4].text
                        ara_5 = opt[6][5].text
                        ara_6 = opt[6][6].text
                        ara_7 = opt[6][7].text
                        ara_8 = opt[6][8].text
                        ara_9 = opt[6][9].text
                        ara_10 = opt[6][10].text
                        ara_11 = opt[6][11].text
                        ara_12 = opt[6][12].text
                        ara_13 = opt[6][13].text
                        ara_14 = opt[6][14].text
                        ara_15 = opt[6][15].text
                        ara_16 = opt[6][16].text
                        ara_18 = opt[6][17].text
                        abcd.write("%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s\n" % (
                            IT, name, exp, SP, OT, ara_17, ara_1, ara_2, ara_3, ara_4, ara_5, ara_6, ara_7, ara_8,
                            ara_9, ara_10, ara_11, ara_12, ara_13, ara_14, ara_15, ara_16, ara_18))

        abcd.close()
        print("span coppied sucessfully ................")
    except:
        print(traceback.print_exc())


def getSpanMargin():
    spanFile = os.path.join(downloadLoc, 'span.csv')
    span1 = pd.read_csv(spanFile,
                        names=['ins', 'symbol', 'exp', 'strk', 'opt', 'close', 's1', 's2', 's3', 's4', 's5', 's6',
                               's7', 's8', 's9', 's10', 's11', 's12', 's13', 's14', 's15', 's16', 'delta'])

    contract = pd.DataFrame(contract_fo[:, [2, 5, 3, 6, 7, 8, 12]],
                            columns=['Token', 'ins', 'symbol', 'exp', 'strk', 'opt', 'strk1'])
    span1.iloc[:, 4] = span1.iloc[:, 4].fillna(' ')
    span1.iloc[:, 3] = span1.iloc[:, 3].fillna(0.0)
    span1.iloc[:, 2] = span1.iloc[:, 2].astype(str)

    spanMargin = pd.merge(contract, span1, how='left', left_on=['symbol', 'exp', 'strk1', 'opt'],
                               right_on=['symbol', 'exp', 'strk', 'opt']).to_numpy()
    return spanMargin




def getEODSpan():
    eodSpanfile()
    parseSpan_margin()
    parseSpan_calSpred()
    parseSpan_spread()

# EODspanMargin = getSpanMargin()

