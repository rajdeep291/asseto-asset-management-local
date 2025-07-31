from django.shortcuts import render, redirect
from dashboard.forms import ProductSubCategoryForm
from django.contrib import messages
# from dashboard.models import ProductSubCategory, ProductType
from ..models import ProductSubCatagory
from django.core.paginator import Paginator
from django.contrib.auth.decorators import permission_required
from django.contrib.auth.decorators import user_passes_test
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
from django.db.models import Q

PAGE_SIZE=10
ORPHANS=1

@login_required
#@user_passes_test(manage_access)
def product_sub_category_list(request):

    all_product_sub_category_list = ProductSubCatagory.objects.filter(
        organization=request.user.organization).order_by('-created_at')
    paginator = Paginator(all_product_sub_category_list,
                          PAGE_SIZE, orphans=ORPHANS)
    page_number = request.GET.get('page')
    page_object = paginator.get_page(page_number)

    context = {
        'sidebar': 'admin',
        'submenu': 'product_category',
        'page_object': page_object,
        'title': 'Product Categories'
    }
    return render(request, 'dashboard/product_sub_category/list.html', context=context)



@login_required
# @permission_required('authentication.add_product_category')
def add_product_sub_category(request):

    form = ProductSubCategoryForm(organization=request.user.organization)

    if request.method == "POST":
        print(request.POST)
        form = ProductSubCategoryForm(
            request.POST, organization=request.user.organization)

        if form.is_valid():
            pc = form.save(commit=False)
            pc.organization = request.user.organization
            pc.save()
            messages.success(
                request, 'Product sub Category added successfully')
            return HttpResponse(status=204)

    context = {'form': form, "modal_title": "Add Product sub Category"}
    return render(request, 'dashboard/product_sub_category/product-sub-category-modal.html', context)


@login_required
def delete_product_sub_category(request, id):

    if request.method == 'POST':
        product_category = get_object_or_404(
            ProductSubCatagory.undeleted_objects, pk=id, organization=request.user.organization)
        product_category.status = False
        product_category.soft_delete()
        history_id = product_category.history.first().history_id
        product_category.history.filter(pk=history_id).update(history_type='-')
        messages.success(request, 'Product Category deleted successfully')

    return redirect(request.META.get('HTTP_REFERER'))


@login_required
def update_product_sub_category(request, id):

    product_category = get_object_or_404(
        ProductSubCatagory.undeleted_objects, pk=id, organization=request.user.organization)
    form = ProductSubCategoryForm(request.POST or None, instance=product_category,
                               organization=request.user.organization,  pk=product_category.id)

    if request.method == "POST":

        if form.is_valid():
            form.save()
            messages.success(request, 'Product Category updated successfully')
            return HttpResponse(status=204)

    context = {'form': form, "modal_title": "Update Product Category"}
    return render(request, 'dashboard/product_category/product-sub-category-modal.html', context)