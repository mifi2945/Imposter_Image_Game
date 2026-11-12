import { createAsyncThunk } from "@reduxjs/toolkit";
import { accountsHub, authHub } from "~/api";
import { validationHelpers } from "~/helpers";
import type { State } from "./store";

export const signIn = createAsyncThunk(
    "auth/signIn",
    async (parameters: { email: string; password: string }) => {
        const { email, password } = parameters;

        validationHelpers.validateUsername(email);
        validationHelpers.validatePassword(password);

        return await authHub.signIn(parameters);
    },
    // this third argument is really weird syntax.
    // but basically what is says is if we are already loading
    // don't try to login again
    {
        condition: (_, { getState }) => {
            const {
                auth: { isLoading },
            } = getState() as State;
            if (isLoading) {
                return false;
            }
        },
    },
);

export const signUp = createAsyncThunk(
    "auth/signUp",
    async (parameters: { email: string; password: string }) => {
        const { email, password } = parameters;

        validationHelpers.validateUsername(email);
        validationHelpers.validatePassword(password);

        return await authHub.signUp(parameters);
    },
    {
        condition: (_, { getState }) => {
            const {
                auth: { isLoading },
            } = getState() as State;
            if (isLoading) {
                return false;
            }
        },
    },
);

export const getAccount = createAsyncThunk(
    "auth/getAccount",
    async () => {
        return await accountsHub.getAccount();
    },
    {
        condition: (_, { getState }) => {
            const {
                auth: { isLoading },
            } = getState() as State;
            if (isLoading) {
                return false;
            }
        },
    },
);
