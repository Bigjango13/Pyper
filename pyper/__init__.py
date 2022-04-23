"""Pyper is a python implementation of the piper networking protocol.
Piper: https://github.com/Luminoso-256/piper
Pyper: https://github.com/Bigjango13/pyper"""
from pyper import client, server

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
# Content Type dict
contentType = {
    utf8: "UTF8",
    gemtext: "Gemtext",
    ascii: "ASCII",
    file: "File",
    redirect: "Redirect",
    notFound: "Content not found",
    internalError: "Internal server error",
    specVersion: "Diffrent specification version. (Currently on version " + piperSpecVersion + ")",
    "F0": "Invalid data",
}

__all__ = ("client", "server")
