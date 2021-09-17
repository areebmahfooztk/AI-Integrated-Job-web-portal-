from django.urls import path
from . import views
from django.urls import path
from django.contrib import admin
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.homepage,name='homepage'),
    path('candprof/', views.candprof,name='candprof'),
    path('emprof/', views.emprof,name='emprof'),
    path('emprof/ml/<int:id>', views.ml,name='ml'),
    path('candhome/', views.candhome, name='candhome'),
    path('create/', views.create, name="create"),
    path('registration/', views.candregistration,name='registration'),
    path('emphome/', views.emphome,name='emphome'),
    path('empreg/', views.empreg, name='empreg'),
    path('empcreate/', views.empcreate, name="empcreate"),
    path('twitter3/', views.twitter3, name="twitter3"),
    path('twitter/', views.twitter, name="twitter"),
    path('edit/<int:id>', views.edit, name="edit"),
    #path('edit/update/<int:id>', views.update, name="update"),
    path('message/', views.message, name="message"),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)