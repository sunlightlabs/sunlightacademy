from django.http import HttpResponseRedirect

from training.models import Profile

def account_details(request, user=None, *args, **kwargs):

	if 'account_settings' not in request.session and user is None:
		return HttpResponseRedirect('/account/setup/')

def set_account_details(request, user=None, *args, **kwargs):

	if user:
		return {'username': user.username}

	if 'account_settings' in request.session:

		settings = request.session['account_settings']

		details = kwargs.get('details')
		details['email'] = settings['email']
		details['username'] = settings['username']

		return {'username': details['username']}

def create_profile(request, user=None, *args, **kwargs):

	settings = request.session.get('account_settings')

	if settings is not None and user is not None:

		try:

			user.get_profile()

		except Profile.DoesNotExist:

			profile = Profile(
				user=user,
				phone=settings['phone'],
				organization=settings['organization'],
				is_a=settings['is_a'],
				interests=settings['interests'],
				notify=settings['notify'] or False
			)
			profile.save()

def cleanup(request, user=None, *args, **kwargs):

	if 'account_settings' in request.session:
		del request.session['account_settings']