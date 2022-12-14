from django.urls import include, path
from django.contrib import admin

from .views import classroom, patients, teachers

urlpatterns = [
    path('', classroom.home, name='home'),
    path('admin/', admin.site.urls ),

    path('patients/', include(([
        path('', patients.QuizListView.as_view(), name='quiz_list'),
        path('interests/', patients.PatientInterestsView.as_view(), name='patient_interests'),
        path('taken/', patients.TakenQuizListView.as_view(), name='taken_quiz_list'),
        path('quiz/<int:pk>/', patients.take_quiz, name='take_quiz'),
    ], 'classroom'), namespace='patients')),

    path('teachers/', include(([
        path('', teachers.QuizListView.as_view(), name='quiz_change_list'),
        path('quiz/add/', teachers.QuizCreateView.as_view(), name='quiz_add'),
        path('quiz/<int:pk>/', teachers.QuizUpdateView.as_view(), name='quiz_change'),
        path('quiz/<int:pk>/delete/', teachers.QuizDeleteView.as_view(), name='quiz_delete'),
        path('quiz/<int:pk>/results/', teachers.QuizResultsView.as_view(), name='quiz_results'),
        path('quiz/<int:pk>/question/add/', teachers.question_add, name='question_add'),
        path('quiz/<int:quiz_pk>/question/<int:question_pk>/', teachers.question_change, name='question_change'),
        path('quiz/<int:quiz_pk>/question/<int:question_pk>/delete/', teachers.QuestionDeleteView.as_view(), name='question_delete'),
    ], 'classroom'), namespace='teachers')),
]
