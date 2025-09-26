from datetime import datetime
from typing import Dict, List

from loguru import logger

from discord import ButtonStyle, Color, Embed, Forbidden, utils
from discord.ext.commands import Bot, Cog, command, Context
from discord.ui import Button, View

from models.equipment import EquipmentResponse
from models.reservation import BotConfig, ReservationPayload, UserReservationState
from models.user import UserPayload, UserResponse

from services.equipment_service import EquipmentService
from services.reservation_service import ReservationService
from services.user_service import UserService
from utils.datetime_utils import (
    generate_next_days,
    generate_possible_end_times,
    generate_time_slots,
    get_available_time_slots,
)
from views.buttons import DateButton, EquipmentButton, TimeButton



class EquipmentManager(Cog):
    config: BotConfig
    user_states: Dict[int, UserReservationState]

    def __init__(self, bot, user_service, reservation_service, equipment_service):
        self.reservation_service: ReservationService = reservation_service        
        self.equipment_service: EquipmentService = equipment_service        
        self.user_service: UserService = user_service        
        self.user_states = {}
        self.bot: Bot = bot
    
    @command(name='equipments')
    async def show_equipment(self, ctx: Context):
        pass