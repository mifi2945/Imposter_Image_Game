import { createBrowserRouter, RouterProvider } from "react-router-dom";
import { AdminPage } from "./pages/admin/Admin.page";
import { CredentialsPage } from "./pages/credentials/Credentials.page";
import { GamePage } from "./pages/game/Game.page";
import { LobbiesPage } from "./pages/lobbies/Lobbies.page";

const router = createBrowserRouter([
    {
        path: "/",
        element: <CredentialsPage />,
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
]);

export function Router() {
    return <RouterProvider router={router} />;
}
