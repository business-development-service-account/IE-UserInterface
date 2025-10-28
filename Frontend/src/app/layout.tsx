import './globals.css'
import type { Metadata } from 'next'
import Navigation from '@/components/ui/Navigation'

export const metadata: Metadata = {
  title: 'AI System Interface',
  description: 'Frontend for AI Agent System',
}

export default function RootLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <html lang="en">
      <body className="h-screen overflow-hidden bg-content-bg font-sans flex">
        <Navigation />
        <main className="flex-1">
          {children}
        </main>
      </body>
    </html>
  )
}