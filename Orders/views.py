from django import forms
from rest_framework.response import Response
from rest_framework.renderers import JSONRenderer
from rest_framework.views import APIView
from rest_framework import generics, status, filters
from rest_framework.pagination import PageNumberPagination
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync

from . import serializers as orders_serializers
from . import models as orders_models
from . import authentication_and_permissions

from Invigilator import models as invigilator_models
from Restaurant import models as restaurant_models
from Restaurant import authentication_and_permissions as restaurant_authentication_and_permissions
from Dishes import models as dish_models
from Client import models as client_models
from Client import authentication_and_permissions as client_authentication_and_permissions


class CreateOrder(APIView):
    permission_classes = [authentication_and_permissions.CreateOrderPermission]
    def post(self, request):
        if 'order' not in self.request.data:
            return Response({'message': 'Include Order in Data'})
        if 'dishes' not in self.request.data:
            return Response({'message': 'Include Dish in Data'})

        order_serializer = orders_serializers.CreateOrderSerializer(data=self.request.data['order'])
        if order_serializer.is_valid():
            self.validate_dishes(self.request.data['dishes'], self.request.data['order']['restaurant'])
            order_serializer.save()
            self.create_order(self.request.data['dishes'], order_serializer.data['id'])

            order_ = orders_models.Order.objects.filter(pk=order_serializer.data['id']).first()
            incoming_order_obj = orders_models.IncomingOrder(order=order_, restaurant=order_.restaurant)
            incoming_order_obj.save()
            channel_layer = get_channel_layer()
            async_to_sync(channel_layer.group_send)(
                "restaurant_incoming_order_"  + str(order_.restaurant.id), {
                "type": "send_incoming_order_to_restaurant",
                "data": {
                    "order": orders_serializers.GetClientRestaurantPastOrdersSerializer(order_).data,
                }
            })

            client_models.ClientCart.objects.filter(client=order_.client).delete()

            return Response({'message': 'Orders Created Successfully', 'id': order_serializer.data['id']})
        return Response(order_serializer.errors)


    def validate_dishes(self, dishes, restaurant):
        restaurant = restaurant_models.Restaurant.objects.filter(pk=restaurant).first()
        if not restaurant:
            raise forms.ValidationError("Invalid Restaurant ID")
        for dish in dishes:
            order_dish_serializer = orders_serializers.CreateOrderDisheSerializer(data=dish)
            if not order_dish_serializer.is_valid():
                raise forms.ValidationError(order_dish_serializer.errors)
            if not dish_models.Dish.objects.filter(restaurant=restaurant, pk=dish['dish']).first():
                raise forms.ValidationError("Dish Id not matched with Restaurant Id")

            add_ons = dish['add_ons']
            dish = dish_models.Dish.objects.filter(restaurant=restaurant, pk=dish['dish']).first()
            for add_on in add_ons:
                if not dish_models.DishAddOns.objects.filter(pk=add_on, dish=dish):
                    raise forms.ValidationError("Dish Addons Id not matched with Dish Id")


    def create_order(self, dishes, order):
        for dish in dishes:
            dish['order'] = order
            order_dish_serializer = orders_serializers.CreateOrderDisheSerializer(data=dish)
            if order_dish_serializer.is_valid():
                order_dish_serializer.save()


class UpdateOrder(generics.UpdateAPIView):
    renderer_classes = [JSONRenderer]
    serializer_class = orders_serializers.UpdateOrderSerializer
    permission_classes = [authentication_and_permissions.UpdateDeleteOrderPermission]
    def get_queryset(self):
        if 'status' in self.request.data:
            self.send_order_status(self.request.data['status'], self.kwargs['pk'])
        if self.request.data['status'] == 'delivered':
            self.delete_ongoing_order()
        return orders_models.Order.objects.all()

    def delete_ongoing_order(self):
        order = orders_models.Order.objects.filter(pk=self.kwargs['pk']).first()
        if not order:
            raise forms.ValidationError("Invalid Order ID")
        ongoing_order = orders_models.OngoingOrder.objects.filter(order=order).first()
        if not ongoing_order:
            raise forms.ValidationError("No Ongoing Order exists with this order id")
        ongoing_order.delete()

    def send_order_status(self, status, order_id):
        order = orders_models.Order.objects.filter(pk=order_id).first()
        order.status = status
        order.save()
        channel_layer = get_channel_layer()
        async_to_sync(channel_layer.group_send)(
            "restaurant_order_status_"  + str(order.id), {
            "type": "send_order_status",
            "status": status
        })


class GetClientPastOrdersPagination(PageNumberPagination):
    page_size = 20
    max_page_size = 20


class GetClientPastOrders(generics.ListAPIView):
    renderer_classes = [JSONRenderer]
    serializer_class = orders_serializers.GetClientRestaurantPastOrdersSerializer
    # pagination_class = GetClientPastOrdersPagination
    permission_classes = [client_authentication_and_permissions.ClientDataAccessPermission]

    def get_queryset(self):
        return orders_models.Order.objects.filter(client__pk=self.kwargs['pk']).order_by('-created')


class GetRestaurantPastOrdersPagination(PageNumberPagination):
    page_size = 20
    max_page_size = 20


