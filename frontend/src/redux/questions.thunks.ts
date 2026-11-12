import { createAsyncThunk } from "@reduxjs/toolkit";
import { questionsHub } from "~/api";
import type { Question } from "~/models";
import type { State } from "./store";

export const getQuestions = createAsyncThunk(
    "questions/getAll",
    async () => questionsHub.getQuestions(),
    {
        condition: (_, { getState }) => {
            const { questions } = getState() as State;
            return !questions.isLoading;
        },
    },
);

export const createQuestion = createAsyncThunk(
    "questions/create",
    async (request: Omit<Question, "id">) => {
        await questionsHub.createQuestion(request);
        return questionsHub.getQuestions();
    },
);

export const deleteQuestion = createAsyncThunk("questions/delete", async (id: number) => {
    await questionsHub.deleteQuestion(id);
    return id;
});
