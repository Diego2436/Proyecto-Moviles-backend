from django.contrib import admin
from django.urls import include, path

from rest_framework_simplejwt import views as jwt_views 

# Importando vistas para convertilas en endpoints
from api import views as endpoint 

urlpatterns = [
    path('api/admin/', admin.site.urls),

    path('api/usuario/iniciar-sesion/', endpoint.iniciar_sesion),
    path('api/usuario/recuperar-password/', endpoint.recuperar_password),
    path('api/usuario/ver-pedidos/', endpoint.ver_pedidos),
    path('api/usuario/ver-detallles-pedido/', endpoint.ver_detalles_pedido),

    path('api/cliente/registrar/', endpoint.registro),
    path('api/cliente/verificar/', endpoint.verificar_cuenta),
    path('api/cliente/ver-productos/', endpoint.ver_productos),
    path('api/cliente/filtrar-productos-categoria/', endpoint.filtrar_productos_categoria),
    path('api/cliente/filtrar-productos-foodtruck/', endpoint.filtrar_productos_foodtruck),
    path('api/cliente/filtrar-foodtruck/', endpoint.obtener_foodtrucks),
    path('api/cliente/realizar-pedido/', endpoint.realizar_pedido),
      
    path('api/empleado/asignar-pedido/', endpoint.asignar_pedido_a_empleado),
    path('api/empleado/consultar-pedidos-asignados/', endpoint.consultar_pedidos_asignados),
    path('api/empleado/obtener-repartidores/', endpoint.obtener_repartidores),
    path('api/empleado/entregar-pedido/', endpoint.entregar_pedido),

    path('api/token/', jwt_views.TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', jwt_views.TokenRefreshView.as_view(), name='token_refresh'),
]
