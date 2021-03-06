from django.contrib.auth import views as auth_views
from django.urls import path, include

from . import views

# app_name = 'account'

urlpatterns = [
    # path('login/', views.user_login, name='login'),
    path('', views.dashboard, name='dashboard'),
    path('login/', auth_views.LoginView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    # Обработчики изменения пароля
    path('password_change/',
         auth_views.PasswordChangeView.as_view(),
         name='password_change'),
    path('password_change/done/',
         auth_views.PasswordChangeDoneView.as_view(),
         name='password_change_done'),
    # Обработчики восстановления пароля
    path('password_reset/',
         auth_views.PasswordResetView.as_view(),
         name='password_reset'),
    path('password_reset/done/',
         auth_views.PasswordResetDoneView.as_view(),
         name='password_reset_done'),
    path('reset/<uidb64>/<token>/',
         auth_views.PasswordResetConfirmView.as_view(),
         name='password_reset_confirm'),
    path('reset/done/',
         auth_views.PasswordResetCompleteView.as_view(),
         name='password_reset_complete'),
    # можем использовать вместо всех обработчиков
    # изменения и восстановления пароля описанных выше
    path('', include('django.contrib.auth.urls')),

    path('register/', views.register, name='register'),
    path('edit/', views.edit, name='edit'),

    path('users/', views.user_list, name='user_list'),

    path('users/follow/', views.user_follow, name='user_follow'), # должен находяится до user_detail для правильной иерархии отработки
    # В противном случае запрос по адресу /users/follow/ подойдет к регулярному отображению шаблона user_detail, при этом будет вызван не тот обработчик, который мы ожидаем
    # Отсюда следуюет - возможно необходимо резервировать как системные определенные username, в данном случае follow
    path('users/<username>/', views.user_detail, name='user_detail'),

]
