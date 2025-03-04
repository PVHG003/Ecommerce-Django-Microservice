from django.contrib.auth import authenticate
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken

from .models import Address
from .serializers import CustomerSerializer, AddressSerializer, RegisterSerializer, LoginSerializer


class RegisterView(APIView):
    def post(self, request):
        serializer = RegisterSerializer(data=request.data)

        if serializer.is_valid():
            user = serializer.save()  # Uses overridden create() method
            refresh = RefreshToken.for_user(user)

            return Response({
                'user': serializer.data,
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            }, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginView(APIView):
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            username = serializer.validated_data['username']
            password = serializer.validated_data['password']

            user = authenticate(username=username, password=password)
            if user is None:
                return Response({
                    'error': 'Invalid credentials',
                    'data': serializer.data
                }, status=status.HTTP_401_UNAUTHORIZED)

            refresh = RefreshToken.for_user(user)
            return Response({
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            }, status=status.HTTP_200_OK)

        return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)


class ProfileView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        serializer = CustomerSerializer(request.user)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request):
        serializer = CustomerSerializer(request.user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ManageAddressesView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        addresses = request.user.addresses.all()
        serializer = AddressSerializer(addresses, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = AddressSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(customer=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, address_id):
        try:
            address = Address.objects.get(id=address_id, customer=request.user)
        except Address.DoesNotExist:
            return Response({'error': 'Address not found'}, status=status.HTTP_404_NOT_FOUND)

        serializer = AddressSerializer(address, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, address_id):
        try:
            address = Address.objects.get(id=address_id, customer=request.user)
            address.delete()
            return Response({'message': 'Address deleted'}, status=status.HTTP_204_NO_CONTENT)
        except Address.DoesNotExist:
            return Response({'error': 'Address not found'}, status=status.HTTP_404_NOT_FOUND)


class CustomerOrdersView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        customer_id = request.user.id

        fake_orders = [
            {"order_id": 1, "customer_id": customer_id, "item_id": "abc123", "quantity": 2, "status": "delivered"},
            {"order_id": 2, "customer_id": customer_id, "item_id": "xyz456", "quantity": 1, "status": "shipped"},
        ]

        # Fake item details from Items Service
        fake_items = {
            "abc123": {"name": "Laptop", "price": 1200, "category": "Electronics"},
            "xyz456": {"name": "Phone", "price": 800, "category": "Mobiles"},
        }

        # Merge order details with item details
        for order in fake_orders:
            item_id = order["item_id"]
            order["item_details"] = fake_items.get(item_id, {"name": "Unknown", "price": 0, "category": "Unknown"})

        return Response(fake_orders, status=status.HTTP_200_OK)
