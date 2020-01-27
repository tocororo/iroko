from flask_wtf import Form, RecaptchaField, FlaskForm
from wtforms import TextField, PasswordField, TextAreaField, StringField, validators
from flask_babelex import lazy_gettext as _


class ContactForm(FlaskForm):   
      email = StringField(_('Email'), [validators.DataRequired(), validators.Email()])
      subject = StringField(_('Subject'), [validators.DataRequired(), validators.Length(max=150)])      
      message = TextAreaField(_('Message'), [validators.DataRequired()])
      #recaptcha = RecaptchaField()