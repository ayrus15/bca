import streamlit as st
import time
import random

# Title and Introduction
st.title("Advanced Traffic Deadlock Detection and Resource Allocation Simulator (No Matplotlib, No NetworkX)")
st.write("""
This advanced traffic simulator incorporates real-time monitoring, rerouting algorithms, and dynamic resource allocation using basic Python data structures and text-based visualization.
The app monitors traffic flow, detects potential deadlocks, and reroutes vehicles to avoid gridlocks.
""")

# Simulation Parameters
refresh_rate = st.slider("Set refresh rate (seconds) for real-time traffic monitoring", min_value=1, max_value=10, value=3)

# Simulating vehicles and intersections with traffic volume
vehicles = st.text_input("Enter the vehicles (comma separated, e.g., V1,V2,V3):", "V1,V2,V3")
intersections = st.text_input("Enter the intersections (comma separated, e.g., I1,I2,I3):", "I1,I2,I3")
vehicles_list = [v.strip() for v in vehicles.split(',')]
intersections_list = [i.strip() for i in intersections.split(',')]

# Initialize traffic volumes and routes
traffic_volumes = {intersection: random.randint(1, 5) for intersection in intersections_list}
vehicle_routes = {v: random.choice(intersections_list) for v in vehicles_list}

# Text-based Traffic Flow Display
def display_traffic_flow(vehicle_routes, traffic_volumes):
    st.write("### Current Traffic Flow and Traffic Volumes")
    for vehicle, intersection in vehicle_routes.items():
        st.write(f"Vehicle {vehicle} is heading towards Intersection {intersection} (Traffic Volume: {traffic_volumes[intersection]})")

# Deadlock detection using simple cycle detection in routes (circular waiting)
def detect_deadlock(vehicle_routes):
    visited = set()
    for vehicle, intersection in vehicle_routes.items():
        if intersection in visited:
            return True, vehicle
        visited.add(intersection)
    return False, None

# Rerouting algorithm to redirect vehicles to less congested intersections
def reroute_vehicle(vehicle, blocked_intersection):
    available_intersections = [i for i in intersections_list if i != blocked_intersection]
    rerouted_intersection = min(available_intersections, key=lambda x: traffic_volumes[x])
    st.write(f"Rerouting {vehicle} from {blocked_intersection} to {rerouted_intersection}")
    return rerouted_intersection

# Simulate the traffic flow with real-time updates
def simulate_traffic(vehicles_list, intersections_list, refresh_rate):
    while True:
        # Update vehicle routes
        for vehicle in vehicles_list:
            requested_intersection = vehicle_routes[vehicle]

            # Check for congestion
            if traffic_volumes[requested_intersection] > 3:
                st.write(f"Congestion detected at {requested_intersection} for {vehicle}.")
                vehicle_routes[vehicle] = reroute_vehicle(vehicle, requested_intersection)

        # Display traffic flow
        display_traffic_flow(vehicle_routes, traffic_volumes)

        # Detect deadlocks (cycle detection)
        deadlock_detected, vehicle_in_deadlock = detect_deadlock(vehicle_routes)
        if deadlock_detected:
            st.write("### Deadlock Detected!")
            st.write(f"Vehicle {vehicle_in_deadlock} is part of a deadlock.")
            vehicle_routes[vehicle_in_deadlock] = reroute_vehicle(vehicle_in_deadlock, vehicle_routes[vehicle_in_deadlock])
        else:
            st.write("### No Deadlocks Detected")

        # Update traffic volume dynamically for each intersection
        for intersection in traffic_volumes:
            traffic_volumes[intersection] = random.randint(1, 5)

        # Wait for the next refresh cycle
        time.sleep(refresh_rate)

# Start real-time traffic simulation
if st.button("Start Simulation"):
    simulate_traffic(vehicles_list, intersections_list, refresh_rate)
