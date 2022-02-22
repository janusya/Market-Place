from datetime import datetime

from django.db import models
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver


class Created(models.Model):
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        abstract = True


class Store(Created):
    founder = models.OneToOneField(
        to=settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        limit_choices_to={
            'is_seller': True,
        },
    )
    name = models.CharField(max_length=200)
    avatar = models.ImageField(upload_to='stores_avatar', null=True)
    description = models.TextField()
    register_date = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.pk:
            self.register_date = datetime.now()

        super(Store, self).save(*args, **kwargs)


class StoreFeedbacks(Created):
    store = models.ForeignKey(Store, on_delete=models.CASCADE,
                              related_name='feedbacks')
    author = models.ForeignKey('account.User', on_delete=models.CASCADE,
                               related_name='feedbacks')
    body = models.TextField()

    rating = models.FloatField(default=0)

    def __str__(self) -> str:
        return f"Feedback to {self.store.name}"

    class Meta:
        ordering = ('-created',)

