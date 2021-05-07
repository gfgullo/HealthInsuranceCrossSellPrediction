from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, SelectField, BooleanField, SubmitField
# from flask.ext.wtf.html5 import NumberInput
from wtforms.widgets import TextArea
from wtforms.validators import DataRequired, length


class DataForm(FlaskForm):

    GENDER_VALUES = ['Male', 'Female' ]

    VEHICLE_AGE_VALUES = ["> 2 Years", "1-2 Year", "< 1 Year"]

    REGION_CODE_VALUES = [ 0,  1,  2,  3,  4,  5,  6,  7,  8,  9, 10, 11, 12, 13, 14, 15, 16,
       17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33,
       34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50,
       51, 52]

    POLICY_SALES_CHANNEL_VALUES = [  1,   2,   3,   4,   6,   7,   8,   9,  10,  11,  12,  13,  14,
        15,  16,  17,  18,  19,  20,  21,  22,  23,  24,  25,  26,  27,
        28,  29,  30,  31,  32,  33,  34,  35,  36,  37,  38,  39,  40,
        41,  42,  43,  44,  45,  46,  47,  48,  49,  50,  51,  52,  53,
        54,  55,  56,  57,  58,  59,  60,  61,  62,  63,  64,  65,  66,
        67,  68,  69,  70,  71,  73,  74,  75,  76,  78,  79,  80,  81,
        82,  83,  84,  86,  87,  88,  89,  90,  91,  92,  93,  94,  95,
        96,  97,  98,  99, 100, 101, 102, 103, 104, 105, 106, 107, 108,
       109, 110, 111, 112, 113, 114, 115, 116, 117, 118, 119, 120, 121,
       122, 123, 124, 125, 126, 127, 128, 129, 130, 131, 132, 133, 134,
       135, 136, 137, 138, 139, 140, 143, 144, 145, 146, 147, 148, 149,
       150, 151, 152, 153, 154, 155, 156, 157, 158, 159, 160, 163]

    DEFAULT = {"Gender":"Male",
            "Age":29,
            "Driving_License":True,
            "Region_Code":REGION_CODE_VALUES[0],
            "Previously_Insured":False,
            "Vehicle_Age":"> 2 Years",
            "Vehicle_Damage":True,
            "Annual_Premium":1200.0,
            "Policy_Sales_Channel":POLICY_SALES_CHANNEL_VALUES[0],
            "Vintage": 217}
    """
    DEFAULT = {"Gender":None,
            "Age":None,
            "Driving_License":None,
            "Region_Code":None,
            "Previously_Insured":None,
            "Vehicle_Age":None,
            "Vehicle_Damage":None,
            "Annual_Premium":None,
            "Policy_Sales_Channel":None,
            "Vintage": None}
    """

    BASE_VALIDATORS = [DataRequired()]

    gender = SelectField('Gender', choices=GENDER_VALUES, validators=BASE_VALIDATORS, default=DEFAULT["Gender"])
    age = IntegerField(validators=BASE_VALIDATORS, default=DEFAULT["Age"])
    driving_license = BooleanField('Driving License', default=DEFAULT["Driving_License"])
    region_code = SelectField('Region Code', choices=REGION_CODE_VALUES, validators=BASE_VALIDATORS, default=DEFAULT["Region_Code"])
    previously_insured = BooleanField('Previously Insured', default=DEFAULT["Previously_Insured"])
    vehicle_age = SelectField('Vehicle Age', choices=VEHICLE_AGE_VALUES, validators=BASE_VALIDATORS, default=DEFAULT["Vehicle_Age"])
    vehicle_damage = BooleanField('Vehicle Damage', default=DEFAULT["Vehicle_Damage"])
    annual_premium = StringField('Annual Premium', validators=BASE_VALIDATORS, default=DEFAULT["Annual_Premium"] )
    policy_sales_channel = SelectField('Policy Sales Channel', choices=POLICY_SALES_CHANNEL_VALUES, validators=BASE_VALIDATORS, default=DEFAULT["Policy_Sales_Channel"])
    vintage = IntegerField(validators=BASE_VALIDATORS, default=DEFAULT["Vintage"])
    submit = SubmitField('Predict')
