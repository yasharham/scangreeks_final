import uvicorn
from Utils.configReader import readConfigServer

data = readConfigServer()
HOST = data[0]
PORT = data[1]

if __name__ == '__main__':
    uvicorn.run("Loader.loader:app", host=HOST, port=PORT)