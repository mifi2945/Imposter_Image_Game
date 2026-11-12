import { createSlice, PayloadAction } from "@reduxjs/toolkit";
import { Account, AccountRole } from "~/models";
import { getAccount, signIn, signUp } from "./auth.thunks";

// The redux store is a centralized place for all the data in our app.
// A slice is like one section of the redux store.
// it is usually a grouping of related data (called state)
// and then functions (called reducers) to update that data.

// This interface defines what data is stored in the slice.
export interface AuthState {
    isLoading: boolean;
    errorMessage: string | undefined;
    accessToken: string;
    refreshToken: string;
    account: Account;
}

// This constant is saying that when the slice is first created,
// what data should it have. Usually just empty stuff.
const initialState: AuthState = {
    isLoading: false,
    errorMessage: "",
    accessToken: "",
    refreshToken: "",
    account: {
        id: "",
        createdAt: new Date().toISOString(),
        username: "",
        role: AccountRole.User,
    },
};

const slice = createSlice({
    name: "auth",
    initialState,
    reducers: {
        reset(state) {
            Object.assign(state, initialState);
        },
        setTokens(state, action: PayloadAction<{ accessToken: string; refreshToken: string }>) {
            state.accessToken = action.payload.accessToken;
            state.refreshToken = action.payload.refreshToken;
        },
        clearError(state) {
            state.errorMessage = "";
        },
    },
    // extra reducers are ones that are defined in other files? i think
    // like for example the thunks in accounts.thunks.ts
    extraReducers: (builder) => {
        builder
            .addCase(signIn.pending, (state) => {
                state.isLoading = true;
            })
            .addCase(signIn.fulfilled, (state, action) => {
                const { accessToken, refreshToken, account } = action.payload;

                state.isLoading = false;
                state.accessToken = accessToken;
                state.refreshToken = refreshToken;
                state.account = account;

                state.errorMessage = "";
            })
            .addCase(signIn.rejected, (state, action) => {
                state.isLoading = false;
                state.errorMessage = action.error.message;
            })

            .addCase(signUp.pending, (state) => {
                state.isLoading = true;
            })
            .addCase(signUp.fulfilled, (state, action) => {
                const { accessToken, refreshToken, account } = action.payload;

                state.isLoading = false;
                state.accessToken = accessToken;
                state.refreshToken = refreshToken;
                state.account = account;

                state.errorMessage = "";
            })
            .addCase(signUp.rejected, (state, action) => {
                state.isLoading = false;
                state.errorMessage = action.error.message;
            })

            .addCase(getAccount.pending, (state) => {
                state.isLoading = true;
            })
            .addCase(getAccount.fulfilled, (state, action) => {
                const { account } = action.payload;

                state.isLoading = false;
                state.account = account;

                state.errorMessage = "";
            })
            .addCase(getAccount.rejected, (state, action) => {
                state.isLoading = false;
                state.errorMessage = action.error.message;
            });
    },
});

export const authSlice = {
    ...slice,
    actions: {
        ...slice.actions,
        signIn,
        signUp,
        getAccount,
    },
};
