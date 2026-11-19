from pydantic import BaseModel, ConfigDict, Field


class Lobby(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    name: str
    code: str
    user_ids: list[int] = Field(alias="userIds")
    round: int


class NewLobbyRequestBody(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    creator_user_id: int = Field(alias="creatorUserId")
    lobby_name: str = Field(alias="lobbyName")


class JoinLobbyRequestBody(BaseModel):
    username: str
    game_id: int | None = None


class VoteRequestBody(BaseModel):
    suspect_username: str
    username: str
