from django.contrib import admin
from django.urls import path
from predictionUI.views import HomePageView, EmployeeCreateView, EmployeeCUpdateView, EmployeeCDeleteView , EmployeeList, linear_regression_view
from predictionUI import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', HomePageView.as_view(), name='home'),
    path('employee_list', EmployeeList.as_view(), name='employee-list'),
    path('employee_list/add', EmployeeCreateView.as_view(), name='employee-add'),
    path('employee_list/<pk>', EmployeeCUpdateView.as_view(), name='employee-update'),
    path('employee_list/<pk>/delete', EmployeeCDeleteView.as_view(), name='employee-delete'),
    path('prediction', linear_regression_view, name='prediction-show'),
]
