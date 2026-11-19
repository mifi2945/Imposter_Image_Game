import { send } from "./hub";
import { getServiceUrls } from "./service-urls";
import { Account } from "~/models";

export interface GetAccountResponse {
    account: Account;
}

export async function getAccount() {
    return await send<GetAccountResponse>({
        baseUrl: getServiceUrls().accounts,
        endpoint: "/accounts/me",
    });
}
