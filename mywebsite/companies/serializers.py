from rest_framework import serializers
from .models import Stock
#converting model into JSON data
class StockSerializer(serializers.ModelSerializer):
	 class Meta:
	 	model=Stock
	 	fields=('ticker','volume')
	 	#fields='_all_'