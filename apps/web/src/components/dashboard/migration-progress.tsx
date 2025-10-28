"use client"

import { useEffect, useState } from "react"
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { Progress } from "@/components/ui/progress"
import { Badge } from "@/components/ui/badge"

interface MigrationStep {
  name: string
  status: "pending" | "in_progress" | "completed" | "error"
  progress?: number
  message?: string
}

interface MigrationProgressProps {
  projectId: string
}

export function MigrationProgress({ projectId }: MigrationProgressProps) {
  const [steps, setSteps] = useState<MigrationStep[]>([
    { name: "Web Scraping", status: "pending" },
    { name: "DOM Analysis", status: "pending" },
    { name: "Component Classification", status: "pending" },
    { name: "Code Generation", status: "pending" },
    { name: "CMS Setup", status: "pending" },
    { name: "Deployment", status: "pending" },
  ])

  useEffect(() => {
    // TODO: Connect to WebSocket for real-time updates
    // const socket = io('http://localhost:8000')
    // socket.on('progress', (data) => { ... })

    // Simulate progress for demo
    const timer = setInterval(() => {
      setSteps(prev => {
        const currentIndex = prev.findIndex(s => s.status === "in_progress")
        const nextIndex = currentIndex === -1 ? 0 : currentIndex

        if (nextIndex >= prev.length) return prev

        return prev.map((step, idx) => {
          if (idx < nextIndex) return { ...step, status: "completed" as const }
          if (idx === nextIndex) {
            const progress = (step.progress || 0) + 10
            if (progress >= 100) {
              return { ...step, status: "completed" as const, progress: 100 }
            }
            return { ...step, status: "in_progress" as const, progress }
          }
          return step
        })
      })
    }, 1000)

    return () => clearInterval(timer)
  }, [projectId])

  const getStatusBadge = (status: MigrationStep["status"]) => {
    switch (status) {
      case "completed":
        return <Badge variant="success">Completed</Badge>
      case "in_progress":
        return <Badge variant="default">In Progress</Badge>
      case "error":
        return <Badge variant="destructive">Error</Badge>
      default:
        return <Badge variant="outline">Pending</Badge>
    }
  }

  return (
    <Card>
      <CardHeader>
        <CardTitle>Migration Progress</CardTitle>
        <CardDescription>
          Real-time status of your website migration
        </CardDescription>
      </CardHeader>
      <CardContent className="space-y-4">
        {steps.map((step, idx) => (
          <div key={idx} className="space-y-2">
            <div className="flex items-center justify-between">
              <div className="flex items-center gap-3">
                <span className="text-sm font-medium">{step.name}</span>
                {getStatusBadge(step.status)}
              </div>
              {step.progress !== undefined && (
                <span className="text-sm text-muted-foreground">
                  {step.progress}%
                </span>
              )}
            </div>
            {step.status === "in_progress" && step.progress !== undefined && (
              <Progress value={step.progress} />
            )}
            {step.message && (
              <p className="text-xs text-muted-foreground">{step.message}</p>
            )}
          </div>
        ))}
      </CardContent>
    </Card>
  )
}
