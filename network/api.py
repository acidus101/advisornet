from django.template import response
from django.urls.base import translate_url
from rest_framework import serializers
from rest_framework.serializers import Serializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.exceptions import AuthenticationFailed
import jwt
import datetime
from . serializers import *
from . models import User, Booking, Advisor

# apis

class RegisterAPI(APIView):
    def post(self, request):
        Serializer = UserSerializer(data=request.data)
        if Serializer.is_valid(raise_exception=True):
            Serializer.save()

            # generate a token and login
            email = request.data['email']
            password = request.data['password']
            user = User.objects.filter(email=email).first()
            payload = {
                'id': user.id,
                'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=60),
                'iat': datetime.datetime.utcnow()
            }
            token = jwt.encode(payload, 'secret',algorithm='HS256').decode('utf-8')

            response = Response({}, status=status.HTTP_200_OK)

            response.set_cookie(key='jwt', value=token, httponly=True)
            response.data = {
                'jwt': token,
                'id': user.id
            }
            return response
        return Response(Serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginAPI(APIView):
    def post(self, request):
        email = request.data['email']
        password = request.data['password']

        # if email or password not provided
        if not email or not password:
            return Response({"error": "email and password field empty"}, status=status.HTTP_400_BAD_REQUEST)

        user = User.objects.filter(email=email).first()

        pass_exist = user.check_password(password)
        if not user or not pass_exist:
            return Response({"error": "email/password combination was wrong"}, status=status.HTTP_401_UNAUTHORIZED)

        payload = {
            'id': user.id,
            'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=60),
            'iat': datetime.datetime.utcnow()
        }

        token = jwt.encode(payload, 'secret',
                           algorithm='HS256').decode('utf-8')

        response = Response({}, status=status.HTTP_200_OK)

        response.set_cookie(key='jwt', value=token, httponly=True)
        response.data = {
            'jwt': token,
            'id': user.id
        }
        return response


class UserAPI(APIView):
    def get(self, request):
        token = request.COOKIES.get('jwt')

        if not token:
            raise AuthenticationFailed('Unauthenticated!')

        try:
            payload = jwt.decode(token, 'secret', algorithm=['HS256'])
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed('Unauthenticated!')

        user = User.objects.filter(id=payload['id']).first()
        serializer = UserSerializer(user)
        return Response(serializer.data)


class LogoutAPI(APIView):
    def post(self, request):
        response = Response()
        response.delete_cookie('jwt')
        response.data = {
            'message': 'successfully logged out'
        }

        return response


class AdvisorsViewAPI(APIView):
    def get(self, request, user_id):
        admin_list = Advisor.objects.all()
        Serializer = AdvisorSerializer(admin_list, many=True)
        return Response(Serializer.data, status=status.HTTP_200_OK)


class AdvisorSetAPI(APIView):
    def post(self, request):
        Serializer = AdvisorSerializer(data=request.data)
        if Serializer.is_valid():
            Serializer.save()
            test_res = {}
            test_res["name"] = Serializer.data["name"]
            test_res["picture_url"] = Serializer.data["picture_url"]
            return Response(test_res, status=status.HTTP_200_OK)
        return Response(Serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class MakeBookingApi(APIView):
    def post(self, request, user_id, advisor_id):
        recieved_data = request.data
        recieved_data["advId"] = advisor_id
        recieved_data["userId"] = user_id
        Serializer = BookingSerializer(data=recieved_data)
        if Serializer.is_valid():
            Serializer.save()
            return Response(None, status=status.HTTP_200_OK)
        return Response(Serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ViewBookingsAPI(APIView):
    def get(self, request, user_id):
        advisor_list = Booking.objects.all().filter(userId=user_id).all()
        Serializer = BookingSerializer(advisor_list, many=True)
        advisors_list_view = []
        for x in Serializer.data:
            test = {}
            test["bookingId"] = x["bookingId"]
            test["bookingTime"] = x["bookingDateTime"]
            advisor = Advisor.objects.all().filter(emp_id=x["advId"]).first()
            SerializerAdv = AdvisorSerializer(advisor)
            test["advisorName"] = SerializerAdv["name"].value
            test["advisorProfilePic"] = SerializerAdv["picture_url"].value
            test["advisorId"] = x["advId"]
            advisors_list_view.append(test)
        Serializer2 = BookingViewSerializer(advisors_list_view, many=True)
        return Response(Serializer2.data, status=status.HTTP_200_OK)
