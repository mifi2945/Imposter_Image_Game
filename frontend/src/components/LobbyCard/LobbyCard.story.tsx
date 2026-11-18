import type { Meta, StoryObj } from "@storybook/react";
import { AccountRole, type Lobby } from "~/models";
import { LobbyCard } from "./LobbyCard";

const lobby: Lobby = {
    name: "Friday Game Night",
    code: "FGN42",
    round: 2,
    accounts: [
        {
            createdAt: "2026-05-01T12:00:00.000Z",
            username: "player-one",
            role: AccountRole.User,
            points: 120,
        },
        {
            createdAt: "2026-05-02T12:00:00.000Z",
            username: "player-two",
            role: AccountRole.User,
            points: 95,
        },
    ],
};

const meta = {
    title: "Lobbies/LobbyCard",
    component: LobbyCard,
    args: { lobby },
} satisfies Meta<typeof LobbyCard>;

export default meta;
type Story = StoryObj<typeof meta>;

export const Default: Story = {};
