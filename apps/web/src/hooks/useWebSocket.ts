'use client'

import { useEffect, useRef, useState, useCallback } from 'react'
import io, { Socket } from 'socket.io-client'
import type { WebSocketMessage } from '@/types'

const WS_URL = process.env.NEXT_PUBLIC_WS_URL || 'ws://localhost:8000'

export function useWebSocket(clientId: string) {
  const [isConnected, setIsConnected] = useState(false)
  const [lastMessage, setLastMessage] = useState<WebSocketMessage | null>(null)
  const socketRef = useRef<Socket | null>(null)
  const handlersRef = useRef<Map<string, (data: unknown) => void>>(new Map())

  useEffect(() => {
    // Initialize Socket.io client
    const socket = io(WS_URL, {
      path: `/ws/${clientId}`,
      transports: ['websocket'],
      reconnection: true,
      reconnectionDelay: 1000,
      reconnectionAttempts: 5,
    })

    socketRef.current = socket

    socket.on('connect', () => {
      console.log('WebSocket connected')
      setIsConnected(true)
    })

    socket.on('disconnect', () => {
      console.log('WebSocket disconnected')
      setIsConnected(false)
    })

    socket.on('message', (data: WebSocketMessage) => {
      setLastMessage(data)

      // Call registered handlers for this message type
      const handler = handlersRef.current.get(data.type)
      if (handler) {
        handler(data)
      }
    })

    socket.on('error', (error) => {
      console.error('WebSocket error:', error)
    })

    return () => {
      socket.disconnect()
    }
  }, [clientId])

  const on = useCallback((eventType: string, handler: (data: unknown) => void) => {
    handlersRef.current.set(eventType, handler)
  }, [])

  const off = useCallback((eventType: string) => {
    handlersRef.current.delete(eventType)
  }, [])

  const send = useCallback((data: unknown) => {
    if (socketRef.current?.connected) {
      socketRef.current.emit('message', data)
    }
  }, [])

  return {
    isConnected,
    lastMessage,
    on,
    off,
    send,
  }
}
