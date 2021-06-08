from django.conf import settings
from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User


class Post(models.Model):
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    text = models.TextField()
    created_date = models.DateTimeField(default=timezone.now)
    published_date = models.DateTimeField(blank=True, null=True)

    def publish(self):
        self.published_date = timezone.now()
        self.save()

    def __str__(self):
        return self.title

    # Create your models here.


class MainCycle(models.Model):
    user = models.OneToOneField(User, null=False, on_delete=models.CASCADE)
    coins_count = models.IntegerField(default=0)
    click_power = models.IntegerField(default=1)
    auto_click_power = models.IntegerField(default=0)
    level = models.IntegerField(default=0)

    def click(self):
        self.coins_count += self.click_power

        if self.coins_count > self.check_level_summ():
            self.level += 1
            return True

        return False

    def check_level_summ(self):
        # 0 = 1000; 1 = 2000; 2 = 5000; 3 = 10000
        return (self.level ** 2 + 1) * 1000


class Boost(models.Model):
    main_cycle = models.ForeignKey(MainCycle, null=False, on_delete=models.CASCADE)
    power = models.IntegerField(default=1)
    price = models.IntegerField(default=10)
    level = models.IntegerField(default=0)
    boost_type = models.IntegerField(default=0)

    def update_boost(self):
        if (self.main_cycle.coins_count < self.price):
            return False

        self.main_cycle.coins_count -= self.price
        self.level += 1
        self.power *= 2
        self.price *= 5

        if self.boost_type == 0:
            self.main_cycle.click_power += self.power
        elif self.boost_type == 1:
            self.main_cycle.auto_click_power += self.power
            # self.price *= 5

        self.main_cycle.save()

        return self