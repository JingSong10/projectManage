from django.urls import path, include
from web.views import account, home, project, manage

urlpatterns = [
    path('register/', account.register, name='register'),
    path('send/sms/', account.send_sms, name='send_sms'),
    path('login/sms/', account.login_sms, name='login_sms'),
    path('login/', account.login, name='login'),
    path('image/code/', account.code_image, name='code_image'),
    path('index/', home.index, name='index'),
    path('logout/', home.logout, name='logout'),
    # 项目列表
    path('project/project_list/', project.project_list, name='project_list'),
    path('project/star/<str:project_type>/<int:project_id>', project.star, name='star'),
    path('project/unstar/<str:project_type>/<int:project_id>', project.unstar, name='unstar'),
    # 项目管理
    path('manage/<int:project_id>/', include([
        path('dashboard/', manage.dashboard, name='dashboard'),
        path('issues/', manage.issues, name='issues'),
        path('statistics/', manage.statistics, name='statistics'),
        path('file/', manage.file, name='file'),
        path('wiki/', manage.wiki, name='wiki'),
        path('setting/', manage.setting, name='setting'),
    ], None)),

]