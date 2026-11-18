import { Button, Container, Group, Stack, Table, Text, Title } from "@mantine/core";
import { useActions, useAppSelector } from "~/hooks";
import { AccountRole } from "~/models";
import { authSlice } from "~/redux";

export function AccountPage() {
    const account = useAppSelector((state) => state.auth.account);
    const { reset } = useActions(authSlice.actions);

    return (
        <Container component="main" size="sm" py="xl">
            <Stack gap="lg">
                <Group justify="space-between" align="center">
                    <div>
                        <Title order={1}>Account</Title>
                        <Text c="dimmed" mt="xs">
                            Your account information
                        </Text>
                    </div>
                    <Button color="red" variant="light" onClick={() => reset()}>
                        Sign out
                    </Button>
                </Group>

                <Table striped>
                    <Table.Tbody>
                        <Table.Tr>
                            <Table.Th scope="row">Username</Table.Th>
                            <Table.Td>{account.username}</Table.Td>
                        </Table.Tr>
                        <Table.Tr>
                            <Table.Th scope="row">Role</Table.Th>
                            <Table.Td>
                                {account.role === AccountRole.Admin ? "Admin" : "User"}
                            </Table.Td>
                        </Table.Tr>
                        <Table.Tr>
                            <Table.Th scope="row">Points</Table.Th>
                            <Table.Td>{account.points}</Table.Td>
                        </Table.Tr>
                        <Table.Tr>
                            <Table.Th scope="row">Member since</Table.Th>
                            <Table.Td>{new Date(account.createdAt).toLocaleDateString()}</Table.Td>
                        </Table.Tr>
                    </Table.Tbody>
                </Table>
            </Stack>
        </Container>
    );
}
