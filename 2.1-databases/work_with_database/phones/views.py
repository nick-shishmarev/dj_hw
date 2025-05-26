from django.shortcuts import render, redirect

from phones.models import Phone


def index(request):
    return redirect('catalog')


def show_catalog(request):
    sort = request.GET.get('sort')

    template = 'catalog.html'

    phone_objects = Phone.objects.all()
    phone_dict = [{'name': p.name, 'price': p.price, 'image': p.image, 'slug': p.slug} for p in phone_objects]
    if sort == 'name':
        phone_dict.sort(key=lambda x: x['name'])
    elif sort == 'min_price':
        phone_dict.sort(key=lambda x: x['price'])
    elif sort == 'max_price':
        phone_dict.sort(key=lambda x: x['price'], reverse=True)

    context = {'phones': phone_dict}
    return render(request, template, context)


def show_product(request, slug):
    template = 'product.html'
    phone = Phone.objects.filter(slug=slug)
    phone_dict = [{
        'name': p.name,
        'price': p.price,
        'image': p.image,
        'slug': p.slug,
        'release_date': p.release_date,
        'lte_exists': p.lte_exists,
    } for p in phone][0]
    context = {'phone': phone_dict}
    return render(request, template, context)
