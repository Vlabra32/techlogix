from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib import messages

from .forms import ProductoForm
from .models import Producto


def es_administrador(user):
    return user.groups.filter(name="Administrador").exists() or user.is_superuser


class AdministradorRequiredMixin(UserPassesTestMixin):
    def test_func(self):
        return es_administrador(self.request.user)


def inicio(request):
    return render(request, "index.html")


def catalogo(request):
    productos = Producto.objects.select_related("categoria").all()

    busqueda = request.GET.get("q", "")
    categoria = request.GET.get("categoria", "")

    if busqueda:
        productos = productos.filter(nombre__icontains=busqueda)

    if categoria:
        productos = productos.filter(categoria_id=categoria)

    categorias = productos.model._meta.get_field("categoria").related_model.objects.all()

    contexto = {
        "productos": productos,
        "categorias": categorias,
        "busqueda": busqueda,
        "categoria_seleccionada": categoria,
    }

    return render(request, "catalogo.html", contexto)


@login_required
def admin_panel(request):
    productos = Producto.objects.select_related("categoria").all()

    return render(
        request,
        "admin_panel.html",
        {
            "productos": productos,
            "es_admin": es_administrador(request.user),
        },
    )


@login_required
def producto_crear(request):
    if not es_administrador(request.user):
        messages.error(request, "No tienes permisos para crear productos.")
        return redirect("admin_panel")

    if request.method == "POST":
        form = ProductoForm(request.POST)

        if form.is_valid():
            form.save()
            messages.success(request, "Producto creado correctamente.")
            return redirect("admin_panel")
    else:
        form = ProductoForm()

    return render(
        request,
        "producto_form.html",
        {
            "form": form,
            "titulo": "Crear producto",
        },
    )


@login_required
def producto_editar(request, pk):
    if not es_administrador(request.user):
        messages.error(request, "No tienes permisos para editar productos.")
        return redirect("admin_panel")

    producto = get_object_or_404(Producto, pk=pk)

    if request.method == "POST":
        form = ProductoForm(request.POST, instance=producto)

        if form.is_valid():
            form.save()
            messages.success(request, "Producto actualizado correctamente.")
            return redirect("admin_panel")
    else:
        form = ProductoForm(instance=producto)

    return render(
        request,
        "producto_form.html",
        {
            "form": form,
            "titulo": "Editar producto",
            "producto": producto,
        },
    )


@login_required
def producto_eliminar(request, pk):
    if not es_administrador(request.user):
        messages.error(request, "No tienes permisos para eliminar productos.")
        return redirect("admin_panel")

    producto = get_object_or_404(Producto, pk=pk)

    if request.method == "POST":
        producto.delete()
        messages.success(request, "Producto eliminado correctamente.")
        return redirect("admin_panel")

    return render(
        request,
        "producto_confirmar_eliminar.html",
        {
            "producto": producto,
        },
    )