from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from .models import Event
from .serializers import EventSerializer, EventEditSerializer, UserSerializer

class RegisterView(APIView):
    permission_classes = [AllowAny]

    @swagger_auto_schema(
        operation_description='Registration',
        request_body=UserSerializer,
        responses={
            201: openapi.Response('User registered successfully.'),
            400: openapi.Response('Bad request'),
        },
    )
    def post(self, request):

        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class AddEventView(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_description='Add New Event',
        request_body=EventSerializer,
        responses={
            201: openapi.Response('Event added.'),
            400: openapi.Response('Bad request'),
        },
    )
    def post(self, request):
        event_serializer = EventSerializer(data=request.data)
        if event_serializer.is_valid():
            event = event_serializer.save(created_by=request.user)
            return Response({'message': 'Event added.'}, status=status.HTTP_201_CREATED)
        return Response(event_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class GetEventView(APIView):
    permission_classes = [IsAuthenticated]


    @swagger_auto_schema(
        operation_description='Get Events',
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'order': openapi.Schema(type=openapi.TYPE_STRING, description='last - last 5 events\n own - last 5 events added by user'),
                'offset': openapi.Schema(type=openapi.TYPE_INTEGER, description='offset to previous events, more value - older events'),
            },
            required=['name'],
        ),
        responses={
            200: EventEditSerializer(many=True),
            400: openapi.Response('Bad request'),
        },
    )
    def post(self, request):
        order = request.data.get('order')
        offset = request.data.get('offset')
        if not offset or not isinstance(offset,int) or offset <= 0:
            offset = 0
        if not order:
            return Response({'error': 'Order is empty.'}, status=status.HTTP_400_BAD_REQUEST)
        if order == 'last':
            events = Event.objects.order_by('-created_at').values('id','title','description','location','start_at')[offset:5]
        elif order == 'own':
            user = request.user
            events = Event.objects.filter(created_by=user).values('id','title','description','location','start_at')[offset:5]
        else:
            return Response({'error': 'Wrong order.'}, status=status.HTTP_400_BAD_REQUEST)
        return Response({'message': events}, status=status.HTTP_200_OK)
        
class DeleteEventView(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_description='Delete Event',
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'id': openapi.Schema(type=openapi.TYPE_INTEGER, description='id - id of event to delete'),
            },
            required=['id'],
        ),
        responses={
            200: openapi.Response('Event deleted.'),
            400: openapi.Response('ID is empty.'),
            403: openapi.Response('You are not owner of this event.'),
            404: openapi.Response('Event dosent exist.'),
        },
    )
    def post(self, request):
        user = request.user
        id = request.data.get('id')
        if not id or not isinstance(id,int) or id <= 0:
            return Response({'error': 'ID is empty.'}, status=status.HTTP_400_BAD_REQUEST)
        if not Event.objects.filter(id=id).exists():
            return Response({'error': 'Event dosent exist.'}, status=status.HTTP_404_NOT_FOUND)
        event = Event.objects.get(id=id)
        if not event.created_by == user:
            return Response({'error': 'You are not owner of this event.'}, status=status.HTTP_403_FORBIDDEN)
        event.delete()
        return Response({'message': 'Event deleted.'}, status=status.HTTP_200_OK)
    
class UpdateEventView(APIView):
    permission_classes = [IsAuthenticated]



    @swagger_auto_schema(
        operation_description='Update Event',
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties=
            {
                'id': openapi.Schema(type=openapi.TYPE_INTEGER),
                'title': openapi.Schema(type=openapi.TYPE_STRING),
                'description': openapi.Schema(type=openapi.TYPE_STRING),
                'location': openapi.Schema(type=openapi.TYPE_STRING),
                'start_at': openapi.Schema(type=openapi.TYPE_STRING,format=openapi.FORMAT_DATETIME),
            },
            required=['id','title','description','location','start_at'],
        ),
        responses={
            200: openapi.Response('Event updated.'),
            400: openapi.Response('Required field is empty.'),
            403: openapi.Response('You are not owner of this event.'),
            404: openapi.Response('Event dosent exist.'),
        },
    )
    def post(self, request):
        user = request.user
        id = request.data.get('id')
        title = request.data.get('title')
        description = request.data.get('description')
        location = request.data.get('location')
        start_at = request.data.get('date')

        if not id or  not isinstance(id,int) or id <= 0 or not title or not description or not location or not start_at:
            return Response({'error': 'Required field is empty.'}, status=status.HTTP_400_BAD_REQUEST)
        if not Event.objects.filter(id=id).exists():
            return Response({'error': 'Event dosent exist.'}, status=status.HTTP_404_NOT_FOUND)
        event = Event.objects.get(id=id)
        if not event.created_by == user:
            return Response({'error': 'You are not owner of this event.'}, status=status.HTTP_403_FORBIDDEN)
        
        event.title = title
        event.description = description
        event.location = location
        event.start_at = start_at
        event.save()
        return Response({'message': 'Event updated.'}, status=status.HTTP_200_OK)

