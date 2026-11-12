import { useEffect, useState, type FormEvent } from "react";
import { useDispatch } from "react-redux";
import {
    Alert,
    Button,
    Card,
    Container,
    Group,
    Stack,
    Text,
    Textarea,
    TextInput,
    Title,
} from "@mantine/core";
import { useActions, useAppSelector } from "~/hooks";
import { AccountRole } from "~/models";
import { questionsSlice, type Dispatch } from "~/redux";

export function AdminPage() {
    const dispatch = useDispatch<Dispatch>();
    const { account } = useAppSelector((state) => state.auth);
    const { clearError, deleteQuestion, getQuestions } = useActions(questionsSlice.actions);
    const { errorMessage, isLoading, questions } = useAppSelector((state) => state.questions);
    const [category, setCategory] = useState("");
    const [questionText, setQuestionText] = useState("");
    const isAdmin = account.role === AccountRole.Admin;

    useEffect(() => {
        if (isAdmin) getQuestions();
    }, [getQuestions, isAdmin]);

    async function handleSubmit(event: FormEvent<HTMLFormElement>) {
        event.preventDefault();
        clearError();

        const result = await dispatch(
            questionsSlice.actions.createQuestion({
                category: category.trim(),
                question: questionText.trim(),
            }),
        );

        if (questionsSlice.actions.createQuestion.fulfilled.match(result)) {
            setCategory("");
            setQuestionText("");
        }
    }

    if (!isAdmin) {
        return (
            <Container component="main" size="md" py="xl">
                <Alert color="red" title="Admin access required">
                    Only administrators can view and manage questions.
                </Alert>
            </Container>
        );
    }

    const questionsByCategory = questions.reduce<Record<string, typeof questions>>(
        (groups, question) => {
            (groups[question.category] ??= []).push(question);
            return groups;
        },
        {},
    );

    return (
        <Container component="main" size="md" py="xl">
            <Stack gap="xl">
                <Title order={1}>Question management</Title>

                {errorMessage && (
                    <Alert color="red" title="Unable to manage questions">
                        {errorMessage}
                    </Alert>
                )}

                <Card withBorder radius="md" padding="lg">
                    <form onSubmit={handleSubmit}>
                        <Stack gap="md">
                            <Title order={2}>Add a question</Title>
                            <TextInput
                                label="Category"
                                value={category}
                                onChange={(event) => setCategory(event.currentTarget.value)}
                                required
                            />
                            <Textarea
                                label="Question"
                                value={questionText}
                                onChange={(event) => setQuestionText(event.currentTarget.value)}
                                minRows={3}
                                autosize
                                required
                            />
                            <Group justify="flex-end">
                                <Button type="submit" loading={isLoading}>
                                    Add question
                                </Button>
                            </Group>
                        </Stack>
                    </form>
                </Card>

                <Stack gap="lg">
                    <Title order={2}>Questions</Title>
                    {isLoading && questions.length === 0 && <Text>Loading questions...</Text>}
                    {!isLoading && !errorMessage && questions.length === 0 && (
                        <Text c="dimmed">No questions have been added yet.</Text>
                    )}

                    {Object.entries(questionsByCategory)
                        .sort(([left], [right]) => left.localeCompare(right))
                        .map(([groupCategory, categoryQuestions]) => (
                            <Stack key={groupCategory} gap="sm">
                                <Title order={3}>{groupCategory}</Title>
                                {categoryQuestions.map((question) => (
                                    <Card key={question.id} withBorder radius="md" padding="md">
                                        <Group justify="space-between" align="flex-start">
                                            <Text style={{ flex: 1 }}>{question.question}</Text>
                                            <Button
                                                color="red"
                                                variant="light"
                                                size="xs"
                                                disabled={isLoading}
                                                onClick={() => deleteQuestion(question.id)}
                                            >
                                                Delete
                                            </Button>
                                        </Group>
                                    </Card>
                                ))}
                            </Stack>
                        ))}
                </Stack>
            </Stack>
        </Container>
    );
}
