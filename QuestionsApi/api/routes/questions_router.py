from fastapi import APIRouter, HTTPException, status
from database import create_question as insert_question
from database import delete_question as remove_question
from database import get_questions as select_questions
from database import get_random_question as select_random_question
from database import get_random_category as select_random_category
from database import random_question as select_random_question
from objects.question import Question, QuestionCreate, RoundQuestion
from pydantic import BaseModel

class ErrorMessage(BaseModel):
    detail: str

router = APIRouter(
    prefix="/questions",
    tags=["questions"],
    responses={404: {"description": "Not found"}},
)

@router.post("/", 
    status_code=status.HTTP_201_CREATED,
    response_model=Question,
    responses={
        201: {"description": "Question created successfully"},
        400: {"model": ErrorMessage, "description": "Invalid request body or failed validation"},
        401: {"model": ErrorMessage, "description": "Unauthorized"},
        403: {"model": ErrorMessage, "description": "Operation forbidden"}})
async def create_question(question: QuestionCreate):
    """
    Create a new question.
    """
    return await insert_question(question.category, question.question)


@router.get("/",
            response_model=list[Question],
            responses={200: {"description": "Questions retrieved successfully"},
                       401: {"model": ErrorMessage, "description": "Unauthorized"},
                       403: {"model": ErrorMessage, "description": "Operation forbidden"}})
async def get_questions(category: str | None = None):
    """
    Get all questions.
    """
    return await select_questions(category)


@router.delete("/{question_id}", 
               status_code=status.HTTP_204_NO_CONTENT,
               responses={
                       401: {"model": ErrorMessage, "description": "Unauthorized"},
                       403: {"model": ErrorMessage, "description": "Operation forbidden"},
                       404: {"model": ErrorMessage, "description": "Question not found"}})
async def delete_question(question_id: int):
    """
    Delete a question by ID.
    """
    if not await remove_question(question_id):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Question with ID {question_id} not found",
        )


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
    category : str = await select_random_category()
    imposter_question : Question = await select_random_question(category)
    non_impostor_question : Question = imposter_question
    while non_impostor_question.id == imposter_question.id:
        non_impostor_question = await select_random_question(category)
    return RoundQuestion(imposter_question=imposter_question, non_impostor_question=non_impostor_question)