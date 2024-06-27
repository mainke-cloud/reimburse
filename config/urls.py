from django.contrib import admin
from django.urls import path, include
from reimburse.views import (index, view, add, delete,download, edit, redraft,
         submit, paid, reject, waiting, involved)

urlpatterns = [
    path("",index, name="reimburse-index"),
    path("waiting/",waiting, name="reimburse-waiting"),
    path("involved/",involved, name="reimburse-involved"),
    path("add/",add, name="reimburse-add"),
    path("download/<int:id>", download, name="reimburse-download"),
    path("view/<int:id>", view, name="reimburse-view"),
    path("redraft/<int:id>", redraft, name="reimburse-redraft"),
    path("edit/<int:id>", edit, name="reimburse-edit"),
    path("delete/<int:id>", delete, name="reimburse-delete"),
    path("submit/<int:id>", submit, name="reimburse-submit"),
    path("paid/<int:id>", paid, name="reimburse-paid"),
    path("reject/<int:id>", reject, name="reimburse-reject"),
    path('oidc/', include('mozilla_django_oidc.urls')),
    path('admin/', admin.site.urls),
]
