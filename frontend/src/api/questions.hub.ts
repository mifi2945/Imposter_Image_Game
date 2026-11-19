import { executeRequest, send } from "./hub";
import { getServiceUrls } from "./service-urls";
import type { Question } from "~/models";

export interface CreateQuestionRequest {
    category: string;
    question: string;
}

export async function getQuestions() {
    return send<Question[]>({
        baseUrl: getServiceUrls().questions,
        endpoint: "/questions/",
    });
}

export async function createQuestion(request: CreateQuestionRequest) {
    await executeRequest({
        baseUrl: getServiceUrls().questions,
        endpoint: "/questions/",
        method: "POST",
        body: request,
    });
}

export async function deleteQuestion(id: number) {
    await executeRequest({
        baseUrl: getServiceUrls().questions,
        endpoint: `/questions/${id}`,
        method: "DELETE",
    });
}
