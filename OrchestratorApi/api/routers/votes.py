from fastapi import APIRouter, HTTPException, status

router = APIRouter(prefix="/votes", tags=["Votes"])


@router.post("", status_code=status.HTTP_501_NOT_IMPLEMENTED)
async def submit_vote():
    """TODO: Record a player's vote for the impostor."""
    raise HTTPException(
        status_code=status.HTTP_501_NOT_IMPLEMENTED,
        detail="Voting is not implemented yet.",
    )
