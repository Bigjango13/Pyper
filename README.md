# Pyper
The [Piper](https://github.com/Luminoso-256/piper) networking protocol in Python.

## How to install?

I haven't uploaed to pip yet, until then it can be installed with
```bash
pip3 install git+https://github.com/Bigjango13/Pyper
```

## How to use?

An example server and an example client can be found under the [examples](https://github.com/Bigjango13/Pyper/tree/main/examples) directory.

### Client

#### `getUrlRedirect(originalUrl, originalUrlPort, url)`

Takes the current url, the current port, and the url that the current url is telling you to redirect to.

Gets the url to redirect to and returns the arguments for `pyper.client.connect`.

#### `getHostname(ip, port, path, args)`

Return the formated url.

#### `connectFromUrl(url)`

Returns the arguments for `pyper.client.connect` (excluding `redirectsAllowed`) from a piper url. 

#### `connect(ip, port, path, options, redirectsAllowed)`

Connects to a piper server based on the ip, port, path, and options.

If `redirectsAllowed` is not equal to zero it will also automatically follow redirects and remove one from `redirectsAllowed`, if it is set below zero it will always redirect.

### Server

#### `PyperServer`

##### `__init__(ip, port)`

Creates a pyper server and binds it to the ip and port.

##### `start()`

Starts the server.

##### `parseRequest(path)`

Meant to be used as a decorator, it maps a function to a path.

For example:

```py
import pyper

pyperServer = pyper.server.PyperServer()

@pyperServer.parseRequest("/")
def index(request):
    return pyper.ascii, "This is the index"

pyperServer.start()
```

