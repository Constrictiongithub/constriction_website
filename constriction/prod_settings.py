HOST_NAME = "constriction.webfootprints.eu"
DB_CONNECTIONSTRING = "/cloudsql/ecstatic-spirit-226714:europe-west1:constriction"
DB_USER = "constriction"
DB_NAME = "constriction"
DB_PASSWORD = "2G(NUev7_gw57un_)E5YXbTwSVU=oLvP"
DEVELOPMENT = False
SECRET_KEY = "^qaet5ed0@76(i:k_qdtzo2jg@!i3955c2n2-36a5j-dd5z#3k"
ROOT_URL = 'constriction.urls'
WSGI_APPLICATION = 'constriction.wsgi.application'
STATIC_URL = 'https://storage.googleapis.com/constriction_django/static/'
MEDIA_URL = 'https://storage.googleapis.com/constriction_django/media/'
DEFAULT_FILE_STORAGE = 'constriction.storage.GoogleCloudStorageMedia'
STATICFILES_STORAGE = 'constriction.storage.GoogleCloudStorageStatic'
ALLOWED_HOSTS = ["constriction.com", ]
SECURE_SSL_REDIRECT = True
ADMINS = (
    ("Matteo Parrucci", "matteo@constriction.com", ),
    ("Roberto Malcotti", "roberto@constriction.com", ),
    ("Luca Franchini", "luca@constriction.com", ),
    ("Gianfilippo Napolitano", "gianfilippo@gmaconstrictionil.com", ),
)
