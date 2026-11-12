import { createAsyncThunk } from "@reduxjs/toolkit";
import { lobbyHub } from "~/api";
import type { State } from "./store";

export const getLobbies = createAsyncThunk("lobby/getLobbies", async () => lobbyHub.getLobbies(), {
    condition: (_, { getState }) => {
        const { lobby } = getState() as State;
        return !lobby.isLoading;
    },
});
