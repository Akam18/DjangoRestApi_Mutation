"""
URL configuration for GrapheneDjangoRestApi project.

The urlpatterns list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include


from django.conf import settings
from django.conf.urls.static import static
from api_main.views import CategoryViewSet, PostViewSet


from drf_yasg.views import get_schema_view
from drf_yasg import openapi

from rest_framework import routers, permissions


schema_view = get_schema_view(
    openapi.Info(
        title="API Documentation",
        default_version='v1',
        description="API Documentation",
        terms_of_service="https://www.example.com/policies/terms/",
        contact=openapi.Contact(email="contact@example.com"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=[
        permissions.IsAuthenticated,
        permissions.IsAdminUser,
    ],
)


router = routers.DefaultRouter()
router.register(r'category', CategoryViewSet)
router.register(r'post',PostViewSet)

 
urlpatterns = [
    path("redoc/", schema_view.with_ui("redoc", cache_timeout=0), name="schema-redoc"),
    path('redoc/', include('django.contrib.admindocs.urls')),
    path("swagger/", schema_view.with_ui("swagger", cache_timeout=0), name="schema-swagger"),
    path('api/', include(router.urls)),
    path('admin/', admin.site.urls),
    path('graphql/', include('graphql_main.urls')),

]




#  он должен только так писат а не то сломается , мы должны вытаскивать из settinga
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
# Если есть хоть один фото, мы должны сделать это
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)