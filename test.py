import pygame
import carla
import time

# Initialize Pygame
pygame.init()

# Initialize the joystick
pygame.joystick.init()

# Check for joysticks
joystick_count = pygame.joystick.get_count()
if joystick_count == 0:
    raise Exception("No joystick detected!")

# Use the first joystick (usually the steering wheel)
steering_wheel = pygame.joystick.Joystick(0)
steering_wheel.init()

print(fJoystick name {steering_wheel.get_name()})
print(fNumber of axes {steering_wheel.get_numaxes()})
print(fNumber of buttons {steering_wheel.get_numbuttons()})

# Connect to the CARLA server
client = carla.Client('localhost', 2000)
client.set_timeout(2.0)

# Get the world
world = client.get_world()

# Get the blueprint library
blueprint_library = world.get_blueprint_library()

# Select a vehicle blueprint
vehicle_bp = blueprint_library.filter('model3')[0]

# Set the spawn point
spawn_point = world.get_map().get_spawn_points()[0]

# Spawn the vehicle
vehicle = world.spawn_actor(vehicle_bp, spawn_point)

def get_steering_wheel_input()
    # Handle axis movements (e.g., steering wheel rotation, pedals)
    steering = steering_wheel.get_axis(0)  # Axis 0 for steering
    throttle = steering_wheel.get_axis(1)  # Axis 1 for throttle
    brake = steering_wheel.get_axis(2)     # Axis 2 for brake

    # Adjust the values to match CARLA's expected range
    throttle = max(0.0, (1.0 - throttle)  2.0)  # Normalize throttle
    brake = max(0.0, (1.0 - brake)  2.0)        # Normalize brake
    steering = steering  2.0                   # Scale steering

    return steering, throttle, brake

# Main loop
try
    while True
        # Process Pygame events
        pygame.event.pump()

        # Get the steering wheel input
        steering, throttle, brake = get_steering_wheel_input()

        # Create control commands for CARLA
        control = carla.VehicleControl()
        control.steer = steering
        control.throttle = throttle
        control.brake = brake

        # Apply control commands to the vehicle
        vehicle.apply_control(control)

        # Sleep to maintain a consistent update rate
        time.sleep(0.05)

except KeyboardInterrupt
    print(Exiting...)

finally
    # Clean up
    vehicle.destroy()
    pygame.quit()
