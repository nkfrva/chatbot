from shared.role import Role


class BaseCommands:

    def register(username: str) -> Role:
        # query
        return Role.Member

    def get_role(username: str) -> Role:
        # query
        return Role.Member
