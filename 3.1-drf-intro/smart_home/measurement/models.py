from django.db import models

# TODO: опишите модели датчика (Sensor) и измерения (Measurement)


class Sensor(models.Model):
    name = models.CharField(max_length=50)
    description = models.TextField(null=True)

    def __str__(self):
        return self.name


class Measurement(models.Model):
    sensor = models.ForeignKey(Sensor, on_delete=models.CASCADE, related_name='measurements')
    # sensor = models.IntegerField()
    temperature = models.DecimalField(max_digits=4, decimal_places=1)
    measure_time = models.DateTimeField(auto_now=True)
    # image = models.ImageField(upload_to='measurements/', null=True, blank=True)

    def __str__(self):
        return f"{self.sensor}: {self.temperature}°C at {self.measure_time:%Y-%m-%d %T}"
