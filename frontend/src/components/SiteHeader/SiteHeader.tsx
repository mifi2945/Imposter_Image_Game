import { Burger, Container, Divider, Drawer, Group, ScrollArea, Stack, Text } from "@mantine/core";
import { useDisclosure } from "@mantine/hooks";
import { NavLink, useLocation } from "react-router-dom";
import classes from "./SiteHeader.module.css";
import { useAppSelector } from "~/hooks";
import { AccountRole } from "~/models";

export function SiteHeader() {
    const [opened, { toggle, close }] = useDisclosure(false);
    const { pathname } = useLocation();
    const { account } = useAppSelector((state) => state.auth);
    const hideNavigation = pathname === "/" || pathname === "/credentials";

    const links = [
        ...(account.role === AccountRole.Admin ? [{ to: "/admin", label: "Admin" }] : []),
        { to: "/game", label: "Game" },
        { to: "/lobbies", label: "Lobbies" },
        { to: "/leaderboard", label: "Leaderboard" },
        { to: "/account", label: "Account" },
    ];

    const items = links.map(({ to, label }) => (
        <NavLink
            key={to}
            to={to}
            className={classes.link}
            data-active={pathname === to || undefined}
            onClick={close}
        >
            {label}
        </NavLink>
    ));

    return (
        <header className={classes.header}>
            <Container size="md" className={classes.inner}>
                <Text fw={700}>Imposter Image Game</Text>
                {!hideNavigation && (
                    <>
                        <Group gap={5} visibleFrom="xs">
                            {items}
                        </Group>
                        <Burger
                            opened={opened}
                            onClick={toggle}
                            hiddenFrom="xs"
                            size="sm"
                            aria-label="Toggle navigation"
                        />
                    </>
                )}
            </Container>

            {!hideNavigation && (
                <Drawer
                    opened={opened}
                    onClose={close}
                    size="100%"
                    padding="md"
                    title="Navigation"
                    hiddenFrom="xs"
                    zIndex={1000000}
                >
                    <ScrollArea h="calc(100vh - 80px)" mx="-md">
                        <Divider my="sm" />
                        <Stack gap={0}>{items}</Stack>
                    </ScrollArea>
                </Drawer>
            )}
        </header>
    );
}
