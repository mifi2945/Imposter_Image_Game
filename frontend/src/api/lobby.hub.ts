import { Lobby } from "~/models";
import { executeRequest, send } from "./hub";

export interface NewLobbyRequestBody {
	creatorUserId: number;
	lobbyName: string;
}

export async function getLobbies() {
	return send<Lobby[]>({
		endpoint: "/lobbies",
	});
}

export async function getLobby(id: string) {
	return send<Lobby>({
		endpoint: `/lobbies/${encodeURIComponent(id)}`,
	});
}

export async function createLobby(body: NewLobbyRequestBody) {
	return send<Lobby>({
		endpoint: "/lobbies/new",
		method: "POST",
		body,
	});
}

export async function startGame() {
	await executeRequest({
		endpoint: "/game/startGame",
		method: "POST",
	});
}
