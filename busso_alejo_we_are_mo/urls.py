from django.contrib import admin
from django.urls import include, path
from busso_alejo_we_are_mo.authorization import ApiKeyCreationView
from drf_spectacular.views import SpectacularAPIView, SpectacularRedocView, SpectacularSwaggerView

urlpatterns =  [
    path('admin/', admin.site.urls),
    path('api/key/', ApiKeyCreationView.as_view(), name='api-key'),
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/schema/swagger-ui/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('api/schema/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),
    path('api/customers/', include('customers.urls')),
    path('api/loans/', include('loans.urls')),
    path('api/payments/', include('payments.urls')),

]

