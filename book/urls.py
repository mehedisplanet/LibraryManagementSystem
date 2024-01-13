from django.urls import path
from .views import DetailsPostView,PurchaseView

urlpatterns = [
    path('details/<int:pk>',DetailsPostView.as_view(), name='details_post'),
    path('purchase/<int:id>/',PurchaseView.as_view(), name='purchase_book'),
]