'use client'

import { createContext, useContext, useState, useEffect, ReactNode } from 'react'
import api from './api'

interface User {
  id: string
  email: string
  username: string
  full_name: string
  company_name: string
  industry: string
  is_verified: boolean
  qr_code_count: number
  subscription_name: string
  qr_code_limit: number
  scan_limit: number
  created_at: string
}

interface AuthContextType {
  user: User | null
  loading: boolean
  login: (email: string, password: string) => Promise<void>
  register: (data: RegisterData) => Promise<void>
  logout: () => void
  updateProfile: (data: Partial<User>) => Promise<void>
}

interface RegisterData {
  email: string
  username: string
  password: string
  password_confirm: string
  full_name?: string
  company_name?: string
  industry?: string
}

const AuthContext = createContext<AuthContextType | undefined>(undefined)

export function AuthProvider({ children }: { children: ReactNode }) {
  const [user, setUser] = useState<User | null>(null)
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    loadUser()
  }, [])

  const loadUser = async () => {
    try {
      const token = localStorage.getItem('access_token')
      if (token) {
        const response = await api.get('/auth/profile/')
        setUser(response.data)
      }
    } catch (error) {
      console.error('Failed to load user:', error)
      localStorage.removeItem('access_token')
      localStorage.removeItem('refresh_token')
    } finally {
      setLoading(false)
    }
  }

  const login = async (email: string, password: string) => {
    const response = await api.post('/auth/login/', { email, password })
    const { user, tokens } = response.data

    localStorage.setItem('access_token', tokens.access)
    localStorage.setItem('refresh_token', tokens.refresh)
    setUser(user)
  }

  const register = async (data: RegisterData) => {
    const response = await api.post('/auth/register/', data)
    const { user, tokens } = response.data

    localStorage.setItem('access_token', tokens.access)
    localStorage.setItem('refresh_token', tokens.refresh)
    setUser(user)
  }

  const logout = () => {
    localStorage.removeItem('access_token')
    localStorage.removeItem('refresh_token')
    setUser(null)
  }

  const updateProfile = async (data: Partial<User>) => {
    const response = await api.put('/auth/profile/', data)
    setUser(response.data)
  }

  return (
    <AuthContext.Provider value={{ user, loading, login, register, logout, updateProfile }}>
      {children}
    </AuthContext.Provider>
  )
}

export function useAuth() {
  const context = useContext(AuthContext)
  if (context === undefined) {
    throw new Error('useAuth must be used within an AuthProvider')
  }
  return context
}
