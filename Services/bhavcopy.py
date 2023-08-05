from os import path,getcwd,remove,rename
import requests,zipfile,traceback,os
from datetime import datetime,timedelta,date


loc = getcwd().split('ScanGreeks')
downloadLoc = os.path.join(loc[0],"ScanGreeks/Download/Bhavcopy")
today =date.today()


def deleteBhavcopy():
    today = date.today()
    # Iterate over the files in the directory
    for filename in os.listdir(downloadLoc):
        filepath = os.path.join(downloadLoc, filename)
        # Check if the file was not modified today
        if not date.fromtimestamp(os.path.getmtime(filepath)) == today:
            # Delete the file
            os.remove(filepath)
            print(f"Deleted file: {filename}")


def get_previous_bhavcopy():
    try:
        deleteBhavcopy()
        diffdays = 1
        if(today.weekday()==0):
            diffdays = 3

        fetchDate = datetime.today() - timedelta(days=diffdays)

        fo_bhav1 = "https://archives.nseindia.com/content/historical/DERIVATIVES/" + fetchDate.strftime(
            '%Y') + r"/" + fetchDate.strftime('%b').upper() + r"/fo" + fetchDate.strftime(
            "%d%b%Y").upper() + "bhav.csv.zip"

        cm_bhav = "https://archives.nseindia.com/content/historical/EQUITIES/" + fetchDate.strftime(
            '%Y') + r"/" + fetchDate.strftime(
            '%b').upper() + r"/cm" + fetchDate.strftime("%d%b%Y").upper() + r"bhav.csv.zip"

        ind_bhav = r"https://archives.nseindia.com/content/indices/ind_close_all_" + fetchDate.strftime(
            '%d%m%Y') + ".csv"

        print("fo_bhav",fo_bhav1)
        re = requests.get(fo_bhav1)
        trial = 0

        while(re.status_code != 200):
            if(trial >5):
                print('error while downloading bhavcopy')
                break
            diffdays += 1
            fetchDate = datetime.today() - timedelta(days=diffdays)

            fo_bhav1 = "https://archives.nseindia.com/content/historical/DERIVATIVES/" + fetchDate.strftime(
                '%Y') + r"/" + fetchDate.strftime('%b').upper() + r"/fo" + fetchDate.strftime(
                "%d%b%Y").upper() + "bhav.csv.zip"

            re = requests.get(fo_bhav1)
            trial +=1

        date = fetchDate.strftime('%d%b%Y').upper()


        ############################## FO_Bhav ######################################

        fobhavLoc = path.join(downloadLoc,"fo_bhav.zip")
        with open(fobhavLoc, 'wb+') as f:
            f.write(re.content)
        f.close()

        zf = zipfile.ZipFile(fobhavLoc, 'r')
        zf.extractall(downloadLoc)
        os.remove(os.path.join(downloadLoc, "fo_bhav.zip"))
        zf.close()

        if path.isfile(path.join(downloadLoc,"fo_bhav.csv")):
            os.remove(path.join(downloadLoc,"fo_bhav.csv"))
        fname = path.join(downloadLoc,'fo' + date + 'bhav.csv')

        os.rename(fname, path.join(downloadLoc,'fo_bhav.csv'))

        ############################## CM_Bhav ######################################

        print("cm_bhav",cm_bhav)
        req = requests.get(cm_bhav)
        cmBHavLoc = path.join(downloadLoc,"cm_bhav.zip")
        with open(cmBHavLoc, 'wb') as f:
            f.write(req.content)
        f.close()

        zf = zipfile.ZipFile(cmBHavLoc, 'r')
        zf.extractall(downloadLoc)
        os.remove(os.path.join(downloadLoc, "cm_bhav.zip"))
        zf.close()

        if path.isfile(path.join(downloadLoc,"cm_bhav.csv")):
            os.remove(path.join(downloadLoc,"cm_bhav.csv"))
        fname = path.join(downloadLoc,'cm' + date + 'bhav.csv')
        os.rename(fname, path.join(downloadLoc,'cm_bhav.csv'))


        ############################## IND_Bhav ######################################
        print("ind_bhav",ind_bhav)
        rez = requests.get(ind_bhav)
        with open(path.join(downloadLoc,"idx_bhav.csv"), 'wb') as f:
            f.write(rez.content)
        f.close()

    except:
        print("error",traceback.print_exc())


