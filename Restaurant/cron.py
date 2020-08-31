from django_cron import CronJobBase, Schedule

from Restaurant import models as restaurant_models


class RestaurantCloseJob(CronJobBase):
    RUN_AT_TIMES = ['00:00']

    schedule = Schedule(run_at_times=RUN_AT_TIMES)
    code = 'restaurant_close_job'

    def do(self):
        restaurants = restaurant_models.Restaurant.objects.all()
        for restaurant in restaurants:
            restaurant.is_open = not restaurant.is_open
            restaurant.save()
