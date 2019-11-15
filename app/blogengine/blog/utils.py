import os

from django.shortcuts import render
from django.shortcuts import redirect
from django.shortcuts import get_object_or_404

from .models import *


class ObjectDetailMixin:
    model = None
    template = None

    def get(self, request, slug):
        obj = get_object_or_404(self.model, slug__iexact=slug)
        images = Images.objects.filter(post_id=obj.id)
        obj.body = obj.body.split('{')

        return render(request, self.template, context={
            self.model.__name__.lower(): obj,
            'admin_object': obj,
            'images': images,
            'detail': True,
            'off_header': True,
            'img': images[0].image.url.replace('static/', '')
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
