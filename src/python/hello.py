import airsim
import time

client = airsim.CarClient()
client.confirmConnection()
client.enableApiControl(True)
car_controls = airsim.CarControls()

while True:
    car_state = client.getCarState()
    print("Speed %d, Gear %d" % (car_state.speed, car_state.gear))
    
    car_controls.throttle = 1
    car_controls.steering = 1
    client.setCarControls(car_controls)

    time.sleep(1)
    
    responses = client.simGetImages([
        airsim.ImageRequest(0, airsim.ImageType.DepthVis),
        airsim.ImageRequest(1, airsim.ImageType.Scene)
    ])
    print("Retrieved %d images" % len(responses))

    for response in responses:
        if response.pixels_as_float:
            print("Type %d, size %d" % (response.image_type, len(response.image_data_float)))
            airsim.write_pfm('py1.pfm', airsim.get_pfm_array(response))
        else:
            print("Type %d, size %d" % (response.image_type, len(response.image_data_uint8)))
            airsim.write_file("py%d.png" % (response.image_type), response.image_data_uint8)