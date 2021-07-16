from django.shortcuts import redirect, render
import pandas as pd
import json
# Create your views here.

def linear_regression(value=0):
    data_set = pd.read_csv('dataset.csv')

    population = data_set['population']
    sales = data_set['sales']

    population_mean = population.mean()
    sales_mean = sales.mean()

    population_sum = population[:] - population_mean
    sales_sum = sales[:] - sales_mean

    m = (population_sum * sales_sum).sum() / (population_sum ** 2).sum()
    c = sales_mean - (m * population_mean)

    return {
        'regression': m * value + c,
        'population': population,
        'sales': sales,
        'data_set': data_set
    }


def index(request):
    context = dict()

    if request.method == 'GET':
        regression = linear_regression()
        data_set = dict(regression['data_set'].values)

        datas = list()
        for key, data in data_set.items():
            datas.append({
                'x': key,
                'y': data
            })

        context['regression'] = json.dumps({})
        context['data'] = json.dumps(datas)
        context['result'] = 0

        return render(request, 'app/index.html', context)
    elif request.method == 'POST':
        context = dict()

        population = float(request.POST['population'])
        regression = linear_regression(population)
        data_set = dict(regression['data_set'].values)

        datas = list()
        for key, data in data_set.items():
            datas.append({
                'x': key,
                'y': data
            })

        context['data'] = json.dumps(datas)
        
        result = regression['regression']
        context['regression'] = json.dumps({
            'x': population,
            'y': result
        })
        context['result'] = result

        return render(request, 'app/index.html', context)