def get_today_bhavcopy():
    try:
        deleteBhavcopy()
        fetchDate = datetime.today()

        fo_bhav1 = "https://archives.nseindia.com/content/historical/DERIVATIVES/" + fetchDate.strftime(
            '%Y') + r"/" + fetchDate.strftime('%b').upper() + r"/fo" + fetchDate.strftime(
            "%d%b%Y").upper() + "bhav.csv.zip"

        cm_bhav = "https://archives.nseindia.com/content/historical/EQUITIES/" + fetchDate.strftime(
            '%Y') + r"/" + fetchDate.strftime(
            '%b').upper() + r"/cm" + fetchDate.strftime("%d%b%Y").upper() + r"bhav.csv.zip"

        ind_bhav = r"https://archives.nseindia.com/content/indices/ind_close_all_" + fetchDate.strftime(
            '%d%m%Y') + ".csv"

        print("fo_bhav", fo_bhav1)
        re = requests.get(fo_bhav1)
        trial = 0

        while (re.status_code != 200):
            if (trial > 5):
                print('error while downloading bhavcopy')
                break

            fo_bhav1 = "https://archives.nseindia.com/content/historical/DERIVATIVES/" + fetchDate.strftime(
                '%Y') + r"/" + fetchDate.strftime('%b').upper() + r"/fo" + fetchDate.strftime(
                "%d%b%Y").upper() + "bhav.csv.zip"
            re = requests.get(fo_bhav1)
            trial += 1

        date = fetchDate.strftime('%d%b%Y').upper()

        ############################## FO_Bhav ######################################

        fobhavLoc = path.join(downloadLoc, "fo_bhav.zip")
        with open(fobhavLoc, 'wb+') as f:
            f.write(re.content)
        f.close()

        zf = zipfile.ZipFile(fobhavLoc, 'r')
        zf.extractall(downloadLoc)
        os.remove(os.path.join(downloadLoc, "fo_bhav.zip"))
        zf.close()

        if path.isfile(path.join(downloadLoc, "fo_bhav.csv")):
            os.remove(path.join(downloadLoc, "fo_bhav.csv"))
        fname = path.join(downloadLoc, 'fo' + date + 'bhav.csv')

        os.rename(fname, path.join(downloadLoc, 'fo_bhav.csv'))

        ############################## CM_Bhav ######################################

        print("cm_bhav", cm_bhav)
        req = requests.get(cm_bhav)
        cmBHavLoc = path.join(downloadLoc, "cm_bhav.zip")
        with open(cmBHavLoc, 'wb') as f:
            f.write(req.content)
        f.close()

        zf = zipfile.ZipFile(cmBHavLoc, 'r')
        zf.extractall(downloadLoc)
        os.remove(os.path.join(downloadLoc, "cm_bhav.zip"))
        zf.close()

        if path.isfile(path.join(downloadLoc, "cm_bhav.csv")):
            os.remove(path.join(downloadLoc, "cm_bhav.csv"))
        fname = path.join(downloadLoc, 'cm' + date + 'bhav.csv')
        os.rename(fname, path.join(downloadLoc, 'cm_bhav.csv'))

        ############################## IND_Bhav ######################################
        print("ind_bhav", ind_bhav)
        rez = requests.get(ind_bhav)
        with open(path.join(downloadLoc, "idx_bhav.csv"), 'wb') as f:
            f.write(rez.content)
        f.close()

    except:
        print("error", traceback.print_exc())

# get_today_bhavcopy()

