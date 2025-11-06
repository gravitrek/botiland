# QRGeek Frontend

Next.js 14+ frontend for QRGeek QR code platform.

## Getting Started

### Prerequisites
- Node.js 18+
- npm or yarn

### Installation

```bash
npm install
```

### Development

```bash
npm run dev
```

Open [http://localhost:3000](http://localhost:3000) in your browser.

### Build

```bash
npm run build
npm start
```

## Project Structure

```
frontend/
├── app/                 # Next.js App Router
│   ├── (auth)/         # Auth pages (login, register)
│   ├── dashboard/      # Dashboard pages
│   ├── qr/            # QR code management
│   └── page.tsx       # Landing page
├── components/         # React components
├── lib/               # Utilities and API client
└── public/            # Static assets
```

## Environment Variables

Create a `.env.local` file:

```
NEXT_PUBLIC_API_URL=http://localhost:8000/api
NEXT_PUBLIC_SITE_URL=http://localhost:3000
```

## Technologies

- Next.js 14+ (App Router)
- React 18
- TypeScript
- Tailwind CSS
- TanStack Query
- Axios
- qrcode.react
- Recharts
