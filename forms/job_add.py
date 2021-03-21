from flask_wtf import FlaskForm
from wtforms import PasswordField, StringField, SubmitField, IntegerField, DateField, BooleanField
from wtforms.fields.html5 import EmailField
from wtforms.validators import DataRequired


class AddJobForm(FlaskForm):
    politryk_id = IntegerField('id политрука', validators=[DataRequired()])
    name = StringField('Описание работы для профсоюза', validators=[DataRequired()])
    plan = IntegerField('Объём плана', validators=[DataRequired()])
    ids_tovarishei = StringField('Бригада, выполняющая план', validators=[DataRequired()])
    start_of_piatiletka = StringField('Дата начала пятилетки', validators=[DataRequired()])
    end_of_piatiletka = StringField('Срок выполнения плана', validators=[DataRequired()])
    result_of_plan = BooleanField('Перевыполнили?')
    submit = SubmitField('Утвердить план')


