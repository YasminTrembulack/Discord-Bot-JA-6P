from discord import ButtonStyle
from discord.ui import Button

class EquipmentButton(Button):
    def __init__(self, equipment, callback):
        style = ButtonStyle.gray if equipment.status == 'maintenance' else ButtonStyle.blurple
        super().__init__(label=equipment.name, style=style, disabled=equipment.status=='maintenance')
        self.callback = callback

class TimeButton(Button):
    def __init__(self, time_str, available: bool, callback):
        style = ButtonStyle.blurple if available else ButtonStyle.red
        super().__init__(label=time_str, style=style, disabled=not available)
        self.callback = callback

class DateButton(Button):
    def __init__(self, date_str, available_times: list, callback):
        style = ButtonStyle.green if available_times else ButtonStyle.red
        super().__init__(label=date_str, style=style, disabled=not available_times)
        self.callback = callback