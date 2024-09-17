from shared.role import Role
from repository.member_repository import MemberRepository
from repository.team_repository import TeamRepository

class BaseCommands:

    async def register(self, username: str) -> Role:
        # query
        return Role.Member

    async def get_role(self, username: str) -> Role:
        # query
        return Role.Member

    async def get_all_user_ids(self):
        member_repository = MemberRepository()


        return [726067906, 798162397, 588035306]
