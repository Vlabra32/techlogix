from django.urls import path
from . import views

urlpatterns = [
    path("", views.inicio, name="inicio"),
    path("catalogo/", views.catalogo, name="catalogo"),

    # Área de administración
    path("admin-panel/", views.admin_panel, name="admin_panel"),

    # CRUD de productos
    path(
        "admin-panel/productos/crear/",
        views.producto_crear,
        name="producto_crear",
    ),

    path(
        "admin-panel/productos/<int:pk>/editar/",
        views.producto_editar,
        name="producto_editar",
    ),

    path(
        "admin-panel/productos/<int:pk>/eliminar/",
        views.producto_eliminar,
        name="producto_eliminar",
    ),
]
