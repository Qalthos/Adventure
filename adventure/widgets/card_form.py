"""Forms for editing cards."""

from tw.api import WidgetsList
from tw.forms import TableForm, TextField, HiddenField, FileField
from tw.forms.validators import NotEmpty


class CardForm(TableForm):

    class fields(WidgetsList):
        id = HiddenField()
        image = FileField(validator=NotEmpty)
        description = TextField(validator=NotEmpty)
        special = TextField()


create_card_form = CardForm("create_card_form", action='save_new_card')
edit_card_form = CardForm("edit_card_form", action='save_edited_card')
