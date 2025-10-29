"use client";
import { Moon, Sun } from "lucide-react";
import { useTheme } from "next-themes";
import { Button } from "./ui/button";

export default function ThemeToggle() {
	const { theme, setTheme } = useTheme();
	function toggle() {
		setTheme(theme === "dark" ? "light" : "dark");
	}
	return (
		<Button variant="ghost" size="icon" onClick={toggle} aria-label="Toggle theme">
			<Sun className="h-5 w-5 hidden dark:block" />
			<Moon className="h-5 w-5 dark:hidden" />
		</Button>
	);
}
