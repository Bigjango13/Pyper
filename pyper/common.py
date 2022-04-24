from os import environ

# Misc
pyperDebug = bool(environ.get("PYPER_DEBUG"))
piperSpecVersion = "0.8.0"

# Content types
utf8 = "00"
gemtext = "01"
ascii = "02"
file = "10"
redirect = "20"
notFound = "22"
internalError = "23"
specVersion = "24"

# Content types borrowed from libpiper
clientOutOfMemory = "F0"
clientConnectionError = "F1"
clientInternalError = "F2"

# Extra one I added myself
clientInvalidData = "F3"

# Content Type dict
contentType = {
    utf8: "UTF8",
    gemtext: "Gemtext",
    ascii: "ASCII",
    file: "File",
    redirect: "Redirect",
    notFound: "Content not found",
    internalError: "Internal server error",
    specVersion: "Diffrent specification version. (Currently on version "
    + piperSpecVersion
    + ")",
    clientOutOfMemory: "Out of memory",
    clientConnectionError: "Connection error",
    clientInternalError: "Internal client error",
    clientInvalidData: "Invalid data",
}
