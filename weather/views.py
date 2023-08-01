from django.shortcuts import render, redirect
import requests
from .models import City
from .forms import CityForm
from django.http import JsonResponse
import os
from dotenv import load_dotenv

load_dotenv()


def index(request):
    appid = os.getenv('WEATHER_API_KEY', 'default_value_if_not_found')
    url = 'https://api.openweathermap.org/data/2.5/weather?q={}&units=metric&appid=' + appid

    if request.method == 'POST':
        form = CityForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('index')  # Перенаправляем на главную страницу после добавления города

    form = CityForm()
    cities = City.objects.all()
    all_info = []  # Создаем пустой список для объектов City

    for city in cities:
        res = requests.get(url.format(city.name)).json()
        city_info = {
            'id': city.id,  # Добавляем ID города
            'city': city.name,
            'temp': round(res['main']['temp']),
            'icon': res['weather'][0]['icon']
        }
        all_info.append(city_info)  # Добавляем объект City в список all_info

    context = {'all_info': all_info, 'form': form}
    return render(request, 'weather/index.html', context)


def delete_info(request):
    if request.method == 'POST':
        try:
            info_id = request.POST.get('id')
            city = City.objects.get(pk=info_id)
            city.delete()
            return redirect('index')
        except City.DoesNotExist:
            return JsonResponse({'success': False, 'error': 'Объект не найден.'})
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)})
    else:
        return JsonResponse({'success': False, 'error': 'Неверный запрос.'})