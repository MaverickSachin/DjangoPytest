from django.shortcuts import render, get_object_or_404
from .models import Product
from django.contrib.auth.decorators import login_required


def index(request):
    return render(request, 'products/index.html')


@login_required
def product_details(request, pk):
    product = get_object_or_404(Product, pk=pk)
    context = {"product": product}
    return render(request, 'products/product_details.html', context=context)
