import { Account } from "~/models";
import { send } from "./hub";

export interface SignUpRequest {
    username: string;
    password: string;
}

export interface SignUpResponse {
    accessToken: string;
    refreshToken: string;
    account: Account;
}

export async function signUp(request: SignUpRequest) {
    return send<SignUpResponse>({
        endpoint: "/auth/signup",
        method: "POST",
        authorization: "None",
        body: request,
    });
}

export interface SignInRequest {
    username: string;
    password: string;
}

export interface SignInResponse {
    accessToken: string;
    refreshToken: string;
    account: Account;
}

export async function signIn(request: SignInRequest) {
    return send<SignInResponse>({
        endpoint: "/auth/signin",
        method: "POST",
        authorization: "None",
        body: request,
    });
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
        endpoint: "/auth/token",
        method: "POST",
        authorization: "None",
        body: request,
    });
}
