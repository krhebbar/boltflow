"use client"

import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { Badge } from "@/components/ui/badge"
import { Button } from "@/components/ui/button"

interface ProjectCardProps {
  project: {
    id: string
    name: string
    url: string
    status: "analyzing" | "generating" | "deploying" | "completed" | "error"
    progress: number
    createdAt: string
  }
  onView: (id: string) => void
}

export function ProjectCard({ project, onView }: ProjectCardProps) {
  const getStatusBadge = () => {
    switch (project.status) {
      case "completed":
        return <Badge variant="success">Completed</Badge>
      case "error":
        return <Badge variant="destructive">Error</Badge>
      case "analyzing":
      case "generating":
      case "deploying":
        return <Badge variant="default">In Progress</Badge>
      default:
        return <Badge variant="outline">Unknown</Badge>
    }
  }

  return (
    <Card className="hover:border-primary transition-colors">
      <CardHeader>
        <div className="flex items-start justify-between">
          <div className="space-y-1">
            <CardTitle className="text-lg">{project.name}</CardTitle>
            <CardDescription className="text-xs">{project.url}</CardDescription>
          </div>
          {getStatusBadge()}
        </div>
      </CardHeader>
      <CardContent>
        <div className="space-y-3">
          <div className="flex justify-between text-sm">
            <span className="text-muted-foreground">Progress</span>
            <span className="font-medium">{project.progress}%</span>
          </div>
          <div className="flex justify-between text-xs text-muted-foreground">
            <span>Created</span>
            <span>{new Date(project.createdAt).toLocaleDateString()}</span>
          </div>
          <Button
            variant="outline"
            className="w-full"
            onClick={() => onView(project.id)}
          >
            View Details
          </Button>
        </div>
      </CardContent>
    </Card>
  )
}
