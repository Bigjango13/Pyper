# Needed for fileServerExample
from os.path import basename, exists

import pyper

# Set pyper to a new pyper server running on port 8080 (not 60 because ports under 1024 need root on *nix).
pyperServer = pyper.server.PyperServer(port=8080)


@pyperServer.parseRequest("/")
def homePageExample(request):
    # An example of text
    # The return value is (contentType, content)
    return pyper.common.ascii, "Helloworld"


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
                # Read the file as binary and send it
                with open(file, "rb") as f:
                    return pyper.common.file, f.read()

    # Return not found message.
    # I am not using pyper.common.notFound becuase then people can't tell if
    # the page doesn't exist or just the file doesn't exist
    return pyper.common.ascii, "File not found"


@pyperServer.parseRequest("/redirect")
def redirectExample(request):
    # Note: Don't include the first slash in redirects.
    # This will redirect to a download of this file.
    return pyper.common.redirect, "download?file=" + basename(__file__)


@pyperServer.parseRequest("/error")
def internalServerErrorExample(request):
    # An example of a internal server error
    raise Exception


@pyperServer.parseRequest("*")
def fallbackExample(request):
    # An example on how can fallback on a function if a path isn't mapped.
    if request["path"] == "/erorr":
        # Redirect from a typo to error
        return pyper.common.redirect, "error"
    else:
        # Return a custom 0x22 message.
        return pyper.common.utf8, "Oh no! Page not found."


# Start running the app.
pyperServer.start()
