import { create } from "zustand";
import { persist } from "zustand/middleware";

interface AuthState {
	token: string | null;
	username: string | null;
	role: string | null;
	setToken: (t: string | null) => void;
	setProfile: (u: { username: string; role: string }) => void;
	logout: () => void;
}

export const useAuthStore = create<AuthState>()(
	persist(
		(set) => ({
			token: null,
			username: null,
			role: null,
			setToken: (t) => set({ token: t }),
			setProfile: (u) => set({ username: u.username, role: u.role }),
			logout: () => set({ token: null, username: null, role: null })
		}),
		{ name: "auth-token" }
	)
);
