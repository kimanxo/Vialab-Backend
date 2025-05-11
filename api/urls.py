from django.urls import path
from api.Views.faqs import FAQsView, FAQView
from api.Views.exams import ExamView, ExamsView, AvailableExamsView
from api.Views.announcements import AnnouncementsView, AnnouncementView
from api.Views.about import AboutView
from api.Views.feedbacks import FeedbacksView, FeedbackView
from api.Views.newsletters import  joiNewsletterView
from api.Views.orders import OrderView, OrderCheckView, OrderEmailView, OrdersView
from api.Views.password import ChangePasswordView 
from api.Views.statistics import StatisticsView
from api.Views.financials import FinancialStatisticsView
from rest_framework_simplejwt.views import  TokenRefreshView, TokenObtainPairView
# from api.Views.auth import CustomObtainPairView

urlpatterns = [
    path("", StatisticsView.as_view()),
    path("about", AboutView.as_view()),
]


faqs_urls = [
    path("faqs", FAQsView.as_view()),
    path("faqs/<int:id>", FAQView.as_view()),
]

exams_urls = [
    path("exams", ExamsView.as_view()),
    path("exams/<int:id>", ExamView.as_view()),
    path("availablExams", AvailableExamsView.as_view()),
]

orders_urls = [
    path("orders", OrdersView.as_view()),
    path("orders/<int:id>", OrderView.as_view()),
    path("orderCheck", OrderCheckView.as_view()),
    path("orderEmail", OrderEmailView.as_view()),
]

announcements_urls = [
    path("ads", AnnouncementsView.as_view()),
    path("ads/<int:id>", AnnouncementView.as_view()),
]


feedbacks_urls = [
    path("feedbacks", FeedbacksView.as_view()),
    path("feedbacks/<int:id>", FeedbackView.as_view()),
]




newsletters_url = [
    path("joiNewsletter", joiNewsletterView.as_view()),
]


Statistics_url = [
    path(
        "financials/<int:year>/<int:month>/<int:week>",
        FinancialStatisticsView.as_view(),
    ),
]


auth_urls = [
    path("token", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("token/refresh", TokenRefreshView.as_view(), name="token_refresh"),
    path("password/change", ChangePasswordView.as_view(), name="change_password")
]


## adding the url sets to the global url patterns
urlpatterns += exams_urls
urlpatterns += orders_urls
urlpatterns += faqs_urls
urlpatterns += announcements_urls
urlpatterns += newsletters_url
urlpatterns += auth_urls
urlpatterns += feedbacks_urls
urlpatterns += Statistics_url
