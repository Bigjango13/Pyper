# Needed for fileServerExample
from os.path import basename, exists

import pyper

# Set pyper to a new pyper server running on port 8080 (not 60 because ports under 1024 need root).
pyperServer = pyper.server.PyperServer(port=8080)


@pyperServer.parseRequest("/")
def homePageExample(request):
    # An example of text
    # The return value is (contentType, content)
    return pyper.ascii, "Helloworld"


@pyperServer.parseRequest("/download")
def fileExample(request):
    # A file download example
    # Checks if "file" is an option
    if "file" in request["options"].keys():
        # Get the file and check if it exists
        file = request["options"]["file"]
        if exists(file):
            # Don't allow directory backtracking.
            if not (file.startswith("..") or file.startswith("/")):
                # Read the file as bianary and send it
                with open(__file__, "rb") as f:
                    return pyper.file, f.read()

    # Return not found message.
    # I am not using pyper.notFound becuase then people can't tell if
    # the page doesn't exist or just the file doesn't exist
    return pyper.ascii, "File not found"


@pyperServer.parseRequest("/redirect")
def redirectExample(request):
    # Note: Don't include the first slash in redirects.
    # This will redirect to a download of this file.
    return pyper.redirect, "download?file=" + basename(__file__)


@pyperServer.parseRequest("/error")
def internalServerErrorExample(request):
    # An example of a internal server error
    raise Exception


# Start running the app.
pyperServer.start()
