"use client";
import { useEffect, useState } from "react";
import { useParams } from "next/navigation";
import Link from "next/link";
import { apiFetch } from "../../../lib/api";
import { Button } from "../../../components/ui/button";
import { useAuthStore } from "../../../store";

interface RuleDto { id: number; text: string; item: number | null }
interface ItemDto { id: number; title: string; description: string; max_team_size: number; rules: RuleDto[] }
interface FestDetailDto { id: number; name: string; description: string; items: ItemDto[]; rules: RuleDto[] }

export default function FestDetailPage() {
	const params = useParams<{ id: string }>();
	const role = useAuthStore((s) => s.role);
	const [fest, setFest] = useState<FestDetailDto | null>(null);
	const [question, setQuestion] = useState("");
	const [answer, setAnswer] = useState("");
	const [itemTitle, setItemTitle] = useState("");
	const [itemDesc, setItemDesc] = useState("");
	const [ruleText, setRuleText] = useState("");

	useEffect(() => {
		load();
		// eslint-disable-next-line react-hooks/exhaustive-deps
	}, [params?.id]);

	async function load() {
		const res = await apiFetch(`/api/fests/${params.id}`);
		if (res.ok) setFest(await res.json());
	}

	async function askFest() {
		const res = await apiFetch(`/api/fests/${params.id}/ask`, { method: "POST", body: JSON.stringify({ question }) });
		if (res.ok) {
			const data = await res.json();
			setAnswer(data.answer || "");
		}
	}

	async function createItem() {
		const res = await apiFetch(`/api/fests/${params.id}/items`, { method: "POST", body: JSON.stringify({ title: itemTitle, description: itemDesc, max_team_size: 1 }) });
		if (res.ok) {
			setItemTitle("");
			setItemDesc("");
			load();
		}
	}

	async function addFestRule() {
		const res = await apiFetch(`/api/fests/${params.id}/rules`, { method: "POST", body: JSON.stringify({ text: ruleText }) });
		if (res.ok) {
			setRuleText("");
			load();
		}
	}

	return (
		<div className="px-4 py-6 max-w-3xl mx-auto space-y-5">
			<Link href="/" className="text-sm underline">Back</Link>
			{fest && (
				<div className="space-y-4">
					<div>
						<h1 className="text-2xl font-semibold">{fest.name}</h1>
						<p className="text-sm text-muted-foreground whitespace-pre-wrap">{fest.description}</p>
					</div>
					{role === "authority" && (
						<div className="grid gap-3 sm:grid-cols-2">
							<div className="space-y-2 border rounded p-3">
								<div className="font-medium">Add Item</div>
								<input className="border px-3 py-2 rounded w-full" placeholder="title" value={itemTitle} onChange={(e) => setItemTitle(e.target.value)} />
								<textarea className="border px-3 py-2 rounded w-full" placeholder="description" value={itemDesc} onChange={(e) => setItemDesc(e.target.value)} />
								<Button onClick={createItem} disabled={!itemTitle}>Create</Button>
							</div>
							<div className="space-y-2 border rounded p-3">
								<div className="font-medium">Add Fest Rule</div>
								<textarea className="border px-3 py-2 rounded w-full" placeholder="Rule text" value={ruleText} onChange={(e) => setRuleText(e.target.value)} />
								<Button onClick={addFestRule} disabled={!ruleText}>Add</Button>
							</div>
						</div>
					)}
					<div className="space-y-2">
						<div className="font-medium">Rules</div>
						<ul className="list-disc pl-6 space-y-1">
							{fest.rules.map(r => (<li key={r.id}>{r.text}</li>))}
							{fest.rules.length === 0 && <li className="text-muted-foreground">No rules</li>}
						</ul>
					</div>
					<div className="space-y-2">
						<div className="font-medium">Items</div>
						<div className="space-y-3">
							{fest.items.map(it => (
								<div key={it.id} className="border rounded p-3">
									<div className="font-semibold">{it.title}</div>
									<p className="text-sm text-muted-foreground">{it.description}</p>
									{it.rules.length > 0 && (
										<ul className="list-disc pl-6 mt-2 space-y-1">
											{it.rules.map(r => (<li key={r.id}>{r.text}</li>))}
										</ul>
									)}
								</div>
							))}
							{fest.items.length === 0 && <div className="text-sm text-muted-foreground">No items</div>}
						</div>
					</div>
					<div className="space-y-2 border rounded p-3">
						<div className="font-medium">Ask about this fest</div>
						<textarea className="border px-3 py-2 rounded w-full" placeholder="Your question" value={question} onChange={(e) => setQuestion(e.target.value)} />
						<Button onClick={askFest} disabled={!question}>Ask</Button>
						{answer && <div className="text-sm whitespace-pre-wrap">{answer}</div>}
					</div>
				</div>
			)}
		</div>
	);
}
