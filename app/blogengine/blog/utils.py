import os

from django.shortcuts import render
from django.shortcuts import redirect
from django.shortcuts import get_object_or_404

from .models import *
from .forms import ImageForm


def handle_uploaded_file(request_files, article_title):
    """ Загрузит файл на сервер в папку posts.

    Args:
        request_files(list): Файлы полученные в форме.
        article_title(str): Название статьи.

    """
    # TODO: Посмотреть, как подставлять static.
    # TODO: Разобратся, как сохраняется tags и реализовать для images класс.
    new_path = "static/img/posts/{0}".format(article_title)
    # Если нет папки сосздадим новую.
    if not os.path.exists(new_path):
        os.makedirs(new_path)
    # Запишим чанками на сервер.
    for i, image in enumerate(request_files):
        destination = open("{0}/{1}_{2}.jpg".format(new_path, article_title, i), 'wb+')
        # object = Image()
        for chunk in image.chunks() or []:
            destination.write(chunk)
        destination.close()


class ObjectDetailMixin:
    model = None
    template = None

    def get(self, request, slug):
        # post = Post.objects.get(slug__iexact=slug)
        obj = get_object_or_404(self.model, slug__iexact=slug)
        return render(request, self.template, context={
            self.model.__name__.lower(): obj,
            'admin_object': obj,
            'detail': True,
            'off_header': True
        })


class ObjectCreateMixin:
    model_form = None
    template = None

    def get(self, request):
        form = self.model_form()
        form_image = ImageForm()
        return render(request, self.template, context={'form': form, 'form_image': form_image})

    def post(self, request):
        bound_form = self.model_form(request.POST)
        request_files = dict(request.FILES)
        request_files = request_files.get('file')
        handle_uploaded_file(request_files, request.POST['title'])
        # ImageForm()
        if bound_form.is_valid():
            new_obj = bound_form.save()
            a = ImageForm(request.POST).save()
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
        handle_uploaded_file(request.FILES['file'])

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
