from flask import render_template
from . import main
from .forms import DataForm
from ..ml import predict


@main.route('/', methods=['GET', 'POST'])
def index():
    form = DataForm()

    if form.validate_on_submit():
        
        data = {"Gender":form.gender.data,
                "Age":form.age.data,
                "Driving_License":form.driving_license.data,
                "Region_code":float(form.region_code.data),
                "Previously_Insured":form.previously_insured.data,
                "Vehicle_Age":form.vehicle_age.data,
                "Vehicle_Damage":form.vehicle_damage.data,
                "Annual_Premium":form.annual_premium.data,
                "Policy_Sales_Channel":float(form.policy_sales_channel.data),
                "Vintage": form.vintage.data}

        response, confidence = predict(data)
        print(response, confidence)
        return render_template('index.html', form=form, response=response, confidence=confidence)


    return render_template('index.html', form=form)
