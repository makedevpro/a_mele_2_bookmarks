import redis

from django.conf import settings
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST

from .forms import ImageCreateForm
from .models import Image
from actions.utils import create_action
from common.decorators import ajax_required


# Подключение к Redis.
# Создаем вне функций, чтобы использовать в обработчиках,
# а не открывать каждый раз
r = redis.StrictRedis(host=settings.REDIS_HOST,
                      port=settings.REDIS_PORT,
                      db=settings.REDIS_DB)


@login_required
def image_create(request):
    form = ImageCreateForm(data=request.GET)
    if request.method == 'POST':
        # Форма отправлена
        form = ImageCreateForm(data=request.POST)
        if form.is_valid():
            # Данные валидны
            cd = form.cleaned_data

            new_item = form.save(commit=False)
            # Добавляем пользователя к созданному объекту.
            new_item.user = request.user
            new_item.save()
            create_action(request.user, 'bookmarked image', new_item)
            messages.success(request, 'Image added successfully')
            # Перенаправляем пользователя на страницу сохраненного изображения.
            return redirect(new_item.get_absolute_url())
        else:
            # Заполняем форму данными из GET-запроса.
            form = ImageCreateForm(data=request.GET)
    return render(request, 'images/image/create.html', {'section': 'images',
                                                        'form': form})


def image_detail(request, id, slug):
    image = get_object_or_404(Image, id=id, slug=slug)
    # Увеличиваем количество просмотров картинки на 1.
    # формируем ключ для хранилища в виде object-type:id:field (image:33:id)
    total_views = r.incr('image:{}:views'.format(image.id))
    return render(request,
                  'images/image/detail.html',
                  {'section': 'image',
                   'image': image,
                   'total_views': total_views,
                   })


@login_required
def image_list(request):
    images = Image.objects.all()

    # Отсортированные по популярности
    images_by_popularity = images.order_by('-total_likes')
    images = images_by_popularity

    paginator = Paginator(images, 4)
    page = request.GET.get('page')
    try:
        images = paginator.page(page)
    except PageNotAnInteger:
        # Если переданная страница не является числом, возвращаем первую.
        images = paginator.page(1)
    except EmptyPage:
        if request.is_ajax():
            # Если получили AJAX-запрос с номером страницы, большим, чем их
            # кол-во возвращаем пустую страницу.
            return HttpResponse('')
        # Если номер страницы больше, чем их кол-во, возвращаем последнюю.
        images = paginator.page(paginator.num_pages)
    if request.is_ajax():
        return render(request, 'images/image/list_ajax.html',
                      {'section': 'image', 'images': images})
    return render(request, 'images/image/list.html',
                  {'section': 'image', 'images': images})


@ajax_required
@login_required
@require_POST
def image_like(request):
    image_id = request.POST.get('id')
    action = request.POST.get('action')
    if image_id and action:
        try:
            image = Image.objects.get(id=image_id)
            if action == 'like':
                image.users_like.add(request.user)
                create_action(request.user, 'likes', image)
            else:
                image.users_like.remove(request.user)
        except:
            pass
    return JsonResponse({'status': 'ok'})
