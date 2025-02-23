import flet as ft
from flet.core.border_radius import horizontal


class MButton:
    def handle_key_press(self, e: ft.KeyboardEvent):
        k = e.key
        print(1)
        if k!='Escape':
            self.colored_square.content = ft.Text(f'{k.replace('Arrow', '')}', color=ft.colors.WHITE)
            self.k = k
            self.colored_square.bgcolor = ft.colors.GREEN
            self.page.on_keyboard_event = None
            self.page.update()
        else:
            self.colored_square.content = ft.Text('', color=ft.colors.WHITE)
            self.k = None
            self.colored_square.bgcolor = ft.colors.RED
            self.page.on_keyboard_event = None
            self.page.update()

    def start_key_binding(self, e):
        self.page.update()
        self.page.on_keyboard_event = self.handle_key_press

    def __init__(self, co, page, add_checker, descr=None, pixel=None, name=None, cost=None, max_n=None, id=None):
        self.id = id
        self.k = None
        self.add_checker = add_checker
        self.co = co
        self.page = page
        self.now = 0
        self.descr = descr
        self.name = name
        self.cost = cost
        self.max_n = max_n
        self.colored_square = ft.Container(width=50,height=25,bgcolor=ft.colors.RED,border_radius=4,alignment=ft.alignment.center,content=ft.Text('', color=ft.colors.WHITE),on_click=lambda e: self.start_key_binding(e),)
        self.tt = ft.Tooltip(self.descr, wait_duration=0, border_radius=5, enable_tap_to_dismiss=False, padding=10, vertical_offset=140, text_align=ft.TextAlign.CENTER)
        self.now_obj = ft.Text(value=f'  {self.now}  ')
        self.pixel_obj = ft.Image(src=f'arts\\{pixel}', border_radius=10)
        self.name_obj = ft.Text(value=self.name, text_align=ft.TextAlign.CENTER, style=ft.TextStyle(italic=True))
        self.cost_obj = ft.Text(value=f'{self.cost}Mh', color='#66c22d')
        self.max_obj = ft.Text(value=f'{max_n} шт', color='#fc1c36')
        self.add_button = ft.IconButton(icon=ft.Icons.ADD, on_click=self.on_add)
        self.clear_button = ft.IconButton(icon=ft.Icons.REMOVE, on_click=self.on_clear, disabled=True)
        self.res = ft.Container(content=ft.Column(
            [
                self.pixel_obj, self.name_obj, ft.Row([self.colored_square, self.max_obj, self.cost_obj], spacing=5), ft.Row(
                [
                    self.clear_button, self.now_obj, self.add_button
                ])
            ]
        , spacing=3, horizontal_alignment=ft.CrossAxisAlignment.CENTER), tooltip=self.tt, bgcolor='#c9debd', border_radius=10, padding=8
            , alignment=ft.alignment.center)
    def on_add(self, x):
        mh = int(self.co.value)
        if self.now < self.max_n and mh>=self.cost:
            mh-=self.cost
            self.co.value = f'{mh}'
            self.now += 1
            self.now_obj.value = f'{self.now}'
            if self.now == self.max_n or mh<self.cost:
                self.add_button.disabled = True
                self.clear_button.disabled = False
            else:
                self.add_button.disabled = False
                self.clear_button.disabled = False
            self.add_checker()
            self.page.update()

    def on_clear(self, x):
        mh = int(self.co.value)
        if self.now > 0:
            mh += self.cost
            self.co.value = f'{mh}'
            self.now -= 1
            self.now_obj.value = f'  {self.now}  '
            if self.now == 0:
                self.add_button.disabled = False
                self.clear_button.disabled = True

            else:
                self.add_button.disabled = False
                self.clear_button.disabled = False
            self.add_checker()
            self.page.update()