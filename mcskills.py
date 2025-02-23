import keyboard

from mc import *
from time import sleep, time
from pyautogui import scroll
from math import pi, sin, cos

peremotka_saved = False
cd = []

def magic_minecart(player='Remix008', t_cnt=10):
    res = get_rot()[0]
    facing = 'north_south'
    z = 0
    x = 0
    if -45 <= res < 45:
        facing = 'north_south'
        z = 1
    elif -135 <= res < -45:
        facing = 'east_west'
        x = 1
    elif -180 <= res < -135 or 135 <= res < 180:
        facing = 'north_south'
        z = -1
    elif 45 <= res < 135:
        facing = 'east_west'
        x = -1

    spawn_mob(player=player, mob='minecart', x=f'~{x}', y='~1', z=f'~{z}')
    tr_pl_pos(player='@e[type=minecart, limit=1, sort=nearest]', abs=False, world=get_dimension(player), r_y=get_rot(player)[0], r_x=0)
    mcr.command(
        f'execute at {player} at @e[type=minecart, limit=1, sort=nearest, distance=..5] run setblock ~ ~-1 ~ minecraft:redstone_block')
    mcr.command(
        f'execute at {player} at @e[type=minecart, limit=1, sort=nearest, distance=..5] run setblock ~ ~ ~ minecraft:powered_rail[shape={facing}]')
    mcr.command(
        f'execute at {player} at @e[type=minecart, limit=1, sort=nearest, distance=..5] run setblock ~{x} ~-1 ~{z} minecraft:redstone_block')
    mcr.command(
        f'execute at {player} at @e[type=minecart, limit=1, sort=nearest, distance=..5] run setblock ~{x} ~ ~{z} minecraft:powered_rail[shape={facing}]')

    nums = (0, 1, 2, 3, 4, 5, 6, 7, 8, 9)
    t = time()
    x = x*3
    z = z*3

    while time() - t < t_cnt:
        show_ttl(player=player, txt=f'Оставшееся время:{round(t_cnt - time() + t, 1)}с', fd_out=0.1, stay=0.1)
        mcr.command(
            f'execute at {player} as @e[type=minecart, limit=1, sort=nearest, distance=..5] at @s run fill ~{x} ~-1 ~{z} ~ ~-1 ~ minecraft:redstone_block')
        mcr.command(f'execute at {player} as @e[type=minecart, limit=1, sort=nearest, distance=..5] at @s run fill ~{x} ~ ~{z} ~{x*0.3} ~ ~{z*0.3} minecraft:powered_rail[shape={facing}]')
        mcr.command(f'execute at {player} run kill @e[type=item, distance=..5, nbt={{Item:{{id:"minecraft:powered_rail",count:1}}}}]')
        mcr.command(f'execute at {player} as @e[type=minecart, limit=1, sort=nearest, distance=..5] at @s run fill ~{-2*x} ~-1 ~{-2*z} ~{x} ~ ~{-z} air')

def anvil(player='Remix008', dmg=100):
    mcr.command(f'execute at {player} run summon falling_block ~ ~10 ~ {{BlockState:{{Name:"minecraft:anvil"}},Time:1,DropItem:0b,CancelDrop:1b,HurtEntities:1b,FallHurtMax:{dmg},FallHurtAmount:{dmg}f,Motion:[0.0,-0.1,0.0],Glowing:1b}}')

def boat(player='Remix008', t_cnt=10):
    mcr.command(f'execute at {player} unless entity @e[type=boat, tag={player}] run summon minecraft:boat ^ ^1 ^2 {{NoGravity:1b, Rotation:[{get_rot(player)[0]}f, 0f], Tags:["{player}"]}}')
    res = 1
    t = time()
    sleep(3)
    while res and time() - t < t_cnt:
        res = mcr.command(f'data get entity {player} RootVehicle.Entity.NoGravity')[0]
        res = 0 if res == 'F' else 1
        show_ttl(player=player, txt=f'Оставшееся время: {round(t_cnt - time() + t, 1)}с', fd_out=0.1, stay=0.1)
        sleep(0.1)
    mcr.command(f'kill @e[type=boat, tag={player}]')

def tnt_hook(player='Remix008', t_cnt=4):
    ctm_name = '{"bold":true,"color":"red","text":"Удочка с TNT"}'
    mcr.command(f"give {player} fishing_rod[custom_name='{ctm_name}'] 1")
    if mcr.command(f'scoreboard players set {player} {player}rod 0') != "Unknown scoreboard objective '{player}rod'":
        mcr.command(f'scoreboard objectives add {player}rod minecraft.used:minecraft.fishing_rod')
    mcr.command(f'scoreboard players set {player} {player}rod 0')
    while int(re.search(r' \d ', str(mcr.command(f'scoreboard players get {player} {player}rod')))[0][1]) == 0:
        sleep(0.1)
    mcr.command(f'execute at {player} at @e[type=minecraft:fishing_bobber, limit=1, sort=nearest] run summon tnt ~ ~ ~ {{fuse:80}}')
    mcr.command(f'scoreboard objectives remove {player}rod')
    sleep(t_cnt)
    mcr.command(f'clear {player} fishing_rod[custom_name="{{"bold":true,"color":"red","text":"Удочка с TNT"}}"] 1')

