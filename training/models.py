import datetime

from django.contrib.auth.models import User
from django.db import models

IS_A_CHOICES = (
    ('other', 'Other'),
    ('journalist', 'Journalist'),
    ('researcher', 'Researcher'),
    ('activist', 'Activist'),
    ('student', 'Student'),
    ('nonprofit', 'Non-profit'),
)

KNOWLEDGE_CHOICES = (
    ('0', 'Know absolutely nothing'),
    ('1', 'A novice'),
    ('2', 'Middle of the road'),
    ('3', 'A trivia night champion'),
    ('4', 'A nobel prize winner'),
)

CLARITY_CHOICES = (
    ('0', 'Not clear at all'),
    ('1', 'Barely understandable'),
    ('2', 'Meh.'),
    ('3', 'Mostly clear'),
    ('4', 'Completely clear'),
)

YESNO_CHOICES = (
    ('y', 'Yes, I would'),
    ('n', 'No, I would not'),
)


class Profile(models.Model):

    user = models.OneToOneField(User)

    phone = models.CharField(max_length=24, blank=True)
    organization = models.CharField(max_length=128, blank=True, null=True)
    is_a = models.CharField(max_length=16, choices=IS_A_CHOICES, blank=True)
    interests = models.TextField(blank=True)
    notify = models.BooleanField(default=False)

    class Meta:
        ordering = ('user__username',)

    def __unicode__(self):
        return self.user.username


class Category(models.Model):
    name = models.CharField(max_length=128)
    slug = models.SlugField()

    class Meta:
        ordering = ('name',)

    def __unicode__(self):
        return self.name

    def public_modules(self):
        return self.modules.filter(is_public=True)


class Module(models.Model):

    title = models.CharField(max_length=128)
    slug = models.SlugField()
    date = models.DateTimeField(blank=True, null=True)
    description = models.TextField(blank=True)
    content = models.TextField(blank=True)

    thumbnail = models.ImageField(upload_to='module_thumbs', blank=True, null=True)
    notes_url = models.URLField(blank=True)

    categories = models.ManyToManyField(Category, related_name='modules')

    is_public = models.BooleanField(default=False)

    class Meta:
        ordering = ('-date', 'title')

    def __unicode__(self):
        return self.title

    @models.permalink
    def get_absolute_url(self):
        return ('training.views.module', [self.slug])

    def related_modules(self):
        qs = Module.objects.exclude(pk=self.pk)
        qs = qs.filter(categories__in=self.categories.all(), is_public=True)
        return qs.distinct()


class Completion(models.Model):

    user = models.ForeignKey(User, related_name='completions')
    module = models.ForeignKey(Module, related_name='completions')
    timestamp = models.DateTimeField(default=datetime.datetime.utcnow)

    class Meta:
        ordering = ('-timestamp',)

    def __unicode__(self):
        return u"%s completed %s" % (self.user.username, self.module.title)


class Training(models.Model):

    title = models.CharField(max_length=255)
    slug = models.SlugField(unique=True)
    date = models.DateField()
    start_time = models.TimeField(blank=True, null=True)
    end_time = models.TimeField(blank=True, null=True)
    url = models.URLField(blank=True,
        help_text="registration url")
    category = models.CharField(max_length=255, blank=True,
        help_text="simple category such as webinar, netposium, conference call, etc.")
    description = models.TextField(blank=True)

    module = models.ForeignKey(Module, related_name='trainings', blank=True, null=True)

    is_public = models.BooleanField(default=False)

    class Meta:
        ordering = ('-date',)

    def __unicode__(self):
        return self.title

    def is_future(self, today=None):
        today = today or datetime.date.today()
        print today, self.date
        return self.date >= today


class Feedback(models.Model):

    user = models.ForeignKey(User, related_name="feedback")
    module = models.ForeignKey(Module, related_name="feedback")

    knowledge_before = models.CharField(max_length=1, choices=KNOWLEDGE_CHOICES)
    knowledge_after = models.CharField(max_length=1, choices=KNOWLEDGE_CHOICES)
    content_clarity = models.CharField(max_length=1, choices=CLARITY_CHOICES)
    suggestions = models.TextField()
    positives = models.TextField()
    would_recommend = models.CharField(max_length=1, choices=YESNO_CHOICES)

    timestamp = models.DateTimeField(default=datetime.datetime.utcnow)

    class Meta:
        ordering = ('-timestamp',)

    def __unicode__(self):
        return u"%s on %s" % (self.user.username, self.module.title)
