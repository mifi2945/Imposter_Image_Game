import { useEffect, useState, type FormEvent } from "react";
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
import { useNavigate } from "react-router-dom";

export function CredentialsPage() {
    const navigate = useNavigate();
    const { clearError, signIn, signUp } = useActions(authSlice.actions);
    const { accessToken, errorMessage, isLoading } = useAppSelector((state) => state.auth);
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

    useEffect(() => {
        navigate("/lobbies");
    }, [accessToken]);

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
                    </Stack>
                </form>
            </Stack>
        </Container>
    );
}
