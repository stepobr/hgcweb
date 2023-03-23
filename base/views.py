import json
from django.urls import reverse
from django.shortcuts import render, redirect
from authlib.integrations.django_client import OAuth
from hgcweb import settings


# CONF_URL = 'https://auth.cern.ch/auth/realms/cern/.well-known/openid-configuration'
# CONF_URL = 'https://keycloak-qa.cern.ch/auth/realms/cern/.well-known/openid-configuration'
# oauth = OAuth()
# oauth.register(
#     name='cern',
#     server_metadata_url=CONF_URL,
#     client_kwargs={
#         'scope': 'openid email profile'
#     }
# )


def homepage(request):
    user = ''
    logout = ''
    if request.session.get('user'):
        user = request.session.get('user')
        logout = '{}?client_id={}&id_token_hint={}'.format(
                                        settings.OAUTH_LOGOUT, 
                                        settings.OAUTH_CLIENT['client_id'],
                                        # settings.OAUTH_CLIENT['post_logout_redirect_uri'],
                                        user['cern_uid']
                                        )
    # print( request.session.items())
    # if user:
    #     user = json.dumps(user)
    return render(request, 'homepage_entry.html', context={'user': user, 'logout': logout})


def login(request):
    # redirect_uri = request.build_absolute_uri(reverse('auth'))
    # return oauth.cern.authorize_redirect(request, redirect_uri)
    return redirect('/')

# def auth(request):
#     token = oauth.cern.authorize_access_token(request)
#     request.session['user'] = token['userinfo']
#     return redirect('/')

def logout(request):
    request.session.pop('user', None)
    return redirect('/')