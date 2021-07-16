from numpy.core.records import array
import pandas as pd
import numpy as np
from sklearn import metrics
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from django.shortcuts import render, redirect

# Create your views here.

def diabetes(request):
    context = dict()

    if request.method == 'POST':
        glucose = int(request.POST['glucose_name'])
        blood_pressure = int(request.POST['blood_pressure_name'])
        insulin = int(request.POST['insulin_name'])
        pedigree = float(request.POST['pedigree_name'])

        data_set = pd.read_csv('diabetes.csv')

        x = np.array(data_set[['Glucose', 'BloodPressure', 'Insulin', 'DiabetesPedigreeFunction']])
        y = np.array(data_set['Outcome'])

        x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=.33, random_state=42)
        model = LogisticRegression()
        model.fit(x_train, y_train)

        y_predict = model.predict([[glucose, blood_pressure, insulin, pedigree]])

        probability = model.predict_proba([[glucose, blood_pressure, insulin, pedigree]])

        if y_predict[0]:
            context['diabetes'] = 'Diabetic!'
        else:
            context['diabetes'] = 'Not Diabetic!'

        context['positive'] = round(probability[0][1] * 100, 2)
        context['negative'] = round(probability[0][0] * 100, 2)

        return render(request, 'diabetes/index.html', context)
    else:
        context['diabetes'] = 'Not Diabetic!'
        context['positive'] = 0
        context['negative'] = 0
        return render(request, 'diabetes/index.html', context)