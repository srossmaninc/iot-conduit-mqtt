

# <---COLORS--->
G = (0, 255, 0)
R = (255, 0, 0)
B = (0, 0, 255)
O = (0,0,0)

# <---ANIMATION & STAGES--->
no_connect = [
    O, O, O, O, O, O, O, O,
    O, R, R, O, O, R, R, O,
    O, R, R, R, R, R, R, O,
    O, O, R, R, R, R, O, O,
    O, O, R, R, R, R, O, O,
    O, R, R, R, R, R, R, O,
    O, R, R, O, O, R, R, O,
    O, O, O, O, O, O, O, O,
]

logo = [
    O, G, G, O, O, G, G, O, 
    O, O, G, G, G, G, O, O,
    O, O, R, R, R, R, O, O, 
    O, R, R, R, R, R, R, O,
    R, R, R, R, R, R, R, R,
    R, R, R, R, R, R, R, R,
    O, R, R, R, R, R, R, O,
    O, O, R, R, R, R, O, O,
]

pub_1 = [
    O, O, O, O, O, O, O, O, 
    O, O, O, G, G, O, O, O,
    O, O, G, G, G, G, O, O, 
    O, G, G, G, G, G, G, O,
    O, O, O, G, G, O, O, O,
    O, O, O, G, G, O, O, O,
    O, O, O, G, G, O, O, O,
    O, O, O, O, O, O, O, O,
]
pub_2 = [
    O, O, G, G, G, G, O, O, 
    O, G, G, G, G, G, G, O,
    O, O, O, G, G, O, O, O, 
    O, O, O, G, G, O, O, O,
    O, O, O, G, G, O, O, O,
    O, O, O, O, O, O, O, O,
    O, O, O, O, O, O, O, O,
    O, O, O, G, G, O, O, O,
]
pub_3 = [
    O, O, O, G, G, O, O, O, 
    O, O, O, G, G, O, O, O,
    O, O, O, G, G, O, O, O, 
    O, O, O, O, O, O, O, O,
    O, O, O, O, O, O, O, O,
    O, O, O, G, G, O, O, O,
    O, O, G, G, G, G, O, O,
    O, G, G, G, G, G, G, O,
]
pub_4 = [
    O, O, O, G, G, O, O, O, 
    O, O, O, O, O, O, O, O,
    O, O, O, O, O, O, O, O, 
    O, O, O, G, G, O, O, O,
    O, O, G, G, G, G, O, O,
    O, G, G, G, G, G, G, O,
    O, O, O, G, G, O, O, O,
    O, O, O, G, G, O, O, O,
]
pub_stages = [pub_1, pub_2, pub_3, pub_4]

sub_1 = [
    O, O, O, O, O, O, O, O, 
    O, O, O, B, B, O, O, O,
    O, O, O, B, B, O, O, O,
    O, O, O, B, B, O, O, O,
    O, B, B, B, B, B, B, O,
    O, O, B, B, B, B, O, O,
    O, O, O, B, B, O, O, O,
    O, O, O, O, O, O, O, O,
]
sub_2 = [
    O, O, O, B, B, O, O, O, 
    O, O, O, O, O, O, O, O,
    O, O, O, O, O, O, O, O,
    O, O, O, B, B, O, O, O,
    O, O, O, B, B, O, O, O,
    O, O, O, B, B, O, O, O,
    O, B, B, B, B, B, B, O,
    O, O, B, B, B, B, O, O,
]
sub_3 = [
    O, B, B, B, B, B, B, O, 
    O, O, B, B, B, B, O, O,
    O, O, O, B, B, O, O, O,
    O, O, O, O, O, O, O, O,
    O, O, O, O, O, O, O, O,
    O, O, O, B, B, O, O, O,
    O, O, O, B, B, O, O, O,
    O, O, O, B, B, O, O, O,
]
sub_4 = [
    O, O, O, B, B, O, O, O, 
    O, O, O, B, B, O, O, O,
    O, B, B, B, B, B, B, O,
    O, O, B, B, B, B, O, O,
    O, O, O, B, B, O, O, O,
    O, O, O, O, O, O, O, O,
    O, O, O, O, O, O, O, O,
    O, O, O, B, B, O, O, O,
]
sub_stages = [sub_1, sub_2, sub_3, sub_4]

# the broker uses custom colors so this has to be a function
def broker_stages(C):
    broker_1 = [
        O, O, O, O, O, O, O, O,
        O, O, O, O, O, O, O, O,
        O, O, O, C, C, O, O, O,
        O, O, C, O, O, C, O, O,
        O, O, C, O, O, C, O, O,
        O, O, O, C, C, O, O, O,
        O, O, O, O, O, O, O, O,
        O, O, O, O, O, O, O, O,
    ]
    broker_2 = [
        O, O, O, O, O, O, O, O,
        O, O, C, C, C, C, O, O,
        O, C, O, O, O, O, C, O,
        O, C, O, O, O, O, C, O,
        O, C, O, O, O, O, C, O,
        O, C, O, O, O, O, C, O,
        O, O, C, C, C, C, O, O,
        O, O, O, O, O, O, O, O,
    ]
    broker_3 = [
        O, O, C, C, C, C, O, O,
        O, C, O, O, O, O, C, O,
        C, O, O, O, O, O, O, C,
        C, O, O, O, O, O, O, C,
        C, O, O, O, O, O, O, C,
        C, O, O, O, O, O, O, C,
        O, C, O, O, O, O, C, O,
        O, O, C, C, C, C, O, O,
    ]
    return [broker_1, broker_2, broker_3]