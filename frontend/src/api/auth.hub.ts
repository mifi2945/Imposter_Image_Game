import { send } from "./hub";
import { getServiceUrls } from "./service-urls";

interface AccountsTokenResponse {
    access_token: string;
    refresh_token: string;
}

export interface SignUpRequest {
    username: string;
    password: string;
}

export interface SignUpResponse {
    accessToken: string;
    refreshToken: string;
}

export async function signUp(request: SignUpRequest) {
    const response = await send<AccountsTokenResponse>({
        baseUrl: getServiceUrls().accounts,
        endpoint: "/sign_up",
        method: "POST",
        authorization: "None",
        body: request,
    });

    return {
        accessToken: response.access_token,
        refreshToken: response.refresh_token,
    };
}

export interface SignInRequest {
    username: string;
    password: string;
}

export interface SignInResponse {
    accessToken: string;
    refreshToken: string;
}

export async function signIn(request: SignInRequest) {
    const response = await send<AccountsTokenResponse>({
        baseUrl: getServiceUrls().accounts,
        endpoint: "/sign_in",
        method: "POST",
        authorization: "None",
        body: request,
    });

    return {
        accessToken: response.access_token,
        refreshToken: response.refresh_token,
    };
}

export interface TokenRequest {
    refreshToken: string;
}

export interface TokenResponse {
    accessToken: string;
    refreshToken: string;
}

export async function exchangeRefreshToken(request: TokenRequest) {
    return send<TokenResponse>({
        baseUrl: getServiceUrls().accounts,
        endpoint: "/auth/token",
        method: "POST",
        authorization: "None",
        body: request,
    });
}
