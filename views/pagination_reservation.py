from typing import List

from discord import ButtonStyle, Embed
from discord.ui import Button, View

from models.reservation import ReservationPayload


class PaginatedReservationView(View):
    def __init__(self, reservations: List[ReservationPayload], per_page: int = 5):
        super().__init__(timeout=None)
        self.reservations = reservations
        self.per_page = per_page
        self.page = 0

        self.prev_button = Button(label="⬅️", style=ButtonStyle.secondary)
        self.next_button = Button(label="➡️", style=ButtonStyle.secondary)

        self.prev_button.callback = self.prev_page
        self.next_button.callback = self.next_page

        self.update_buttons()
        self.add_item(self.prev_button)
        self.add_item(self.next_button)

    def update_buttons(self):
        self.prev_button.disabled = self.page == 0
        self.next_button.disabled = (self.page + 1) * self.per_page >= len(self.reservations)

    async def prev_page(self, interaction):
        self.page -= 1
        self.update_buttons()
        await interaction.response.edit_message(embed=self.get_page_embed(), view=self)

    async def next_page(self, interaction):
        self.page += 1
        self.update_buttons()
        await interaction.response.edit_message(embed=self.get_page_embed(), view=self)

    def get_page_embed(self) -> Embed:
        embed = Embed(title=f"Reservas - Página {self.page + 1}")
        start_index = self.page * self.per_page
        end_index = start_index + self.per_page
        for res in self.reservations[start_index:end_index]:
            embed.add_field(
                name=f"Reserva {res.user_id}",
                value=(
                    f"**Equipamento ID:** {res.equipment_id}\n"
                    f"**Responsável:** {res.responsible_id or 'Nenhum'}\n"
                    f"**Início:** {res.start.strftime('%d/%m/%Y %H:%M')}\n"
                    f"**Fim:** {res.end.strftime('%d/%m/%Y %H:%M')}\n"
                    f"**Status:** {res.status}"
                ),
                inline=False
            )
        return embed
