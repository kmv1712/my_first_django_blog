import os

from django.shortcuts import render
from django.shortcuts import redirect
from django.shortcuts import get_object_or_404
from django.forms import modelformset_factory
from django.contrib import messages

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
        image_form_set = modelformset_factory(Images, form=ImageForm, extra=1)
        image_form = image_form_set(queryset=Images.objects.none())
        return render(request, self.template, context={'form': form, 'image_form': image_form})

    def post(self, request):
        image_form_set = modelformset_factory(Images, form=ImageForm, extra=3)
        bound_form = self.model_form(request.POST)
        image_form = image_form_set(request.POST, request.FILES, queryset=Images.objects.none())
        # request_files = dict(request.FILES)
        # request_files = request_files.get('file')
        # handle_uploaded_file(request_files, request.POST['title'])

        if bound_form.is_valid() and image_form.is_valid():
            new_obj = bound_form.save(commit=False)
            new_obj.user = request.user
            new_obj.save()

            for form in image_form.cleaned_data:
                # this helps to not crash if the user
                # do not upload all the photos
                if form:
                    image = form['image']
                    photo = Images(post=new_obj, image=image)
                    photo.save()
            messages.success(request, "Yeeew, check it out on the home page!")
            return redirect(new_obj)
            # return HttpResponseRedirect("/")
        return render(request, self.template, context={'form': bound_form, 'image_form': image_form})


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
