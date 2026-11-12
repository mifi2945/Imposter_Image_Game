import { Card, Group, Text } from "@mantine/core";
import type { Lobby } from "~/models";

export interface LobbyCardProps {
    lobby: Lobby;
}

export function LobbyCard({ lobby }: LobbyCardProps) {
    return (
        <Card withBorder radius="md" padding="lg">
            <Group justify="space-between" align="flex-start">
                <div>
                    <Text fw={600} size="lg">
                        {lobby.name}
                    </Text>
                    <Text c="dimmed" size="sm">
                        Code: {lobby.code}
                    </Text>
                </div>
                <Text size="sm">Round {lobby.round}</Text>
            </Group>
            <Text size="sm" mt="md">
                {lobby.accounts.length} {lobby.accounts.length === 1 ? "player" : "players"}
            </Text>
        </Card>
    );
}
