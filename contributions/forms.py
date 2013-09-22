# Summary: Forms for adding new contributions(Posts) and contributions' comments
from django.forms import ModelForm
from contributions.models import Comments, Posts

class CommentForm(ModelForm):
    class Meta:
        model = Comments
        fields = ('text','contribution_id')

class PostForm(ModelForm):
    class Meta:
        model = Posts
        fields = ('description','formatted_description','title')