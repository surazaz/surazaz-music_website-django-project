from django.conf.urls import url
from django.contrib.auth.views import login,logout
from . import views
app_name='music'
#using genric views
urlpatterns=[
	url(r'^$',views.IndexView.as_view(),name="index"),
    url(r'^(?P<pk>[0-9]+)/$',views.DetailView.as_view(),name="detail"),
    url(r'^album/add/$',views.AlbumCreate.as_view(),name='album-add'),
    url(r'^album/(?P<pk>[0-9]+)/$',views.AlbumUpdate.as_view(),name="album-update"),
     url(r'^album/(?P<pk>[0-9]+)/delete/$',views.AlbumDelete.as_view(),name="album-delete"),
    url(r'^register/$',views.UserFormView.as_view(),name='register'),
        #url(r'^register/$',views.register,name='register'),
        url(r'^login/$',login,{'template_name': 'music/login.html'},name='login'),
        url(r'^logout/$',logout,{'template_name': 'music/logout.html'}, name='logout'),
        url(r'^profile/$',views.profile, name='profile'),
        url(r'^profile/edit/$',views.edit_profile, name='editprofile'),
        url(r'^changepassword/$',views.changepassword, name='changepassword'),
        
        ]
# urlpatterns = [
#     url(r'^$',views.index,name="index"),
#     url(r'^(?P<album_id>[0-9]+)/$',views.detail,name="detail"),
#     url(r'^(?P<album_id>[0-9]+)/favourite/$',views.favourite,name="favourite")
#     ,
    
#     #album_id is the variable we can pass to views

# ]
