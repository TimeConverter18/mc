from mcrcon import MCRcon
import re

i = 'TimeConverter18'
host = "26.11.111.77"
port = 25575
password = "leshagay"
mcr = MCRcon(host, password, port)
mcr.connect()


def get_pos(player='Remix008'):
    response = mcr.command(f"data get entity {player} Pos")
    match = re.search(r'\[(-?\d+\.\d+)d, (-?\d+\.\d+)d, (-?\d+\.\d+)d\]', response)
    x = float(match.group(1))
    y = float(match.group(2))
    z = float(match.group(3))
    return x, y, z


def get_dimension(player='Remix008'):
    dimension = mcr.command(f"data get entity {player} Dimension")
    dimension = re.search(r'\w+:\w+', dimension)
    dimension = dimension.group(0)
    return dimension


def get_gamemode(player='Remix008'):
    s = ('survival', 'creative', 'adventure', 'spectator')
    gamemode = mcr.command(f'data get entity {player} playerGameType')
    gamemode = int(re.search(r': \d+', gamemode)[0][2:])
    return s[gamemode]


def tell(players=['Remix008'], txt='test', color='green'):
    for e in players:
        mcr.command(f'tellraw {e} {{"text":"{txt}", "color":"{color}"}}')


def spawn_block(player='Remix008', block='lava', x_off=0, y_off=0, z_off=0):
    x, y, z = get_pos(player)
    y = int(y + 0.5 if y >= 0 else y - 0.5)
    x = int(x) if x >= 0 else int(x - 1)
    z = int(z) if z >= 0 else int(z - 1)
    x, y, z = x + x_off, y + y_off, z + z_off
    mcr.command(f'setblock {x} {y} {z} minecraft:{block}')


def spawn_mob(player='Remix008', mob='creeper', x='~', y='~', z='~', custom_name='none', world='overworld'):
    if custom_name == 'none':
        mcr.command(f'execute in {world} at {player} run summon minecraft:{mob} {x} {y} {z}')
    else:
        custom_name = f'"{custom_name}"'
        mcr.command(f"execute in {world} at {player} run summon minecraft:{mob} {x} {y} {z} {{CustomNameVisible:1b,CustomName:'{custom_name}'}}")


def show_ttl(player='Remix008', type='actionbar', txt='ПРОВЕРКА СВЯЗИ', clr='green', fd_in='0.2s', stay='2s', fd_out='1s'):
    mcr.command(f'title {player} times {fd_in} {stay} {fd_out}')
    mcr.command(f'title {player} {type} {{"text":"{txt}", "color":"{clr}"}}')
    mcr.command(f'title {player} times 0s 2s 1s')


def tr_pl_pos(player='Remix008', x=0, y=0, z=0, r_y=0.0, r_x=0.0, abs=True, world='overworld'):
    if abs:
        mcr.command(f'execute in {world} run tp {player} {x} {y} {z} {r_y} {r_x}')
    else:
        mcr.command(f'execute at {player} run tp {player} ~{x} ~{y} ~{z} {r_y} {r_x}')


def give_eff(player='Remix008', type='speed', level=1, hide_p='true', time=10):
    mcr.command(f'effect give {player} minecraft:{type} {time} {level-1} {hide_p}')


def get_rot(player='Remix008'):
    res = mcr.command(f'data get entity {player} Rotation')
    res = re.search(r'\[(-?\d+\.\d+)f, (-?\d+\.\d+)f', res)
    r_y = float(res.group(1))
    r_x = float(res.group(2))
    return r_y, r_x

def tr_gm(player='Remix008', gm='spectator'):
    mcr.command(f'gamemode {gm} {player}')

def get_inv(player='Remix08'):
    res = mcr.command(f'data get entity {player} Inventory')
    res = re.search(r'has the following entity data: \[(\{count: \d+, Slot: \d+\w, id: "\w+:\w+"})]', res)[0].replace('has the following entity data: ', '')
    return res


def get_slot(player='Remix008'):
    res = mcr.command(f'data get entity {player} SelectedItemSlot')
    res = int(re.search(r': \d+', res)[0][2:])
    return res