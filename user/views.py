from .models import Freelancer, Employer
from .serializers import FreelancerSerializer, EmployerSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.status import HTTP_204_NO_CONTENT
from rest_framework.generics import CreateAPIView


class FreelancerRegisterView(CreateAPIView):
    serializer_class = FreelancerSerializer
    queryset = Freelancer.objects.all()


class EmployerRegisterView(CreateAPIView):
    serializer_class = EmployerSerializer
    queryset = Employer.objects.all()


class LogoutView(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        request.auth.delete()

        return Response(status=HTTP_204_NO_CONTENT)
