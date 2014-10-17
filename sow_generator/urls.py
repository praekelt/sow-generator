from django.conf.urls import patterns, include, url


urlpatterns = patterns(
    '',

    url(
        r'^ajax-sync-repository/(?P<id>\d+)/$',
        'sow_generator.views.ajax_sync_repository',
        {},
        name='sow-generator-ajax-sync-repository'
    ),

    url(
        r'^get-auth-token/$',
        'sow_generator.views.get_auth_token',
        {},
        name='sow-generator-get-auth-token'
    ),

    url(
        r'^get-auth-token-callback/$',
        'sow_generator.views.get_auth_token_callback',
        {},
        name='sow-generator-get-auth-token-callback'
    ),

)
