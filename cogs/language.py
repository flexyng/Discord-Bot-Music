import discord
from discord.ext import commands
from config import COLORS, SUPPORTED_LANGUAGES
from logger import log_command, log_error
import db
from i18n import translate, get_text

class Language(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.hybrid_command(name="language", description="Cambiar idioma / Change language / غير اللغة / Mudar idioma")
    async def language(self, ctx, lang_code: str = None):
        try:
            user_language = await db.get_user_language(ctx.author.id)
            
            if lang_code is None:
                available_langs = "\n".join([
                    f"• `{code}` - {name}"
                    for code, name in SUPPORTED_LANGUAGES.items()
                ])
                
                embed = discord.Embed(
                    title=get_text("language", user_language) if user_language in ["es", "en", "ar", "pt"] else "🌐 Idiomas",
                    description="Idiomas disponibles / Available languages / اللغات المتاحة / Idiomas disponíveis",
                    color=COLORS["primary"]
                )
                embed.add_field(name="Códigos", value=available_langs, inline=False)
                embed.add_field(name="Uso / Usage / الاستخدام / Uso", value="/language [código]", inline=False)
                embed.set_footer(text=get_text("footer_credit", "es"))
                return await ctx.send(embed=embed)
            
            if lang_code.lower() not in SUPPORTED_LANGUAGES:
                embed = discord.Embed(
                    title=get_text("error", user_language),
                    description=f"Idioma no válido. Usa: {', '.join(SUPPORTED_LANGUAGES.keys())}",
                    color=COLORS["error"]
                )
                embed.set_footer(text=get_text("footer_credit", user_language))
                return await ctx.send(embed=embed)
            
            lang_code = lang_code.lower()
            await db.set_user_language(ctx.author.id, lang_code)
            
            log_command(ctx.author, f"language {lang_code}", ctx.guild.name)
            
            lang_name = SUPPORTED_LANGUAGES[lang_code]
            
            embed = discord.Embed(
                title=get_text("language_changed", lang_code),
                description=f"{get_text('language_set', lang_code)} **{lang_name}**",
                color=COLORS["success"]
            )
            embed.set_footer(text=get_text("footer_credit", lang_code))
            await ctx.send(embed=embed)
            
        except Exception as e:
            log_error(str(e), "language")
            user_language = await db.get_user_language(ctx.author.id)
            embed = discord.Embed(
                title=get_text("error", user_language),
                description=str(e),
                color=COLORS["error"]
            )
            embed.set_footer(text=get_text("footer_credit", user_language))
            await ctx.send(embed=embed)

    @commands.hybrid_command(name="mylanguage", description="Ver tu idioma actual / Your current language / لغتك الحالية / Seu idioma atual")
    async def my_language(self, ctx):
        try:
            user_language = await db.get_user_language(ctx.author.id)
            lang_name = SUPPORTED_LANGUAGES.get(user_language, "Desconocido")
            
            embed = discord.Embed(
                title="🌐 Tu Idioma / Your Language / لغتك / Seu Idioma",
                description=f"**{lang_name}** (`{user_language}`)",
                color=COLORS["primary"]
            )
            embed.add_field(
                name="Cambiar / Change / تغيير / Mudar",
                value="/language [código]",
                inline=False
            )
            embed.set_footer(text=get_text("footer_credit", user_language))
            await ctx.send(embed=embed)
            
        except Exception as e:
            log_error(str(e), "my_language")
            embed = discord.Embed(
                title="❌ Error",
                description=str(e),
                color=COLORS["error"]
            )
            embed.set_footer(text="Hecho por flexyng | BSD-3-Clause License")
            await ctx.send(embed=embed)

    @commands.hybrid_command(name="languages", description="Lista todos los idiomas disponibles")
    async def languages_list(self, ctx):
        try:
            user_language = await db.get_user_language(ctx.author.id)
            
            embed = discord.Embed(
                title="🌐 Idiomas Disponibles",
                color=COLORS["primary"]
            )
            
            descriptions = {
                "es": "Español - Idioma por defecto",
                "en": "English - Default language for English speakers",
                "ar": "العربية - اللغة العربية",
                "pt": "Português - Linguagem padrão para falantes de português"
            }
            
            for code, name in SUPPORTED_LANGUAGES.items():
                desc = descriptions.get(code, "")
                embed.add_field(name=f"{code.upper()} - {name}", value=desc, inline=False)
            
            embed.add_field(
                name="💡 Cambiar tu idioma",
                value="Usa `/language [código]` para cambiar tu idioma",
                inline=False
            )
            embed.set_footer(text=get_text("footer_credit", user_language))
            
            await ctx.send(embed=embed)
            
        except Exception as e:
            log_error(str(e), "languages_list")
            embed = discord.Embed(
                title="❌ Error",
                description=str(e),
                color=COLORS["error"]
            )
            embed.set_footer(text="Hecho por flexyng | BSD-3-Clause License")
            await ctx.send(embed=embed)

async def setup(bot):
    await bot.add_cog(Language(bot))
