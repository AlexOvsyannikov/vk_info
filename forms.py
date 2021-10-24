from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms.validators import DataRequired

class VK_LINK(FlaskForm):
    vk_link = StringField('Страница ВК', validators=[DataRequired()])


