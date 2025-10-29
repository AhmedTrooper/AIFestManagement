"use client";
import { useEffect, useState } from "react";
import { useParams } from "next/navigation";
import Link from "next/link";
import { apiFetch } from "../../../lib/api";
import { Button } from "../../../components/ui/button";

interface TeamDto { id: number; name: string; member_usernames: string[] }

export default function ItemDetailPage() {
	const params = useParams<{ id: string }>();
	const [teams, setTeams] = useState<TeamDto[]>([]);
	const [name, setName] = useState("");

	useEffect(() => { load(); }, [params?.id]);

	async function load() {
		const res = await apiFetch(`/api/items/${params.id}/teams`);
		if (res.ok) {
			const data = await res.json();
			setTeams(data.results || []);
		}
	}

	async function createTeam() {
		const res = await apiFetch(`/api/items/${params.id}/teams`, { method: "POST", body: JSON.stringify({ name }) });
		if (res.ok) {
			setName("");
			load();
		}
	}

	return (
		<div className="px-4 py-6 max-w-3xl mx-auto space-y-5">
			<Link href="/" className="text-sm underline">Back</Link>
			<div className="space-y-2 border rounded p-3">
				<div className="font-medium">Create Team</div>
				<input className="border px-3 py-2 rounded w-full" placeholder="Team name" value={name} onChange={(e) => setName(e.target.value)} />
				<Button onClick={createTeam} disabled={!name}>Create</Button>
			</div>
			<div className="space-y-2">
				<div className="font-medium">Teams</div>
				<div className="space-y-2">
					{teams.map(t => (
						<div key={t.id} className="border rounded p-3">
							<div className="font-semibold">{t.name}</div>
							<div className="text-sm text-muted-foreground">Members: {t.member_usernames.join(", ") || "none"}</div>
						</div>
					))}
					{teams.length === 0 && <div className="text-sm text-muted-foreground">No teams</div>}
				</div>
			</div>
		</div>
	);
}
