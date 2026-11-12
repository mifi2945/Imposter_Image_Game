import { Outlet } from "react-router-dom";
import { SiteHeader } from "~/components/SiteHeader/SiteHeader";

export function SiteLayout() {
    return (
        <>
            <SiteHeader />
            <Outlet />
        </>
    );
}
