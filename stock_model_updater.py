import os
from django.conf import settings
import django
from django.apps import apps



# conf = {
#     'INSTALLED_APPS': [
#         'django.contrib.admin',
#         'django.contrib.auth',
#         'django.contrib.contenttypes',
#         'django.contrib.messages',
#         'django.contrib.sessions',
#         'django.contrib.sitemaps',
#         'django.contrib.sites',
#         'django.contrib.staticfiles',
#         'stocks.apps.StocksConfig',

#     ],
#     'DATABASES': {
#         'default': {
#          'ENGINE': 'django.db.backends.postgresql',
#           'NAME':'smartstocksdb',
#           'USER':'postgres',
#           'PASSWORD':'123456',
#           'HOST':'localhost'
#     }
#     },
#     'TIME_ZONE': 'UTC'
# }

# settings.configure(**conf)
# apps.populate(settings.INSTALLED_APPS)

# from stocks.models import Stock
from stocks.ml import Prediction,Preprocessing




cwd = os.getcwd()
path = os.path.join(cwd,"ml_models")
available_models = os.listdir(path)
available_models = [ model[:-3] for model in available_models ]


for model in available_models:  
  Prediction(model).update_model(10)
  print("Updating model :",model)






