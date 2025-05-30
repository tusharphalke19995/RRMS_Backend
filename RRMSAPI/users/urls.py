from django.urls import path
from .views import CreateUserView,UserListView,SetPasswordView,RequestPasswordResetOTP,RequestPasswordResetView,ResetPassword,VerifyPasswordResetOTP,UpdateUserView,CustomTokenObtainPairView,SearchUsersAPIView,GetDivisionrAdminsView, GetLoggedInUsersView
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

urlpatterns = [
    path('',UserListView.as_view(),name='user-list'), #path for fetching all the users
    path('create', CreateUserView.as_view(), name='create_user'),
    path('update-user/<int:kgid_user>', UpdateUserView.as_view(), name='update_user'),
    path('login', CustomTokenObtainPairView.as_view(), name='login'),
    path('currentUsers',GetLoggedInUsersView.as_view(), name = 'logged-in-users'),
    path('getcmoradmins', GetDivisionrAdminsView.as_view(),name = 'cm-admins'),
    path('search-users',SearchUsersAPIView.as_view(),name='search-users'),
    path('set-password', SetPasswordView.as_view(), name='set-password'),
    path('request-otp/<str:pk>', RequestPasswordResetOTP.as_view(),name='request-otp'),
    path('verify-otp', VerifyPasswordResetOTP.as_view(),name='verify-otp'),
    path('reset-password', ResetPassword.as_view(),name='reset-pwd'),
    path('reset-pwd-request', RequestPasswordResetView.as_view(),name='reset-pwd-request')

]