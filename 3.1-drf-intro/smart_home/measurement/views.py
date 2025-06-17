# TODO: опишите необходимые обработчики, рекомендуется использовать generics APIView классы:
# TODO: ListCreateAPIView, RetrieveUpdateAPIView, CreateAPIView
from rest_framework.generics import ListAPIView, RetrieveAPIView, ListCreateAPIView, UpdateAPIView, \
    RetrieveUpdateAPIView, CreateAPIView
from rest_framework.response import Response

from measurement.models import Sensor, Measurement
from measurement.serializers import SensorSerializer, SensorDetailSerializer, MeasurementSerializer


class SensorsListView(ListCreateAPIView):
    queryset = Sensor.objects.all()
    serializer_class = SensorSerializer

    # def post(self, request):
    #     sensor = Sensor()
    #     sensor.name = request.POST.get('name')
    #     sensor.description = request.POST['description']
    #     sensor.save()
    #     ser = SensorSerializer(sensor, many=False)
    #     return Response(ser.data)


class SensorUpdateView(RetrieveUpdateAPIView):
    queryset = Sensor.objects.all()
    serializer_class = SensorDetailSerializer

    # def get(self, request, pk):
    #     sensor = Sensor.objects.select_related("measurement").get(id=pk)
    #     ser = SensorDetailSerializer(sensor, many=False)
    #     return Response(ser.data)

    # def put(self, request, pk):
    #     sensor = Sensor.objects.get(id=pk)
    #     setattr(sensor, 'name', request.POST.get('name'))
    #     setattr(sensor, 'description', request.POST.get('description'))
    #     print("sensor ",sensor.name, sensor.description)
    #     sensor.save()
    #     ser = SensorSerializer(sensor, many=False)
    #     return Response(ser.data)

    # def patch(self, request, pk):
    #     sensor = Sensor.objects.get(id=pk)
    #     print(request.data)
    #     setattr(sensor, 'name', request.data.get('name'))
    #     setattr(sensor, 'description', request.data.get('description'))
    #     print("sensor ",sensor.name, sensor.description)
    #     sensor.save()
    #     ser = SensorSerializer(sensor, many=False)
    #     return Response(ser.data)


class MeasurementCreateView(CreateAPIView):
    queryset = Measurement.objects.all()
    serializer_class = MeasurementSerializer


# class SensorDetailView(RetrieveAPIView):
#     queryset = Sensor.objects.all()
#     serializer_class = SensorDetailSerializer
