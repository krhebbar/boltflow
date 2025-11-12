'use client'

import React, { createContext, useContext, useState, useEffect } from 'react'
import { User } from '@/types'
import { api } from '@/lib/api-client'

interface AuthContextType {
  user: User | null
  token: string | null
  login: (email: string, password: string) => Promise<void>
  signup: (email: string, password: string, name?: string) => Promise<void>
  logout: () => void
  isLoading: boolean
}

const AuthContext = createContext<AuthContextType | undefined>(undefined)

export function AuthProvider({ children }: { children: React.ReactNode }) {
  const [user, setUser] = useState<User | null>(null)
  const [token, setToken] = useState<string | null>(null)
  const [isLoading, setIsLoading] = useState(true)

  // Load token and user from localStorage on mount
  useEffect(() => {
    const storedToken = localStorage.getItem('auth_token')
    if (storedToken) {
      api.auth
        .me(storedToken)
        .then((userData) => {
          setUser(userData)
          setToken(storedToken)
        })
        .catch(() => {
          // Token is invalid, clear it
          localStorage.removeItem('auth_token')
        })
        .finally(() => {
          setIsLoading(false)
        })
    } else {
      setIsLoading(false)
    }
  }, [])

  const login = async (email: string, password: string) => {
    const response = await api.auth.login(email, password)
    setUser(response.user)
    setToken(response.access_token)
    localStorage.setItem('auth_token', response.access_token)
  }

  const signup = async (email: string, password: string, name?: string) => {
    const response = await api.auth.signup(email, password, name)
    setUser(response.user)
    setToken(response.access_token)
    localStorage.setItem('auth_token', response.access_token)
  }

  const logout = () => {
    setUser(null)
    setToken(null)
    localStorage.removeItem('auth_token')
  }

  return (
    <AuthContext.Provider value={{ user, token, login, signup, logout, isLoading }}>
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
