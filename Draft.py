# Imports
import pandas as pd
import mysql.connector
from sqlalchemy import create_engine
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
import matplotlib.pyplot as plt
from sklearn.metrics import r2_score
import numpy as np

# Test Connection to database (MySQL)
conn_params = {
    'host' : 'localhost',
    'user' : 'root',
    'password' : '12345',
    'database' : 'hrm_feature'
}

# Connection to database (MySQL)
connection_string = 'mysql+mysqlconnector://root:12345@localhost/hrm_feature'

# Test the Connection of Database
try:
    conn = mysql.connector.connect(**conn_params)
    print("Connection to the database successful.")

except mysql.connector.Error as err:
    print(f"Error: {err}")

# To Connect
engine = create_engine(connection_string)

# SQL query
query = """SELECT TIMESTAMPDIFF(YEAR, birthdate, CURDATE()) as age , employees.sex as gender, 
employees.civil_status, count(employees_relatives.Relatives_idrelatives) as relative_size,
TIMESTAMPDIFF(YEAR, service_records.appointment_start_date, service_records.appointment_end_date) as work_experiences, 
CAST(service_records.monthly_salary AS SIGNED) as monthly_salary FROM employees

INNER JOIN employees_relatives ON employees.idemployees = employees_relatives.employees_idemployees 
INNER JOIN service_records ON employees.idemployees = service_records.employees_idemployees
INNER JOIN employees_unitassignments ON employees.idemployees = employees_unitassignments.employees_idemployees
group by age, gender, employees.civil_status, service_records.monthly_salary, work_experiences LIMIT 100"""

# Execute query using pandas to read and sqlalchemy to execute table
df = pd.read_sql(query, engine)
engine.dispose()

df['gender'] = df['gender'].astype('category')
df['gender'] = df['gender'].cat.codes
df['civil_status'] = df['civil_status'].astype('category')
df['civil_status'] = df['civil_status'].cat.codes

X = df.drop(columns=['monthly_salary'])
y = df['monthly_salary']

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.5, random_state= 0)

lr = LinearRegression()
lr.fit(X_train, y_train)

# Intercept
c = lr.intercept_
# Coeficent
m = lr.coef_

y_pred_train = lr.predict(X_train)

plt.scatter(y_train, y_pred_train)
plt.xlabel("Actual Monthly Salary")
plt.ylabel("Predicted Monthly Salary")
plt.show()

r2_score(y_train, y_pred_train)