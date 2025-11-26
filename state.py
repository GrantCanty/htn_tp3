from pyhop import hop


# define initial state
state = hop.State('state0')
state.robot_pos = {'robot': 'rooma'}

state.stock = {
    'roof_brick': {'red': 40, 'blue': 35, 'green': 55},
    'wall_brick': {'black': 30, 'blue': 63, 'red': 18, 'yellow': 54},
    'trunk_brick': {'brown': 42},
    'branches_brick': {'brown': 65},
    'ground': {'blue': 48, 'green': 102},
    'chassis': {'black': 83},
    'body': {'red': 63, 'blue': 82, 'yellow': 67}
}

state.bags = {
    'main_bag': [],
    'house_bag': [],
    'tree_bag': [],
    'ground_bag': [],
    'car_bag': [],
}

state.ready = set()

def move_to(state, zone):
    if state.robot_pos['robot'] != zone:
        state.robot_pos['robot'] = zone
        return state
    return False

def take_bricks(state, brick_type, color, quantity, bag_name):
    if state['stock'][brick_type][color] > quantity:
        state['stock'][brick_type][color] -= quantity
        state['bags'][bag_name][brick_type] += quantity
        return state
    return False

def pack_bag(state, sub_bag, main_bag):
    if sub_bag.key() not in state.ready:
        state['bags']

def mark_ready(state, bag_name):
    state['ready'].add(bag_name)
    return state