import ev3dev.ev3 as ev3

a=ev3.LargeMotor('outA')
b=ev3.LargeMotor('outB')
c=ev3.LargeMotor('outC')
d=ev3.LargeMotor('outD')

def move_forward(sec=5):
    a.run_timed(speed_sp=1000,time_sp=10)
    b.run_timed(speed_sp=1000,time_sp=sec*1000)
    c.run_timed(speed_sp=-1000,time_sp=10)
    d.run_timed(speed_sp=-1000,time_sp=10)

def move_backward(sec=5):
    a.run_timed(speed_sp=-1000,time_sp=10)
    b.run_timed(speed_sp=-1000,time_sp=sec*1000)
    c.run_timed(speed_sp=1000,time_sp=10)
    d.run_timed(speed_sp=1000,time_sp=10)

if __name__ == '__main__':
    move_backward(2)

# helpful things: https://ev3dev-lang.readthedocs.io/projects/python-ev3dev/en/stable/motors.html
# from ev3dev2.motor import OUTPUT_A, OUTPUT_B, MoveDifferential, SpeedRPM
# from ev3dev2.wheel import EV3Tire

# STUD_MM = 8

# # test with a robot that:
# # - uses the standard wheels known as EV3Tire
# # - wheels are 16 studs apart
# mdiff = MoveDifferential(OUTPUT_A, OUTPUT_B, EV3Tire, 16 * STUD_MM)

# # Rotate 90 degrees clockwise
# mdiff.turn_right(SpeedRPM(40), 90)

# # Drive forward 500 mm
# mdiff.on_for_distance(SpeedRPM(40), 500)

# # Drive in arc to the right along an imaginary circle of radius 150 mm.
# # Drive for 700 mm around this imaginary circle.
# mdiff.on_arc_right(SpeedRPM(80), 150, 700)

# # Enable odometry
# mdiff.odometry_start()

# # Use odometry to drive to specific coordinates
# mdiff.on_to_coordinates(SpeedRPM(40), 300, 300)

# # Use odometry to go back to where we started
# mdiff.on_to_coordinates(SpeedRPM(40), 0, 0)

# # Use odometry to rotate in place to 90 degrees
# mdiff.turn_to_angle(SpeedRPM(40), 90)

# # Disable odometry
# mdiff.odometry_stop()
