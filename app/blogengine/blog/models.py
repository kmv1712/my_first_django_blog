from django.db import models
from django.shortcuts import reverse

from django.utils.text import slugify
from time import time

alphabet_cyrillic_to_latin = {'а': 'a', 'б': 'b', 'в': 'v', 'г': 'g', 'д': 'd', 'е': 'e', 'ё': 'yo', 'ж': 'zh',
                              'з': 'z', 'и': 'i', 'й': 'j', 'к': 'k', 'л': 'l', 'м': 'm', 'н': 'n', 'о': 'o', 'п': 'p',
                              'р': 'r', 'с': 's', 'т': 't', 'у': 'u', 'ф': 'f', 'х': 'kh', 'ц': 'ts', 'ч': 'ch',
                              'ш': 'sh', 'щ': 'shch', 'ы': 'i', 'э': 'e', 'ю': 'yu', 'я': 'ya', 'ь': '', 'ъ': ''}


def convert_cyrillic_to_latin(cyrillic_slug):
    """ Конвертировать слаг из кириллицы в латиницу.
    Args:
         cyrillic_slug(str): Слаг с русскими символами.
    Returns:
        str
    """
    return slugify(''.join(alphabet_cyrillic_to_latin.get(w, w) for w in cyrillic_slug.lower()), allow_unicode=True)


def gen_slug(s):
    """ Сгенерирует слаг переведенный с кирилицы в латиницу и временем создание поста.
    Args:
        s: Слаг с русскими символами.
    Returns:
        str
    """
    new_slug = convert_cyrillic_to_latin(s)
    return '{0}-{1}'.format(new_slug, str(int(time())))


# Create your models here.
class Post(models.Model):
    title = models.CharField(max_length=150, db_index=True)
    slug = models.SlugField(max_length=150, blank=True, unique=True)
    body = models.TextField(blank=True, db_index=True)
    tags = models.ManyToManyField('Tag', blank=True, related_name='posts')
    date_pub = models.DateTimeField(auto_now_add=True)

    def get_absolute_url(self):
        return reverse('post_detail_url', kwargs={'slug': self.slug})

    def get_update_url(self):
        return reverse('post_update_url', kwargs={'slug': self.slug})

    def get_delete_url(self):
        return reverse('post_delete_url', kwargs={'slug': self.slug})

    def save(self, *args, **kwargs):
        if not self.id:
            self.slug = gen_slug(self.title)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['-date_pub']


class Tag(models.Model):
    title = models.CharField(max_length=50)
    slug = models.SlugField(max_length=50, unique=True)

    def get_absolute_url(self):
        return reverse('tag_detail_url', kwargs={'slug': self.slug})

    def get_update_url(self):
        return reverse('tag_update_url', kwargs={'slug': self.slug})

    def get_delete_url(self):
        return reverse('tag_delete_url', kwargs={'slug': self.slug})

    def __str__(self):
        return '{}'.format(self.title)

    class Meta:
        ordering = ['title']


PATH_FOR_POST_IMAGES = 'static/img/post_images/'


def get_image_filename(instance, filename):
    """Получить ссылку, куда сохраним файл.
    Args:
        instance(Images):
        filename(str): Имя загруженного файла.
    Returns:
        str
    """
    slug = gen_slug(instance.post.title)
    return "{0}{1}_{2}".format(PATH_FOR_POST_IMAGES, slug, filename)


class Images(models.Model):
    post = models.ForeignKey(Post, default=None, on_delete=models.CASCADE)
    image = models.ImageField(upload_to=get_image_filename, verbose_name='Image', default='pic_folder/None/no-img.jpg')
