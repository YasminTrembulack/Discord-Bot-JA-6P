from loguru import logger
from datetime import datetime, timedelta
from discord import Embed, ButtonStyle, Color, utils
from discord.ui import Button, View
from discord.ext.commands import Cog, command


class Calendar(Cog):
    """Cog to handle reservation calendar and booking logic"""

    def __init__(self, bot):
        self.bot = bot
        # Store reservations in memory (later replace with a DB)
        # Format: { "DD/MM/YYYY": { "08:00": user_id, ... } }
        self.reservations = {}

    # ---------------- Command to open calendar ----------------
    @command(name='calendario')
    async def calendar(self, ctx):
        """Shows the next 7 days for the user to pick a date"""
        
        # ✅ Só permite no canal "reservations"
        if ctx.channel.name != "📅reservations":
            await ctx.send("⚠️ Este comando só pode ser usado no canal 'reservations'.", delete_after=10)
            return
    
        embed = Embed(
            title="📅 Calendário de Reservas",
            description="Escolha um dia para fazer uma reserva",
            color=Color.blue())

        buttons = View()
        # ____________________________________________________________________
        today = datetime.today()
        next_days = [today + timedelta(days=i) for i in range(7)]
        
        available_times = self.bot.api_client.get_available_times(days=next_days)
        logger.warning(next_days)
        # ____________________________________________________________________
        
        for i in range(7): # Next 7 days
            day = today + timedelta(days=i)
            date_str = day.strftime("%d/%m/%Y")

            button = Button(label=date_str, style=ButtonStyle.green)

            async def callback(interaction, date=date_str):
                await self.show_times(interaction, date)

            button.callback = callback
            buttons.add_item(button)

        await ctx.send(embed=embed, view=buttons)

    # ---------------- Show times for a selected day ----------------
    async def show_times(self, interaction, date):
        embed = Embed(
            title=f"⏰ Escolha o horário de início em {date}",
            description="Depois escolha o horário de término",
            color=Color.green())

        buttons = View()

        for hour in range(8, 21):
            time_slot = f"{hour:02d}:00"

            # Already reserved -> red button disabled
            if date in self.reservations and time_slot in self.reservations[date]:
                button = Button(label=time_slot, style=ButtonStyle.red, disabled=True)
            else:
                button = Button(label=time_slot, style=ButtonStyle.blurple)

                async def callback(interaction, h=time_slot, d=date):
                    await self.choose_end(interaction, d, h)

                button.callback = callback

            buttons.add_item(button)

        await interaction.response.send_message(embed=embed, view=buttons, ephemeral=True)

    # ---------------- Choose ending time ----------------
    async def choose_end(self, interaction, date, start_time):
        embed = Embed(
            title=f"📌 Reserva em {date}",
            description=f"Início: {start_time}\nAgora escolha o horário de término:",
            color=Color.purple())

        buttons = View()
        start_hour = int(start_time.split(":")[0])

        for hour in range(start_hour + 1, 22):
            end_time = f"{hour:02d}:00"
            conflict = any(f"{h:02d}:00" in self.reservations.get(date, {}) for h in range(start_hour, hour))

            if conflict:
                button = Button( label=end_time, style=ButtonStyle.red, isabled=True)
            else:
                button = Button(label=end_time, style=ButtonStyle.green)

                async def callback(interaction, d=date, i=start_time, f=end_time):
                    await self.reserve_slot(interaction, d, i, f)

                button.callback = callback

            buttons.add_item(button)

        await interaction.response.send_message(embed=embed, view=buttons, ephemeral=True)

    # ---------------- Reserve the slot ----------------
    async def reserve_slot(self, interaction, date, start_time, end_time):
        start_hour = int(start_time.split(":")[0])
        end_hour = int(end_time.split(":")[0])

        if date not in self.reservations:
            self.reservations[date] = {}

        conflicts = [
            f"{h:02d}:00" for h in range(start_hour, end_hour)
            if f"{h:02d}:00" in self.reservations[date]
        ]
        if conflicts:
            await interaction.response.send_message(
                f"❌ Já existem reservas às {', '.join(conflicts)} em {date}.",
                ephemeral=True)
            return

        logger.info(f"⏰ Reserva realizada por {interaction.user.name} ({interaction.user.id}) em {date} das {start_time} até {end_time}")

        # 🔹 Não salvar ainda como confirmada, apenas marcar como pendente
        self.reservations[date][f"{start_hour:02d}:00-{end_hour:02d}:00"] = {
            "user_id": interaction.user.id,
            "status": "pending"
        }

        # Mensagem para o usuário
        await interaction.response.send_message(
            "📨 Sua reserva foi enviada para aprovação de um responsável.\n"
            "Você receberá uma mensagem assim que for **aprovada ou rejeitada**.",
            ephemeral=True
        )

        # Envia para canal de aprovação
        await self.send_for_approval(interaction.user, date, start_time, end_time)

    # ---------------- Send reservation to approval channel ----------------
    async def send_for_approval(self, user, date, start_time, end_time):
        start_hour = int(start_time.split(":")[0])
        end_hour = int(end_time.split(":")[0])
        channel = utils.get(self.bot.get_all_channels(), name="📝pending-approval")  

        if not channel:
            logger.error("❌ Canal 'pending-approval' não encontrado.")
            return

        embed = Embed(
            title="📝 Nova reserva pendente",
            description=f"**Usuário:** {user.mention}\n"
                        f"**Data:** {date}\n"
                        f"**Início:** {start_time}\n"
                        f"**Fim:** {end_time}",
            color=Color.orange()
        )

        view = View()

        approve_btn = Button(label="Aprovar ✅", style=ButtonStyle.green)
        reject_btn = Button(label="Recusar ❌", style=ButtonStyle.red)

        async def approve_callback(interaction):
            role = utils.get(interaction.guild.roles, name="Teacher")
            if role not in interaction.user.roles:
                await interaction.response.send_message("⚠️ Você não tem permissão para aprovar reservas.", ephemeral=True)
                return
            
            self.reservations[date][f"{start_hour:02d}:00-{end_hour:02d}:00"]["status"] ="aproved"

            await user.send(f"🎉 Sua reserva em **{date}** das **{start_time}** às **{end_time}** foi **APROVADA**!")
            await channel.send(f"✅ Reserva de {user.mention} aprovada por {interaction.user.mention}")

        async def reject_callback(interaction):
            role = utils.get(interaction.guild.roles, name="Teacher")
            if role not in interaction.user.roles:
                await interaction.response.send_message("⚠️ Você não tem permissão para recusar reservas.", ephemeral=True)
                return

            self.reservations[date][f"{start_hour:02d}:00-{end_hour:02d}:00"]["status"] = "rejected"
    

            await user.send(f"🚫 Sua reserva em **{date}** das **{start_time}** às **{end_time}** foi **RECUSADA**.")
            await channel.send(f"❌ Reserva de {user.mention} recusada por {interaction.user.mention}")

        approve_btn.callback = approve_callback
        reject_btn.callback = reject_callback

        view.add_item(approve_btn)
        view.add_item(reject_btn)

        await channel.send(embed=embed, view=view)


# ---------------- Setup function to load the Cog ----------------
async def setup(bot):
    await bot.add_cog(Calendar(bot))
