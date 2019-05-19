from discord.ext.commands import check

owner_id = 132694825454665728


def is_owner():
    return check(lambda ctx: ctx.author.id == owner_id)


def has_perm(perm):
    def inner(ctx):
        return getattr(ctx.author.guild_permissions, perm)
    return check(inner)
