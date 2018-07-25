# Python Simple Rest Client

I have often found myself needing to interact with RESTful services but not
wanting to install a large dependency set to use some more advanced library.

The `requests` library is very commonly available (including in CentOS 6/7) but
I was constantly repeating things.  [Create session, set headers, set ssl settings,
call `session.get(urljoin())` and so on.]  `requests.Session` does _almost_
everything I would want.  So I subclassed it to do the _rest_ (get it? REST).

## Goals

1. CentOS 6/7 Support
   1. Use core and libraries commonly available in CentOS
   2. Python 2.6 support (CentOS 6)
2. Make no assumptions about the consumed API
   We could go on and on about how this RESTful API or that RESTful API is
   is implemented incorrectly, but I would rather just make my client flexible.
3. Easy to reuse, single class
   Sure it's a bad idea, but I want to be able to copy the Class wholesale into
   the source of some utility script.  For my intended use, packaging this
   library up is overkill.

# Usage

## Basic

```python
client = SimpleRESTClient(
    'https://example.com/api/',
    accept='*/*',
    content_type='application/json;utf8'
)

bars = client.get('foo/1/bars').json()
```

**Note:** the trailing `/` in the baseurl `https://example.com/api/` **<-- here**

Without the trailing slash `urlparse.urljoin()` would think "/api" was a filename
and cut it off when joining urls.

**Also Note:** the lack of a leading slash in the `client.get()` method.

## Authentication

### Basic Auth

The `requests` library supports basic auth and so does `SimpleRESTClient` but be careful
with using `SimpleRESTClient(auth=...)` or `client.auth=('foouser', 'password123')`, this
will cause **EVERY** request to contain an `Authorization` header.  Sometimes this is
necessary, but should be avoided if possible.

#### Preferred

[Katello](https://theforeman.org/plugins/katello/), built on 
[The Foreman](https://theforeman.org/) for example, will send a \_session\_id cookie back 
to the client that can be used in subsequent requests.  `requests.Session` (which
SimpleRESTClient) is built on, will handle the cookies for us.

Other APIs might have ways of generating some kind of token for subsequent requests.  Please
investigate that before simply using `auth=()`.

**Note:** Keep in mind too that depending on the app or server, sending `Authorization`
headers could cause poort response times. Authentication calls to things like LDAP can be
expensive, relatively speaking. 

```python
from getpass import getpass
from simplerestclient import SimpleRESTClient

katello=SimpleRESTClient(
    'https://%s/katello/api/v2/' % socket.getfqdn(),
)

# The katello API has a "ping" resource which does nothing really, so we can use it
# to send our credentials to the server.
resp=katello.get('ping', auth=('admin', getpass()))
if resp.status_code == 401:
    raise Exception('Auth failure...')
elif resp.status_code != 200:
    raise Exception('Some other problem: %s' % resp.content)

envs=katello.get('environments').json()
```

#### Not Ideal

Some APIs however do not use cookies or some kind of token authentication.  **For shame!**

```python
from simplerestclient import SimpleRESTClient

client = SimpleRESTClient(
    'https://oldapp.mycorp.local/API/FooBar/v1.0/',
    auth=('admin', config['somepassword']),
)
```

#### Certificate Authentication

Some APIs ([Pulp](https://pulpproject.org/)) may support authentication by client certificates.

```python
from simplerestclient import SimpleRESTClient

client = SimpleRESTClient(
    'https://%s/pulp/api/' % config['my_pulp_server'],
    cert=os.path.expanduser('~root/.pulp/user-cert.pem'),
)
```

**Note:** Currently it is assumed the cert and private key are both in the same file.  If they
PEM encoded and separated they can simply be concatenated together.

```shell
$ cat /path/to/cert.pem /path/to/key.pem > ~/.my-client-cert.pem
$ chmod 600 ~/.my-client-cert.pem # Please, please! Have your permissions set restrictively.
```
