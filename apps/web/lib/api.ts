import { useAuthStore } from "../store";

const baseURL = process.env.NEXT_PUBLIC_API_BASE_URL || "http://localhost:8000";

export async function apiFetch(path: string, init?: RequestInit) {
	const token = useAuthStore.getState().token;
	const headers = new Headers(init?.headers || {});
	headers.set("Content-Type", "application/json");
	if (token) headers.set("Authorization", `Bearer ${token}`);
	const res = await fetch(`${baseURL}${path}`, { ...init, headers });
	return res;
}
