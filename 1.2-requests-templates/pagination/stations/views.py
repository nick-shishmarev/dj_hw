import csv

from django.shortcuts import render, redirect
from django.urls import reverse
from django.core.paginator import Paginator
from pagination.settings import BUS_STATION_CSV


def index(request):
    return redirect(reverse('bus_stations'))


def bus_stations(request):
    # получите текущую страницу и передайте ее в контекст
    # также передайте в контекст список станций на странице
    try:
        page_number = int(request.GET.get('page', 1))
    except ValueError:
        page_number = 1
    station_list = []
    with open(BUS_STATION_CSV, newline='', encoding='utf-8') as csv_file:
        reader = csv.DictReader(csv_file)
        for row in reader:
            station_list.append({'Name': row['Name'],
                                 'Street': row['Street'],
                                 'District': row['District']})

    paginator = Paginator(station_list, 25)
    stations = paginator.get_page(page_number)

    context = {
        'bus_stations': stations,
        'page': stations
    }
    return render(request, 'stations/index.html', context)
