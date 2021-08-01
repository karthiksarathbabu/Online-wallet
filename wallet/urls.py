from wallet import views
from django.urls import path


urlpatterns = [
    path('wallet/',views.EnableWalletAPIView.as_view(),name='wallet'),
    path('deposits/',views.AddVirtualMoneyAPIView.as_view(),name='deposits'),
    path('withdrawals/',views.WithdrawMoneyAPIView.as_view(),name='withdrawals'),
    path('disable/',views.DisableWalletAPIView.as_view(),name='disable')

    ]