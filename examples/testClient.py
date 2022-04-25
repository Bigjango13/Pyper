# Used for file downloading
from os.path import basename

import pyper


# The client is extremly simple, just pyper.client.connectFromUrl and pyper.client.connect
def connectAndPrint(server):
    # Get the args for pyper.client.connect from the hostname
    args = pyper.client.connectFromUrl(server)
    try:
        # Connect to the server, used *args to turn the args list into function arguments.
        contentType, content = pyper.client.connect(**args, redirectsAllowed=0)
    except ConnectionRefusedError:
        # If it fails
        print("Unknown host, the server may not be running")
    else:
        # Handle the data send by the server
        # Text
        if contentType in [pyper.common.utf8, pyper.common.gemtext, pyper.common.ascii]:
            print(content)
        # Files
        elif contentType == pyper.common.file:
            file = basename(args["path"])
            downloadYN = input('Would you like to download "' + file + '"? ').lower()
            if downloadYN in ["yes", "y"]:
                with open(file, "wb+") as f:
                    f.write(content)
        # "Status-code like things"
        elif contentType == pyper.common.redirect:
            downloadYN = input(
                'Would you like to be redirected to "' + content + '"? '
            ).lower()
            if downloadYN in ["yes", "y"]:
                connectAndPrint(content)
        elif contentType in [
            pyper.common.notFound,
            pyper.common.internalError,
            pyper.common.specVersion,
        ]:
            print("[Error]:", pyper.common.contentType[contentType])
        # Unknown id
        else:
            print("[Error]: Unknown code, here is the raw data:", contentType, content)


server = input("Enter the server URL: ").strip()
connectAndPrint(server)
