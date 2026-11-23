import type { Metadata } from "next";
import "./globals.css";

export const metadata: Metadata = {
  title: "DomainFolio — Domain Marketplace",
  description:
    "Buy and sell domain names on DomainFolio, a multi-vendor marketplace with verified ownership and secure escrow.",
};

export default function RootLayout({
  children,
}: Readonly<{ children: React.ReactNode }>) {
  return (
    <html lang="en">
      <body className="min-h-screen bg-white text-neutral-900 antialiased">
        <header className="border-b border-neutral-200">
          <nav className="mx-auto flex max-w-6xl items-center justify-between px-4 py-4">
            <a href="/" className="text-xl font-bold tracking-tight">
              DomainFolio
            </a>
            <div className="flex items-center gap-6 text-sm">
              <a href="/browse" className="hover:underline">
                Browse
              </a>
              <a href="/sell" className="hover:underline">
                Sell
              </a>
              <a href="/auctions" className="hover:underline">
                Auctions
              </a>
              <a href="/how-it-works" className="hover:underline">
                How it works
              </a>
              <a
                href="/login"
                className="rounded-md bg-neutral-900 px-3 py-1.5 text-white"
              >
                Sign in
              </a>
            </div>
          </nav>
        </header>
        <main className="mx-auto max-w-6xl px-4 py-8">{children}</main>
        <footer className="border-t border-neutral-200 py-6 text-center text-sm text-neutral-500">
          DomainFolio marketplace — P0 skeleton. No listings yet; inventory
          is never fabricated.
        </footer>
      </body>
    </html>
  );
}
