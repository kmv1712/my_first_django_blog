#!/bin/bash
	source /home/karpov-mv/code/blog/env/bin/activate
	exec gunicorn  -c "/home/karpov-mv/code/blog/my_first_django_blog/gunicorn_config.py" blogengine.wsgi
