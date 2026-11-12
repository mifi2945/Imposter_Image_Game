import type { Question } from "~/models";
import { executeRequest, send } from "./hub";

export interface CreateQuestionRequest {
    category: string;
    question: string;
}

export async function getQuestions() {
    return send<Question[]>({
        endpoint: "/questions/",
    });
}

export async function createQuestion(request: CreateQuestionRequest) {
    await executeRequest({
        endpoint: "/questions/",
        method: "POST",
        body: request,
    });
}

export async function deleteQuestion(id: number) {
    await executeRequest({
        endpoint: `/questions/${id}`,
        method: "DELETE",
    });
}
