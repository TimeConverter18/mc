import sys
import flet as ft
import socket
import threading
import krcollections as krc
from mcskills import *
from keyboard import on_press

card_list = []
runner_skills = {}
hunter_skills = {}
sk_bind = {}
skills = []
pl_roles = {}
all_players_skills = {}
isRunner = None
selector = 'f5'
selected_player = None
r_and_h = {}
other = []

def mn(page: ft.Page):
    def tell_info(p):
        s = [f'{e[0].name}:{e[1]}шт' for e in sk_bind.values() if e[1]>0]
        tell(players=[p], txt=f'У вас остались следующие способности:')
        for k in sk_bind.values():
            if k[1] > 0:
                tell(players=[p], color='green', txt=f'{k[0].name}: {k[1]}шт')
            else:
                tell(players=[p], color='red', txt=f'{k[0].name}: {k[1]}шт')
        tell(players=[p], txt='')

    def handle_key_press(e: ft.KeyboardEvent):
        global selector
        k = e.key
        selector = k.lower()
        colored_square.content = ft.Text(f'{k.replace('Arrow ', '')}', color=ft.Colors.WHITE)
        page.on_keyboard_event = None
        page.update()
    def start_key_binding(e):
        page.update()
        page.on_keyboard_event = handle_key_press
    def press(event):
        i = nick_dropdown.value
        global sk_bind
        global selected_player
        global other
        button = event.name
        print(button)
        if button == selector:
            other.reverse()
            selected_player = other[0]
            show_ttl(player=i, txt=selected_player)
            mcr.command(f'execute at {i} run playsound minecraft:block.note_block.bit block {i} ~ ~ ~ 1 1.5')
        if button in sk_bind:
            obj = sk_bind[button][0]
            c = sk_bind[button][1]
            id = obj.id
            if c > 0:
                mcr.command(f'execute at {i} run playsound minecraft:block.note_block.bell block {i} ~ ~ ~ 1 1.2')
                mcr.command(f'execute at {i} run particle dust{{color:[60, 0, 50],scale:0.7}} ~ ~ ~ 0 1 0 2 1000 normal {i}')
                match id:
                    case 1: #тест х
                        hunter = i
                        runner = r_and_h['Runner']
                        test(hunter=hunter, runner=runner)
                    case 2: #наблюдатель р
                        t = 5 + ((obj.now-1)*1.5)
                        spectr(player=i, t_cnt=t)
                    case 3: #лава р
                        lava(player=selected_player, size=4)
                    case 4: #тошнота х
                        t = 20 + ((obj.now - 1) * 10)
                        matushka(player=selected_player, time=t)
                    case 5: #тошнота р
                        t = 20 + ((obj.now - 1) * 10)
                        matushka(player=selected_player, time=t)
                    case 6: #наковальня р
                        anvil(player=selected_player)
                    case 7: #шипоголовый р
                        d = 10 + ((obj.now - 1) * 3)
                        spikehead(player=i, dmg=d)
                    case 8: #чек скиллов х
                        skill_checker(skills=skills, i=i, player=selected_player)
                    case 9: #чек скиллов р
                        skill_checker(skills=skills, i=i, player=selected_player)
                    case 10: #майнкарт р
                        t = 15 + ((obj.now - 1) * 10)
                        magic_minecart(player=i, t_cnt=t)
                    case 11: #тп к тиммейту х
                        to_who = r_and_h['Hunter']
                        to_who.remove(i)
                        tp_h_to_h(i,to_who[0])
                    case 12: #тнт хук х
                        tnt_hook(player=i, t_cnt=5)
                    case 13: #тнт хук р
                        tnt_hook(player=i, t_cnt=5)
                    case 14: #инвизка мобам х
                        t = 80 + ((obj.now - 1) * 80)
                        invisibility2mobs(i=i, player=r_and_h['Runner'], time=t, dist=60)
                    case 15: #инвизка себе р
                        t = 30 + ((obj.now-1)*10)
                        invisibility2pl(player=i, time_dur=t)
                    case 16: #дельфин х
                        dolphin(i)
                    case 17: #дельфин р
                        dolphin(i)
                    case 18: #лодка х
                        t = 30 + ((obj.now - 1) * 20)
                        boat(player=i, t_cnt=t)
                    case 19: #лодка р
                        t = 30 + ((obj.now - 1) * 20)
                        boat(player=i, t_cnt=t)
                    case 20: #картофан х
                        t = 3 + ((obj.now-1)*3)
                        kartofan(player=r_and_h['Runner'], time_dur=t)
                    case 21: #картофан р
                        t = 3 + ((obj.now - 1) * 3)
                        kartofan(player=selected_player, time_dur=t)
                    case 22: #подсветка х
                        d = 25 + ((obj.now-1)*20)
                        t = 3 + ((obj.now-1)*3)
                        podsvetka(i=i, player=r_and_h['Runner'], dist=d, time=t)
                    case 23: #спавн крипера х
                        creeper(r_and_h['Runner'])
                    case 24: #скорка р
                        t = 20 + ((obj.now-1)*20)
                        speed(i=i, time=t)
                    case 25: #перемотка р
                        peremotka(players=players)
                sk_bind[button][1] = c-1
                tell_info(i)
            else:
                mcr.command(f'execute at {i} run playsound minecraft:block.note_block.bass block {i} ~ ~ ~ 1 1')
                show_ttl(player=i, txt=f'У вас закончились способности {obj.name}', clr='red')
                tell_info(i)

    def add_checker():
        if isRunner:
            for e in r_c_list:
                if e.cost > int(coins_obj_r.value):
                    e.add_button.disabled = True
                elif e.max_n > e.now:
                    e.add_button.disabled = False
                page.update()
        else:
            for e in h_c_list:
                if e.cost > int(coins_obj_h.value):
                    e.add_button.disabled = True
                elif e.max_n > e.now:
                    e.add_button.disabled = False
                page.update()
    def start_game():
        global other
        global sk_bind
        global skills
        global selected_player
        ready_sw.disabled = True
        nick_dropdown.disabled = True
        role_dropdown.disabled = True
        txt.value = 'Запускаю игру...'
        page.update()
        selection_pl = nick_dropdown.value
        selection_rol = role_dropdown.value
        if selection_rol == 'Runner':
            for e in r_c_list:
                k = e.k
                if k and e.now>0:
                    sk_bind[k.lower()] = [e, e.now]
                    skills.append(e.name)
            print(sk_bind)
        else:
            for e in h_c_list:
                k = e.k
                if k and e.now>0:
                    sk_bind[k.lower()] = [e, e.now]
                    skills.append(e.name)
            print(sk_bind)
        t = players
        t.remove(selection_pl)
        other = t
        client.send(f'{selection_pl}@{skills}'.encode('utf-8'))
        on_press(lambda x: press(x))
        selected_player = other[0]
        txt.value = f'Игра запущена и начнётся когда {'вы ударите хантеров' if isRunner else 'вас ударит спидраннер'}.'
        page.update()

    def receive_messages(client_socket):
        global all_players_skills
        global pl_roles
        global r_and_h
        while True:
            try:
                message = client_socket.recv(1024).decode('utf-8')
                if message:
                    if message != 'readytostart':
                        print(f"Сообщение от сервера: {message}")
                        if message == 'ready!':
                            ready_sw.disabled = False
                            txt.value = 'Все игроки выбрали роли. Когда будете готовы начать, нажмите на кнопку.'
                            page.update()
                        elif message == 'hmm':
                            ready_sw.disabled = True
                            if nick_dropdown.value and role_dropdown.value:
                                txt.value = 'Ждём, пока все верно введут данные.'
                                ready_sw.value = False
                            else:
                                txt.value = 'Выбери ник и роль, чтобы начать игру!'
                                ready_sw.value = False
                            page.update()
                        else:
                            message = message.split('†')
                            s = eval(f'{message[0]}')
                            all_players_skills = s
                            v = eval(f'{message[1]}')
                            pl_roles = v
                            v = list(v.items())
                            res3 = {'Hunter': []}
                            res1 = list(filter(lambda x: x[1] == 'Runner', v))
                            res2 = list(filter(lambda x: x[1] == 'Hunter', v))
                            res1 = {e[1]: e[0] for e in res1}
                            for e in res2:
                                res3[e[1]].append(e[0])
                            res1.update(res3)
                            r_and_h = res1
                            print(s, r_and_h)
                    else:
                        print(message)
                        start_game()
            except Exception as e:
                print(e)
                print("Отключение от сервера")
                client_socket.close()
                break
    def change_theme(e):
        page.theme_mode = 'light' if page.theme_mode == 'dark' else 'dark'
        for t in r_c_list:
            t.res.bgcolor = '#06718a' if page.theme_mode == 'dark' else '#c9debd'
        for t in h_c_list:
            t.res.bgcolor = '#06718a' if page.theme_mode == 'dark' else '#c9debd'
        page.update()

    def ready_switcher(e):
        r = e.data
        print(r)
        if r == 'false':
            txt.value = 'Когда будете готовы начать, нажмите на кнопку.'
            client.send('n'.encode('utf-8'))
            page.update()
        else:
            client.send('y'.encode('utf-8'))
            txt.value = 'Ждём, пока все будут готовы к игре.'
            page.update()

    def send_selection(e):
        global selector
        global card_list
        global isRunner
        selection_pl = nick_dropdown.value
        selection_rol = role_dropdown.value
        if selection_rol == 'Runner' and runner_row not in page.controls:
            if selector_row in page.controls:
                page.remove(selector_row)
            isRunner = True
            if hunter_row in page.controls:
                page.remove(hunter_row)
                control_row.controls.remove(hunter_money_row)
            control_row.controls.append(runner_money_row)
            page.add(runner_row)
            if selector_row not in page.controls:
                page.add(selector_row)
            page.update()
        elif selection_rol == 'Hunter' and hunter_row not in page.controls:
            if selector_row in page.controls:
                page.remove(selector_row)
            isRunner = False
            selector = None
            if runner_row in page.controls:
                page.remove(runner_row)
                control_row.controls.remove(runner_money_row)
            control_row.controls.append(hunter_money_row)
            page.add(hunter_row)
            if selector_row not in page.controls:
                page.add(selector_row)
            page.update()
        if selection_pl and selection_rol:
            data = f"{selection_pl} {selection_rol}"
            client.send(data.encode('utf-8'))
            txt.value = 'Ждём, пока другие игроки выберут ник и роль.'
            page.update()
    page.title = 'ManHunt 1.21.1 utility'
    page.theme_mode = 'light'
    page.window.width = 1300
    page.window.height = 700
    #page.window.resizable = False
    page.vertical_alignment = ft.MainAxisAlignment.START
    theme_button = ft.IconButton(icon=ft.Icons.SUNNY, on_click=change_theme, tooltip='Поменять тему приложения', on_blur=lambda x: print('hi'))
    txt = ft.Text(value='Выбери ник и роль, чтобы начать игру!', text_align=ft.alignment.center)
    ready_sw = ft.Switch(on_change=ready_switcher, disabled=True, inactive_track_color='red', active_track_color='green', inactive_thumb_color='white')
    nick_dropdown = ft.Dropdown(options=[
            ft.dropdown.Option('TimeConverter18'),
            ft.dropdown.Option('AlexUgar'),
            ft.dropdown.Option('Remix008'),
        ], on_change=send_selection)
    role_dropdown = ft.Dropdown(options=[
        ft.dropdown.Option('Runner'),
        ft.dropdown.Option('Hunter')
    ], on_change=send_selection)
    coins_obj_r = ft.Text(value='999999', size=25, color='red')
    coins_obj_h = ft.Text(value='50', size=25, color='red')

    try:
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client.connect(('26.11.111.77', 12345))
        receive_thread = threading.Thread(target=receive_messages, args=(client,), daemon=True)
        receive_thread.start()
    except:
        print('Похоже сервер не запущен, или КИРИЛЛ ВЫКЛЮЧИ ВПН!!!(ору сам на себя)')
        sys.exit()

    test_mh_h = krc.MButton(coins_obj_h, page, add_checker, cost=50, name='ТЕСТ_МЭНХАНТ???', descr='АХАХАХАХАХ\nХАХАХАХАХА', max_n=1, pixel='test_manhunt.png', id=1)
    endereye_mh_r = krc.MButton(coins_obj_r, page, add_checker, cost=6, name='Эндерчел', descr='Выдаёт наблюдателя без ограничений ровно на 5 секунд.\nСкейлится время.', max_n=10, pixel='ender_eye.png', id=2)
    lava_mh_r = krc.MButton(coins_obj_r, page, add_checker, cost=5, name='Окружение лавой', descr='Окружает хантера лавой.\nЛава спавнится по квадрату на 3-й блок от охотника.\nНа выбранного противника.', max_n=4, pixel='lava.png', id=3)
    matushka_mh_h = krc.MButton(coins_obj_r, page, add_checker, cost=2, name='Отравление', descr='Выдаёт кучу дебаффов и включает Матушку на полную громкость!\nНа выбранного игрока.', max_n=3, pixel='nausea.png', id=4)
    matushka_mh_r = krc.MButton(coins_obj_r, page, add_checker, cost=2, name='Отравление',descr='Выдаёт кучу дебаффов и включает Матушку на полную громкость!\nНа выбранного игрока.', max_n=3,pixel='nausea.png', id=5)
    nakovalniy_mh_r =krc.MButton(coins_obj_r, page, add_checker, cost=10, name='Наковальня', descr='Сбрось наковальню на голову хантерам.\nСпавнится в 5 блоках над игроком и убивает его!\nНа выбранного противника.', max_n=5, pixel='nakovalniy.png', id=6)
    shipogoloviy_mh_r = krc.MButton(coins_obj_r, page, add_checker, cost=12, name='Шипоголовый', descr='Выпускает стрелы во все стороны.\nСкейлится урон стрел.', max_n=3, pixel='шипоголовый.png', id=7)
    check_skills_mh_h = krc.MButton(coins_obj_r, page, add_checker, cost=15, name='Чек скиллов', descr='Отправляет в чат список скиллов игрока.\nНа выбранного игрока.', max_n=1, pixel='скиллы.png', id=8)
    check_skills_mh_r = krc.MButton(coins_obj_r, page, add_checker, cost=15, name='Чек скиллов',descr='Отправляет в чат список скиллов игрока.\nНа выбранного игрока.', max_n=1,pixel='скиллы.png', id=9)
    minecart_mh_r = krc.MButton(coins_obj_r, page, add_checker, cost=8, name='Майнкарт', descr='Спавнит волшебную вагонетку.\nСкейлится время езды.', max_n=3, pixel='minecart.png', id=10)
    tphtoh_mh_h = krc.MButton(coins_obj_r, page, add_checker, cost=3, name='ТП к тиммейту', descr='Телепортирует к тиммейту.', max_n=15, pixel='tp.png', id=11)
    tnthook_mh_h = krc.MButton(coins_obj_r, page, add_checker, cost=2, name='ТНТ хук', descr='Даёт удочку и динамит.', max_n=5, pixel='TNT_rod.png', id=12)
    tnthook_mh_r = krc .MButton(coins_obj_r, page, add_checker, cost=2, name='ТНТ хук', descr='Даёт удочку и динамит.', max_n=5, pixel='TNT_rod.png', id=13)
    invizmobam_mh_h = krc.MButton(coins_obj_r, page, add_checker, cost=7, name='Инвиз мобам', descr='Делает мобов вокруг раннера невидимыми.\nРаботает на раннера.\nСкейлится время.', max_n=4, pixel='iviz.png', id=14)
    invizsebe_mh_r = krc.MButton(coins_obj_r, page, add_checker, cost=10, name='Инвиз себе', descr='Делает тебя невидимым на 30с.\nСкейлится время.', max_n=5, pixel='iviz.png', id=15)
    dolphin_mh_h = krc.MButton(coins_obj_r, page, add_checker, cost=2, name='Фуриёбка', descr='Спавнит дельфина, который ускоряет тебя в воде.', max_n=5, pixel='dolphin.png', id=16)
    dolphin_mh_r = krc.MButton(coins_obj_r, page, add_checker, cost=2, name='Фуриёбка',descr='Спавнит дельфина, который ускоряет тебя в воде.', max_n=5, pixel='dolphin.png',id=17)
    boat_mh_h = krc.MButton(coins_obj_r, page, add_checker, cost=6, name='Алладин', descr='Спавнит летающую лодку на 30с.\nСкейлится время.', max_n=3, pixel='oak_boat.png', id=18)
    boat_mh_r = krc.MButton(coins_obj_r, page, add_checker, cost=6, name='Алладин',descr='Спавнит летающую лодку на 30с.\nСкейлится время.', max_n=3, pixel='oak_boat.png',id=19)
    kartofan_mh_h = krc.MButton(coins_obj_r, page, add_checker, cost=10, name='Картофан', descr='Заменяет предмет в хотслоте на картошку на 5с.\nСкелится время.\nРаботает на раннера.', max_n=5, pixel='картофан.png', id=20)
    kartofan_mh_r = krc.MButton(coins_obj_r, page, add_checker, cost=10, name='Картофан', descr='Заменяет предмет в хотслоте на картошку на 5с.\nСкелится время.\nРаботает на выбранного противника.', max_n=5, pixel='картофан.png', id=21)
    podsvetka_mh_h = krc.MButton(coins_obj_r, page, add_checker, cost=4, name='Подсветка', descr='Подсвечивает раннера.\nСкейлится время и дальность подсветки.', max_n=5, pixel='Подсветka.png', id=22)
    spawnkreeper_mh_h = krc.MButton(coins_obj_r, page, add_checker, cost=15, name='Крипер', descr='Спавнит крипера внутри раннера.', max_n=1, pixel='creeper.png', id=23)
    speed_mh_r = krc.MButton(coins_obj_r, page, add_checker, cost=5, name='Скорка', descr='Даёт скорость 1 на 20с.\nСкейлится время.', max_n=10, pixel='speed.png', id=24)
    peremotka_mh_r = krc.MButton(coins_obj_r, page, add_checker, cost=25, name='Перемотка', descr='Перематывает время.\nПервое нажатие - запоминает координаты игроков.\nВторое - телепортирует на эти координаты.', max_n=1, pixel='peremotka.png', id=25)

    r_c_list = [endereye_mh_r, lava_mh_r, nakovalniy_mh_r, matushka_mh_r, shipogoloviy_mh_r, check_skills_mh_r, minecart_mh_r, tnthook_mh_r, invizsebe_mh_r, dolphin_mh_r, boat_mh_r, kartofan_mh_r, speed_mh_r, peremotka_mh_r]
    h_c_list = [test_mh_h, matushka_mh_h, check_skills_mh_h, tphtoh_mh_h, tnthook_mh_h, invizmobam_mh_h, dolphin_mh_h, boat_mh_h, kartofan_mh_h, podsvetka_mh_h, spawnkreeper_mh_h]
    runner_row = ft.GridView([e.res for e in r_c_list], expand=True,max_extent=145, child_aspect_ratio=0.6, run_spacing=15, spacing=20)
    hunter_row = ft.GridView([e.res for e in h_c_list],expand=True,max_extent=145, child_aspect_ratio=0.6, run_spacing=15, spacing=20)
    hunter_money_row = ft.Row([ft.Text(value='У вас', size=20), coins_obj_h, ft.Text(value='Mh', size=20)],alignment=ft.MainAxisAlignment.CENTER)
    runner_money_row = ft.Row([ft.Text(value='У вас', size=20), coins_obj_r, ft.Text(value='Mh', size=20)],alignment=ft.MainAxisAlignment.CENTER)
    control_row = ft.Row([ready_sw, nick_dropdown, role_dropdown],alignment=ft.MainAxisAlignment.CENTER)
    colored_square = ft.Container(width=50, height=25, bgcolor=ft.Colors.GREEN, border_radius=4,alignment=ft.alignment.center, content=ft.Text('F5', color=ft.Colors.WHITE),on_click=lambda e: start_key_binding(e), )
    selector_row = ft.Row([ft.Text(value='Бинд селектера: ', size=15), colored_square],
                          alignment=ft.MainAxisAlignment.CENTER)
    page.add(
        ft.Row(
            [
                txt, theme_button
            ], alignment=ft.MainAxisAlignment.END, spacing=430
        ),
        control_row
    )
players = ['TimeConverter18', 'Remix008', 'AlexUgar']
roles = ['Runner', 'Hunter']
ft.app(target=mn)
