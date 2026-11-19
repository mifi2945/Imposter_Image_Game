import { createSlice, type PayloadAction } from "@reduxjs/toolkit";
import type { Question } from "~/models";

export type GamePhase =
    | "waiting"
    | "starting"
    | "question"
    | "answering"
    | "discussion"
    | "voting"
    | "reveal"
    | "finished";

export interface GamePlayer {
    username: string;
    score: number;
    hasAnswered: boolean;
    hasVoted: boolean;
}

export interface GameAnswer {
    username: string;
    answer: string;
}

export interface GameVoteTally {
    username: string;
    votes: number;
}

export interface GameState {
    phase: GamePhase;
    currentRound: number;
    totalRounds: number;
    players: GamePlayer[];
    currentQuestion: Question | null;
    answers: GameAnswer[];
    voteTallies: GameVoteTally[];
    impostorUsername: string | null;
    winners: string[];
}

const initialState: GameState = {
    phase: "waiting",
    currentRound: 0,
    totalRounds: 0,
    players: [],
    currentQuestion: null,
    answers: [],
    voteTallies: [],
    impostorUsername: null,
    winners: [],
};

const slice = createSlice({
    name: "game",
    initialState,
    reducers: {
        reset: () => initialState,
        setGameState: (_state, action: PayloadAction<GameState>) => action.payload,
        nextPhase: (state) => {
            switch (state.phase) {
                case "waiting":
                    state.phase = "starting";
                    break;
                case "starting":
                    state.phase = "question";
                    state.currentRound = Math.max(state.currentRound, 1);
                    state.totalRounds = Math.max(state.totalRounds, 1);
                    break;
                case "question":
                    state.phase = "answering";
                    break;
                case "answering":
                    state.phase = "discussion";
                    break;
                case "discussion":
                    state.phase = "voting";
                    break;
                case "voting":
                    state.phase = "reveal";
                    break;
                case "reveal":
                    if (state.currentRound < state.totalRounds) {
                        state.currentRound += 1;
                        state.phase = "question";
                    } else {
                        state.phase = "finished";
                    }
                    break;
                case "finished":
                    break;
            }
        },
    },
});

export const gameSlice = slice;
