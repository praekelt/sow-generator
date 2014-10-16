from django.conf.urls import patterns, include, url


urlpatterns = patterns(
    '',

    url(
        r'^ajax-sync-repository/(?P<id>\d+)/$',
        'sow_generator.views.ajax_sync_repository',
        {},
        name='sow-generator-ajax-sync-repository'
    ),

)
