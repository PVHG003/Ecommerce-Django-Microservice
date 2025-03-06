from django.contrib.auth import authenticate
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView

from .models import Address
from .serializers import CustomerSerializer, AddressSerializer, RegisterSerializer, LoginSerializer, \
    CustomTokenObtainPairSerializer


def fetch_customer_orders():
    pass


class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer


class RegisterView(APIView):
    def post(self, request):
        serializer = RegisterSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response({
                'success': True,
                'message': 'Registration successful.'
            }, status=status.HTTP_201_CREATED)

        return Response({
            'success': False,
            'errors': serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)


class LoginView(APIView):
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            username = serializer.validated_data['username']
            password = serializer.validated_data['password']

            user = authenticate(username=username, password=password)
            if user is None:
                return Response({
                    'success': False,
                    'message': 'Invalid credentials',
                    'errors': serializer.errors
                }, status=status.HTTP_401_UNAUTHORIZED)

            refresh = RefreshToken.for_user(user)

            return Response({
                'success': True,
                'message': 'Login successful.',
                'data': {
                    'refresh': str(refresh),
                    'access': str(refresh.access_token),
                }
            }, status=status.HTTP_200_OK)

        return Response({
            'success': False,
            'message': 'Invalid credentials',
            'errors': serializer.errors
        }, status=status.HTTP_401_UNAUTHORIZED)


class ProfileView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        serializer = CustomerSerializer(request.user)
        return Response({
            'success': True,
            'message': 'Profile fetched successfully.',
            'data': serializer.data
        }, status=status.HTTP_200_OK)

    def put(self, request):
        serializer = CustomerSerializer(request.user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({
                'success': True,
                'message': 'Profile updated successfully.',
                'data': serializer.data
            }, status=status.HTTP_200_OK)

        return Response({
            'success': False,
            'errors': serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)


class ManageAddressesView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        addresses = request.user.addresses.all()
        serializer = AddressSerializer(addresses, many=True)
        return Response({
            'success': True,
            'message': 'Addresses retrieved successfully.',
            'data': serializer.data
        }, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = AddressSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(customer=request.user)
            return Response({
                'success': True,
                'message': 'Address added successfully.',
                'data': serializer.data
            }, status=status.HTTP_201_CREATED)

        return Response({
            'success': False,
            'errors': serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, address_id):
        try:
            address = Address.objects.get(id=address_id, customer=request.user)
        except Address.DoesNotExist:
            return Response({
                'success': False,
                'message': 'Address not found'
            }, status=status.HTTP_404_NOT_FOUND)

        serializer = AddressSerializer(address, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({
                'success': True,
                'message': 'Address updated successfully.',
                'data': serializer.data
            }, status=status.HTTP_200_OK)

        return Response({
            'success': False,
            'errors': serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, address_id):
        try:
            address = Address.objects.get(id=address_id, customer=request.user)
            address.delete()
            return Response({
                'success': True,
                'message': 'Address deleted successfully.'
            }, status=status.HTTP_204_NO_CONTENT)
        except Address.DoesNotExist:
            return Response({
                'success': False,
                'message': 'Address not found'
            }, status=status.HTTP_404_NOT_FOUND)

# class CustomerOrdersView(APIView):
#     permission_classes = [IsAuthenticated]
#
#     def get(self, request):
#         customer_id = request.user.id
# orders = fetch_customer_orders(customer_id)  # Implement fetch_customer_orders properly

# if orders:
#     return Response({
#         'success': True,
#         'message': 'Orders retrieved successfully.',
#         'data': orders
#     }, status=status.HTTP_200_OK)
# return Response({
#     'success': False,
#     'message': 'No orders found.'
# }, status=status.HTTP_404_NOT_FOUND)
