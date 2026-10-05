from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.utils.text import slugify

from . import pkpass
from .forms import WalletPassForm
from .models import WalletPass


def pass_list(request):
    return render(request, "passes/list.html", {"passes": WalletPass.objects.all()})


def pass_create(request):
    form = WalletPassForm(request.POST or None, request.FILES or None)
    if request.method == "POST" and form.is_valid():
        wallet_pass = form.save()
        return redirect(wallet_pass)
    return render(request, "passes/form.html", {"form": form})


def pass_detail(request, pk):
    wallet_pass = get_object_or_404(WalletPass, pk=pk)
    return render(
        request,
        "passes/detail.html",
        {"p": wallet_pass, "signing_configured": pkpass.signing_configured()},
    )


def pass_download(request, pk):
    wallet_pass = get_object_or_404(WalletPass, pk=pk)
    data, signed = pkpass.build_pkpass(wallet_pass)
    name = slugify(wallet_pass.member_name) or "pase"
    response = HttpResponse(data, content_type="application/vnd.apple.pkpass")
    suffix = "" if signed else "-sin-firmar"
    response["Content-Disposition"] = f'attachment; filename="{name}{suffix}.pkpass"'
    return response


def pass_images(request, pk):
    wallet_pass = get_object_or_404(WalletPass, pk=pk)
    name = slugify(wallet_pass.member_name) or "pase"
    response = HttpResponse(pkpass.build_images_zip(wallet_pass), content_type="application/zip")
    response["Content-Disposition"] = f'attachment; filename="{name}-imagenes.zip"'
    return response


def pass_image(request, pk, name):
    wallet_pass = get_object_or_404(WalletPass, pk=pk)
    images = pkpass.build_images(wallet_pass)
    if name not in images:
        return HttpResponse(status=404)
    return HttpResponse(images[name], content_type="image/png")
