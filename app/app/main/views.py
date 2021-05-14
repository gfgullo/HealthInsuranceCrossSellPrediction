from flask import render_template, request, session
from flask_session import Session
from . import main
from .forms import DataForm
from ..ml import predict
import codecs


@main.route('/', methods=['GET', 'POST'])
def index():

    form = DataForm()

    if form.validate_on_submit():
        
        data =  [{"Gender":form.gender.data,
                "Age":form.age.data,
                "Driving_License":form.driving_license.data,
                "Region_code":float(form.region_code.data),
                "Previously_Insured":form.previously_insured.data,
                "Vehicle_Age":form.vehicle_age.data,
                "Vehicle_Damage":form.vehicle_damage.data,
                "Annual_Premium":form.annual_premium.data,
                "Policy_Sales_Channel":float(form.policy_sales_channel.data),
                "Vintage": form.vintage.data}]

        response, confidence = predict(data)

        return render_template('index.html', form=form, response=response[0], confidence=confidence[0])

    return render_template('index.html', form=form)



@main.route('/batch', methods=['GET', 'POST'])
def batch():
    if request.method == 'POST':
        print("-------POST------")
        f = request.files.get('file')
        stream = codecs.iterdecode(f.stream, 'utf-8')

        data = []
        print("-------1-------")
        for line in stream:
            print(line)
            sample = line.replace("\n","").split(",")
            data.append(
                {"Gender": sample[0],
                 "Age": sample[1],
                 "Driving_License": sample[2],
                 "Region_code": float(sample[3]),
                 "Previously_Insured": sample[4],
                 "Vehicle_Age": sample[5],
                 "Vehicle_Damage": sample[6],
                 "Annual_Premium": sample[7],
                 "Policy_Sales_Channel": float(sample[8]),
                 "Vintage": sample[9]}
            )

        response, confidence = predict(data)
        print(response)
        session['data'] = data
        session['response'] =response
        session['confidence'] = confidence
        
    return render_template('batch.html')


@main.route('/result', methods=['GET', 'POST'])
def result():
    return render_template('result.html', data=session['data'], response=session['response'], confidence=session['confidence'])
