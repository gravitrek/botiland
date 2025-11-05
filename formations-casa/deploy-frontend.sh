#!/bin/bash

# Formations.casa Frontend Deployment Script

echo "🚀 Formations.casa Frontend Deployment"
echo "======================================"
echo ""

# Check if we're in the right directory
if [ ! -d "frontend" ]; then
    echo "❌ Error: frontend directory not found"
    echo "Please run this script from the formations-casa root directory"
    exit 1
fi

cd frontend

echo "📦 Installing dependencies..."
npm install

echo ""
echo "🔧 Building production frontend..."
npm run build

if [ $? -ne 0 ]; then
    echo "❌ Build failed! Check errors above."
    exit 1
fi

echo ""
echo "✅ Build successful!"
echo ""
echo "Choose deployment method:"
echo "1) Vercel (Recommended)"
echo "2) Start local server (PM2)"
echo "3) Just build (manual deployment)"
echo ""
read -p "Enter choice [1-3]: " choice

case $choice in
    1)
        echo ""
        echo "📤 Deploying to Vercel..."
        if ! command -v vercel &> /dev/null; then
            echo "Installing Vercel CLI..."
            npm install -g vercel
        fi
        vercel --prod
        echo ""
        echo "✅ Deployed to Vercel!"
        echo "Your site should be live at the URL shown above"
        ;;
    2)
        echo ""
        echo "🚀 Starting with PM2..."
        if ! command -v pm2 &> /dev/null; then
            echo "Installing PM2..."
            npm install -g pm2
        fi
        pm2 delete formations-frontend 2>/dev/null
        pm2 start npm --name "formations-frontend" -- start
        pm2 save
        echo ""
        echo "✅ Frontend started on http://localhost:3000"
        echo ""
        echo "Useful PM2 commands:"
        echo "  pm2 logs formations-frontend  # View logs"
        echo "  pm2 restart formations-frontend  # Restart"
        echo "  pm2 stop formations-frontend  # Stop"
        ;;
    3)
        echo ""
        echo "✅ Build complete!"
        echo ""
        echo "Next steps for manual deployment:"
        echo "1. Upload the .next directory to your server"
        echo "2. Run: npm start"
        echo "3. Configure your reverse proxy (Nginx/Apache)"
        ;;
    *)
        echo "Invalid choice"
        exit 1
        ;;
esac

echo ""
echo "🎉 Deployment complete!"
echo ""
echo "Important reminders:"
echo "1. Make sure your backend is running at https://formations.casa"
echo "2. Check CORS settings in Django to allow your frontend domain"
echo "3. Set NEXT_PUBLIC_API_URL=https://formations.casa/api"
echo ""
echo "Need help? Check DEPLOYMENT.md for detailed instructions"
