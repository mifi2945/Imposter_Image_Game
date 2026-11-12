from fastapi import APIRouter, HTTPException, status
from objects.question import Question, RoundQuestion
from pydantic import BaseModel

class ErrorMessage(BaseModel):
    detail: str

router = APIRouter(
    prefix="/questions",
    tags=["questions"],
    responses={404: {"description": "Not found"}},
)

@router.post("/", 
    responses={
        201: {"description": "Question created successfully"},
        400: {"model": ErrorMessage, "description": "Invalid request body or failed validation"},
        401: {"model": ErrorMessage, "description": "Unauthorized"},
        403: {"model": ErrorMessage, "description": "Operation forbidden"}})
async def create_question(question: Question):
    """
    Create a new question.
    """
    # TODO
    raise HTTPException(status_code=400, detail="Invalid request body or failed validation")
    return {"message": "Question created successfully", "question": question}


@router.get("/", 
            response_model=list[Question],
            responses={200: {"description": "Questions retrieved successfully"},
                       401: {"model": ErrorMessage, "description": "Unauthorized"},
                       403: {"model": ErrorMessage, "description": "Operation forbidden"}})
async def get_questions():
    """
    Get all questions.
    """
    # TODO
    return []


@router.delete("/{question_id}", 
               response_code=status.HTTP_204_NO_CONTENT,
               responses={
                       401: {"model": ErrorMessage, "description": "Unauthorized"},
                       403: {"model": ErrorMessage, "description": "Operation forbidden"},
                       404: {"model": ErrorMessage, "description": "Question not found"}})
async def delete_question(question_id: int):
    """
    Delete a question by ID.
    """
    # TODO
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Question with ID {question_id} not found")
    return {"message": f"Question with ID {question_id} deleted successfully"}


@router.get("/round",
            response_model=RoundQuestion,
            responses={201: {"description": "Successful Response"},
                       401: {"model": ErrorMessage, "description": "Unauthorized"},
                       418: {"model": ErrorMessage, "description": "I'm a teapot"}})
async def get_question_for_round():
    """
    Gets questions for a round.
    """
    # Gives 1 question for non impostor
    # Gives 1 question for impostor
    # Body: category (string)
    # TODO
    raise HTTPException(status_code=status.HTTP_418_IM_A_TEAPOT, detail="I'm a teapot")
    return RoundQuestion()