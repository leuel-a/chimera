import type { Metadata } from "next";
import "./globals.css";

export const metadata: Metadata = {
  title: "Platform",
  description: "Platform for Project Chimera",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en">
      <body>
        {children}
      </body>
    </html>
  );
}
