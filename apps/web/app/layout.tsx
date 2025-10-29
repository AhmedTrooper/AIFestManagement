import "./globals.css";
import { ThemeProvider } from "../components/theme-provider";

export const metadata = {
	title: "AI Fest Management",
	description: "Monorepo Next.js + Django"
};

export const viewport = {
	width: "device-width",
	initialScale: 1,
	maximumScale: 1
};

export default function RootLayout({ children }: { children: React.ReactNode }) {
	return (
		<html lang="en" suppressHydrationWarning>
			<body className="min-h-screen bg-background text-foreground">
				<ThemeProvider>{children}</ThemeProvider>
			</body>
		</html>
	);
}
