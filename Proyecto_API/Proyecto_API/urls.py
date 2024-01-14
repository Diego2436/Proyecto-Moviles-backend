from django.contrib import admin
from django.urls import include, path

from rest_framework_simplejwt import views as jwt_views 

# Importando vistas para convertilas en endpoints
from api import views as endpoint

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/cuenta/registrar/', endpoint.registro),
    path('api/cuenta/verificar/', endpoint.verificar_cuenta),
    path('api/cuenta/iniciar-sesion/', endpoint.iniciar_sesion),
    path('api/cuenta/recuperar-password/', endpoint.recuperar_password),
    path('api/token/', jwt_views.TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', jwt_views.TokenRefreshView.as_view(), name='token_refresh'),
]
