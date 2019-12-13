from django.urls import path
from .views import ProjectAddView, ProjectEditView, ProjectAddViewWithParameter, ProjectDeleteView
from daily_report.views import WageAddView, CostView

appname='daily_report'
urlpatterns = [
    path('add', ProjectAddView.as_view(),name='add'),
    path('edit', ProjectEditView.as_view(), name='edit'),
    path('show/<int:pk>', ProjectAddViewWithParameter.as_view(), name='show_para'),
    path('delete', ProjectDeleteView.as_view(), name='delete'),
    path('add_wage', WageAddView.as_view(), name='add_wage'),
    path('show_cost', CostView.as_view(), name='show_cost'),
    ]