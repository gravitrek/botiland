'use client';

import { useEffect, useState } from 'react';
import { useRouter } from 'next/navigation';
import Link from 'next/link';
import { useAuth } from '@/contexts/AuthContext';
import { formsAPI, landingPagesAPI, leadsAPI, usersAPI } from '@/lib/api';
import { FileText, Globe, Users, TrendingUp, Plus, Settings, LogOut } from 'lucide-react';

export default function DashboardPage() {
  const { user, loading, logout } = useAuth();
  const router = useRouter();
  const [stats, setStats] = useState<any>(null);
  const [loadingStats, setLoadingStats] = useState(true);

  useEffect(() => {
    if (!loading && !user) {
      router.push('/login');
    }
  }, [user, loading, router]);

  useEffect(() => {
    const fetchStats = async () => {
      try {
        const [userStats, formStats, leadStats] = await Promise.all([
          usersAPI.stats(),
          formsAPI.stats(),
          leadsAPI.stats(),
        ]);

        setStats({
          ...userStats.data,
          ...formStats.data,
          ...leadStats.data,
        });
      } catch (error) {
        console.error('Failed to fetch stats', error);
      } finally {
        setLoadingStats(false);
      }
    };

    if (user) {
      fetchStats();
    }
  }, [user]);

  if (loading || !user) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <div className="text-xl">Loading...</div>
      </div>
    );
  }

  const statCards = [
    {
      title: 'Total Forms',
      value: stats?.total_forms || 0,
      icon: <FileText className="w-8 h-8" />,
      color: 'bg-blue-500',
      link: '/dashboard/forms',
    },
    {
      title: 'Total Landing Pages',
      value: stats?.total_landing_pages || 0,
      icon: <Globe className="w-8 h-8" />,
      color: 'bg-green-500',
      link: '/dashboard/landing-pages',
    },
    {
      title: 'Total Leads',
      value: stats?.total_leads || 0,
      icon: <Users className="w-8 h-8" />,
      color: 'bg-purple-500',
      link: '/dashboard/leads',
    },
    {
      title: 'Conversion Rate',
      value: stats?.total_submissions && stats?.total_views
        ? `${((stats.total_submissions / stats.total_views) * 100).toFixed(1)}%`
        : '0%',
      icon: <TrendingUp className="w-8 h-8" />,
      color: 'bg-orange-500',
    },
  ];

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Header */}
      <header className="bg-white shadow-sm">
        <div className="container mx-auto px-4 py-4">
          <div className="flex justify-between items-center">
            <h1 className="text-2xl font-bold text-gray-900">PaidSignups</h1>
            <div className="flex items-center gap-4">
              <span className="text-sm text-gray-600">
                {user.email} | {user.subscription_plan}
              </span>
              <button onClick={logout} className="btn btn-secondary flex items-center gap-2">
                <LogOut className="w-4 h-4" />
                Logout
              </button>
            </div>
          </div>
        </div>
      </header>

      <div className="container mx-auto px-4 py-8">
        {/* Welcome Section */}
        <div className="mb-8">
          <h2 className="text-3xl font-bold mb-2">
            Welcome back, {user.first_name || user.username}!
          </h2>
          <p className="text-gray-600">Here's what's happening with your account today.</p>
        </div>

        {/* Stats Cards */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
          {statCards.map((stat, index) => (
            <Link
              key={index}
              href={stat.link || '#'}
              className="card hover:shadow-lg transition-shadow cursor-pointer"
            >
              <div className="flex items-center justify-between">
                <div>
                  <p className="text-sm text-gray-600 mb-1">{stat.title}</p>
                  <p className="text-3xl font-bold">{stat.value}</p>
                </div>
                <div className={`${stat.color} text-white p-3 rounded-lg`}>
                  {stat.icon}
                </div>
              </div>
            </Link>
          ))}
        </div>

        {/* Quick Actions */}
        <div className="card mb-8">
          <h3 className="text-xl font-bold mb-4">Quick Actions</h3>
          <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
            <Link
              href="/dashboard/forms/new"
              className="flex items-center gap-3 p-4 border-2 border-dashed border-gray-300 rounded-lg hover:border-primary-500 hover:bg-primary-50 transition-colors"
            >
              <Plus className="w-6 h-6 text-primary-600" />
              <div>
                <div className="font-medium">Create New Form</div>
                <div className="text-sm text-gray-600">Build a lead generation form</div>
              </div>
            </Link>

            <Link
              href="/dashboard/landing-pages/new"
              className="flex items-center gap-3 p-4 border-2 border-dashed border-gray-300 rounded-lg hover:border-primary-500 hover:bg-primary-50 transition-colors"
            >
              <Plus className="w-6 h-6 text-primary-600" />
              <div>
                <div className="font-medium">Create Landing Page</div>
                <div className="text-sm text-gray-600">Design a landing page</div>
              </div>
            </Link>

            <Link
              href="/dashboard/settings"
              className="flex items-center gap-3 p-4 border-2 border-dashed border-gray-300 rounded-lg hover:border-primary-500 hover:bg-primary-50 transition-colors"
            >
              <Settings className="w-6 h-6 text-primary-600" />
              <div>
                <div className="font-medium">Account Settings</div>
                <div className="text-sm text-gray-600">Manage your account</div>
              </div>
            </Link>
          </div>
        </div>

        {/* Subscription Info */}
        <div className="card">
          <h3 className="text-xl font-bold mb-4">Your Plan: {user.subscription_plan}</h3>
          <div className="space-y-2 mb-4">
            <div className="flex justify-between">
              <span>Forms Created:</span>
              <span className="font-medium">{user.forms_created}</span>
            </div>
            <div className="flex justify-between">
              <span>Landing Pages Created:</span>
              <span className="font-medium">{user.landing_pages_created}</span>
            </div>
            <div className="flex justify-between">
              <span>Leads This Month:</span>
              <span className="font-medium">{user.leads_this_month}</span>
            </div>
          </div>
          {user.subscription_plan === 'FREE' && (
            <Link href="/dashboard/upgrade" className="btn btn-primary w-full">
              Upgrade to Pro
            </Link>
          )}
        </div>
      </div>
    </div>
  );
}
