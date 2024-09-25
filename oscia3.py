import streamlit as st
import pandas as pd
import random

# Title
st.title("Smart Traffic Management System by 2341566 an 2341512")

# Initialize session state
if 'initialized' not in st.session_state:
    # Input fields for the user to enter number of vehicles on each side
    st.session_state.traffic_count = {
        'North': st.number_input('Enter number of vehicles on North side:', min_value=0, value=random.randint(1, 10)),
        'South': st.number_input('Enter number of vehicles on South side:', min_value=0, value=random.randint(1, 10)),
        'East': st.number_input('Enter number of vehicles on East side:', min_value=0, value=random.randint(1, 10)),
        'West': st.number_input('Enter number of vehicles on West side:', min_value=0, value=random.randint(1, 10))
    }
    st.session_state.signal_state = 'None'
    st.session_state.rounds_waited = { 'North': 0, 'South': 0, 'East': 0, 'West': 0 }
    st.session_state.process_log = pd.DataFrame(columns=["Step", "Signal State", "Direction Allowed", "Vehicles Moved", "North Traffic", "South Traffic", "East Traffic", "West Traffic"])
    st.session_state.initialized = True
    st.session_state.step = 0

# Traffic and Signal Parameters
min_green_time = 5  # Minimum time each side gets to move (in seconds)
max_green_time = 15  # Maximum time a highly congested side can get to move
max_rounds_before_priority = 3  # Maximum number of rounds a side can wait before getting priority

# Display current traffic counts
st.write("### Current Traffic Counts")
for direction, count in st.session_state.traffic_count.items():
    st.write(f"{direction}: {count} vehicles")

# Function to simulate traffic moving in a given direction
def move_traffic(direction, move_count):
    st.session_state.traffic_count[direction] = max(st.session_state.traffic_count[direction] - move_count, 0)

# Function to select the next direction based on traffic count
def select_next_direction():
    # Prioritize based on traffic and fairness (i.e., prevent starvation)
    direction_with_most_traffic = max(st.session_state.traffic_count, key=st.session_state.traffic_count.get)
    for direction in st.session_state.traffic_count:
        if st.session_state.rounds_waited[direction] >= max_rounds_before_priority:
            return direction
    return direction_with_most_traffic

# Function to log each step
def log_process(step, signal_state, direction, vehicles_moved):
    new_row = pd.DataFrame({
        "Step": [step],
        "Signal State": [signal_state],
        "Direction Allowed": [direction],
        "Vehicles Moved": [vehicles_moved],
        "North Traffic": [st.session_state.traffic_count["North"]],
        "South Traffic": [st.session_state.traffic_count["South"]],
        "East Traffic": [st.session_state.traffic_count["East"]],
        "West Traffic": [st.session_state.traffic_count["West"]],
    })
    st.session_state.process_log = pd.concat([st.session_state.process_log, new_row], ignore_index=True)

# Function to switch signals
def switch_signals():
    st.session_state.step += 1

    # Select the next direction to allow traffic
    next_direction = select_next_direction()
    opposite_directions = {'North': 'South', 'South': 'North', 'East': 'West', 'West': 'East'}
    
    # Ensure we aren't allowing opposite directions simultaneously
    if next_direction in ['North', 'South']:
        st.session_state.signal_state = 'North-South'
    else:
        st.session_state.signal_state = 'East-West'

    # Reset the waiting time for the direction we are moving
    for direction in st.session_state.traffic_count:
        if direction == next_direction or direction == opposite_directions[next_direction]:
            st.session_state.rounds_waited[direction] = 0
        else:
            st.session_state.rounds_waited[direction] += 1

    # Simulate traffic moving
    traffic_movement = min(random.randint(2, 5), st.session_state.traffic_count[next_direction])
    move_traffic(next_direction, traffic_movement)

    # Log the process
    log_process(st.session_state.step, st.session_state.signal_state, next_direction, traffic_movement)
    st.write(f"Green Light: {next_direction} (Moved {traffic_movement} vehicles)")

# Simulation control
if st.button("Next Step"):
    switch_signals()

# Display the process log as a table
if len(st.session_state.process_log) > 0:
    st.write("### Process Log")
    st.write(st.session_state.process_log)

# Stop simulation button
if st.button("Stop Simulation"):
    st.session_state.signal_state = 'None'
    st.write("Simulation stopped.")
