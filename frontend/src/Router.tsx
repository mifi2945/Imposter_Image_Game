import { createBrowserRouter, RouterProvider } from "react-router-dom";
import { SiteLayout } from "./layouts/SiteLayout";
import { AccountPage } from "./pages/account/Account.page";
import { AdminPage } from "./pages/admin/Admin.page";
import { CredentialsPage } from "./pages/credentials/Credentials.page";
import { GamePage } from "./pages/game/Game.page";
import { LeaderboardPage } from "./pages/leaderboard/Leaderboard.page";
import { LobbiesPage } from "./pages/lobbies/Lobbies.page";

const router = createBrowserRouter([
    {
        element: <SiteLayout />,
        children: [
            {
                path: "/",
                element: <CredentialsPage />,
            },
            {
                path: "/account",
                element: <AccountPage />,
            },
            {
                path: "/admin",
                element: <AdminPage />,
            },
            {
                path: "/credentials",
                element: <CredentialsPage />,
            },
            {
                path: "/game",
                element: <GamePage />,
            },
            {
                path: "/lobbies",
                element: <LobbiesPage />,
            },
            {
                path: "/leaderboard",
                element: <LeaderboardPage />,
            },
        ],
    },
]);

export function Router() {
    return <RouterProvider router={router} />;
}
