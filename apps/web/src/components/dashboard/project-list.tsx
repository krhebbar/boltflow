"use client"

import { useState } from "react"
import { Button } from "@/components/ui/button"
import { ProjectCard } from "./project-card"
import { NewProjectDialog } from "./new-project-dialog"

export function ProjectList() {
  const [showNewProject, setShowNewProject] = useState(false)
  const [projects, setProjects] = useState([
    // Demo data - in production this would come from API/database
    {
      id: "1",
      name: "Example Migration",
      url: "https://example.com",
      status: "analyzing" as const,
      progress: 45,
      createdAt: new Date().toISOString(),
    },
  ])

  const handleViewProject = (id: string) => {
    // TODO: Navigate to project details page
    console.log("View project:", id)
  }

  return (
    <div className="grid gap-6">
      <div className="flex justify-between items-center">
        <h3 className="text-xl font-semibold">Your Projects</h3>
        <Button onClick={() => setShowNewProject(true)}>
          New Project
        </Button>
      </div>

      {showNewProject && (
        <NewProjectDialog onClose={() => setShowNewProject(false)} />
      )}

      {projects.length === 0 ? (
        <div className="border rounded-lg p-8 text-center text-muted-foreground">
          No projects yet. Create your first migration project to get started.
        </div>
      ) : (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
          {projects.map((project) => (
            <ProjectCard
              key={project.id}
              project={project}
              onView={handleViewProject}
            />
          ))}
        </div>
      )}
    </div>
  )
}
