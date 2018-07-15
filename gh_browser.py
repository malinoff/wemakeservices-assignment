import os

import requests
from flask import Flask, url_for, request

GITHUB_CLIENT = os.environ['GITHUB_CLIENT']
GITHUB_SECRET = os.environ['GITHUB_SECRET']

template = '''
<html>
  <head>
    <style>
    .content * {{padding: 0.8em;}}
    </style>
  </head>
  <body>
    <div class="content">
    {content}
    </div>
    Created by <a href="https://github.com/malinoff">https://github.com/malinoff</a>,
    source code: <a href="https://github.com/malinoff/wemakeservices-assignment">https://github.com/malinoff/wemakeservices-assignment</a>.
  </body>
</html>
'''


app = Flask(__name__)


@app.route('/')
def index():
    content = f'''
    <form action="https://github.com/login/oauth/authorize" method="get">
      <input type="hidden" name="client_id" value="{GITHUB_CLIENT}">
      <input type="hidden" name="redirect_url" value="{url_for('github')}">
      <button type="submit">Log in with Github</button>
    </form>
    '''
    return template.format(content=content)


@app.route('/github')
def github():
    code = request.args['code']
    access_token = _get_access_token(code)
    user = _get_github('user', access_token)
    header = f'''
    <div>
      <img src="{user['avatar_url']}" height="200" width="200">
      <span>{user['name']}</span>
    </div>
    '''
    repos = '\n'.join([
        f"<li><a href=\"{repo['html_url']}\">{repo['name']}</a></li>"
        for repo in _get_github('user/repos', access_token)
    ])
    repos = f'''
    Repositories:
    <ul>
    {repos}
    </ul>
    '''
    return template.format(content=header + repos)


def _get_access_token(code):
    response = requests.post(
        'https://github.com/login/oauth/access_token',
        headers={'Accept': 'application/json'},
        json={
            'client_id': GITHUB_CLIENT,
            'client_secret': GITHUB_SECRET,
            'code': code,
        },
    )
    response.raise_for_status()
    return response.json()['access_token']


def _get_github(endpoint, access_token):
    response = requests.get(
        f'https://api.github.com/{endpoint}',
        headers={
            'Accept': 'application/vnd.github.v3+json',
            'Authorization': f'token {access_token}',
        },
    )
    response.raise_for_status()
    return response.json()
