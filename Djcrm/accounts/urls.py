from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('register/',views.registerPage,name="register"),
    path('login/',views.loginPage,name="login"),
    path('logout/',views.logoutUser,name="logout"),
    path('user/', views.userPage, name="user-page"),
    path('account/', views.accountSettings, name="account"),
    path('', views.Home,name="home"),
    path('products/', views.Products,name="products"),
    path('customers/<str:pk_test>/', views.Customers,name="customer"),
    path('create-order/<str:pk>', views.CreateOrder,name="createorder"),
    path('update-order/<str:pk>', views.UpdateOrder,name="updateorder"),
    path('delete-order/<str:pk>', views.DeleteOrder,name="deleteorder"),

   path('reset_password/',
     auth_views.PasswordResetView.as_view(template_name="accounts/password_reset.html"),
     name="reset_password"),

    path('reset_password_sent/', 
        auth_views.PasswordResetDoneView.as_view(template_name="accounts/password_reset_sent.html"), 
        name="password_reset_done"),

    path('reset/<uidb64>/<token>/',
     auth_views.PasswordResetConfirmView.as_view(template_name="accounts/password_reset_form.html"), 
     name="password_reset_confirm"),

    path('reset_password_complete/', 
        auth_views.PasswordResetCompleteView.as_view(template_name="accounts/password_reset_done.html"), 
        name="password_reset_complete"),

]
