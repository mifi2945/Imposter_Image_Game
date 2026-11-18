// API hub. This file contains helper functions which will make calling our api easier.
import { tokenHelpers } from "~/helpers";
import { type State, type Store } from "~/redux";
import { TokenRequest, TokenResponse } from "./auth.hub";

const apiBaseUrl = "TODO";

class HttpError extends Error {
    public readonly status: number;

    constructor(status: number, message: string) {
        super(message);
        this.name = "HttpError";
        this.status = status;
    }
}

export type HttpMethod = "GET" | "PUT" | "POST" | "PATCH" | "DELETE";
export type AuthorizationOption = "Bearer" | "None";

export interface RequestOptions {
    baseUrl?: string;
    endpoint: string;
    method?: HttpMethod;
    authorization?: AuthorizationOption;
    body?: object | string;
}

let lateBoundStore: Store | null;

export function bindStore(store: Store) {
    lateBoundStore = store;
}

function getStore() {
    if (lateBoundStore == null) {
        throw new Error("Redux store hasn't been bound yet.");
    }

    return lateBoundStore;
}

async function getRefreshedTokens(refreshToken: string) {
    // unfortunately we have to call this manually with fetch
    // to avoid circular dependency
    const response = await fetch(`${apiBaseUrl}/auth/token`, {
        method: "POST",
        body: JSON.stringify({
            refreshToken,
        } as TokenRequest),
    });

    if (!response.ok) {
        throw new HttpError(response.status, `Failed to refresh tokens: ${await response.text()}`);
        // Note: if this fails, that means the refresh token is expired.
        // The user should be brought to the sign in page since they have
        // to sign in again to get a new token.
    }

    return (await response.json()) as TokenResponse;
}

function buildHeaders(accessToken: string) {
    return {
        "Conent-Type": "application/json",
        ...(accessToken && { Authorization: `Bearer ${accessToken}` }),
    };
}

function buildBody(body: object | string | undefined) {
    switch (typeof body) {
        case "undefined":
            return undefined;
        case "string":
            return body;
        case "object":
            return JSON.stringify(body);
    }
}

export async function executeRequest(request: RequestOptions) {
    const {
        baseUrl = apiBaseUrl,
        endpoint,
        method = "GET",
        authorization = "Bearer",
        body,
    } = request;
    const url = `${baseUrl}${endpoint}`;

    let accessToken = "";
    let refreshToken = "";

    if (authorization == "Bearer") {
        const state = getStore().getState() as State;
        accessToken = state.auth.accessToken;
        refreshToken = state.auth.refreshToken;

        if (tokenHelpers.isTokenExpired(accessToken)) {
            const newTokens = await getRefreshedTokens(refreshToken);
            accessToken = newTokens.accessToken;
            refreshToken = newTokens.refreshToken;

            getStore().dispatch({
                type: "auth/setTokens",
                payload: { accessToken, refreshToken },
            });
        }
    }

    const response = await fetch(url, {
        method,
        headers: buildHeaders(accessToken),
        body: buildBody(body),
    });

    if (!response.ok) {
        throw new HttpError(response.status, await response.text());
    }

    return response;
}

export async function send<T>(request: RequestOptions) {
    const response = await executeRequest(request);
    return (await response.json()) as T;
}

export async function fallback<T>(request: RequestOptions, defaultValue: T) {
    try {
        const response = await executeRequest(request);
        return (await response.json()) as T;
    } catch {
        return defaultValue;
    }
}
