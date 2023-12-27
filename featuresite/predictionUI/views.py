from django.shortcuts import render
from django.views.generic.list import ListView
from predictionUI.models import EmployeeData
from predictionUI.forms import EmployeeForm
from django.views.generic.edit import UpdateView, DeleteView, CreateView
from django.urls import reverse_lazy

import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('Agg')
from io import BytesIO
import base64

# Create your views here.
class HomePageView(ListView):
    model = EmployeeData
    context_object_name = 'home'
    template_name = "base.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

# class PredictionPageView(ListView):
#     model = EmployeeData
#     context_object_name = 'prediction'
#     template_name = "prediction.html"

#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)

class EmployeeList(ListView):
    model = EmployeeData
    context_object_name = 'employee'
    template_name = "employee.html"
    paginate_by = 10

class EmployeeCreateView(CreateView):
    model = EmployeeData
    form_class = EmployeeForm
    template_name = 'add.html'
    success_url = reverse_lazy('employee-list')

class EmployeeCUpdateView(UpdateView):
    model = EmployeeData
    form_class = EmployeeForm
    template_name = 'update.html'
    success_url = reverse_lazy('employee-list')

class EmployeeCDeleteView(DeleteView):
    model = EmployeeData
    template_name = 'delete.html'
    success_url = reverse_lazy('employee-list')


def linear_regression_view(request):
    # Retrieve data from the EmployeeData model
    employee_data = EmployeeData.objects.all()

    # Extract relevant features and target variable, excluding date fields
    features = ['age', 'gender', 'civil_status', 'relative_size', 'work_experiences']
    X = employee_data.values(*features)
    y = employee_data.values('monthly_salary')

    # Convert queryset data to pandas DataFrame
    df = pd.DataFrame(list(employee_data.values()))

    # Convert categorical variables to numerical codes
    df['gender'] = df['gender'].astype('category').cat.codes
    df['civil_status'] = df['civil_status'].astype('category').cat.codes

    # Split the data into training and testing sets
    X_train, X_test, y_train, y_test = train_test_split(df[features], df['monthly_salary'], test_size=0.5, random_state=0)

    # Train the linear regression model
    lr = LinearRegression()
    lr.fit(X_train, y_train)

    # Predict monthly salary for the training set
    y_pred_train = lr.predict(X_train)

    # Plotting and converting to base64 for HTML display
    plt.scatter(y_train, y_pred_train)
    plt.xlabel("Actual Monthly Salary")
    plt.ylabel("Predicted Monthly Salary")
    plt.title("Linear Regression Results")
    buffer = BytesIO()
    plt.savefig(buffer, format='png')
    plt.close()
    plot_data = base64.b64encode(buffer.getvalue()).decode('utf-8')

    # Pass relevant data to the template
    context = {
        'plot_data': plot_data,
        'r2_score': r2_score(y_train, y_pred_train),
        # Any other data you want to pass
    }

    return render(request, 'prediction.html', context)
