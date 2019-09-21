from rest_framework import permissions
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Workstation
from .serializers import WorkstationSerializer


class WorkstationView(APIView):

    def get(self, request):
        #permission_classes = [permissions.IsAuthenticated, ]
        #permission_classes = [permissions.AllowAny, ]

        workstations = Workstation.objects.all()
        serializer = WorkstationSerializer(workstations, many=True)
        return Response({'data': serializer.data})

    # def post(self, request):
    #     workstation = WorkstationSerializer(data=request.data)
    #     if workstation.is_valid():
    #         workstation.save(user=request.user)
    #         return Response({'Status': 'Add'})
    #     else:
    #         return Response({'Status': 'Error'})
