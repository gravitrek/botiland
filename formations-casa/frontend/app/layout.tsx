import type { Metadata } from 'next'
import './globals.css'

export const metadata: Metadata = {
  title: 'Formations.casa - Training Marketplace in Casablanca',
  description: 'Find and book professional training courses in Casablanca, Morocco',
}

export default function RootLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <html lang="en">
      <body>{children}</body>
    </html>
  )
}
