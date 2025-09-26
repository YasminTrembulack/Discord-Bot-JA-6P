from datetime import datetime
from typing import Dict, List

from loguru import logger

from discord import ButtonStyle, Color, Embed, Forbidden, utils
from discord.ext.commands import Bot, Cog, command
from discord.ui import Button, View

from models.equipment import EquipmentResponse
from models.reservation import ReservationConfig, ReservationPayload, UserReservationState
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



class ReservationManager(Cog):
    config: ReservationConfig
    user_states: Dict[int, UserReservationState]

    def __init__(self, bot, user_service, reservation_service, equipment_service):
        self.reservation_service: ReservationService = reservation_service        
        self.equipment_service: EquipmentService = equipment_service        
        self.user_service: UserService = user_service        
        self.user_states = {}
        self.bot: Bot = bot

    # ---------------- Command to open ReservationManager ----------------
    @command(name='reservar')
    async def show_equipment(self, ctx):
        self.config = await self.reservation_service.get_reservation_config()

        reservation_chanel = self.config.reservation_chanel
        if reservation_chanel and ctx.channel.name != reservation_chanel:
            await ctx.send(f"⚠️ Este comando só pode ser usado no canal '{reservation_chanel}'.", delete_after=10)
            return

        embed = Embed(
            title="⚙️ Equipamentos disponiveis",
            description="Escolha o equipamento que deseja reservar",
            color=Color.blue())

        view = View()
        equipments: List[EquipmentResponse] = await self.equipment_service.get_equipments()

        for equipment in equipments:
            async def on_click(interaction, e=equipment):
                user_id = interaction.user.id
                if user_id not in self.user_states:
                    self.user_states[user_id] = UserReservationState()

                state = self.user_states[user_id]
                async with state.lock:
                    state.equipment_name = e.name
                    state.equipment_id = e.id

                await self.show_available_dates(interaction)

            view.add_item(EquipmentButton(equipment, on_click))

        await ctx.send(embed=embed, view=view)

    # ---------------- Show calendar ----------------
    async def show_available_dates(self, interaction):
        state = self.user_states[interaction.user.id]
            
        view = View()
        embed = Embed(
            title=f"📅 Dias disponiveis para {state.equipment_name}",
            description="Escolha um dia para fazer uma reserva",
            color=Color.blue()
        )

        next_days = generate_next_days(
            holidays={h.date() for h in set(self.config.holidays)},
            allowed_weekdays=set(self.config.days_of_week),
            max_days=self.config.max_reservation_days,
            start=datetime.today(),
        )

        unavailable_time_slots_by_date = (
            await self.reservation_service.fetch_unavailable_slots(next_days, state.equipment_id))

        for date_str in next_days:
            unavailable_time_slots = unavailable_time_slots_by_date.get(date_str, [])

            available_time_slots = get_available_time_slots(
                start_time=datetime.strptime(self.config.start_time.strftime("%H:%M"), "%H:%M"),
                end_time=datetime.strptime(self.config.end_time.strftime("%H:%M"), "%H:%M"),
                interval=self.config.min_reservation,
                unavailable_time_slots=unavailable_time_slots,)

            async def on_click(interaction, d=date_str, u=unavailable_time_slots):
                state = self.user_states[interaction.user.id]
                async with state.lock:
                    state.unavailable_time_slots = u
                    state.date = d
                await self.show_available_times(interaction)

            view.add_item(DateButton(date_str, available_time_slots, on_click))

        await interaction.response.send_message(embed=embed, view=view, ephemeral=True)

    # ---------------- Show times ----------------
    async def show_available_times(self, interaction):
        state = self.user_states[interaction.user.id]

        embed = Embed(
            title=f"⏰ Escolha o horário de início em {state.date}",
            description="Depois escolha o horário de término",
            color=Color.green()
        )
        view = View()

        time_slots = generate_time_slots(
            start_time=datetime.strptime(self.config.start_time.strftime("%H:%M"), "%H:%M"),
            end_time=datetime.strptime(self.config.end_time.strftime("%H:%M"), "%H:%M"),
            interval=self.config.min_reservation,)

        for time_str in time_slots:
            available = time_str not in state.unavailable_time_slots
    
            async def on_click(interaction, t=time_str):
                state = self.user_states[interaction.user.id]
                async with state.lock:
                    state.start_time = t
                await self.show_end_time_options(interaction)

            view.add_item(TimeButton(time_str, available, on_click))

        await interaction.response.send_message(embed=embed, view=view, ephemeral=True)

    # ---------------- Choose end time ----------------
    async def show_end_time_options(self, interaction):
        state = self.user_states[interaction.user.id]

        embed = Embed(
            title=f"📌 Reserva em {state.date}",
            description=f"Início: {state.start_time}\nAgora escolha o horário de término:",
            color=Color.purple()
        )
        view = View()

        possible_ends = generate_possible_end_times(
            end_time=datetime.strptime(self.config.end_time.strftime("%H:%M"), "%H:%M"),
            current=datetime.strptime(state.start_time, "%H:%M"),
            blocks=self.config.max_reservation_blocks,
            unavailable_time_slots=state.unavailable_time_slots,
            interval=self.config.min_reservation,)

        for t_end in possible_ends:
            async def on_click(interaction, h=t_end):
                state = self.user_states[interaction.user.id]
                async with state.lock:
                    state.end_time = h
                await self.reserve_slot(interaction)

            view.add_item(TimeButton(t_end, True, on_click))

        await interaction.response.send_message(embed=embed, view=view, ephemeral=True)

    # ---------------- Reserve slot ----------------
    async def reserve_slot(self, interaction):
        state = self.user_states[interaction.user.id]

        user: UserResponse = await self.user_service.get_user(UserPayload(
            member_id=str(interaction.user.id), 
            username=interaction.user.global_name))
        
        start_datetime = datetime.strptime(state.start_time, "%H:%M").time()
        end_datetime = datetime.strptime(state.end_time, "%H:%M").time()
        date = datetime.strptime(state.date, "%d/%m/%Y").date()

        reservation = await self.reservation_service.create_reservation(
            ReservationPayload(
                status="pending" if self.config.reservation_approval_chanel else "approved",
                start=datetime.combine(date, start_datetime),
                end=datetime.combine(date, end_datetime),
                equipment_id=state.equipment_id,
                user_id=user.id,))
    
        state.reservation = reservation

        if not self.config.reservation_approval_chanel:
            dm_sent = await self.send_user_dm(interaction.user,
                f"✅ Sua reserva no dia **{state.date}** das **{state.start_time}** até **{state.end_time}** foi confirmada!")

            msg = "✅ Reserva confirmada! (cheque sua DM 👀)" if dm_sent else \
                f"⚠️ {interaction.user.mention}, Não consegui enviar uma DM. Por favor, habilite as DMs."

            await interaction.response.send_message(msg, ephemeral=True)

            async with state.lock:
                del self.user_states[interaction.user.id]
        else:
            await interaction.response.send_message(
                "📨 Sua reserva foi enviada para aprovação de um responsável.\n"
                "Você receberá uma mensagem assim que for **aprovada ou rejeitada**.",
                ephemeral=True)

            await self.send_for_approval(interaction.user)

    # ---------------- Send reservation to approval ----------------
    async def send_for_approval(self, user):
        state = self.user_states[user.id]

        channel = utils.get(self.bot.get_all_channels(), name=self.config.reservation_approval_chanel)
        if not channel:
            logger.error(f"❌ Canal {self.config.reservation_approval_chanel} não encontrado.")
            return

        embed = Embed(
            title="📝 Nova reserva pendente",
            description=f"**Usuário:** {user.mention}\n**Data:** {state.date}\n**Início:** {state.start_time}\n**Fim:** {state.end_time}",
            color=Color.orange())

        view = View()

        async def handle_decision(interaction, status: str, emoji: str, user_msg: str, channel_msg: str):
            role = utils.get(interaction.guild.roles, name="Teacher")
            if role not in interaction.user.roles:
                await interaction.response.send_message("⚠️ Você não tem permissão para aprovar ou recusar reservas.", ephemeral=True)
                return

            responsible: UserResponse = await self.user_service.get_user(
                UserPayload(
                    mber_id=str(interaction.user.id), 
                    username=interaction.user.global_name))
            
            state.reservation.status = status
            state.reservation.responsible_id = responsible.id
            await self.reservation_service.update_reservation(state.reservation)
            async with state.lock:
                del self.user_states[user.id]

            dm_sent = await self.send_user_dm(user, user_msg)

            await channel.send(channel_msg.format(user=user.mention, approver=interaction.user.mention))
            
            response_msg = f"{emoji} Reserva processada! Uma DM foi enviada para o usuário." if dm_sent else \
                f"{emoji} Reserva processada! Não consegui enviar DM ao usuário."

            await interaction.response.send_message(response_msg, ephemeral=True)

        base_user_msg = f"Sua reserva em **{state.date}** das **{state.start_time}** às **{state.end_time}** foi"
        
        # Botão Aprovar 
        approve_btn = Button(label="Aprovar ✅", style=ButtonStyle.green) 
        async def approve_callback(interaction): 
            await handle_decision( 
                interaction, 
                status="approved",
                emoji="✅", 
                user_msg=f"🎉 {base_user_msg} **APROVADA**!", 
                channel_msg="✅ Reserva de {user} aprovada por {approver}" ) 
        approve_btn.callback = approve_callback 
        
        # Botão Recusar 
        reject_btn = Button(label="Recusar ❌", style=ButtonStyle.red) 
        async def reject_callback(interaction):
            await handle_decision(
                interaction,
                status="rejected",
                emoji="❌", 
                user_msg=f"🚫 {base_user_msg} **RECUSADA**.", 
                channel_msg="❌ Reserva de {user} aprovada por {approver}" ) 
        reject_btn.callback = reject_callback 
        
        view.add_item(approve_btn) 
        view.add_item(reject_btn)

        await channel.send(embed=embed, view=view)
        
    async def send_user_dm(self, user, message: str):
        try:
            await user.send(message)
            return True
        except Forbidden:
            return False


# ---------------- Setup function ----------------
async def setup(bot):
    await bot.add_cog(ReservationManager(bot))
