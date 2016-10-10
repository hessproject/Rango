from django.conf.urls import url
from rango import views

urlpatterns = [
    url(r'^$',
        views.index,
        name='index'),

    url(r'^about/$',
        views.about,
        name='about'),

    url(r'^category/(?P<category_name_slug>[\w\-]+)/$',
        views.show_category,
        name='show_category'),

    url(r'^add_category/$',
        views.add_category,
        name='add_category'),

    url(r'^category/(?P<category_name_slug>[\w\-]+)/add_page/$',
        views.add_page,
        name='add_page'),

    url(r'^restricted/$',
        views.restricted,
        name="restricted"),

    url(r'^goto/$',
        views.track_url,
        name='goto'),

    url(r'^suggest_category/$',
        views.suggest_category,
        name='suggest_category'),

    url(r'^auto_add_page/$',
        views.auto_add_page,
        name='auto_add_page'),


]