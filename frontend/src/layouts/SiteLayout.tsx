import { useEffect } from "react";
import { Outlet, useLocation, useNavigate } from "react-router-dom";
import { SiteHeader } from "~/components/SiteHeader/SiteHeader";
import { useAppSelector } from "~/hooks";

export function SiteLayout() {
    const accessToken = useAppSelector((state) => state.auth.accessToken);
    const { pathname } = useLocation();
    const navigate = useNavigate();
    const isCredentialsRoute = pathname === "/" || pathname === "/credentials";
    const shouldRedirect =
        (!accessToken && !isCredentialsRoute) || (accessToken && isCredentialsRoute);

    useEffect(() => {
        if (!accessToken && !isCredentialsRoute) {
            navigate("/credentials", { replace: true });
        } else if (accessToken && isCredentialsRoute) {
            navigate("/lobbies", { replace: true });
        }
    }, [accessToken, isCredentialsRoute, navigate]);

    if (shouldRedirect) return null;

    return (
        <>
            <SiteHeader />
            <Outlet />
        </>
    );
}
