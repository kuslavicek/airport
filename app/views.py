from django.shortcuts import render
from .tasks import simulate_airplane_movement

def home(request):
    simulate_airplane_movement(repeat=4)  # Trigger the cyclic task (runs every 10 seconds)
    return render(request, 'home.html', {"message": "Cyclic task started!"})
