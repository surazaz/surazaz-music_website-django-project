from django.urls import path
from mainapp import views

urlpatterns = [
    path('sign/', views.sign, name='signin'),
    path('logout/', views.logout, name='logout'),
    path('allform/<str:formtype>/', views.allform,name='allform'),
    path('allform/<str:formtype>/<str:id>/', views.allform,name='allform'),
    path('userform/<str:formtype>/', views.userform, name='userform'),
    path('userform/<str:formtype>/<str:id>/', views.userform, name='userform'),
    path('source/companyadmin/', views.companyadmin, name='companyadmin'),
    path('source/parent/', views.parent, name='parent'),
    path('source/schooladmin/', views.schooladmin, name='schooladmin'),
    path('source/student/', views.studentview, name='student'),
    path('allform/<str:formtype>/<str:id>', views.allform,name='allform'),
    path('teacher/home/', views.TeacherView.as_view(), name='teacher'),
    path('teacher/courses/', views.courses, name='courses'),
    path('teacher/topics/', views.topic, name='topic'),
    path('teacher/students/', views.students, name='students'),
    path('teacher/questioncreate/<str:quizid>/', views.question, name='question'),
    path('teacher/classes/', views.classes, name='classes'),
    path('teacher/quizcreate/', views.quizcreate, name='quizcreate'),

    path('sidenav/', views.sidebarnav, name='sidenav'),
    path('editprofile/', views.editprofile, name = 'editprofile'),
    path('verify/', views.verifyemail, name = 'verify'),
    path('forgot/', views.forgotpass, name = 'forgot'),

# For Quiz
    path('quiz/', views.tabquiz, name='tabquiz'),
    path('takequiz/', views.takequiz, name='takequiz'),
    path('quizlist/', views.quizlist, name='quizlist'),
    path('coursequiz/', views.coursequiz, name='coursequiz'),
    path('coursequiz/', views.quizforfun, name='quizforfun'),

# For Schooladmin
    path('grade/', views.grade, name='grade'),

# For Assigning teacher
    path('assign/', views.assign, name='assign'),


# for showing particular course of particulat grade
    path('viewcourse/<str:id>/', views.viewcourse, name='viewcourse'),
    path('delete/<str:quizid>/<str:deleteid>/', views.delete, name='deletequestion'),
    path('details/<str:questionid>/', views.questiondetail, name='questiondetail'),
]