def tp_h_to_h(who='Remix008', to_who='TimeConverter18'):
    mcr.command(f'tp {who} {to_who}')
    show_ttl(player=who, txt=f'Вы телепортированы к {to_who}')
    show_ttl(player=to_who, txt=f'К вам телепортирован {who}')

def spectr(player='Remix008', t_cnt=5):
    gm = get_gamemode(player)
    mcr.command(f'gamemode spectator {player}')
    sleep(0.01)
    scroll(6000)
    t = time()
    while time() - t < t_cnt:
        show_ttl(player=player, txt=f'Оставшееся время: {round(t_cnt - time() + t, 1)}с', fd_out=0.1, stay=0.1)
        sleep(0.1)
    mcr.command(f'gamemode {gm} {player}')

def invisibility2mobs(i='TimeConverter18', player='Remix008', dist=10, time=10):
    mcr.command(f'effect give @e[type=!minecraft:player, type=!minecraft:ender_dragon, distance=..{dist}] minecraft:invisibility {time} 0 true')
    show_ttl(player=i, txt=f'Мобам в радиусе {dist} блоков вокруг {player} выдана инвизка на {time}с')
def invisibility2pl(player='Remix008', time_dur=60):
    mcr.command(f'effect give {player} minecraft:invisibility {time_dur} 0 true')
    t = time()
    while time() - t < time_dur:
        show_ttl(player=player, txt=f'Оставшееся время: {round(time_dur - time() + t, 1)}с', fd_out=0.1, stay=0.1)
        sleep(0.1)

def skill_checker(skills, i='TimeConverter18', player='Remix008'):
    s = skills[player]
    s = eval(s)
    tell([i], txt=f'{player} имеет следующие способности:\n{s}')

def test(hunter='Remix008', runner='Timeconverter18'):
    for n in range(27):
        res = mcr.command(f'data get entity {runner} Inventory[{{Slot: {n + 9}b}}].components')
        in_slot = mcr.command(f'data get entity {runner} Inventory[{{Slot: {n + 9}b}}]')
        if 'Found no el' in in_slot:
            in_slot = ('minecraft:air', ' 1')
        else:
            in_slot = [re.search(r'id: "\w+:\w+"', in_slot)[0][5:-1],
                       re.search(r'count: \d+', in_slot)[0][6:]]
        res1, res2 = '', ''
        flg1, flg2 = False, False
        if 'custom_name' in res:
            res1 = re.search(r'me": \'".+"\'', res)[0][6:]
            flg1 = True
        if 'enchantments' in res:
            flg2 = True
            res2 = re.search(r'nts": \{levels: \{.+}},', res)[0][7:-1]

        mcr.command(f'item replace entity {runner} inventory.{n} from entity {hunter} inventory.{n}')
        print(mcr.command(
            f'item replace entity {hunter} inventory.{n} with {in_slot[0]}[{f'custom_name=\'{res1},' if flg1 else ''}{f'enchantments={{{res2}' if flg2 else ''}]{in_slot[1]}'))

    for n in range(9):
        res = mcr.command(f'data get entity {runner} Inventory[{{Slot: {n}b}}].components')
        in_slot = mcr.command(f'data get entity {runner} Inventory[{{Slot: {n}b}}]')
        if 'Found no el' in in_slot:
            in_slot = ('minecraft:air', ' 1')
        else:
            in_slot = [re.search(r'id: "\w+:\w+"', in_slot)[0][5:-1],
                       re.search(r'count: \d+', in_slot)[0][6:]]
        res1, res2 = '', ''
        flg1, flg2 = False, False
        if 'custom_name' in res:
            res1 = re.search(r'me": \'".+"\'', res)[0][6:]
            flg1 = True
        if 'enchantments' in res:
            flg2 = True
            res2 = re.search(r'nts": \{levels: \{.+}},', res)[0][7:-1]

        mcr.command(f'item replace entity {runner} hotbar.{n} from entity {hunter} hotbar.{n}')
        print(mcr.command(
            f'item replace entity {hunter} hotbar.{n} with {in_slot[0]}[{f'custom_name=\'{res1},' if flg1 else ''}{f'enchantments={{{res2}' if flg2 else ''}]{in_slot[1]}'))

    pos1, pos2 = get_pos(runner), get_pos(hunter)
    rot1, rot2 = get_rot(runner), get_rot(hunter)

    tr_pl_pos(player=hunter, x=pos1[0], y=pos1[1], z=pos1[2], r_y=rot1[0], r_x=rot1[1])
    tr_pl_pos(player=runner, x=pos2[0], y=pos2[1], z=pos2[2], r_y=rot1[0], r_x=rot2[1])

    mcr.command(f'sudoop TimeConverter18 runner add {hunter}')
    mcr.command(f'sudoop TimeConverter18 hunter add {runner}')

