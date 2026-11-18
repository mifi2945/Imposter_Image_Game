export enum AccountRole {
    User,
    Admin,
}

export interface Account {
    createdAt: string;
    username: string;
    role: AccountRole;
    points: number;
}
