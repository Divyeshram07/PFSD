
from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),

    path('login/', views.login_view, name='login'),
    path('products/', views.product_list, name='product_list'),
    path('cart/', views.view_cart, name='view_cart'),
    path('add_to_cart/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('remove_from_cart/<int:cart_item_id>/', views.remove_from_cart, name='remove_from_cart'),
    path('order-confirmation/<int:order_id>/', views.order_confirmation, name='order_confirmation'),
    path('order_success/', views.order_success, name='order_success'),
    path('process_order/', views.process_order, name='process_order'),
    path('register/', views.register, name='register'),
    path('logout/', views.logout_view, name='logout'),
    path('checkout/', views.checkout, name='checkout'),
    path('order-summary/<int:order_id>/', views.order_summary, name='order_summary'),
    path('place_order/', views.place_order, name='place_order'),
    path('contact/', views.contact, name='contact'),
    path('profile/', views.profile_view, name='profile'),  # View for profile page
    path('profile/edit/', views.edit_profile, name='edit_profile'),
    path('profile/update/', views.edit_profile, name='update_profile'),
    path('product1/', views.product1_view, name='product1'),

    path('privacy-policy/', views.privacy_policy, name='privacy_policy'),
    path('return-policy/', views.return_policy, name='return_policy'),
    path('seller-terms/', views.seller_terms, name='seller_terms'),
    path('terms-of-use/', views.terms_of_use, name='terms_of_use'),

    path('cancellation-policy/', views.cancellation_policy, name='cancellation_policy'),

    path('faq/', views.faq, name='faq'),

    path('about-us/', views.about_us, name='about_us'),

    path('customer-care/', views.customer_care, name='customer_care'),
    path('submit-query/', views.submit_query, name='submit_query'),
    path('orders/', views.order_history, name='order_history'),
    path('orders/cancel/<int:order_id>/', views.cancel_order, name='cancel_order'),
]
