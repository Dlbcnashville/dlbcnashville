from .base import *

DEBUG = False

try:
    from .local import *
except ImportError:
    pass


import environ
import cloudinary.uploader
import cloudinary.api
import cloudinary


env = environ.Env(
    DEBUG=(bool, False)
)
environ.Env.read_env(os.path.join(BASE_DIR, '.env'))
DEBUG = env('DEBUG')

ALLOWED_HOSTS = ["dlbcnashville-production.up.railway.app", "dlbcnashville.org"]
          
cloudinary.config( 
  cloud_name = "ddlhu2ayf", 
  api_key = "115566937972984", 
  api_secret = "yacFCzoP_W-q9tvXaeIrex4CzvU" 
)

EMAIL_HOST = 'smtp.elasticemail.com'
EMAIL_USE_TLS = True
EMAIL_PORT = 2525
# EMAIL_HOST_USER = 'clarksvillelbc@gmail.com'
# EMAIL_HOST_PASSWORD = '4DC6317573C5B115FB1FFE24C96AF91CBA4A'
# DEFAULT_FROM_EMAIL = 'clarksvillesdlbc@gmail.com'
# EMAIL_HOST_USER = ""
# EMAIL_HOST_PASSWORD = ""
# DEFAULT_FROM_EMAIL = ""
EMAIL_HOST_USER = 'info@dlbcnashville.org'
EMAIL_HOST_PASSWORD = env('EMAIL_HOST_PASSWORD')
DEFAULT_FROM_EMAIL = 'info@dlbcnashville.org'