from django.shortcuts import render
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from .app import agent
import json

@api_view(['POST'])
# @permission_classes([IsAuthenticated])
def send_message(request):
    """
    API endpoint to send message to AI agent and get response
    """
    try:
        if agent is None:
            return Response(
                {'error': 'AI Agent is not initialized', 'success': False},
                status=status.HTTP_503_SERVICE_UNAVAILABLE
            )
        
        data = request.data
        user_message = data.get('message', '').strip()
        
        if not user_message:
            return Response(
                {'error': 'Message cannot be empty'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Get response from AI agent
        response = agent.invoke({
            "input": user_message
        })
        
        ai_response = response.get('output', 'Unable to process your request.')
        
        return Response({
            'success': True,
            'message': ai_response,
            'user_message': user_message
        }, status=status.HTTP_200_OK)
        
    except Exception as e:
        return Response(
            {'error': str(e), 'success': False},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )
