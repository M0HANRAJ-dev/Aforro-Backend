from rest_framework import serializers

class OrderItemInputSerializer(serializers.Serializer):
    product_id = serializers.IntegerField()
    quantity_requested = serializers.IntegerField()

class OrderCreateSerializer(serializers.Serializer):
    store_id = serializers.IntegerField()
    items = OrderItemInputSerializer(many=True)