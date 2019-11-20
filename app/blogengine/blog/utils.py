import re

from django.shortcuts import render
from django.shortcuts import redirect
from django.shortcuts import get_object_or_404

from .models import *


class ObjectDetailMixin:
    model = None
    template = None

    def prepare_field_body_for_output_in_html(self, obj):
        """
        Подготавить данные в body для вывода текста и изображений в html.

        Метод разделяет текст на части по разделителю {},
        сопоставляет Имя изображения и Путь к изображению на сервере,
        заменяет {src=Имя изображения} на {'img': Путь к изображению на сервере}
        """
        # Получим список имен изображений загруженные на сервер.
        images = Images.objects.filter(post_id=obj.id)
        list_url_image = [image.image.name.split('_')[2].replace('.jpg', '') for image in images]

        # Разделим текст по шаблону {}
        prepared_data_for_body = re.split(r'\{(.*?)\}', obj.body)
        # Сопоставим имя с сервера с именем в body и заменим на Путь к изображению на сервере
        for i, part_text in enumerate(prepared_data_for_body):
            if re.findall('src=', part_text):
                part_text = part_text.replace('src=', '')
                prepared_data_for_body[i] = {
                    'img': images[list_url_image.index(part_text)].image.name.replace('static/', '')}
        obj.body = prepared_data_for_body

    def get(self, request, slug):
        obj = get_object_or_404(self.model, slug__iexact=slug)
        self.prepare_field_body_for_output_in_html(obj)

        return render(request, self.template, context={
            self.model.__name__.lower(): obj,
            'admin_object': obj,
            'detail': True,
            'off_header': True,
        })


def save_image(post_obj, input_images):
    """Создаст в БД запись(связаную с постом) и запишет переданное изображение на сервер.

    Args:
        post_obj(Post): Пост, записаный в БД.
        input_images(list): Переданные изображения в input multiple c id = image.
    """
    for item in input_images or []:
        data_for_model_images = {'post': post_obj, 'image': item}
        new_image = Images.objects.create(
            post=data_for_model_images.get('post'),
            image=data_for_model_images.get('image')
        )
        new_image.save()


class ObjectCreateMixin:
    model_form = None
    template = None

    def get(self, request):
        form = self.model_form()
        return render(request, self.template, context={'form': form})

    def post(self, request):
        bound_form = self.model_form(request.POST)

        if bound_form.is_valid():
            new_obj = bound_form.save()
            input_images = dict(request.FILES).get('image')
            save_image(new_obj, input_images)
            post = Post.objects.filter(id=new_obj.id)
            images = Images.objects.filter(post_id=new_obj.id)
            list_url_image = [image.image.name.split('_')[2].replace('.jpg', '') for image in images]
            for item in post:
                if item.main_image in list_url_image:
                    item.main_image = images[list_url_image.index(item.main_image)].image.name.replace('static/', '')
                    item.save()
            return redirect(new_obj)
        return render(request, self.template, context={'form': bound_form})


class ObjectUpdateMixin:
    model = None
    model_form = None
    template = None

    def get(self, request, slug):
        obj = self.model.objects.get(slug__iexact=slug)
        bound_form = self.model_form(instance=obj)
        return render(request, self.template, context={'form': bound_form, self.model.__name__.lower(): obj})

    def post(self, request, slug):
        obj = self.model.objects.get(slug__iexact=slug)
        bound_form = self.model_form(request.POST, instance=obj)

        if bound_form.is_valid():
            new_obj = bound_form.save()
            input_images = dict(request.FILES).get('image')
            save_image(new_obj, input_images)
            post = Post.objects.filter(id=new_obj.id)
            images = Images.objects.filter(post_id=new_obj.id)
            list_url_image = [image.image.name.split('_')[2].replace('.jpg', '') for image in images]
            for item in post:
                if item.main_image in list_url_image:
                    item.main_image = images[list_url_image.index(item.main_image)].image.name.replace('static/', '')
                    item.save()
            return redirect(new_obj)
        return render(request, self.template, context={'form': bound_form, self.model.__name__.lower(): obj})


class ObjectDeleteMixin:
    model = None
    template = None
    redirect_url = None

    def get(self, request, slug):
        obj = self.model.objects.get(slug__iexact=slug)
        return render(request, self.template, context={self.model.__name__.lower(): obj})

    def post(self, request, slug):
        obj = self.model.objects.get(slug__iexact=slug)
        obj.delete()
        return redirect(reverse(self.redirect_url))
