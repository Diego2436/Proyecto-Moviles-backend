from django.contrib import admin
from django.urls import include, path

from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt import views as jwt_views 

# Importando vistas para convertilas en endpoints
from api import views as endpoint

router = DefaultRouter()
router.register(r'food_truck', endpoint.FoodTruckSet, basename='food_truck')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)),
    path('api/token/', jwt_views.TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', jwt_views.TokenRefreshView.as_view(), name='token_refresh'),
]
