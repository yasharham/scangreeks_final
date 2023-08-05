import os,requests,datetime,traceback
import numpy as np
import pandas as pd
from Utils.configReader import readConfigFile

API = readConfigFile()
# API_IP = API[0]

API_IP = "http://192.168.103.11:3333"

loc = os.getcwd().split('ScanGreeks')
directory = os.path.join(loc[0],"ScanGreeks/Download/Apidocuments")

# global mainAel,maincontract_eq,maincontract_fo,mainspan,mainindxbhav,maincalspread

def deleteOldFiles():
    # Get today's date
    today = datetime.date.today()

    # Iterate over the files in the directory
    for filename in os.listdir(directory):
        filepath = os.path.join(directory, filename)
        # Check if the file was not modified today
        if not datetime.date.fromtimestamp(os.path.getmtime(filepath)) == today:
            # Delete the file
            os.remove(filepath)
            print("y1",f"Deleted file: {filename}")


def spanMargin():
    # global span
    path = os.path.join(directory, 'spanMargin.csv')

    if not os.path.exists(path):
        response = requests.post(f"{API_IP}/v1/dbspanMargin",
                                 {'Content-Type': 'application/json'})
        print("spanMargin",response.status_code)
        if response.status_code == 200:
            with open(path, "wb") as f:
                for chunk in response.iter_content(chunk_size=512):
                    if chunk:
                        f.write(chunk)
            spanM = pd.read_csv(path, low_memory=False, header=None, skiprows=1)
            spanM = spanM.to_numpy()
            return spanM
        else:
            print("x2",traceback.print_exc())
    else:
        spanM = pd.read_csv(path, low_memory=False, header=None, skiprows=1)
        spanM = spanM.to_numpy()
        return spanM


def AEL():
    path = os.path.join(directory, 'AEL.csv')
    if not os.path.exists(path):
        response = requests.post(f"{API_IP}/v1/dbAEL",
                                 {'Content-Type': 'application/json'})
        print("AEL",response.status_code)
        if response.status_code == 200:
            with open(path, "wb") as f:
                for chunk in response.iter_content(chunk_size=512):
                    if chunk:
                        f.write(chunk)
            AEL= pd.read_csv(path, low_memory=False, header=None, skiprows=1)
            AEL_np = AEL.to_numpy()
            return AEL_np
        else:
            print("x1",traceback.print_exc())
    else:
        AEL = pd.read_csv(path, low_memory=False, header=None, skiprows=1)
        AEL_np = AEL.to_numpy()
        return AEL_np


def calspread():
    response = requests.post(f"{API_IP}/v1/dbcalSpred")
    print("calspread", response.status_code)

    if response.status_code == 200:
        calspread = pd.DataFrame(response.json()['data'])[['calSprd_changes','symbol','AEL_Margin','future_price']].values
        return calspread
    else:
        print("3",traceback.print_exc())


def indxbhav():
    path = os.path.join(directory, 'idxbhav.csv')
    if not os.path.exists(path):
        response = requests.post(f"{API_IP}/v1/dbindAT")
        print("indxbhav", response.status_code)
        if response.status_code == 200:
            with open(path, "wb") as f:
                for chunk in response.iter_content(chunk_size=512):
                    if chunk:
                        f.write(chunk)
            idx_bhav = pd.read_csv(path, low_memory=False, header=None, skiprows=1)
            idx_bhav = idx_bhav.to_numpy()
            return idx_bhav
        else:
            print("nb",traceback.print_exc())
    else:
        idx_bhav = pd.read_csv(path, low_memory=False, header=None, skiprows=1)
        idx_bhav = idx_bhav.to_numpy()
        return idx_bhav


def getMaster():
    response = requests.post(f"{API_IP}/v1/dbcontractEQ")
    print("dbcontractEQ",response.status_code)
    if response.status_code == 200:
        contract_eq = response.json()['data']
        contract_eq = pd.DataFrame(contract_eq)
        path = os.path.join(directory, 'contract_eq.csv')
        contract_eq.to_csv(path)
        contract_eq  = contract_eq.to_numpy()
        #contract_eq = contract_eq[:, 1:]

        return contract_eq
    else:
        print("4",traceback.print_exc())



def update_contract_FOletest():
    response = requests.post(f"{API_IP}/v1/dbcontractFO",stream=True)
    print("dbcontractFO",response.status_code)
    if response.status_code == 200:
        path = os.path.join(directory, 'contract_fo.csv')
        with open(path, "wb") as f:
            for chunk in response.iter_content(chunk_size=512):
                if chunk:
                    f.write(chunk)
        contract_fo = pd.read_csv(path, low_memory=False, header=None, skiprows=1).to_numpy()
        nan_array = np.where(contract_fo[:, 1] == 'x')
        non_nan_array = np.where(contract_fo[:, 1] != 'x')
        contract_fo[nan_array, 6] = ''
        contract_fo[non_nan_array, 6] = contract_fo[non_nan_array, 6].astype('int')
        contract_fo[non_nan_array, 6] = contract_fo[non_nan_array, 6].astype('str')
        return contract_fo
    else:
        print(5,traceback.print_exc())





deleteOldFiles()
span = spanMargin()
Ael = AEL()
calSpread = calspread()
contract_eq = getMaster()
contract_fo = update_contract_FOletest()
idxbhav = indxbhav()

















# @router.post('/v1/dbspanMargin', tags=['Scangreeks'])
# def dbspanMargin():
#     data = list(spanMargin_collection.find({}, {'_id': 0}))
#     loc1 = getcwd().split('FAST_API')
#     downloadLoc = path.join('Downloads', 'spanMargin.csv')
#     # path = os.path.join(fr"\\192.168.113.60\Users\contractFO_raw.txt")
#     with open(downloadLoc, 'w', newline='') as csvfile:
#         fieldnames = ['Token','instrument_type', 'symbol', 'exp', 'strike', 'option_type','strike2', 'instrument_type2', 'strike3', 'close', 'S1','S2', 'S3', 'S4', 'S5', 'S6','S7', 'S8', 'S9', 'S10', 'S11','S12', 'S13', 'S14', 'S15', 'S16','delta']
#         writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
#         writer.writeheader()
#         for row in data:
#             writer.writerow(row)
#     return FileResponse(path=downloadLoc, filename='spanMargin.csv')



# def readmaster(main):
#     # global contract_eq,contract_fo
#     try:
#         eq_path = os.path.join(directory, 'contract_eq.csv')
#         fo_path=os.path.join(direct, 'contract_fo.csv')
#
#         eq_contract = pd.read_csv(eq_path, low_memory=False, header=None, skiprows=1)
#         contract_eq = eq_contract.to_numpy()
#         main.contract_eq = contract_eq[:, 1:]
#
#         fo_contract = pd.read_csv(fo_path, low_memory=False, header=None, skiprows=1)
#
#         main.contract_fo = fo_contract.to_numpy()
#
#         nan_array = np.where(main.contract_fo[:, 1] == 'x')
#         non_nan_array = np.where(main.contract_fo[:, 1] != 'x')
#         main.contract_fo[nan_array, 6] = ''
#         main.contract_fo[non_nan_array, 6] = main.contract_fo[non_nan_array, 6].astype('int')
#         main.contract_fo[non_nan_array, 6] = main.contract_fo[non_nan_array, 6].astype('str')
#
#     except:
#         print(traceback.print_exc())