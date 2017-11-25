from allauth.account.views import SignupView, LoginView
from allauth.account.forms import LoginForm, SignupForm
from django.shortcuts import redirect, reverse


class SignupLogin(SignupView):
    template_name = "account/login-or-signup.html"

    def get_context_data(self, **kwargs):
        if 'form' in self.request.session and 'login_form' in self.request.session:
            ctx = {}
            if self.request.session['form']:
                ctx['form'] = SignupForm(self.request.session['form'])
                ctx['form'].is_valid()
            else:
                ctx['form'] = SignupForm()
            if self.request.session['login_form']:
                ctx['login_form'] = LoginForm(self.request.session['login_form'])
                ctx['login_form'].is_valid()

            else:
                ctx['login_form'] = LoginForm()
            del self.request.session['form']
            del self.request.session['login_form']
        else:
            ctx = super(SignupView, self).get_context_data(**kwargs)
            ctx['login_form'] = LoginForm()
        return ctx


class RedirectFormInvalidMixin(object):
    def form_invalid(self, form):
        if 'login' in self.request.POST:
            ctx = {}
            ctx['login_form'] = self.get_form_kwargs()['data']
            ctx['form'] = {}
        else:
            ctx = {}
            ctx['form'] = self.get_form_kwargs()['data']
            ctx['login_form'] = {}
        self.request.session['form'] = ctx['form']
        self.request.session['login_form'] = ctx["login_form"]
        return redirect(reverse('login-signup'))


class SignUp(RedirectFormInvalidMixin, SignupView):
    pass


class Login(RedirectFormInvalidMixin, LoginView):
    pass
