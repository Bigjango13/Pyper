# Needed for fileServerExample
from os.path import exists

import pyper

# Set pyper to a new pyper server running on port 8080 (not 60 because ports under 1024 need root).
pyper = pyper.server.PyperServer(port=8080)


@pyper.parseRequest("/")
def homePageExample(request):
    # 0x02 is Ascii, you can also return Unicode (0x00), and Unicode Gentext (0x01)
    return b"\x02", "Helloworld"


@pyper.parseRequest("/download")
def fileServerExample(request):
    # Checks if "file" is an option
    if "file" in request["options"].keys():
        # Get the file and check if it exists
        file = request["options"]["file"]
        if exists(file):
            # Don't allow directory backtracking.
            if not file.startswith(".."):
                # Read the file as bianary and send it
                with open(__file__, "rb") as f:
                    return b"\x10", f.read()

    # Return not found message.
    # I am not using 0x22 becuase then people can't tell if
    # the page doesn't exist or just the file doesn't exist
    return b"\x02", "File not found"


@pyper.parseRequest("/redirect")
def redirectExample(request):
    # Note: Don't include the first slash in redirects.
    # This will redirect to a download of this file.
    return b"\x20", "download?file=" + __file__


# Start running the app.
pyper.start()
