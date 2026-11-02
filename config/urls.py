from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.urls import include, path
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from inventario.api_views import (
    DetalleVentaViewSet,
    ProductoViewSet,
    VentaViewSet,
)

router = DefaultRouter()
router.register("productos", ProductoViewSet, basename="producto")
router.register("ventas", VentaViewSet, basename="venta")
router.register("detalles-venta", DetalleVentaViewSet, basename="detalle-venta")

urlpatterns = [
    path("admin/", admin.site.urls),
    path(
        "accounts/login/",
        auth_views.LoginView.as_view(template_name="registration/login.html"),
        name="login",
    ),
    path("accounts/logout/", auth_views.LogoutView.as_view(), name="logout"),
    path("api/token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("api/token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("api/", include(router.urls)),
    path("", include(("inventario.urls", "inventario"), namespace="inventario")),
]
