import { createSlice } from "@reduxjs/toolkit";
import type { Question } from "~/models";
import { createQuestion, deleteQuestion, getQuestions } from "./questions.thunks";

export interface QuestionsState {
    isLoading: boolean;
    errorMessage: string | undefined;
    questions: Question[];
}

const initialState: QuestionsState = {
    isLoading: false,
    errorMessage: "",
    questions: [],
};

const slice = createSlice({
    name: "questions",
    initialState,
    reducers: {
        reset(state) {
            Object.assign(state, initialState);
        },
        clearError(state) {
            state.errorMessage = "";
        },
    },
    extraReducers: (builder) => {
        builder
            .addCase(getQuestions.pending, (state) => {
                state.isLoading = true;
                state.errorMessage = "";
            })
            .addCase(getQuestions.fulfilled, (state, action) => {
                state.isLoading = false;
                state.questions = action.payload;
            })
            .addCase(getQuestions.rejected, (state, action) => {
                state.isLoading = false;
                state.errorMessage = action.error.message;
            })
            .addCase(createQuestion.pending, (state) => {
                state.isLoading = true;
                state.errorMessage = "";
            })
            .addCase(createQuestion.fulfilled, (state, action) => {
                state.isLoading = false;
                state.questions = action.payload;
            })
            .addCase(createQuestion.rejected, (state, action) => {
                state.isLoading = false;
                state.errorMessage = action.error.message;
            })
            .addCase(deleteQuestion.pending, (state) => {
                state.isLoading = true;
                state.errorMessage = "";
            })
            .addCase(deleteQuestion.fulfilled, (state, action) => {
                state.isLoading = false;
                state.questions = state.questions.filter(
                    (question) => question.id !== action.payload,
                );
            })
            .addCase(deleteQuestion.rejected, (state, action) => {
                state.isLoading = false;
                state.errorMessage = action.error.message;
            });
    },
});

export const questionsSlice = {
    ...slice,
    actions: {
        ...slice.actions,
        getQuestions,
        createQuestion,
        deleteQuestion,
    },
};
