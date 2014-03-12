from django import template
from django.template.loader import get_template

from labgeeks_people.models import ReviewForm
from labgeeks_people.forms import SaveForm

register = template.Library()


class BuiltFormNode(template.Node):

    def __init__(self, name, value):
        self.name = name
        self.value = value

    def render(self, context):
        request = context["request"]
        user = getattr(request, "user", None)
        post = getattr(request, "POST", None)
        if self.name != "form":
            lookup = {
                str(self.name): template.Variable(self.value).resolve(context)
            }
            try:
                form = ReviewForm.objects.published(for_user=user).get(**lookup)
            except ReviewForm.DoesNotExist:
                form = None
        else:
            form = template.Variable(self.value).resolve(context)
        if not isinstance(form, ReviewForm) or (form.login_required and not
                                          user.is_authenticated()):
            return ""
        t = get_template("form.html")
        context["form"] = form
        form_args = (form, context, post or None)
        context["save_form"] = SaveForm(*form_args)
        return t.render(context)


@register.tag
def build_reviewform(parser, token):

    try:
        _, arg = token.split_contents()
        if "=" not in arg:
            arg = "form=" + arg
        name, value = arg.split("=", 1)
        if name not in ("form", "id", "slug"):
            raise ValueError
    except ValueError:
        e = ()
        raise template.TemplateSyntaxError(render_built_form.__doc__)
    return BuiltFormNode(name, value)
