import { useEffect } from "react";
import { Alert, Container, Stack, Text, Title } from "@mantine/core";
import { useActions, useAppSelector } from "~/hooks";
import { lobbySlice } from "~/redux";
import { LobbyCard } from "~/components/LobbyCard/LobbyCard";

export function LobbiesPage() {
    const { getLobbies } = useActions(lobbySlice.actions);
    const { errorMessage, isLoading, lobbies } = useAppSelector((state) => state.lobby);

    useEffect(() => {
        getLobbies();
        const intervalId = window.setInterval(() => getLobbies(), 60_000);

        return () => window.clearInterval(intervalId);
    }, [getLobbies]);

    return (
        <Container component="main" size="md" py="xl">
            <Stack gap="lg">
                <Title order={1}>Lobbies</Title>

                {errorMessage && (
                    <Alert color="red" title="Unable to load lobbies">
                        {errorMessage}
                    </Alert>
                )}

                {isLoading && lobbies.length === 0 && <Text>Loading lobbies...</Text>}

                {!isLoading && !errorMessage && lobbies.length === 0 && (
                    <Text c="dimmed">There are no lobbies available right now.</Text>
                )}

                <Stack gap="md">
                    {lobbies.map((lobby) => (
                        <LobbyCard key={lobby.code} lobby={lobby} />
                    ))}
                </Stack>
            </Stack>
        </Container>
    );
}
