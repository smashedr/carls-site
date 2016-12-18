from django.shortcuts import render
import logging
import requests
from urllib.parse import parse_qs
from carls_site.settings import config

logger = logging.getLogger(__name__)


def home(request):
    # View: /
    pgdata = {'client_id': config.get('GitHub', 'client_id')}
    return render(request, 'home.html', {
        'pgdata': pgdata,
    })


def github(request):
    # View: /github/
    pgdata = {'success': False}
    if 'code' in request.GET and 'state' in request.GET:
        code = request.GET['code']
        state = request.GET['state']
        try:
            results = github_token(code)
            # save_token('shane', results)
            access_token = results['access_token'][0]
            ship_it(state, access_token)
            if ship_it:
                pgdata['success'] = True
            else:
                pgdata['error'] = 'Unable to verify request.'
        except Exception as error:
            logger.exception(error)
            pgdata['error'] = error
    else:
        pgdata['error'] = 'Unable to parse: code or state'

    return render(request, 'github.html', {
        'pgdata': pgdata,
    })


def ship_it(state, access_token):
    try:
        logger.info(state + ' - ' + access_token)
        data = {
            'state': state,
            'access_token': access_token,
        }
        r = requests.post(url=config.get('Api', 'github_uri'), data=data)
        response = r.json()
        if response['success']:
            return True
        else:
            return False
    except Exception as error:
        logger.exception(error)
        return False


def github_token(code):
    uri = 'https://github.com/login/oauth/access_token'
    data = {
        'client_id': config.get('GitHub', 'client_id'),
        'client_secret': config.get('GitHub', 'client_secret'),
        'code': code,
    }
    r = requests.post(uri, data=data)
    logger.info(r.text)
    results = parse_qs(r.text)
    logger.info(results)
    return results
