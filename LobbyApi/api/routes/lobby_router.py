from fastapi import APIRouter, HTTPException, status

from objects.lobby import (
    JoinLobbyRequestBody,
    Lobby,
    NewLobbyRequestBody,
    VoteRequestBody,
)

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
async def get_lobbies() -> list[Lobby]:
    not_implemented()


@router.get(
    "/lobbies/{lobby_id}",
    response_model=Lobby,
    responses={
        401: {"description": "Unauthorized"},
        404: {"description": "Lobby not found"},
    },
)
async def get_lobby(lobby_id: str) -> Lobby:
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
async def create_lobby(body: NewLobbyRequestBody) -> Lobby:
    not_implemented()


@router.post(
    "/lobbies/start",
    responses={401: {"description": "Unauthorized"}, 501: {"description": "Not implemented"}},
)
async def start_lobby() -> None:
    not_implemented()


@router.post(
    "/lobbies/join/ws",
    responses={401: {"description": "Unauthorized"}, 501: {"description": "Not implemented"}},
)
async def join_lobby(body: JoinLobbyRequestBody) -> None:
    not_implemented()


@router.post(
    "/game/startGame",
    responses={401: {"description": "Unauthorized"}, 501: {"description": "Not implemented"}},
)
async def start_game() -> None:
    not_implemented()


@router.delete(
    "/game/removePlayer/{game_id}/{username}",
    responses={401: {"description": "Unauthorized"}, 501: {"description": "Not implemented"}},
)
async def remove_player(game_id: int, username: str) -> None:
    not_implemented()


@router.post(
    "/votes",
    responses={401: {"description": "Unauthorized"}, 501: {"description": "Not implemented"}},
)
async def vote(body: VoteRequestBody) -> None:
    not_implemented()
