from datetime import datetime, timezone
from typing import Dict, List
from uuid import uuid4

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

class PaginatedEquipmentView(View):
    def __init__(self, equipments: List[EquipmentResponse], per_page: int = 5):
        super().__init__(timeout=None)  # Timeout None = nunca expira
        self.equipments = equipments
        self.per_page = per_page
        self.page = 0

        # Botões
        self.prev_button = Button(label="⬅️ Anterior", style=ButtonStyle.secondary)
        self.next_button = Button(label="Próximo ➡️", style=ButtonStyle.secondary)
        self.prev_button.callback = self.prev_page
        self.next_button.callback = self.next_page
        self.add_item(self.prev_button)
        self.add_item(self.next_button)

        self.update_buttons()

    def update_buttons(self):
        self.prev_button.disabled = self.page == 0
        self.next_button.disabled = (self.page + 1) * self.per_page >= len(self.equipments)

    def get_page_embed(self) -> Embed:
        start = self.page * self.per_page
        end = start + self.per_page
        page_items = self.equipments[start:end]

        embed = Embed(title="Equipamentos Disponíveis", color=0x00ff00)
        for eq in page_items:
            embed.add_field(
                name=f"{eq.name} [{eq.status}]",
                value=f"{eq.description}\nCriado em: {eq.created_at.strftime('%d/%m/%Y %H:%M')}",
                inline=False
            )
        embed.set_footer(text=f"Página {self.page + 1}/{(len(self.equipments) - 1)//self.per_page + 1}")
        return embed

    async def prev_page(self, interaction):
        if self.page > 0:
            self.page -= 1
            self.update_buttons()
            await interaction.response.edit_message(embed=self.get_page_embed(), view=self)

    async def next_page(self, interaction):
        if (self.page + 1) * self.per_page < len(self.equipments):
            self.page += 1
            self.update_buttons()
            await interaction.response.edit_message(embed=self.get_page_embed(), view=self)


class EquipmentManager(Cog):
    config: BotConfig
    user_states: Dict[int, UserReservationState]

    def __init__(self, bot, user_service, reservation_service, equipment_service):
        self.reservation_service: ReservationService = reservation_service        
        self.equipment_service: EquipmentService = equipment_service        
        self.user_service: UserService = user_service        
        self.user_states = {}
        self.bot: Bot = bot
    
    @command(name="equipamentos")
    async def show_equipment(self, ctx: Context):
        equipments = await self.equipment_service.get_equipments()
        if not equipments:
            await ctx.send("Nenhum equipamento encontrado.")
            return

        view = PaginatedEquipmentView(equipments, per_page=5)
        await ctx.send(embed=view.get_page_embed(), view=view)
        
    @command(name="criar_equipamento")
    async def create_equipment(self, ctx: Context, name: str, description: str, status: str = "available"):
        try:
            equipment = EquipmentResponse(
                id=uuid4(),
                name=name,
                description=description,
                status=status,
                created_at=datetime.now(tz=timezone.utc),
                updated_at=datetime.now(tz=timezone.utc),
                deleted_at=None
            )

            await self.equipment_service.create_equipment(equipment)

            embed = Embed(
                title="✅ Equipamento Criado",
                description=f"**Nome:** {equipment.name}\n**Descrição:** {equipment.description}\n**Status:** {equipment.status}",
                color=Color.green()
            )
            await ctx.send(embed=embed)

        except Exception as e:
            await ctx.send(f"❌ Erro ao criar equipamento: {e}")