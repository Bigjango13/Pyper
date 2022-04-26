import socketserver
import struct
import urllib.parse
from urllib.parse import urlparse

from pyper.common import pyperDebug

pathToFunc = {}


class PyperServer:
    def __init__(self, port=60):
        """Takes the ip and port of the server and binds the pyper server to the ip and port

        :param ip: The ip to bind the server to
        :type path: str
        :param port: The port to bind the server to, defualts to 60
        :type port: int"""
        self.port = port
        self.serverClass = PyperTCPServer
        self.server = socketserver.TCPServer(("0.0.0.0", port), self.serverClass)
        self.server.allow_reuse_address = True

    def start(self):
        """Starts the pyper server"""
        print("Started server on 0.0.0.0:" + str(self.port) + ".")
        print("Ctrl+C to quit.")
        try:
            with self.server:
                self.server.serve_forever()
        except KeyboardInterrupt:
            # Backspace over the "^C" text
            print("\b\b", end="")
            # Close the socket.
            # TODO: Fix the bug where the socket doesn't close.
            self.server.shutdown()
            self.server.server_close()

    def parseRequest(self, path):
        """The wrapper factory that allows function to be mapped to piper url paths, not meant to be called directly, meant to be used as a decorator

        :param path: The piper url path to be mapped to the function
        :type path: str

        :rtype: function
        :return: wrapper"""

        def wrapper(func):
            """The wrapper itself"""
            pathToFunc.update({path: func})
            # Leaves the function as it is.
            return func

        return wrapper


class PyperTCPServer(socketserver.BaseRequestHandler):
    def handle(self):
        """Handles a connection"""
        self.data = self.request.recv(4096)
        self.fmtAddress = ":".join(map(str, self.client_address))
        self.error = None

        if pyperDebug:
            print(self.data)
        # Unpacks the URL in the request
        try:
            unpackedRequest = struct.unpack(
                "<H%ds" % struct.unpack("<H", self.data[0:2])[0], self.data
            )[1].decode()
        except:
            self.request.close()
            return
        # Set path
        path = urlparse(unpackedRequest).path
        path = path if path else "/"
        # Log the request
        print("<" + self.fmtAddress + ">", path)
        # Set the default to 0x22 (Not found)
        self.contentType, self.returndata = "22", b""
        # Turn the url options into a dict
        options = dict(
            urllib.parse.parse_qsl(urllib.parse.urlsplit(unpackedRequest).query)
        )
        if path in pathToFunc.keys() or "*" in pathToFunc.keys():
            try:
                if path in pathToFunc.keys():
                    self.contentType, self.returndata = pathToFunc[path](
                        {
                            "client_addr": self.client_address,
                            "options": options,
                            "path": path,
                        }
                    )
                # Allows falling back to "*" if a path isn't mapped to a function
                elif "*" in pathToFunc.keys():
                    self.contentType, self.returndata = pathToFunc["*"](
                        {
                            "client_addr": self.client_address,
                            "options": options,
                            "path": path,
                        }
                    )
            except Exception as e:
                self.error = e
                self.contentType, self.returndata = "23", b""

        self.contentType = bytes.fromhex(self.contentType)
        # Encode the data to bytes
        self.returnDataEncoded = self.returndata
        if self.contentType in b"\x00\x01\x20":
            self.returnDataEncoded = bytes(self.returndata, "utf-8")
        elif self.contentType == b"\x02":
            self.returnDataEncoded = bytes(self.returndata, "ascii")
        elif self.contentType == b"\x22\x23":
            # 0x22 and 0x23 don't need data, until they do pyper will force them to use no data
            self.returnDataEncoded = b""

        # Pack the data
        self.rawData = struct.pack(
            "<Q%ds" % len(self.returnDataEncoded),
            len(self.returnDataEncoded),
            self.returnDataEncoded,
        )
        # Add the content type
        self.rawData = self.contentType + self.rawData
        if pyperDebug:
            print(self.rawData)
        self.request.send(self.rawData)
        self.request.close()
        if self.error:
            raise self.error
