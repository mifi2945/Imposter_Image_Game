export function validateUsername(username: string) {
    if (!username) {
        throw new Error("Username cannot be empty");
    }

    if (username.length < 3) {
        throw new Error("Invalid username");
    }
}

export function validatePassword(password: string) {
    if (!password) {
        throw new Error("Password cannot be empty");
    }

    if (password.length < 8) {
        throw new Error("Invalid Password");
    }
}
