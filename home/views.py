import logging
import requests
from django.shortcuts import render, redirect
from django.contrib import messages
from carls_site.settings import config

logger = logging.getLogger(__name__)


def home(request):
    """
    View: /
    """
    return render(request, 'home.html')


def github(request):
    """
    View: /github/
    """
    return render(request, 'github.html')


def github_auth(request):
    """
    View: /github/auth/
    """
    if 'code' in request.GET and 'state' in request.GET:
        code = request.GET['code']
        state = request.GET['state']
        try:
            results = github_token(code)
            access_token = results['access_token']
            ship_it(state, access_token)
            if ship_it:
                messages.add_message(
                    request, messages.SUCCESS,
                    'Account Authorized.',
                )
            else:
                messages.add_message(
                    request, messages.ERROR,
                    'Unable to verify request.',
                )
        except Exception as error:
            logger.exception(error)
            messages.add_message(
                request, messages.ERROR,
                error,
            )
    else:
        messages.add_message(
            request, messages.ERROR,
            'Unable to parse: code or state.',
        )
    return redirect('github')


def ship_it(state, access_token):
    """
    Portable function to ship and verify access_token and state to carl-api
    """
    try:
        logger.info(state + ' - ' + access_token)
        data = {
            'state': state,
            'access_token': access_token,
        }
        r = requests.post(url=config.get('Carl', 'api_uri'), data=data)
        response = r.json()
        if response['success']:
            return True
        else:
            return False
    except Exception as error:
        logger.exception(error)
        return False


def github_token(code):
    """
    Post OAuth code to GitHub and parse response data
    """
    uri = '%s/login/oauth/access_token' % config.get('GitHub', 'base_url')
    data = {
        'client_id': config.get('GitHub', 'client_id'),
        'client_secret': config.get('GitHub', 'client_secret'),
        'code': code,
    }
    headers = {'Accept': 'application/json'}
    r = requests.post(uri, data=data, headers=headers)
    results = r.json()
    logger.info(results)
    return results
