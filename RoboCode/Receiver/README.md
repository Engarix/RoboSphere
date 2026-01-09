# RECEIVER

## KINEMATICS
### WHEEL SPEED CALCULATOR
MOVE {v} {omega}

    v omega   l  r
    --------------
    1   0  =  1  1
    1   1  =  0  1
    1  -1  =  1  0

    0   0  =  0  0
    0   1  =  1 -1
    0  -1  = -1  1

    -1  0  = -1 -1
    -1  1  =  0 -1
    -1 -1  = -1  0

*l* - Left Wheel

*r* - Right Wheel

pendulum = |v| * omega