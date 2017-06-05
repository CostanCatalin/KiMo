from django.db import models
from authentication.models import Account


class KidsManager(models.Manager):
    def of_user(self, user_id):
        return super(KidsManager, self).filter(parent_id=user_id)

    def stats(self, age):
        from django.db import connection
        with connection.cursor() as cursor:
            result = 1.0
            d = cursor.callfunc('children_functions.getAgeDistribution', float, [age])
        return d

    def registered_in_month(self, month):
        from django.db import connection
        with connection.cursor() as cursor:
            count = cursor.callfunc('children_functions.getChildrenInThatMonth', int, [month])
        return count


class Kid(models.Model):
    parent = models.ForeignKey(Account, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=40)
    last_name = models.CharField(max_length=40)
    birth_date = models.DateField()

    registered_date = models.DateTimeField(auto_now_add=True)

    objects = KidsManager()

    @property
    def full_name(self):
        return ' '.join([self.first_name, self.last_name])

    def get_age(self):
        from django.db import connection
        age = 1
        with connection.cursor() as c:
            # c.execute("BEGIN")
            k_age = c.callfunc("children_functions.getAge", age, [self.pk])
        return k_age

    def __str__(self):
        return str(self.first_name)


class Notification(models.Model):
    kid = models.ForeignKey(Kid, on_delete=models.CASCADE)
    notification_type = models.CharField(max_length=32)
    text = models.CharField(max_length=255)
    seen = models.BooleanField()
    date_created = models.DateTimeField(auto_now_add=True)


class Encounter(models.Model):
    kid_1 = models.ForeignKey(Kid, related_name='kid_1', on_delete=models.CASCADE)
    kid_2 = models.ForeignKey(Kid, related_name='kid_2', on_delete=models.CASCADE)
    date_created = models.DateTimeField(auto_now_add=True)


class Location(models.Model):
    kid = models.ForeignKey(Kid, on_delete=models.CASCADE)
    latitude = models.FloatField(unique=False)
    longitude = models.FloatField(unique=False)
    date_created = models.DateTimeField(auto_now_add=True)


class Restriction(models.Model):
    kid = models.ForeignKey(Kid, on_delete=models.CASCADE)
    latitude = models.FloatField(unique=False)
    longitude = models.FloatField(unique=False)
    distance = models.FloatField()
    date_created = models.DateTimeField(auto_now_add=True)



