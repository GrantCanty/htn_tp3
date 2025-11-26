from pyhop import hop


# define initial state
state = hop.State('state0')
state.robot_pos = {'robot': 'start_zone'}

state.stock = {
    'roof_brick': {'red': 40, 'blue': 35, 'green': 55},
    'wall_brick': {'black': 30, 'blue': 63, 'red': 18, 'yellow': 54},
    'trunk_brick': {'brown': 42},
    'branches_brick': {'brown': 65},
    'ground_brick': {'blue': 48, 'green': 102},
    'chassis_brick': {'black': 83},
    'body_brick': {'red': 63, 'blue': 82, 'yellow': 67}
}

state.bags = {
    #'main_bag': {},
    'house_bag': {
        'roof_bag': {},
        'walls_bag': {}
    },
    'tree_bag': {
        'trunk_bag': {},
        'branches_bag': {}
    },
    'ground_bag': {},
    'car_bag': {
        'chassis_bag': {},
        'body_bag': {}
    },
}

state.ready = set()

def move_to(state, zone):
    if zone in ZONES:
        if state.robot_pos['robot'] != zone:
            state.robot_pos['robot'] = zone
            return state
    return False

def take_bricks(state, brick_type, color, quantity, bag_name):
    if brick_type in state.stock and color in state.stock['brick_type']:
        if state.stock[brick_type][color] > quantity:
            state.stock[brick_type][color] -= quantity
            state.bags[bag_name][brick_type] += quantity
            return state
    return False

def pack_bag(state, sub_bag, main_bag):
    if sub_bag in state.ready:
        state.bags[main_bag][sub_bag] = state['bags'][sub_bag]
        return state
    return False

def mark_ready(state, bag_name):
    state.ready.add(bag_name)
    return state

ZONES = ['roof_zone', 'wall_zone', 'trunk_zone', 'branch_zone', 'ground_zone', 'chassis_zone', 'body_zone', 'assembly_zone', 'start_zone']

## house methods
def prepare_roof(state, color):
    move_to(state, 'roof_zone')
    take_bricks(state, 'roof_brick', color, 1, 'roof_bag')
    mark_ready(state, 'roof_bag')

hop.declare_methods('prepare_roof', prepare_roof)

def prepare_wall(state, color):
    move_to(state, 'wall_zone')
    take_bricks(state, 'wall_brick', color, 1, 'walls_bag')
    mark_ready(state, 'walls_bag')

hop.declare_methods('prepare_wall', prepare_wall)

def prepare_house(state, roof_color, wall_color):
    prepare_roof(state, roof_color)
    prepare_wall(state, wall_color)
    pack_bag(state, 'roof_bag' 'house_bag')
    pack_bag(state, 'walls_bag' 'house_bag')

hop.declare_methods('prepare_house', prepare_house)
## end of house methods

## tree methods
def prepare_trunk(state, color):
    move_to(state, 'trunk_zone')
    take_bricks(state, 'trunk_brick', color, 1, 'trunk_bag')
    mark_ready(state, 'trunk_bag')

hop.declare_methods('prepare_trunk', prepare_trunk)

def prepare_branch(state, color):
    move_to(state, 'branch_zone')
    take_bricks(state, 'branches_brick', color, 1, 'branches_bag')
    mark_ready(state, 'branches_bag')

hop.declare_methods('prepare_branch', prepare_branch)

def prepare_tree(state, trunk_color, branch_color):
    prepare_trunk(state, trunk_color)
    prepare_branch(state, branch_color)
    pack_bag(state, 'trunk_bag' 'tree_bag')
    pack_bag(state, 'branches_bag' 'tree_bag')

hop.declare_methods('prepare_tree', prepare_tree)
## end of tree methods

## ground methods
def prepare_ground(state, color):
    move_to(state, 'ground_zone')
    take_bricks(state, 'ground_brick', color, 1, 'ground_bag')
    mark_ready(state, 'ground_bag')

hop.declare_methods('prepare_ground', prepare_ground)
## end of ground methods

## car bag
def prepare_chasis(state, color):
    move_to(state, 'chassis_zone')
    take_bricks(state, 'chassis_brick', color, 1, 'chassis_bag')
    mark_ready(state, 'chassis_bag')

hop.declare_methods('prepare_chasis', prepare_chasis)

def prepare_body(state, color):
    move_to(state, 'body_zone')
    take_bricks(state, 'body_brick', color, 1, 'body_bag')
    mark_ready(state, 'body_bag')

hop.declare_methods('prepare_body', prepare_body)

def prepare_car(state, chasis_color, body_color):
    prepare_chasis(state, chasis_color)
    prepare_body(state, body_color)
    pack_bag(state, 'chassis_bag' 'car_bag')
    pack_bag(state, 'body_bag' 'car_bag')

hop.declare_methods('prepare_car', prepare_car)
## end of car bag



