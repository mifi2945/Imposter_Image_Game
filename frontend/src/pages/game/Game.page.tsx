import {
    Badge,
    Button,
    Card,
    Container,
    Grid,
    Group,
    Paper,
    Stack,
    Text,
    TextInput,
    Title,
} from "@mantine/core";
import { useActions, useAppSelector } from "~/hooks";
import { gameSlice, type GamePhase } from "~/redux";

const phaseLabels: Record<GamePhase, string> = {
    waiting: "Waiting for players",
    starting: "Starting",
    question: "Question",
    answering: "Answering",
    discussion: "Discussion",
    voting: "Voting",
    reveal: "Round results",
    finished: "Game over",
};

export function GamePage() {
    const game = useAppSelector((state) => state.game);
    const currentLobby = useAppSelector((state) => state.lobby.currentLobby);
    const { nextPhase } = useActions(gameSlice.actions);
    const hasRound = game.currentRound > 0;
    const isDiscussion = game.phase === "discussion";
    const isReveal = game.phase === "reveal";

    return (
        <Container component="main" size="xl" py="xl">
            <Grid gap="xl" align="start">
                <Grid.Col span={{ base: 12, md: 8 }}>
                    <Stack gap="xl">
                        {currentLobby && (
                            <Paper withBorder radius="md" p="md">
                                <Group justify="space-between" align="flex-start">
                                    <div>
                                        <Text size="sm" c="dimmed">
                                            Current lobby
                                        </Text>
                                        <Title order={3}>{currentLobby.name}</Title>
                                    </div>
                                    <Badge size="lg" variant="light">
                                        Code: {currentLobby.code}
                                    </Badge>
                                </Group>
                            </Paper>
                        )}
                        <Group justify="space-between" align="flex-start">
                            <div>
                                <Title order={1}>Game</Title>
                                {hasRound && (
                                    <Text c="dimmed" mt="xs">
                                        Round {game.currentRound} of {game.totalRounds}
                                    </Text>
                                )}
                            </div>
                            <Badge size="lg" variant="light">
                                {phaseLabels[game.phase]}
                            </Badge>
                        </Group>

                        {game.phase === "waiting" && (
                            <Text c="dimmed">Waiting for enough players to start the game.</Text>
                        )}
                        {game.phase === "starting" && <Text>The game is starting.</Text>}

                        {(game.phase === "question" || game.phase === "answering") && (
                            <Card withBorder radius="md" padding="lg">
                                <Stack gap="sm">
                                    <Title order={2}>Your question</Title>
                                    {game.currentQuestion ? (
                                        <>
                                            <Text size="sm" c="dimmed">
                                                {game.currentQuestion.category}
                                            </Text>
                                            <Text>{game.currentQuestion.question}</Text>
                                        </>
                                    ) : (
                                        <Text c="dimmed">
                                            The question has not been shared yet.
                                        </Text>
                                    )}
                                    {game.phase === "answering" && (
                                        <Text c="dimmed">Players are entering their answers.</Text>
                                    )}
                                </Stack>
                            </Card>
                        )}

                        {game.phase === "voting" && (
                            <Text c="dimmed">
                                {game.players.filter((player) => player.hasVoted).length} of{" "}
                                {game.players.length} players have voted.
                            </Text>
                        )}

                        {(isDiscussion || isReveal) && (
                            <Stack gap="sm">
                                <Title order={2}>Answers</Title>
                                {game.answers.length > 0 ? (
                                    game.answers.map((answer, index) => (
                                        <Card
                                            key={`${answer.username}-${index}`}
                                            withBorder
                                            radius="md"
                                        >
                                            <Group justify="space-between" align="flex-start">
                                                <Text>{answer.answer}</Text>
                                                <Text size="sm" c="dimmed">
                                                    {answer.username}
                                                </Text>
                                            </Group>
                                        </Card>
                                    ))
                                ) : (
                                    <Text c="dimmed">No answers are available yet.</Text>
                                )}
                            </Stack>
                        )}

                        {isReveal && (
                            <Stack gap="sm">
                                <Title order={2}>Round results</Title>
                                {game.impostorUsername && (
                                    <Text>
                                        Impostor: <strong>{game.impostorUsername}</strong>
                                    </Text>
                                )}
                                {game.voteTallies.map((tally) => (
                                    <Text key={tally.username}>
                                        {tally.username}: {tally.votes} votes
                                    </Text>
                                ))}
                            </Stack>
                        )}

                        {game.phase === "finished" && (
                            <Stack gap="xs">
                                <Title order={2}>Winners</Title>
                                {game.winners.length > 0 ? (
                                    <Text>{game.winners.join(", ")}</Text>
                                ) : (
                                    <Text c="dimmed">No winner has been reported.</Text>
                                )}
                            </Stack>
                        )}

                        <Stack gap="sm">
                            <Title order={2}>Players</Title>
                            {game.players.length > 0 ? (
                                game.players.map((player) => (
                                    <Card key={player.username} withBorder radius="md" padding="sm">
                                        <Group justify="space-between">
                                            <Text>{player.username}</Text>
                                            <Group gap="md">
                                                <Text size="sm" c="dimmed">
                                                    {player.score} points
                                                </Text>
                                                {(game.phase === "question" ||
                                                    game.phase === "answering") && (
                                                    <Text size="sm" c="dimmed">
                                                        {player.hasAnswered
                                                            ? "Answered"
                                                            : "Waiting to answer"}
                                                    </Text>
                                                )}
                                            </Group>
                                        </Group>
                                    </Card>
                                ))
                            ) : (
                                <Text c="dimmed">No players are in the game yet.</Text>
                            )}
                        </Stack>
                    </Stack>
                </Grid.Col>
                <Grid.Col span={{ base: 12, md: 4 }}>
                    <Stack gap="md">
                        <Paper withBorder radius="md" p="md" style={{ minHeight: 420 }}>
                            <Stack h={388} justify="space-between">
                                <div>
                                    <Title order={2}>Chat</Title>
                                    <Text c="dimmed" size="sm" mt="xs">
                                        Messages will appear here when live chat is connected.
                                    </Text>
                                </div>
                                <Group align="flex-end" wrap="nowrap">
                                    <TextInput
                                        aria-label="Chat message"
                                        placeholder="Chat is not connected yet"
                                        disabled
                                        style={{ flex: 1 }}
                                    />
                                    <Button disabled>Send</Button>
                                </Group>
                            </Stack>
                        </Paper>
                        {/* Temporary developer control: remove this card when phase stepping is no longer needed. */}
                        <Card withBorder radius="md" padding="md">
                            <Stack gap="sm">
                                <Title order={3}>Admin controls</Title>
                                <Text size="sm" c="dimmed">
                                    Current phase: {phaseLabels[game.phase]}
                                </Text>
                                <Button
                                    onClick={() => nextPhase()}
                                    disabled={game.phase === "finished"}
                                >
                                    Next phase
                                </Button>
                            </Stack>
                        </Card>
                    </Stack>
                </Grid.Col>
            </Grid>
        </Container>
    );
}
