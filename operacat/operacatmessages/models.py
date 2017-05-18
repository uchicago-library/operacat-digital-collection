from django.db import models
from django.core.mail import send_mail
from datetime import date

from modelcluster.fields import ParentalKey
from wagtail.wagtailadmin.edit_handlers import (FieldPanel, FieldRowPanel,
    InlinePanel, MultiFieldPanel)
from wagtail.wagtailcore.fields import RichTextField
from wagtail.wagtailforms.models import AbstractEmailForm, AbstractFormField

# Create your models here.


class FormField(AbstractFormField):
    page = ParentalKey('FormPage', related_name='form_fields')

class FormPage(AbstractEmailForm):
    intro = RichTextField(blank=True)
    thank_you_text = RichTextField(blank=True)

    content_panels = AbstractEmailForm.content_panels + [
        FieldPanel('intro', classname="full"),
        InlinePanel('form_fields', label="Form fields"),
        FieldPanel('thank_you_text', classname="full"),
        MultiFieldPanel([
            FieldRowPanel([
                FieldPanel('from_address', classname="col6"),
                FieldPanel('to_address', classname="col6"),
            ]),
            FieldPanel('subject'),
        ], "Email"),
    ]

    def send_mail(self, form):
        addresses = [x.strip() for x in self.to_address.split(',')]
        print(addresses)
        content = []
        for field in form:
            value = field.value()
            if isinstance(value, list):
                value = ', '.join(value)
            content.append('{}: {}'.format(field.label, value))
        submitted_date_str = date.today().strftime('%x')
        content.append('{}: {}'.format(
            'Submitted', submitted_date_str))
        content.append('{}: {}'.format(
            'Submitted Via', self.full_url))
        content = '\n'.join(content)
        subject = self.subject + " - " + submitted_date_str
        send_mail(subject, content, self.from_address, addresses)
