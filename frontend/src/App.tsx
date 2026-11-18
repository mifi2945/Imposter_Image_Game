import "@mantine/core/styles.css";

import { Provider } from "react-redux";
import { MantineProvider } from "@mantine/core";
import { bindStore } from "~/api";
import { store } from "~/redux";
import { Router } from "./Router";
import { theme } from "./theme";

bindStore(store);

export default function App() {
    return (
        <Provider store={store}>
            <MantineProvider theme={theme} defaultColorScheme="dark">
                <Router />
            </MantineProvider>
        </Provider>
    );
}
