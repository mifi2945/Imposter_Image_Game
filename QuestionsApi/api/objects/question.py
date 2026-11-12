from pydantic import BaseModel

class QuestionCreate(BaseModel):
    category: str
    question: str

class Question(BaseModel):
    id: int
    category: str
    question: str

class RoundQuestion(BaseModel):
    imposter_question: Question
    non_impostor_question: Question