class GetRestaurantPastOrders(generics.ListAPIView):
    renderer_classes = [JSONRenderer]
    serializer_class = orders_serializers.GetClientRestaurantPastOrdersSerializer
    pagination_class = GetRestaurantPastOrdersPagination
    permission_classes = [restaurant_authentication_and_permissions.RestaurantDataPermission]

    def get_queryset(self):
        restaurant = restaurant_models.Restaurant.objects.filter(pk=self.kwargs['pk']).first()
        return orders_models.Order.objects.filter(restaurant=restaurant)


class AcceptOrder(APIView):
    permission_classes = [authentication_and_permissions.RestaurantOperationsOnOrders]
    def post(self, request, pk):
        order = orders_models.Order.objects.filter(pk=pk).first()
        if not order:
            return Response({'message': 'Invalid Order ID'}, status=status.HTTP_400_BAD_REQUEST)
        if order.status == "Accepted":
            return Response({'message': 'Order Accepted Already'}, status=status.HTTP_200_OK)

        incoming_order = orders_models.IncomingOrder.objects.filter(order=order).first()
        if not incoming_order:
            return Response({'message': "Order didn't exist in Incoming Order"}, status=status.HTTP_400_BAD_REQUEST)
        incoming_order.delete()

        ongoing_order = orders_models.OngoingOrder(order=order, restaurant=order.restaurant)
        ongoing_order.save()

        order.is_accepted = True
        order.status = "Accepted"
        order.save()
        invigilator = self.get_invigilator_for_order(order.restaurant)
        channel_layer = get_channel_layer()
        async_to_sync(channel_layer.group_send)(
            "incoming_order_for_invigilator_"  + str(invigilator.id), {
            "type": "send_order_to_invigilator_group",
            "order": orders_serializers.GetClientRestaurantPastOrdersSerializer(order).data,
            "invigilator": orders_serializers.GetClientRestaurantPastOrdersSerializer(order).data["invigilator"]
        })
        return Response({'message': 'Order Accepted Successfully'}, status=status.HTTP_200_OK)

    def get_invigilator_for_order(self):
        invigilator = invigilator_models.InvigilatorRestaurant.objects.filter(restaurant=obj.restaurant).first()
        return invigilator.invigilator


class RejectOrder(APIView):
    permission_classes = [authentication_and_permissions.RestaurantOperationsOnOrders]
    def post(self, request, pk):
        order = orders_models.Order.objects.filter(pk=pk).first()
        if not order:
            return Response({'message': 'Invalid Order ID'}, status=status.HTTP_400_BAD_REQUEST)
        if order.status == "Rejected":
            return Response({'message': 'Order Rejected Already'}, status=status.HTTP_200_OK)

        order.is_accepted = False
        order.status = "Rejected"
        order.save()
        incoming_order = orders_models.IncomingOrder.objects.filter(order=order).first()
        if not incoming_order:
            return Response({'message': "Order didn't exist in Incoming Order"}, status=status.HTTP_400_BAD_REQUEST)
        incoming_order.delete()
        return Response({'message': 'Order Rejected Successfully'}, status=status.HTTP_200_OK)


class OrderCompleted(APIView):
    permission_classes = [authentication_and_permissions.RestaurantOperationsOnOrders]
    def post(self, request):
        renderer_classes = [JSONRenderer]
        if 'order' not in self.request.data:
            return Response({'message': 'Include Order in Data'}, status=status.HTTP_400_BAD_REQUEST)

        order = orders_models.Order.objects.filter(pk=self.request.data['order']).first()
        if not order:
            return Response({'message': 'Invalid Order ID'}, status=status.HTTP_400_BAD_REQUEST)

        obj = invigilator_models.InvigilatorOrderAssignment.objects.filter(order=order).first()
        if obj:
            obj.delete()
        return Response({'message': 'Order Completed Successfully'}, status=status.HTTP_200_OK)


class GetIncomingOrdersPagination(PageNumberPagination):
    page_size = 20
    max_page_size = 20


class GetIncomingOrders(generics.ListAPIView):
    renderer_classes = [JSONRenderer]
    serializer_class = orders_serializers.GetClientRestaurantPastOrdersSerializer
    pagination_class = GetIncomingOrdersPagination
    permission_classes = [restaurant_authentication_and_permissions.RestaurantDataPermission]

    def get_queryset(self):
        incoming_orders = orders_models.IncomingOrder.objects.filter(restaurant__pk=self.kwargs['pk'])
        orders = []
        for incoming_order in incoming_orders:
            orders.append(incoming_order.order)
        return orders


class GetOngoingOrdersPagination(PageNumberPagination):
    page_size = 20
    max_page_size = 20


class GetOngoingOrders(generics.ListAPIView):
    renderer_classes = [JSONRenderer]
    serializer_class = orders_serializers.GetClientRestaurantPastOrdersSerializer
    pagination_class = GetOngoingOrdersPagination
    permission_classes = [restaurant_authentication_and_permissions.RestaurantDataPermission]

    def get_queryset(self):
        restaurant = restaurant_models.Restaurant.objects.filter(pk=self.kwargs['pk']).first()
        ongoing_orders = orders_models.OngoingOrder.objects.filter(restaurant=restaurant)
        orders = []
        for ongoing_order in ongoing_orders:
            orders.append(ongoing_order.order)
        return orders


class GetSpecificOrder(generics.ListAPIView):
    renderer_classes = [JSONRenderer]
    serializer_class = orders_serializers.GetClientRestaurantPastOrdersSerializer
    def get_queryset(self):
        return orders_models.Order.objects.filter(pk=self.kwargs['pk'])
