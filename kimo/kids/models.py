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


class Kids(models.Model):
    parent = models.ForeignKey(Account)
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


