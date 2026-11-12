import { createSlice } from "@reduxjs/toolkit";
import { Lobby } from "~/models/lobby.model";
import { getLobbies } from "./lobby.thunks";

export interface LobbyState {
    isLoading: boolean;
    errorMessage: string | undefined;
    lobbies: Lobby[];
}

const initialState: LobbyState = {
    isLoading: false,
    errorMessage: "",
    lobbies: [],
};

const slice = createSlice({
    name: "lobby",
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
            .addCase(getLobbies.pending, (state) => {
                state.isLoading = true;
                state.errorMessage = "";
            })
            .addCase(getLobbies.fulfilled, (state, action) => {
                state.isLoading = false;
                state.lobbies = action.payload;
            })
            .addCase(getLobbies.rejected, (state, action) => {
                state.isLoading = false;
                state.errorMessage = action.error.message;
            });
    },
});

export const lobbySlice = {
    ...slice,
    actions: {
        ...slice.actions,
        getLobbies,
    },
};
