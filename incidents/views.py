from rest_framework import viewsets
from .models import User, Incident
from .serializers import UserSerializer, IncidentSerializer
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import PasswordResetForm
from django.contrib.sites.shortcuts import get_current_site
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from django.core.mail import EmailMessage
from django.shortcuts import render, redirect
from django.urls import reverse
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django.views.generic.base import View
from rest_framework.generics import RetrieveAPIView

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.urls import path
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth import authenticate, login


from .models import Incident
from .serializers import IncidentSerializer
from django.views import View


# Some code that uses str
my_str = str(object)


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class IncidentViewSet(viewsets.ModelViewSet):
    queryset = Incident.objects.all()
    serializer_class = IncidentSerializer


class UserRegistrationView(APIView):
    @staticmethod
    def post(request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            login(request, user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserLoginView(View):
    @staticmethod
    def login_view(request):
        if request.method == 'POST':
            email = request.POST.get('email')
            password = request.POST.get('password')

            if email and password:
                user = authenticate(request, email=email, password=password)

                if user is not None:
                    login(request, user)
                    return redirect('login_success')

            return redirect('login_fail')

        return render(request, 'login.html')

    @staticmethod
    def get(_):
        return HttpResponse("User Login View")


class ForgotPasswordView(APIView):
    @staticmethod
    def post(request):
        email = request.data.get('email')
        form = PasswordResetForm(request.data)
        if form.is_valid():
            current_site = get_current_site(request)
            mail_subject = 'Reset your password'
            message = render_to_string('forgot_password_email.html', {
                'user': form.user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(bytes(form.user.pk)),
                'token': form.default_token_generator.make_token(form.user),
            })
            to_email = email
            email = EmailMessage(mail_subject, message, to=[to_email])
            email.send()
            return Response({'message': 'Password reset email sent'}, status=status.HTTP_200_OK)
        return Response(form.errors, status=status.HTTP_400_BAD_REQUEST)


class IncidentCreateView(APIView):
    @staticmethod
    def post(request):
        serializer = IncidentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class IncidentUpdateView(APIView):
    @staticmethod
    def put(request, pk):
        try:
            incident = Incident.objects.get(pk=pk)
        except Incident.DoesNotExist:
            return Response({"error": "Incident not found"}, status=status.HTTP_404_NOT_FOUND)

        serializer = IncidentSerializer(incident, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class IncidentRetrieveView(RetrieveAPIView):
    queryset = Incident.objects.all()
    serializer_class = IncidentSerializer

    @staticmethod
    def get(_, pk):
        try:
            incident = Incident.objects.get(pk=pk)
        except Incident.DoesNotExist:
            return Response({"error": "Incident not found"}, status=status.HTTP_404_NOT_FOUND)

        serializer = IncidentSerializer(incident)
        return Response(serializer.data)


class IncidentListView(APIView):
    @staticmethod
    def get(_):
        incidents = Incident.objects.all()
        serializer = IncidentSerializer(incidents, many=True)
        return Response(serializer.data)


class IncidentDeleteView(LoginRequiredMixin, APIView):
    permission_classes = [IsAuthenticated]

    @staticmethod
    def delete(request, pk):
        incident = get_object_or_404(Incident, pk=pk)
        # Check if the user has permission to delete the incident
        if incident.reporter == request.user:
            incident.delete()
            return Response("Incident deleted successfully.", status=status.HTTP_204_NO_CONTENT)
        else:
            return Response("You are not authorized to delete this incident.", status=status.HTTP_403_FORBIDDEN)


class IncidentSearchView(APIView):
    @staticmethod
    def get(request):
        incident_id = request.query_params.get('incident_id')
        if incident_id:
            try:
                incident = Incident.objects.get(incident_id=incident_id)
                serializer = IncidentSerializer(incident)
                return Response(serializer.data)
            except Incident.DoesNotExist:
                return Response({"error": "Incident not found"}, status=status.HTTP_404_NOT_FOUND)
        else:
            return Response({"error": "Incident ID not provided"}, status=status.HTTP_400_BAD_REQUEST)
