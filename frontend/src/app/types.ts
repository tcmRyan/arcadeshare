export interface Role {
	id: number;
	name: string;
	description: string;
}

export interface User {
	roles: Role[];
	id: number;
	email: string;
	username: string;
	active: boolean;
	last_login: Date;
}

export interface Profile {
	user: User;
	access_token: string;
	refresh_token: string;
	expires_in: number;
}