def lava(player='Remix008', size=3):
    mcr.command(f'execute at {player} run fill ~{size} ~-{size/3} ~{size} ~2 ~{size/3 - 1} ~-1 minecraft:lava')
    mcr.command(f'execute at {player} run fill ~{size} ~-{size/3} ~-{size} ~-1 ~{size/3 - 1} ~-2 minecraft:lava')
    mcr.command(f'execute at {player} run fill ~-{size} ~-{size/3} ~-{size} ~-2 ~{size/3 - 1} ~1 minecraft:lava')
    mcr.command(f'execute at {player} run fill ~-{size} ~-{size/3} ~{size} ~1 ~{size/3 - 1} ~2 minecraft:lava')

def kartofan(player='Remix008', time_dur=5):
    slot = get_slot(player)
    res = mcr.command(f'data get entity {player} SelectedItem.components')
    in_slot = mcr.command(f'data get entity {player} SelectedItem')
    if in_slot == 'Found no elements matching SelectedItem':
        in_slot = ('minecraft:air', '1')
    else:
        in_slot = [re.search(r'id: "\w+:\w+"', in_slot)[0][5:-1],
                   re.search(r'count: \d+', in_slot)[0][6:]]
    mcr.command(f'item replace entity {player} hotbar.{slot} with minecraft:poisonous_potato[minecraft:enchantment_glint_override=1] 1')
    t = time()
    while time() - t < time_dur:
        show_ttl(player=player, txt=f'Картофельное время: {round(time_dur - time() + t, 1)}с', fd_out=0.1, stay=0.1)
        sleep(0.1)
    mcr.command(f'clear {player} minecraft:poisonous_potato[minecraft:enchantment_glint_override=1] 1')
    print(res)
    res1, res2 = '', ''
    flg1, flg2 = False, False
    if 'custom_name' in res:
        res1 = re.search(r'me": \'".+"\'', res)[0][6:]
        flg1 = True
    if 'enchantments' in res:
        flg2 = True
        res2 = re.search(r'nts": \{levels: \{.+}},', res)[0][7:-1]

    mcr.command(
        f'give {player} {in_slot[0]}[{f'custom_name=\'{res1},' if flg1 else ''}{f'enchantments={{{res2}' if flg1 else ''}]{in_slot[1]}')
    print(
        f'give {player} {in_slot[0]}[{f'custom_name=\'{res1},' if flg1 else ''}{f'enchantments={{{res2}' if flg1 else ''}]{in_slot[1]}')

def dolphin(player='Remix008'):
    spawn_mob(player=player, x='~', y='~', z='~', mob='dolphin', custom_name='Фуриёбка')

def spikehead(player='Remix008', dmg=10):
    show_ttl(player=player, txt='Погнали!')
    a = -pi
    while a <= pi:
        mcr.command(f'execute at {player} run summon arrow ~ ~2 ~ {{pickup:0b, damage:{dmg}d, Fire:120, Motion:[{sin(a)},0.0,{cos(a)}], Tags:["spikeheadarrow{player}"]}}')
        a += 0.08
    sleep(7)
    mcr.command(f'kill @e[type=arrow, tag=spikeheadarrow{player}]')

def podsvetka(i='TimeConverter18', player='AlexUgar', dist=25, time=3):
    mcr.command(f'execute at {i} run effect give @a[distance=..{dist}, name={player}] minecraft:glowing {time}')

def speed(i='TimeConverter18', time=20):
    give_eff(player=i,type='speed', level=0, time=time)

def creeper(player='AlexUgar'):
    world = get_dimension(player)
    spawn_mob(player=player, mob='creeper', world=world, x='~', y='~', z='~', custom_name='Взрыватель жопы')

def matushka(i='TimeConverter18', player='AlexUgar', time=20):
    show_ttl(i, txt='Вы использовали матушку!')
    mcr.command(f'effect give {player} minecraft:darkness {time} 2')
    mcr.command(f'effect give {player} minecraft:blindness {time} 2')
    mcr.command(f'effect give {player} minecraft:nausea {time} 2')
    mcr.command(f'effect give {player} minecraft:mining_fatigue {time} 2')
    mcr.command(f'execute at {player} run playsound minecraft:custom.matushka block {player} ~ ~ ~ 3 1.1')

def peremotka(players):
    global peremotka_saved
    global cd
    if peremotka_saved:
        for player, c in enumerate(players):
            tr_pl_pos(player=player, x=cd[c][0], y=cd[c][1], z=cd[c][2], world=cd[c][3])
    else:
        cd = []
        for player in players:
            cd.append(list(get_pos(player)) + [get_dimension(player)])
