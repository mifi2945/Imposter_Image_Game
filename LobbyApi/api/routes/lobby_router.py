from fastapi import APIRouter, HTTPException, status

from objects.lobby import Lobby, NewLobbyRequestBody, VoteRequestBody
from util.auth import AuthUser

router = APIRouter(tags=["lobbies"])


def not_implemented() -> None:
    raise HTTPException(
        status_code=status.HTTP_501_NOT_IMPLEMENTED,
        detail="Not implemented",
    )


@router.get(
    "/lobbies",
    response_model=list[Lobby],
    responses={401: {"description": "Unauthorized"}},
)
async def get_lobbies(user: AuthUser) -> list[Lobby]:
    not_implemented()


@router.get(
    "/lobbies/{lobby_id}",
    response_model=Lobby,
    responses={
        401: {"description": "Unauthorized"},
        404: {"description": "Lobby not found"},
    },
)
async def get_lobby(lobby_id: str, user: AuthUser) -> Lobby:
    not_implemented()


@router.post(
    "/lobbies/new",
    status_code=status.HTTP_201_CREATED,
    response_model=Lobby,
    responses={
        400: {"description": "Validation failed"},
        401: {"description": "Unauthorized"},
        501: {"description": "Not implemented"},
    },
)
async def create_lobby(body: NewLobbyRequestBody, user: AuthUser) -> Lobby:
    if (not user):
        raise HTTPException(status=status.HTTP_401_UNAUTHORIZED, detail="Not a valid user")
    # TODO enforce single lobby per user
    # TODO create lobby
    not_implemented()


@router.post(
    "/lobbies/start",
    responses={401: {"description": "Unauthorized"}, 501: {"description": "Not implemented"}},
)
async def start_lobby(user: AuthUser) -> None:
    # TODO user must be current owner of lobby
    # TODO start the game
    not_implemented()


@router.post(
    "/lobbies/{lobby_id}/join/",
    responses={401: {"description": "Unauthorized"}, 501: {"description": "Not implemented"}},
)
async def join_lobby(lobby_id: int, user: AuthUser) -> None:
    not_implemented()


@router.post(
    "/lobbies/{lobby_id}/start/",
    responses={401: {"description": "Unauthorized"}, 501: {"description": "Not implemented"}},
)
async def start_game(user: AuthUser) -> None:
    not_implemented()


@router.delete(
    "/lobbies/{lobby_id}/removePlayer/{username}",
    responses={401: {"description": "Unauthorized"}, 501: {"description": "Not implemented"}},
)
async def remove_player(lobby_id: int, username: str, authUser: AuthUser) -> None:
    not_implemented()


@router.post(
    "/lobbies/{lobby_id}/vote",
    responses={401: {"description": "Unauthorized"}, 501: {"description": "Not implemented"}},
)
async def vote(body: VoteRequestBody, authUser: AuthUser) -> None:

    not_implemented()
