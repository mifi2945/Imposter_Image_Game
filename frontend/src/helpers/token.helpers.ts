import { jwtDecode } from "jwt-decode";

export function isTokenExpired(token: string) {
    const claims = jwtDecode(token);
    // claims.exp in seconds, Date.now() in millis, so multiply by 1000.
    return !claims.exp || claims.exp <= Date.now() * 1000;
}
