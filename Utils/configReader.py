import sys,logging,os,json,traceback

loc = os.getcwd().split('ScanGreeks')
config_location = os.path.join(loc[0],  'ScanGreeks/Settings/configJSON.json')

# config_location = "/home/arham001/Yash/ScanGreeksBackend/setting/configJSON.json"

def readConfigFile():

    try:
        f1 = open(config_location)
        jConfig = json.load(f1)

        API_IP = jConfig["API_IP"]
        HOLIDAY_LIST = jConfig["HOLIDAYS"]

        f1.close()
        data = [API_IP,HOLIDAY_LIST]
        return data
    except:
        logging.error(sys.exc_info()[1])
        print(traceback.print_exc())


def readConfigServer():
    try:
        f1 = open(config_location)
        jConfig = json.load(f1)

        HOST = jConfig['HOST']
        PORT = jConfig['PORT']
        DB_PATH = jConfig['DB_PATH']

        f1.close()
        data = [HOST, PORT, DB_PATH]
        return data
    except:
        print(traceback.print_exc())



