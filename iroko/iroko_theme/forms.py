from flask_babelex import lazy_gettext as _
from flask_wtf import RecaptchaField, FlaskForm
from wtforms import TextAreaField, StringField, validators, BooleanField, SelectField

from iroko.utils import IrokoVocabularyIdentifiers
from iroko.vocabularies.models import Vocabulary, Term


class ContactForm(FlaskForm):
    email = StringField(_('Email'), [validators.DataRequired(), validators.Email()])
    subject = StringField(_('Subject'), [validators.DataRequired(), validators.Length(max=150)])
    message = TextAreaField(_('Message'), [validators.DataRequired()])
    recaptcha = RecaptchaField()


class IrokoSearchForm(FlaskForm):
    institutions = SelectField(
        _("Institucion"),
        id='iroko_search_form_institutions',
        coerce=str)
    status = BooleanField(label=_("Oficial"))

    def __init__(self, *args, **kwargs):
        super(IrokoSearchForm, self).__init__()
        voc = Vocabulary.query.filter_by(identifier=IrokoVocabularyIdentifiers.CUBAN_INTITUTIONS.value).first()
        self.institutions.choices = [(str(choice.uuid), choice.name) for choice in
                                     Term.query.filter_by(vocabulary_id=voc.identifier, parent_id=None).all()]
