"""Some simple examples of simplerestclient.SimpleRESTClient"""

__author__ = "Alan Evans <alanwevans@gmail.com>"

import json
import lorem
from simplerestclient import SimpleRESTClient

client = SimpleRESTClient(
    'https://jsonplaceholder.typicode.com/',
    verify = True)

print json.dumps(client.get('posts/1').json(), indent=4)


resp = client.put('posts/%d' % 1,
        json={'body': lorem.paragraph()})

print 'updated post id: %d, status_code: %d, content: %s' % (
        1, resp.status_code, resp.content)

post = client.post('posts',
        json = {
            'author_id': 1,
            'title': lorem.sentence(),
            'body': lorem.paragraph(),
            }
        ).json()
print 'created post: ', json.dumps(post, indent=4)
