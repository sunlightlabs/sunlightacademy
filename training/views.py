from cStringIO import StringIO
import datetime

from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.views import logout
from django.contrib.sites.models import RequestSite, Site
from django.core.mail import send_mail
from django.db.models import Count
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render, redirect
from django.template.loader import render_to_string
from django.views.generic import DetailView
from registration import signals
from registration.models import RegistrationProfile
from registration.views import RegistrationView
import unicodecsv

from training.forms import SettingsForm, AccountSetupForm, UniqueEmailRegistrationForm, FeedbackForm
from training.models import Profile, Module, Completion, Category, Training


def dashboard(request):
    """ The user dashboard.
    """

    if request.user.is_authenticated():

        categories = Category.objects.all() \
            .prefetch_related('modules') \
            .annotate(num_modules=Count('modules')) \
            .order_by('name') \
            .select_related()

        modules = Module.objects.filter(is_public=True)
        completed_ids = modules.filter(completions__user=request.user).values_list('id', flat=True)

        context = {
            #'modules': modules,
            'categories': categories,
            'completed_ids': completed_ids,
        }

        return render(request, 'dashboard.html', context)
    else:
        return render(request, 'index.html')


def category(request, slug):

    if request.user.is_authenticated():

        category = Category.objects.get(slug=slug)
        modules = category.modules.filter(is_public=True)
        completed_ids = modules.filter(completions__user=request.user).values_list('id', flat=True)

        context = {
            'category': category,
            'modules': modules,
            'completed_ids': completed_ids,
        }

        return render(request, 'category.html', context)

    else:
        return render(request, 'index.html')


class ModuleView(DetailView):
    model = Module
    context_object_name = 'module'

    def get_queryset(self):
        if self.request.user.is_staff:
            return Module.objects.all()
        return Module.objects.filter(is_public=True)

    def get_context_data(self, **kwargs):
        context = super(ModuleView, self).get_context_data(**kwargs)
        context['categories'] = Category.objects.all().prefetch_related('modules')
        if self.request.user.is_authenticated():
            modules = self.get_queryset()
            context['completed_ids'] = modules.filter(completions__user=self.request.user).values_list('id', flat=True)
        return context

# def module(request, slug):

#     else:
#         completed_ids = []

#     return object_detail(request,
#         queryset=modules,
#         slug=slug,
#         template_name='module_detail.html',
#         template_object_name='module',
#         extra_context={
#             'completed_ids': completed_ids,
#             #'other_modules': other_modules,
#             'categories': categories,
#         })


def module_feedback(request, slug):

    if not request.user.is_authenticated():
        return redirect('training_module', slug=slug)

    module = get_object_or_404(Module, is_public=True, slug=slug)

    if request.method == 'POST':

        form = FeedbackForm(request.POST)

        if form.is_valid():

            feedback = form.save()

            send_mail(
                '[Sunlight Academy] Feedback on %s' % module.title,
                render_to_string('email/feedback.txt', {'feedback': feedback}),
                'contact@sunlightfoundation.com',
                ['angai@sunlightfoundation.com'],
                fail_silently=True)

            messages.success(request, "Thank you for your feedback!")
            return redirect('training_module', slug=slug)

    else:
        form = FeedbackForm(initial={'module': module, 'user': request.user})

    context = {
        'form': form,
        'module': module,
    }

    return render(request, 'module_feedback.html', context)


def module_mark(request, slug):

    if request.method == 'POST':

        module = get_object_or_404(Module, is_public=True, slug=slug)
        is_completed = request.POST.get('completed', '') == '1'

        if is_completed:
            Completion.objects.get_or_create(user=request.user, module=module)
        else:
            module.completions.filter(user=request.user).delete()

        if request.is_ajax():
            return HttpResponse('1' if is_completed else '0', content_type='text/plain')

    return HttpResponseRedirect('/module/%s/' % slug)


def tagged(request, slug):
    tag = Category.objects.get(slug=slug)
    modules = Module.objects.filter(is_public=True, category=tag)
    return render(request, 'module_list.html', {'modules': modules, 'tag': tag})


def training_list(request):
    today = datetime.date.today()
    upcoming = Training.objects.filter(is_public=True, date__gte=today)
    previous = Training.objects.filter(is_public=True, date__lt=today)
    return render(request, 'training_list.html',
        {'upcoming': upcoming, 'previous': previous})


def training_detail(request, slug):
    training = get_object_or_404(Training, is_public=True, slug=slug)
    return render(request, 'training_detail.html', {'training': training})


