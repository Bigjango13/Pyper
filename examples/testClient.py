# Used for file downloading
from os.path import basename

import pyper


# The client is extremly simple, just pyper.client.connectFromUrl and pyper.client.connect
def connectAndPrint(server):
    # Get the args for pyper.client.connect from the hostname
    args = pyper.client.connectFromUrl(server)
    try:
        # Connect to the server, used *args to turn the args list into function arguments.
        id, content = pyper.client.connect(*args, 0)
    except ConnectionRefusedError:
        # If it fails
        print("Unknown host, the server may not be running")
    else:
        # Handle the data send by the server
        # Content
        if id == "00":
            print("[UTF-8]: " + content)
        elif id == "01":
            print("[Gemtext]: " + content)
        elif id == "02":
            print("[ASCII]: " + content)
        # Files
        elif id == "10":
            # args[2] is the path
            file = basename(args[2])
            downloadYN = input('Would you like to download "' + file + '"? ').lower()
            if downloadYN in ["yes", "y"]:
                with open(file, "wb+") as f:
                    f.write(content)
        # "Status-code like things"
        elif id == "20":
            downloadYN = input(
                'Would you like to be redirected to "' + content + '"? '
            ).lower()
            if downloadYN in ["yes", "y"]:
                connectAndPrint(content)
        elif id == "22":
            print("[Error]: Resource not found.")
        elif id == "23":
            print("[Error]: Internal server error.")
        elif id == "24":
            print("[Error]: Diffrent Spec Version. Client version:" + pyper.specVersion)
        # Unknown id
        else:
            print("[Error]: Unknown code, here is the raw data:", id, content)


server = input("Enter the server URL: ").strip()
connectAndPrint(server)
