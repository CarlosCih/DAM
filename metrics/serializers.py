from rest_framework import serializers

class SummarySerializer(serializers.Serializer):
    total=serializers.IntegerField()
    open=serializers.IntegerField()
    in_progress=serializers.IntegerField()
    closed=serializers.IntegerField()
    reopened=serializers.IntegerField()
    avg_resolution_hours=serializers.FloatField(allow_null=True)
    
class ChartDataSerializer(serializers.Serializer):
    label=serializers.ListField(child=serializers.CharField())
    datasets=serializers.ListField(child=serializers.DictField())
    