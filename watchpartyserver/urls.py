"""watchpartyserver URL Configuration"""

from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls import url, include
from django.conf.urls.static import static
from rest_framework import routers
from rest_framework.authtoken.views import obtain_auth_token
from watchpartyserverapi.models import *
from watchpartyserverapi.views import *

router = routers.DefaultRouter(trailing_slash=False)
router.register(r'channels', Channels, 'channel')
router.register(r'channelmembers', ChannelMembers, 'channelmember')
router.register(r'members', Members, 'member')
router.register(r'parties', Parties, 'party')
router.register(r'partyguests', PartyGuests, 'partyguest')
router.register(r'reactions', Reactions, 'reaction')
router.register(r'messagereactions', MessageReactions, 'messagereaction')


urlpatterns = [
    path('admin/', admin.site.urls),
    url(r'^', include(router.urls)),
    url(r'^register$', register_user),
    url(r'^login$', login_user),
    url(r'^api-token-auth$', obtain_auth_token),
    url(r'^api-auth', include('rest_framework.urls', namespace='rest_framework')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
