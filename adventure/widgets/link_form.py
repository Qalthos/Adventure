"""Forms for editing cards and links."""

from tw.api import WidgetsList
from tw.forms import TableForm, SingleSelectField, TextField, HiddenField, CheckBox
from tw.forms.validators import NotEmpty


class LinkForm(TableForm):

    class fields(WidgetsList):
        id = HiddenField()
        card_id = TextField(validator=NotEmpty)
        direction = TextField(validator=NotEmpty)
        new_card_id = SingleSelectField(validator=NotEmpty)
        reverse = CheckBox()


create_link_form = LinkForm("create_link_form", action='save_new_link')
edit_link_form = LinkForm("edit_link_form", action='save_edited_link')
