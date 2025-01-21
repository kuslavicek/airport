from background_task import background
from django.utils.timezone import now
from .models import Plane, Runway, Gate, Hangar
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from datetime import timedelta
import random

# Timeout duration for stuck states
TIMEOUT_SECONDS = 10  # Adjust based on your simulation needs

@background(schedule=4)  # Run every 4 seconds
def simulate_airplane_movement():
    channel_layer = get_channel_layer()
    now_time = now()
    print(f'running task: {now_time}')
    planes = Plane.objects.all()
    
    for plane in planes:
        # Flying state: plane might want to land
        if plane.status == "flying":
            if random.choice([True, False]):  # 50% chance to land
                plane.status = "landing"
                plane.location = "waiting for runway"
        
        # Landing state: plane needs to land on an available runway
        elif plane.status == "landing":
            runway = Runway.objects.filter(is_free=True).first()
            if runway:
                # Land on the runway
                plane.status = "on runway"
                plane.location = runway.name
                runway.is_free = False
                runway.current_plane = plane
                runway.save()
            else:
                plane.location = "waiting for runway"
        
        # On runway state: After landing, the plane needs to move to the gate
        elif plane.status == "on runway":
            runway = Runway.objects.filter(current_plane=plane).first()
            if runway:
                # The plane has landed, and now it should clear the runway
                runway.is_free = True
                runway.current_plane = None
                runway.save()
                plane.status = "waiting for gate"
                plane.location = "waiting for gate"

        # Explicit handling for planes in "waiting for gate" state
        elif plane.status == "waiting for gate":
            gate = Gate.objects.filter(is_free=True).first()
            if gate:
                plane.status = "at gate"
                plane.location = gate.name
                gate.is_free = False
                gate.current_plane = plane
                gate.save()
            else:
                plane.location = "waiting for gate"

        # At gate state: plane can either go to a hangar or prepare for takeoff
        elif plane.status == "at gate":
            hangar = Hangar.objects.filter(is_free=True).first()
            if hangar:
                plane.status = "in hangar"
                plane.location = hangar.name
                hangar.is_free = False
                hangar.current_plane = plane
                hangar.save()
            else:
                plane.status = "preparing for takeoff"

        # In hangar state: plane can move back to a gate if needed
        elif plane.status == "in hangar":
            gate = Gate.objects.filter(is_free=True).first()
            if gate:
                plane.status = "at gate"
                plane.location = gate.name
                hangar = Hangar.objects.get(current_plane=plane)
                hangar.is_free = True
                hangar.current_plane = None
                hangar.save()
                gate.is_free = False
                gate.current_plane = plane
                gate.save()

        # Preparing for takeoff state: plane can take off once a runway is available
        elif plane.status == "preparing for takeoff":
            runway = Runway.objects.filter(is_free=True).first()
            if runway:
                plane.status = "flying"
                plane.location = "sky"
                runway.is_free = False
                runway.current_plane = plane
                runway.save()
            else:
                plane.location = "waiting for runway"
        
        # Update plane's timestamp to avoid being stuck
        plane.updated_at = now_time
        plane.save()

    cleanup_stuck_entities()

    # Send updated data to WebSocket clients
    data = {
        "planes": list(Plane.objects.values("id", "name", "status", "location")),
        "runways": list(Runway.objects.values("id", "name", "is_free", "current_plane__name")),
        "gates": list(Gate.objects.values("id", "name", "is_free", "current_plane__name")),
        "hangars": list(Hangar.objects.values("id", "name", "is_free", "current_plane__name")),
    }
    async_to_sync(channel_layer.group_send)(
        "dashboard",
        {
            "type": "update.dashboard",
            "data": data,
        }
    )


def cleanup_stuck_entities():
    """
    Ensures no entities (runways, gates, hangars) are incorrectly marked as occupied.
    Fixes inconsistencies in the statuses of planes and entities.
    """
    # Reset runways if planes are not in "flying" or "preparing for takeoff"
    for runway in Runway.objects.all():
        if runway.current_plane:
            plane = runway.current_plane
            if plane.status not in ["preparing for takeoff", "flying", "on runway"]:
                runway.is_free = True
                runway.current_plane = None
                runway.save()

    # Reset gates if planes are not in "at gate" or "preparing for takeoff"
    for gate in Gate.objects.all():
        if gate.current_plane:
            plane = gate.current_plane
            if plane.status not in ["at gate", "preparing for takeoff"]:
                gate.is_free = True
                gate.current_plane = None
                gate.save()

    # Reset hangars if planes are not in "in hangar"
    for hangar in Hangar.objects.all():
        if hangar.current_plane:
            plane = hangar.current_plane
            if plane.status != "in hangar":
                hangar.is_free = True
                hangar.current_plane = None
                hangar.save()

    # Ensure all planes' locations are consistent with their statuses
    for plane in Plane.objects.all():
        if plane.status == "flying":
            plane.location = "sky"
        elif plane.status == "landing":
            if not Runway.objects.filter(current_plane=plane).exists():
                plane.location = "waiting for gate"
        elif plane.status == "at gate":
            if not Gate.objects.filter(current_plane=plane).exists():
                plane.status = "preparing for takeoff"
        elif plane.status == "in hangar":
            if not Hangar.objects.filter(current_plane=plane).exists():
                plane.status = "at gate"
        elif plane.status == "preparing for takeoff":
            if not Runway.objects.filter(current_plane=plane).exists():
                plane.location = "waiting for runway"
        plane.save()
