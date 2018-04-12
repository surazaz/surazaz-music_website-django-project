from django.db import models



# Create your models here.
class Stock(models.Model):
	ticker=models.CharField(max_length=10)
	opening=models.FloatField()
	close=models.FloatField()
	volume=models.IntegerField()

	def _str_(self):
		return self.ticker;