class JoinEventView(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_description='Join Event',
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'id': openapi.Schema(type=openapi.TYPE_INTEGER, description='id - event id'),
            },
            required=['id'],
        ),
        responses={
            200: openapi.Response('You have joined event.'),
            400: openapi.Response('ID is empty.'),
            403: openapi.Response('You are owner of this event.'),
            404: openapi.Response('Event dosent exist.'),
        },
    )
    def post(self, request):
        user = request.user
        id = request.data.get('id')
        if not id or not isinstance(id,int) or id <= 0:
            return Response({'error': 'ID is empty.'}, status=status.HTTP_400_BAD_REQUEST)
        if not Event.objects.filter(id=id).exists():
            return Response({'error': 'Event dosent exist.'}, status=status.HTTP_404_NOT_FOUND)
        event = Event.objects.get(id=id)
        if event.created_by == user:
            return Response({'error': 'You are owner of this event.'}, status=status.HTTP_400_BAD_REQUEST)
        if user in event.participants:
            return Response({'error': 'You already in.'}, status=status.HTTP_400_BAD_REQUEST)
        event.participants.add(user)
        return Response({'message': 'You have joined event.'}, status=status.HTTP_200_OK)

class LeaveEventView(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_description='Leave Event',
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'id': openapi.Schema(type=openapi.TYPE_INTEGER, description='id - event id'),
            },
            required=['id'],
        ),
        responses={
            200: openapi.Response('You  have leaved event.'),
            400: openapi.Response('ID is empty.'),
            403: openapi.Response('You are owner of this event.'),
            404: openapi.Response('Event dosent exist.'),
        },
    )
    def post(self, request):
        user = request.user
        id = request.data.get('id')
        if not id or not isinstance(id,int) or id <= 0:
            return Response({'error': 'ID is empty.'}, status=status.HTTP_400_BAD_REQUEST)
        if not Event.objects.filter(id=id).exists():
            return Response({'error': 'Event dosent exist.'}, status=status.HTTP_404_NOT_FOUND)
        event = Event.objects.get(id=id)
        if event.created_by == user:
            return Response({'error': 'You are owner of this event.'}, status=status.HTTP_400_BAD_REQUEST)
        if user in event.participants:
            return Response({'error': 'You are not in.'}, status=status.HTTP_400_BAD_REQUEST)
        event.participants.remove(user)
        return Response({'message': 'You  have leaved event.'}, status=status.HTTP_200_OK)
    
class GetEventPsrticipantsView(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_description='Get Event\'s Partisipants',
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'id': openapi.Schema(type=openapi.TYPE_INTEGER, description='id - event id'),
            },
            required=['id'],
        ),
        responses={
            200: openapi.Response({'participants': '[str]'}),
            400: openapi.Response('ID is empty.'),
            403: openapi.Response('You are not owner of this event.'),
            404: openapi.Response('Event dosent exist.'),
        },
    )
    def post(self, request):
        user = request.user
        id = request.data.get('id')
        if not id or not isinstance(id,int) or id <= 0:
            return Response({'error': 'ID is empty.'}, status=status.HTTP_400_BAD_REQUEST)
        if not Event.objects.filter(id=id).exists():
            return Response({'error': 'Event dosent exist.'}, status=status.HTTP_404_NOT_FOUND)
        event = Event.objects.get(id=id)
        if not event.created_by == user:
            return Response({'error': 'You are not owner of this event.'}, status=status.HTTP_403_FORBIDDEN)
        participants = event.participants
        participants_names = [participant.username for participant in participants]
        return Response({'participants': participants_names}, status=status.HTTP_200_OK)
