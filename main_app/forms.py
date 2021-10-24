from django.forms import ModelForm
from .models import Comment

# this is what will be included on the events_detail page
# 1:M relationship

class CommentForm(ModelForm):
    class Meta:
        model = Comment
        fields = []