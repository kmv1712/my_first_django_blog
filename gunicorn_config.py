command = '/home/karpov-mv/code/blog/env/bin/gunicorn'
pythonpath = '/home/karpov-mv/code/blog/my_first_django_blog'
bind = '127.0.0.1:8001'
workers = 2 
user = 'karpov-mv'
limit_request_fields = 32000
limit_request_field_size = 0
raw_env = 'DJANGO_SETTINGS_MODULE=blogengine.settings'
