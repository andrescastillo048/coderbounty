from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.contrib.auth.decorators import login_required
from website.views import UserProfileDetailView, IssueDetailView, UserProfileEditView, LeaderboardView
from django.views.generic.base import TemplateView
from rest_framework import routers, serializers, viewsets
from website.models import Issue, Service
from django.contrib.auth.models import User


admin.autodiscover()


urlpatterns = patterns('',
    #url(r'^activity/', include('actstream.urls')),
    url(r'^$', 'website.views.home', name='home'),
    url(r'^about/$', 'website.views.about', name='about'),  
    url(r'^accounts/', include('allauth.urls')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^edit_profile/$', login_required(UserProfileEditView.as_view()), name="edit_profile"),
    url(r'^help/$', 'website.views.help', name='help'),
    url(r'^issue/(?P<slug>\w+)/$', IssueDetailView.as_view(), name="issue"),
    url(r'^leaderboard/$', LeaderboardView.as_view(), name="leaderboard"),
    url(r'^list/$', 'website.views.list', name='list'),
    url(r'^parse_url_ajax/$', 'website.views.parse_url_ajax', name='parse_url_ajax'),
    url(r'^post/$', 'website.views.create_issue_and_bounty', name='post'),
    url(r'^profile/$', 'website.views.profile', name='profile'),
    url(r'^profile/(?P<slug>[\w-]+)/$', UserProfileDetailView.as_view(), name="profile"),
    url(r'^robots.txt$', TemplateView.as_view(template_name='robots.txt')),
    url(r'^terms/$', 'website.views.terms', name='terms'),   
)

class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ('username','date_joined','last_login')

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

class ServiceSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Service
        fields = ('name','domain','template','regex','type','api_url','link_template')

class ServiceViewSet(viewsets.ModelViewSet):
    queryset = Service.objects.all()
    serializer_class = ServiceSerializer

class IssueSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Issue
        fields = ('id','service','project','user','number','image','title','content','language',
            'status','winner','paid','closed_by','created','modified','notified_user','views')

class IssueViewSet(viewsets.ModelViewSet):
    queryset = Issue.objects.all()
    serializer_class = IssueSerializer

router = routers.DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'issues', IssueViewSet)
router.register(r'services', ServiceViewSet)

urlpatterns += (
    url(r'^api/', include(router.urls)),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework'))
)