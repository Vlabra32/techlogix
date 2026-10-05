from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType

from inventario.models import Producto


class Command(BaseCommand):
    help = "Crea los grupos Administrador y Asistente con sus permisos"

    def handle(self, *args, **kwargs):

        # Obtener los grupos
        grupo_admin, _ = Group.objects.get_or_create(
            name="Administrador"
        )

        grupo_asistente, _ = Group.objects.get_or_create(
            name="Asistente"
        )

        # Obtener permisos del modelo Producto
        content_type = ContentType.objects.get_for_model(Producto)

        permiso_ver = Permission.objects.get(
            codename="view_producto",
            content_type=content_type
        )

        permiso_crear = Permission.objects.get(
            codename="add_producto",
            content_type=content_type
        )

        permiso_editar = Permission.objects.get(
            codename="change_producto",
            content_type=content_type
        )

        permiso_eliminar = Permission.objects.get(
            codename="delete_producto",
            content_type=content_type
        )

        # Administrador: todos los permisos
        grupo_admin.permissions.set([
            permiso_ver,
            permiso_crear,
            permiso_editar,
            permiso_eliminar,
        ])

        # Asistente: solamente lectura
        grupo_asistente.permissions.set([
            permiso_ver,
        ])

        self.stdout.write(
            self.style.SUCCESS(
                "Grupos y permisos creados correctamente."
            )
        )