class RegisterPlusView(RegistrationView):

    form_class = UniqueEmailRegistrationForm
    success_url = '/account/register/complete/'

    def register(self, request, **cleaned_data):

        username, email, password = cleaned_data['username'], cleaned_data['email'], cleaned_data['password1']
        if Site._meta.installed:
            site = Site.objects.get_current()
        else:
            site = RequestSite(request)

        user = RegistrationProfile.objects.create_inactive_user(username, email,
                                                                password, site)
        signals.user_registered.send(sender=self.__class__,
                                     user=user,
                                     request=request)

        try:
            user.get_profile()
        except Profile.DoesNotExist:
            profile = Profile(
                user=user,
                phone=cleaned_data.get('phone', ''),
                organization=cleaned_data.get('organization', ''),
                is_a=cleaned_data.get('is_a', ''),
                interests=cleaned_data.get('interests', ''),
                notify=cleaned_data.get('notify'),
            )
            profile.save()

        return user


def account(request):

    if not request.user.is_authenticated():
        return HttpResponseRedirect('/account/login/')

    if request.method == 'POST':

        form = SettingsForm(request.POST)

        if form.is_valid():

            still_valid = True

            user = request.user

            qs = User.objects.exclude(pk=user.pk)

            if qs.filter(email=form.cleaned_data['email']).exists():
                form.errors['email'] = ['Email address has been used by another account']
                still_valid = False

            if qs.filter(username=form.cleaned_data['username']).exists():
                form.errors['username'] = ['Username has been used by another account']
                still_valid = False

            if still_valid:

                # set user attributes

                user.username = form.cleaned_data['username']
                user.first_name = form.cleaned_data['first_name']
                user.last_name = form.cleaned_data['last_name']
                user.email = form.cleaned_data['email']

                if form.cleaned_data['new_password']:
                    user.set_password(form.cleaned_data['new_password'])

                user.save()

                # set profile attributes

                try:

                    profile = user.get_profile()

                    profile.phone = form.cleaned_data['phone']
                    profile.organization = form.cleaned_data['organization']
                    profile.is_a = form.cleaned_data['is_a']
                    profile.interests = form.cleaned_data['interests']
                    profile.notify = form.cleaned_data['notify']

                    profile.save()

                except Profile.DoesNotExist:
                    messages.warning(request, 'Your account does not have a profile. Please contact us to let us know.')

                messages.success(request, 'Your account has been updated.')

                return HttpResponseRedirect('/account/')

    else:

        initial = {
            'username': request.user.username,
            'first_name': request.user.first_name,
            'last_name': request.user.last_name,
            'email': request.user.email,
        }

        try:

            profile = request.user.get_profile()

            initial['phone'] = profile.phone
            initial['organization'] = profile.organization
            initial['is_a'] = profile.is_a
            initial['interests'] = profile.interests
            initial['notify'] = profile.notify

        except Profile.DoesNotExist:
            pass

        form = SettingsForm(initial=initial)

    return render(request, 'account.html', {'form': form})


def setup_account(request):

    if 'partial_pipeline' not in request.session:
        return HttpResponseRedirect('/')

    pipeline = request.session['partial_pipeline']

    print pipeline

    if request.method == 'POST':

        form = AccountSetupForm(request.POST)

        if form.is_valid():

            request.session['account_settings'] = form.cleaned_data

            return redirect('socialauth_complete', backend=pipeline['backend'])

    else:
        form = AccountSetupForm(initial=pipeline['kwargs']['details'])

    return render(request, 'account_setup.html', {'form': form})


def account_error(request):
    return render(request, 'account_error.html')


def delete_account(request):

    if request.user.is_staff:
        messages.warning(request,
            'Unable to delete account. Staff accounts must be deleted by an administrator.')
        return HttpResponseRedirect('/account/')

    if request.method == 'POST':

        if 'iamreallysure' in request.POST:

            user = request.user
            resp = logout(request, next_page='/')
            user.delete()

            return resp

    return render(request, 'account_delete.html')


def registrations(request):

    if not request.user.is_staff:
        return HttpResponseRedirect('/')

    bffr = StringIO()

    writer = unicodecsv.writer(bffr)
    writer.writerow(('username', 'first_name', 'last_name', 'organization',
        'date_joined', 'email', 'can_email', 'completion_count',
        'role', 'interests'))

    for user in User.objects.filter(is_staff=False).annotate(completion_count=Count('completions')).order_by('date_joined'):

        profile = Profile.objects.get(user=user)

        can_email = 'Y' if profile.notify else 'N'

        writer.writerow((user.username, user.first_name, user.last_name, profile.organization,
            user.date_joined.date(), user.email, can_email, user.completion_count,
            profile.is_a, profile.interests))

    content = bffr.getvalue()
    bffr.close()

    return HttpResponse(content, content_type='text/csv')
