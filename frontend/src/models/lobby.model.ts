import { Account } from "./accounts.model";

export interface Lobby {
    name: string;
    code: string;
    accounts: Account[];
    round: number;
}
