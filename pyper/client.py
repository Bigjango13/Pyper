import socket
import struct
import urllib.parse

from pyper.common import pyperDebug


def getUrlRedirect(originalUrl: str, originalUrlPort: int = 60, url: str = "/") -> str:
    """Gets the url to redirect to.

    :param originalUrl: The url you are currently on
    :type originalUrl: str
    :param originalUrlPort: The port you are currently on
    :type originalUrlPort: int, defaults to 60
    :param url: The url originalUrl is telling you to redirect to
    :type url: str
    """
    if url.startswith("piper://"):
        return connectFromUrl(url)
    else:
        return connectFromUrl(
            "piper://" + originalUrl + ":" + str(originalUrlPort) + ("/" + url)
        )


def getHostname(ip: str, port: int, path: str, args: dict = {}) -> str:
    """Formats a hostname from the ip, port, path, and args

    :param ip: The hostname/IP of the server
    :type ip: str
    :param port: The server port, defaults to 60
    :type port: int
    :param path: The path to go to on the server, defaults to /
    :type path: str
    :param args: The args to send to the server, defaults to {}
    :type args: dict

    :rtype: str
    :return: hostname"""
    hostname = "piper://" if not ip.startswith("piper://") else ""
    hostname += ip
    hostname += ":" + str(port)
    if path not in ["/", ""]:
        if not path.startswith("/"):
            hostname += "/"
        hostname += path
    if args:
        hostname += "?" + urllib.parse.urlencode(args)
    return hostname


def connectFromUrl(url: str) -> str:
    """Gets the args for pyper.client.connect (execpt for redirectsAllowed) from a url.

    :param url: The URL
    :type url: str

    :rtype: (str, int, str, dict)
    :return: (ip, port, path, options)"""
    url = url if url.startswith("piper://") else "piper://" + url
    data = urllib.parse.urlparse(url)
    server = data.netloc
    port, path, options = 60, "/", dict()
    if server.find("[", 0, 2) == -1:
        if server.find(":", 0, len(server)) == -1:
            ip = server
        else:
            ip, port = server.split(":")
    else:
        # IPv6 support
        index = server.find("]", 0, len(server))
        if index == -1:
            new_ip = "localhost"
        else:
            if server.find(":", index, len(server)) == -1:
                new_ip = server
            else:
                new_ip, port = server.rsplit(":", 1)
        ip = new_ip.strip("[]")

    try:
        port = int(port)
    except ValueError:
        port = 60
    path = data.path if data.path else ""
    options = dict(urllib.parse.parse_qsl(urllib.parse.urlsplit(url).query))
    args = {"ip": ip, "port": port, "path": path, "args": options}
    return args


def connect(
    ip: str,
    port: int = 60,
    path: str = "/",
    args: dict = dict(),
    redirectsAllowed: int = 10,
):
    """Connects to a piper server and return the ID and data of the server reponse

    :param ip: The hostname/IP of the server
    :type ip: str
    :param port: The server port, defaults to 60
    :type port: int
    :param path: The path to go to on the server, defaults to /
    :type path: str
    :param args: The args to send to the server, defaults to {}
    :type args: dict
    :param redirectsAllowed: A number of the amount of redirects allowed, if it is -1 then infinite redirects are allowed, defaults to 10
    :type redirectsAllowed: int

    :rtype: (str, Union[str, bytes])
    :return: (ID, content)
    """
    hostname = getHostname(ip, port, path, args)
    # Remove the "piper://hostname:port" part
    hostname = hostname[hostname.index(str(port)) + len(str(port)) :]
    # Connect the socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((ip, port))
    # Pack the request
    request = struct.pack(
        "<H%ds" % len(hostname), len(hostname), hostname.encode("utf-8")
    )
    if pyperDebug:
        print(request)
    sock.sendall(request)
    # Receive the data
    received = b""
    while (data := sock.recv(4096)) != b"":
        received += data
    try:
        # Unpack the data
        receivedUnpacked = struct.unpack(
            "<Q%ds" % struct.unpack("<Q", received[1:9])[0], received[1:]
        )[1]
        if pyperDebug:
            print(received)
    except:
        return "F3", received
    # Set the default message
    msg = (
        "The data was fomatted incorrectly or an error occurred, here is the raw data: "
        + str(received)
    )
    id = received[0:1]
    # Don't let the server send client side content types
    if id.hex().upper()[1] == "F":
        return "F3", received
    if id in b"\x00\x01":
        # Gemtext and unicode
        msg = receivedUnpacked.decode("utf-8")
    elif id == b"\x02":
        # ASCII
        msg = receivedUnpacked.decode("ascii")
    elif id == b"\x10":
        # File transfer
        msg = receivedUnpacked
    elif id == b"\x20":
        # Redirect
        newUrl = receivedUnpacked.decode("utf-8")
        msg = getUrlRedirect(ip, port, newUrl)
        if redirectsAllowed:
            id, msg = connect(**msg, redirectsAllowed=redirectsAllowed - 1)
        else:
            msg = getHostname(**msg)
    elif id == b"\x22":
        # Resource not found
        msg = "0x22: Resource not found. :("
    elif id == b"\x23":
        # Internal server error
        msg = "0x23: Internal server error."
    elif id == b"\x24":
        # Wrong spec version
        msg = "0x24: Wrong Specification Version."
    # Use .hex() to return the hex as a string. ("aa" instead of b"\xaa")
    return id.hex().upper(), msg
