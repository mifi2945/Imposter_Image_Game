import { combineReducers, configureStore } from "@reduxjs/toolkit";
import { AuthState, authSlice } from "~/redux/auth.slice";

// Each time a new slice is added, you need to add the State here...
export interface State {
    auth: AuthState;
}

// and the reducers here.
export const rootReducer = combineReducers({
    [authSlice.name]: authSlice.reducer,
});

// this is so that we can access them all from the "state" variable.
export function createStore(preloadedState?: State) {
    return configureStore({
        reducer: rootReducer,
        preloadedState,
    });
}

export const store = createStore();

export type Store = ReturnType<typeof createStore>;
export type Dispatch = Store["dispatch"];

export interface AsyncActionOptions {
    getState: () => State; // this is how we get the state variable
    dispatch: Dispatch;
}
