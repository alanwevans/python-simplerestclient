import requests
import urlparse

__author__ = "Alan Evans <alanwevans@gmail.com>"
__version__ = "1.0.0"

class SimpleRESTClient(requests.Session):
    def __init__(self, base_url,
            auth=None,
            cert=None,
            verify=True,
            user_agent='python-%s/%s' % (__name__, __version__),
            accept='application/json',
            content_type='application/json',
            headers={},
            *args, **kwargs):
        super(SimpleRESTClient, self).__init__(*args, **kwargs)
        if not base_url.endswith('/'):
            raise Warning("base_url does not end with '/'")
        self.base_url = base_url
        if type(auth) == tuple:
            self.auth = auth
        self.verify = verify
        self.headers.update(headers)
        self.headers['accept'] = accept
        self.headers['content-type'] = content_type
        self.headers['user-agent'] = user_agent

    def request(self, method, url, *args, **kwargs):
	url = urlparse.urljoin(self.base_url, url)
        if not 'verify' in kwargs:
            kwargs['verify'] = self.verify
        return super(SimpleRESTClient, self).request(
		method=method, url=url, *args, **kwargs)
