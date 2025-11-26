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
    'main_bag': {},
    'house_bag': {},
    'tree_bag': {},
    'ground_bag': {},
    'car_bag': {},
    'roof_bag': {},
    'walls_bag': {},
    'trunk_bag': {},
    'branches_bag': {},
    'chassis_bag': {},
    'body_bag': {}
}

state.ready = set()

def move_to(state, zone):
    if zone in ZONES:
        if state.robot_pos['robot'] != zone:
            state.robot_pos['robot'] = zone
            return state
    return False

def take_bricks(state, brick_type, color, quantity, bag_name): # Remove sub_bag parameter
    if brick_type in state.stock and color in state.stock[brick_type]:
        if state.stock[brick_type][color] >= quantity:
            state.stock[brick_type][color] -= quantity
            state.bags[bag_name][brick_type] = int(state.bags[bag_name].get(brick_type) or 0) + quantity
            return state
    return False

def pack_bag(state, sub_bag, main_bag):
    if sub_bag in state.ready:
        state.bags[main_bag][sub_bag] = state.bags[sub_bag]
        return state
    return False

def mark_ready(state, bag_name):
    state.ready.add(bag_name)
    return state

hop.declare_operators(move_to, take_bricks, pack_bag, mark_ready) # Don't forget this!

ZONES = ['roof_zone', 'wall_zone', 'trunk_zone', 'branch_zone', 'ground_zone', 'chassis_zone', 'body_zone', 'assembly_zone', 'start_zone']

## house methods
def prepare_roof(state, color):
    return [
        ('move_to', 'roof_zone'),
        ('take_bricks', 'roof_brick', color, 1, 'roof_bag'),
        ('mark_ready', 'roof_bag')
    ]

hop.declare_methods('prepare_roof', prepare_roof)

def prepare_wall(state, color):
    return [
        ('move_to', 'wall_zone'),
        ('take_bricks', 'wall_brick', color, 1, 'walls_bag'),
        ('mark_ready', 'walls_bag')
    ]

hop.declare_methods('prepare_wall', prepare_wall)

def prepare_house(state, roof_color, wall_color):
    return [
        ('prepare_roof', roof_color),
        ('prepare_wall', wall_color),
        ('pack_bag', 'roof_bag', 'house_bag'),
        ('pack_bag', 'walls_bag', 'house_bag'),
        ('mark_ready', 'house_bag')
    ]
    

hop.declare_methods('prepare_house', prepare_house)
## end of house methods

## tree methods
def prepare_trunk(state, color):
    return [
        ('move_to', 'trunk_zone'),
        ('take_bricks', 'trunk_brick', color, 1, 'trunk_bag'),
        ('mark_ready', 'trunk_bag')
    ]

hop.declare_methods('prepare_trunk', prepare_trunk)

def prepare_branch(state, color):
    return [
        ('move_to', 'branch_zone'),
        ('take_bricks', 'branches_brick', color, 1, 'branches_bag'),
        ('mark_ready', 'branches_bag')
    ]

hop.declare_methods('prepare_branch', prepare_branch)

def prepare_tree(state, trunk_color, branch_color):
    return [
        ('prepare_trunk', trunk_color),
        ('prepare_branch', branch_color),
        ('pack_bag', 'trunk_bag', 'tree_bag'),
        ('pack_bag', 'branches_bag', 'tree_bag'),
        ('mark_ready', 'tree_bag')
    ]

hop.declare_methods('prepare_tree', prepare_tree)
## end of tree methods

## ground methods
def prepare_ground(state, color):
    return [
        ('move_to', 'ground_zone'),
        ('take_bricks', 'ground_brick', color, 1, 'ground_bag'),
        ('mark_ready', 'ground_bag'),
        ('mark_ready', 'ground_bag')
    ]

hop.declare_methods('prepare_ground', prepare_ground)
## end of ground methods

## car bag
def prepare_chasis(state, color):
    return [
        ('move_to', 'chassis_zone'),
        ('take_bricks', 'chassis_brick', color, 1, 'chassis_bag'),
        ('mark_ready', 'chassis_bag')
    ]

hop.declare_methods('prepare_chasis', prepare_chasis)

def prepare_body(state, color):
    return [
        ('move_to', 'body_zone'),
        ('take_bricks', 'body_brick', color, 1, 'body_bag'),
        ('mark_ready', 'body_bag')
    ]

hop.declare_methods('prepare_body', prepare_body)

def prepare_car(state, chasis_color, body_color):
    return [
        ('prepare_chasis', chasis_color),
        ('prepare_body', body_color),
        ('pack_bag', 'chassis_bag', 'car_bag'),
        ('pack_bag', 'body_bag', 'car_bag'),
        ('mark_ready', 'car_bag')
    ]
    
hop.declare_methods('prepare_car', prepare_car)
## end of car bag



def prepare_order(state, order):
    return [
        ('prepare_house', order['house'][0], order['house'][1]),
        ('prepare_tree', order['tree'][0], order['tree'][0]), # Assuming trunk color == branch color ('brown')
        ('prepare_ground', order['ground']),
        ('prepare_car', order['car'][0], order['car'][1]),
        
        ('pack_bag', 'house_bag', 'main_bag'), 
        ('pack_bag', 'tree_bag', 'main_bag'), 
        ('pack_bag', 'ground_bag', 'main_bag'),
        ('pack_bag', 'car_bag', 'main_bag'),
        ('mark_ready', 'main_bag')
    ]

hop.declare_methods('prepare_order', prepare_order)

if __name__ == "__main__":
    st = state
    order = {
        'house': ('red', 'black'),
        'tree': ('brown', False),  # False = no leaves
        'ground': 'blue',
        'car': ('black', 'red')
    }

    #prepare_order(st, order)
    plan = hop.plan(st, [('prepare_order', order)], hop.get_operators(),hop.get_methods(),verbose=1)
    #print(f"\nGenerated plan with {len(plan)} actions")