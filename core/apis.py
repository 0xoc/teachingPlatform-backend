from django.conf.urls import url
from django.urls import path
from .views import UserProfileCreateView, ClassRoomCreateView, ClassRoomRetrieveView, QuizCreateView, RegisterQuitClass, \
    AddRemoveStudentClass, ClassRoomUpdateView, QuizQuestionsList, AddQuizQuestion, RUDQuestion, StartQuiz, \
    CreateAnswer, QuizAnswerDetailedView, SetScoreView, ClassList, AuthenticateView

from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework.authtoken import views

schema_view = get_schema_view(
   openapi.Info(
      title="Teaching Platform API",
      default_version='v1',
      description="API Documents",
      contact=openapi.Contact(email="snparvizi752@gmail.com"),
      license=openapi.License(name="GPL V3 License"),
   ),
   public=True,
   permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path('user/create', UserProfileCreateView.as_view()),

    # create retrieve class
    path('class/create/', ClassRoomCreateView.as_view()),
    path('class/<int:class_id>/', ClassRoomRetrieveView.as_view()),
    path('class/list/', ClassList.as_view()),
    path('class/<int:class_id>/update/', ClassRoomUpdateView.as_view()),

    path('class/<int:class_id>/register/', RegisterQuitClass.as_view()),
    path('class/<int:class_id>/register/<user_username>/', AddRemoveStudentClass.as_view()),

    path('class/<int:class_id>/quiz/create/', QuizCreateView.as_view()),

    path('quiz/<int:quiz_id>/question/create/', AddQuizQuestion.as_view()),
    path('question/<int:question_id>/', RUDQuestion.as_view()),

    path('quiz/<int:quiz_id>/questions/', QuizQuestionsList.as_view()),
    path('quiz/<int:quiz_id>/start/', StartQuiz.as_view()),
    path('submit-answer/', CreateAnswer.as_view()),
    path('quiz-answer/<int:quiz_answer_id>/', QuizAnswerDetailedView.as_view()),
    path('answer/<int:answer_id>/set-score/', SetScoreView.as_view()),

    path('api-token-auth/', AuthenticateView.as_view()),

    url(r'^swagger(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    url(r'^swagger/$', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    url(r'^redoc/$', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),

]