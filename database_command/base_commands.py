from shared.role import Role


class BaseCommands:

    async def register(self, username: str) -> Role:
        # query
        return Role.Member

    async def get_role(self, username: str) -> Role:
        # query
        return Role.Member

    async def get_all_user_ids(self):
        return [726067906, 798162397]
