import { useState, type FormEvent } from "react";
import {
    Alert,
    Button,
    Container,
    Group,
    PasswordInput,
    Stack,
    Text,
    TextInput,
    Title,
} from "@mantine/core";
import { useActions, useAppSelector } from "~/hooks";
import { authSlice } from "~/redux";

export function CredentialsPage() {
    const { clearError, setMockAuth, signIn, signUp } = useActions(authSlice.actions);
    const { errorMessage, isLoading } = useAppSelector((state) => state.auth);
    const [username, setUsername] = useState("");
    const [password, setPassword] = useState("");

    function handleSubmit(event: FormEvent<HTMLFormElement>) {
        event.preventDefault();
        clearError();

        const submitter = (event.nativeEvent as SubmitEvent).submitter as HTMLButtonElement | null;
        const isSignUp = submitter?.value === "signUp";
        if (isSignUp) signUp({ username, password });
        else signIn({ username, password });
    }

    return (
        <Container size="xs" py="xl">
            <Stack gap="lg">
                <div>
                    <Title order={1}>Sign in or create an account</Title>
                    <Text c="dimmed" mt="xs">
                        Continue with your username and password.
                    </Text>
                </div>

                <form onSubmit={handleSubmit}>
                    <Stack gap="md">
                        <TextInput
                            label="Username"
                            autoComplete="username"
                            value={username}
                            onChange={(event) => setUsername(event.currentTarget.value)}
                            required
                        />
                        <PasswordInput
                            label="Password"
                            autoComplete="current-password"
                            value={password}
                            onChange={(event) => setPassword(event.currentTarget.value)}
                            minLength={8}
                            required
                        />

                        {errorMessage && (
                            <Alert color="red" title="Unable to continue">
                                {errorMessage}
                            </Alert>
                        )}

                        <Group grow>
                            <Button type="submit" name="action" value="signIn" loading={isLoading}>
                                Sign in
                            </Button>
                            <Button type="submit" name="action" value="signUp" loading={isLoading}>
                                Sign up
                            </Button>
                        </Group>
                        <Button type="button" variant="light" onClick={() => setMockAuth()}>
                            Explore with demo account
                        </Button>
                    </Stack>
                </form>
            </Stack>
        </Container>
    );
}
