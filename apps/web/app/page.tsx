"use client";

import { useEffect, useState } from "react";
import { useAppStore } from "../store";
import { useAuthStore } from "../store";
import { Button } from "../components/ui/button";
import ThemeToggle from "../components/theme-toggle";
import { apiFetch } from "../lib/api";

export default function HomePage() {
	const message = useAppStore((s) => s.message);
	const setMessage = useAppStore((s) => s.setMessage);
	const token = useAuthStore((s) => s.token);
	const setToken = useAuthStore((s) => s.setToken);
	const logout = useAuthStore((s) => s.logout);
	const [reply, setReply] = useState("");
	const [username, setUsername] = useState("");
	const [password, setPassword] = useState("");

	useEffect(() => {
		setMessage("Welcome to AI Fest Management ✨");
	}, [setMessage]);

	async function callApi() {
		const res = await apiFetch("/api/echo", { method: "POST", body: JSON.stringify({ text: "Hello from Next.js" }) });
		const data = await res.json();
		setReply(data.reply ?? "");
	}

	async function doLogin() {
		const res = await apiFetch("/api/auth/token/", { method: "POST", body: JSON.stringify({ username, password }) });
		if (res.ok) {
			const data = await res.json();
			setToken(data.access);
		}
	}

	async function doRegister() {
		await apiFetch("/api/auth/register/", { method: "POST", body: JSON.stringify({ username, password }) });
	}

	return (
		<div className="px-4 py-6 max-w-3xl mx-auto space-y-5">
			<div className="flex items-center justify-between gap-3">
				<h1 className="text-xl sm:text-2xl font-semibold">{message}</h1>
				<ThemeToggle />
			</div>
			<p className="text-sm text-muted-foreground">Next.js + Zustand + Django + DRF + JWT</p>
			<div className="flex flex-col sm:flex-row gap-2 sm:items-center">
				<Button className="w-full sm:w-auto" onClick={callApi}>Ping API</Button>
				{reply && <span className="text-sm break-words">API: {reply}</span>}
			</div>
			<div className="space-y-3">
				<div className="flex flex-col sm:flex-row gap-2">
					<input className="border px-3 py-2 rounded w-full sm:w-48" placeholder="username" value={username} onChange={(e) => setUsername(e.target.value)} />
					<input className="border px-3 py-2 rounded w-full sm:w-48" placeholder="password" type="password" value={password} onChange={(e) => setPassword(e.target.value)} />
					<div className="flex gap-2 sm:ml-auto">
						<Button className="w-full sm:w-auto" variant="secondary" onClick={doRegister}>Register</Button>
						<Button className="w-full sm:w-auto" onClick={doLogin}>Login</Button>
					</div>
				</div>
				<div className="flex items-center gap-2">
					<span className="text-sm">{token ? "Authenticated" : "Guest"}</span>
					{token && (
						<Button variant="ghost" onClick={logout}>Logout</Button>
					)}
				</div>
			</div>
		</div>
	);
}
