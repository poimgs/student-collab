from django.urls import path, include
from rest_framework import routers
# from rest_framework_nested import routers
# from .views import RoomViewSet, QuestionViewSet, AnswerViewSet
from .views import RoomViewSet

router = routers.DefaultRouter()
router.register('rooms', RoomViewSet, basename='rooms')
# router.register('units', UnitViewSet, basename='units')

urlpatterns = router.urls

# rooms_router = routers.NestedDefaultRouter(router, 'rooms', lookup='room')
# rooms_router.register('questions', QuestionViewSet, basename='room-questions')

# questions_router = routers.NestedDefaultRouter(rooms_router, 'questions', lookup='question')
# questions_router.register('answers', AnswerViewSet, basename='question-answers')

# urlpatterns = [
#     path('', include(router.urls)),
#     # path('', include(rooms_router.urls)),
#     # path('', include(questions_router.urls)),
# ]
