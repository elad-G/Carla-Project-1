import carla
import random
import time

class CarlaControl:
    def __init__(self):
        try:
            self.client = carla.Client('localhost', 2000)
            self.client.set_timeout(100.0)  # Increase timeout if needed
            self.world = self.client.get_world()
            self.blueprint_library = self.world.get_blueprint_library()
        except RuntimeError as e:
            print(f"Error connecting to CARLA: {e}")
            raise

    def spawn_vehicle(self, blueprint_name, spawn_point):
        blueprint = random.choice(self.blueprint_library.filter(blueprint_name))
        vehicle = self.world.spawn_actor(blueprint, spawn_point)
        return vehicle

    def spawn_npc_vehicle(self, blueprint_name, spawn_point):
        blueprint = random.choice(self.blueprint_library.filter(blueprint_name))
        blueprint.set_attribute('role_name', 'autopilot')
        npc_vehicle = self.world.try_spawn_actor(blueprint, spawn_point)
        return npc_vehicle

    def check_collision(self, actor1, actor2):
        collision = False
        for actor in [actor1, actor2]:
            bbox = actor.bounding_box
            location = actor.get_location()
            collision = collision or any(location.distance(actor2.get_location()) < 2.0 for actor2 in self.world.get_actors().filter('vehicle.*'))
        return collision

    def cleanup(self):
        actors = self.world.get_actors().filter('vehicle.*')
        for actor in actors:
            actor.destroy()

if __name__ == '__main__':
    try:
        carla_control = CarlaControl()

        # Spawn ego vehicle (controllable car)
        spawn_point_ego = carla.Transform(carla.Location(x=230, y=195, z=40), carla.Rotation(yaw=180))
        ego_vehicle = carla_control.spawn_vehicle('vehicle.tesla.model3', spawn_point_ego)

        # Spawn NPC vehicle (uncontrollable bicycle)
        spawn_point_npc = carla.Transform(carla.Location(x=230, y=200, z=40))
        npc_vehicle = carla_control.spawn_npc_vehicle('vehicle.bicycle', spawn_point_npc)

        # Control ego vehicle (simple straight motion)
        ego_vehicle.apply_control(carla.VehicleControl(throttle=0.5, steer=0.0))

        # Main simulation loop
        while True:
            # Check collision
            if carla_control.check_collision(ego_vehicle, npc_vehicle):
                print("Collision occurred!")
                break

            # Tick the simulation
            carla_control.world.tick()

            # Example: Break condition to end simulation (e.g., after 20 seconds)
            if carla_control.world.get_snapshot().timestamp.frame >= 2000:
                break

    finally:
        if 'carla_control' in locals():
            carla_control.cleanup()
