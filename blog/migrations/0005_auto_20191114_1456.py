# Generated by Django 2.2.5 on 2019-11-14 14:56

import blog.models
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0004_auto_20191114_1419'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='post',
            name='image',
        ),
        migrations.CreateModel(
            name='Images',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(default='pic_folder/None/no-img.jpg', upload_to=blog.models.get_image_filename, verbose_name='Image')),
                ('post', models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='blog.Post')),
            ],
        ),
    ]
