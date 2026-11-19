import { executeRequest, send } from "./hub";
import { getServiceUrls } from "./service-urls";
import { Lobby } from "~/models";

export interface NewLobbyRequestBody {
    creatorUserId: number;
    lobbyName: string;
}

export async function getLobbies() {
    return send<Lobby[]>({
        baseUrl: getServiceUrls().lobby,
        endpoint: "/lobbies",
    });
}

export async function getLobby(id: string) {
    return send<Lobby>({
        baseUrl: getServiceUrls().lobby,
        endpoint: `/lobbies/${encodeURIComponent(id)}`,
    });
}

export async function createLobby(body: NewLobbyRequestBody) {
    return send<Lobby>({
        baseUrl: getServiceUrls().lobby,
        endpoint: "/lobbies/new",
        method: "POST",
        body,
    });
}

export async function startGame() {
    await executeRequest({
        baseUrl: getServiceUrls().lobby,
        endpoint: "/game/startGame",
        method: "POST",
    });
}
