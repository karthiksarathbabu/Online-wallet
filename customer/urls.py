from customer import views
from django.urls import path


urlpatterns = [
    # path('create-user/',views.CreateCustomerAPIView.as_view(),name='create-user'),
    path('init/',views.InitializeWalletAcoountAPIView.as_view(),name='init'),
    ]