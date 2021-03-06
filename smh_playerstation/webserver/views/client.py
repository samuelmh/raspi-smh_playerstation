# -*- coding: utf-8 -*-

from flask import request


class Client:

    def __init__(self, app, url_prefix, path_client):
        self.app = app
        self.url_prefix = url_prefix
        self.path_client = path_client
        app.add_url_rule(
            rule=self.url_prefix,
            endpoint='client_client',
            view_func=self.send_client
        )

    def send_client(self):
        page = 'ERROR'
        with open(self.path_client+'/client.html') as f:
            page = f.read() \
                .replace('</body>','') \
                .replace('</html>','') \
                +('<!-- AUTOGENERATED SERVER ENDPOINT URL -->') \
                +('<script>') \
                +('smh_playerstation.url_api_set("{}api/v1.0")').format(request.base_url) \
                +('</script>\n\n') \
                +('</body></html>')
        return page
