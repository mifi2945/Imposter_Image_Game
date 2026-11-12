import { Account } from "~/models";
import { send } from "./hub";

export interface GetAccountResponse {
    account: Account;
}

export async function getAccount() {
    return await send<GetAccountResponse>({
        endpoint: "/accounts/me",
    });
}
