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
    path('api/cuenta/catalogo/', endpoint.consultar_catalogo),
    path('api/cuenta/filtrar-productos/', endpoint.filtrar_productos),
    path('api/cuenta/ver-pedidos/', endpoint.ver_pedidos),
    path('api/cuenta/ver-detallles-pedido/', endpoint.ver_detalles_pedido),
    path('api/cuenta/cancelar-pedido/', endpoint.cancelar_pedido),  
    path('api/cuenta/asignar-pedido/', endpoint.asignar_pedido),
    path('api/cuenta/consultar-pedidos-asignados/', endpoint.consultar_pedidos_asignados),
    path('api/token/', jwt_views.TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', jwt_views.TokenRefreshView.as_view(), name='token_refresh'),
]
