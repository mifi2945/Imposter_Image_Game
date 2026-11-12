export enum AccountRole {
    User,
    Admin,
}

export interface Account {
    id: string;
    createdAt: string;
    username: string;
    role: AccountRole;
}
