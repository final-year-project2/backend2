from django.contrib import admin
from django.urls import path,include
from django.conf.urls.static import static
from django.conf import settings
urlpatterns = [
    path('admin/', admin.site.urls),
    path('user/',include('UserAccount.urls')),
    
    path('product/',include('Product.urls')),
    path('ticket/', include('PurchasedTicket.urls')),
    path('comment/', include('Comments.urls')),
    path('seller_admin/', include('selleradmin.urls')),
    
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)