# Pyper
The [Piper](https://github.com/Luminoso-256/piper) networking protocol in Python.

## How to install?

The version on pypi is the stable version, and the version on github is the development version.

To get it from pypi use:
```bash
pip3 install pyper-piper
```

To install from github use:
```bash
pip3 install git+https://github.com/Bigjango13/Pyper
```

If you are making you're own changes to pyper it can be installed with 
```bash
pip3 install path/to/pyper
```

## How to use?

An example server and an example client can be found under the [examples](https://github.com/Bigjango13/Pyper/tree/main/examples) directory.

### Pyper

These are variables that are build directly into the `__init__.py` file of pyper.

#### Piper specification version

The piper specification version that pyper is currently based on can be accesesed throught the `piperSpecVersion` variables.

#### Content types
These content types can be used instead of the ids for content types, here they are:

`utf8` (00)<br>
`gemtext` (01)<br>
`ascii` (02)<br>
`file` (10)<br>
`redirect` (20)<br>
`notFound` (22)<br>
`internalError` (23)<br>
`specVersion` (24)<br>

There is also a dictonary that can be used to translate the ids into more human friendly variants, it is called `contentType`

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

