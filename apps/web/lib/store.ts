import { create } from "zustand";

interface AppState {
	message: string;
	setMessage: (v: string) => void;
}

export const useAppStore = create<AppState>((set) => ({
	message: "",
	setMessage: (v) => set({ message: v })
}));
