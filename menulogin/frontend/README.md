# MenuLogin Frontend

Next.js frontend for the MenuLogin Restaurant SaaS Platform.

## Getting Started

### Install Dependencies
```bash
npm install
```

### Development Server
```bash
npm run dev
```

Open [http://localhost:3000](http://localhost:3000) in your browser.

### Build for Production
```bash
npm run build
npm start
```

## Environment Variables

Create a `.env.local` file:

```bash
NEXT_PUBLIC_API_URL=http://localhost:8000/api
NEXT_PUBLIC_STRIPE_PUBLIC_KEY=your-stripe-public-key
```

## Project Structure

```
frontend/
├── app/                    # Next.js App Router
│   ├── (auth)/            # Authentication routes
│   │   ├── login/
│   │   └── register/
│   ├── (dashboard)/       # Dashboard routes
│   │   ├── restaurant/
│   │   ├── menu/
│   │   ├── orders/
│   │   └── analytics/
│   ├── (public)/          # Public routes
│   │   ├── restaurants/
│   │   └── order/
│   ├── layout.tsx         # Root layout
│   └── page.tsx           # Home page
├── components/            # Reusable components
│   ├── ui/               # UI components
│   ├── forms/            # Form components
│   └── layouts/          # Layout components
├── lib/                   # Utility functions
│   ├── api.ts            # API client
│   └── utils.ts          # Helper functions
├── contexts/             # React contexts
│   └── AuthContext.tsx   # Authentication context
├── types/                # TypeScript types
└── public/               # Static assets
```

## Features to Implement

### Phase 1: Authentication
- [ ] Login page
- [ ] Registration page
- [ ] Password reset
- [ ] JWT token management

### Phase 2: Restaurant Dashboard
- [ ] Restaurant profile management
- [ ] Menu management interface
- [ ] Order management
- [ ] Table management

### Phase 3: Customer Interface
- [ ] Restaurant listing
- [ ] Menu browsing
- [ ] Cart functionality
- [ ] Checkout process
- [ ] Order tracking

### Phase 4: Advanced Features
- [ ] Real-time order updates
- [ ] Analytics dashboard
- [ ] QR code scanning
- [ ] Payment integration

## Tech Stack

- **Framework**: Next.js 15
- **React**: 18.3
- **TypeScript**: 5.x
- **Styling**: Tailwind CSS
- **API Client**: Axios
- **State Management**: React Context API

## Development Guidelines

1. Use TypeScript for all components
2. Follow Next.js App Router conventions
3. Use Tailwind CSS for styling
4. Implement responsive design
5. Add loading and error states
6. Handle authentication properly
7. Test on multiple devices

## API Integration

The frontend connects to the Django REST API backend:

```typescript
// lib/api.ts
import axios from 'axios';

const api = axios.create({
  baseURL: process.env.NEXT_PUBLIC_API_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Add auth token to requests
api.interceptors.request.use((config) => {
  const token = localStorage.getItem('token');
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

export default api;
```

## Deployment

### Vercel (Recommended)
```bash
npm install -g vercel
vercel
```

### AWS Amplify
Connect your GitHub repository to AWS Amplify and configure build settings.

### Self-Hosted
```bash
npm run build
npm start
```

## Contributing

Follow the project coding standards and submit pull requests for review.

## License

Proprietary - All rights reserved
