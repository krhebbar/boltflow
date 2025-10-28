import { DashboardShell } from "@/components/dashboard/shell"
import { MigrationProgress } from "@/components/dashboard/migration-progress"
import { Button } from "@/components/ui/button"
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import Link from "next/link"

export default function ProjectDetailsPage({ params }: { params: { id: string } }) {
  // TODO: Fetch project details from API
  const project = {
    id: params.id,
    name: "Example Migration",
    url: "https://example.com",
    status: "analyzing",
    createdAt: new Date().toISOString(),
  }

  return (
    <DashboardShell>
      <div className="flex flex-col gap-6">
        <div className="flex items-center justify-between">
          <div>
            <h2 className="text-3xl font-bold">{project.name}</h2>
            <p className="text-muted-foreground">{project.url}</p>
          </div>
          <Link href="/dashboard">
            <Button variant="outline">Back to Dashboard</Button>
          </Link>
        </div>

        <div className="grid gap-6 md:grid-cols-2">
          <MigrationProgress projectId={params.id} />

          <Card>
            <CardHeader>
              <CardTitle>Project Information</CardTitle>
              <CardDescription>Details about this migration project</CardDescription>
            </CardHeader>
            <CardContent className="space-y-4">
              <div className="grid grid-cols-2 gap-2 text-sm">
                <div className="text-muted-foreground">Project ID</div>
                <div className="font-mono">{project.id}</div>

                <div className="text-muted-foreground">Source URL</div>
                <div className="truncate">{project.url}</div>

                <div className="text-muted-foreground">Status</div>
                <div className="capitalize">{project.status}</div>

                <div className="text-muted-foreground">Created</div>
                <div>{new Date(project.createdAt).toLocaleString()}</div>
              </div>

              <div className="pt-4 space-y-2">
                <Button className="w-full" variant="outline">
                  View Generated Code
                </Button>
                <Button className="w-full" variant="outline">
                  Download Project
                </Button>
                <Button className="w-full" variant="outline">
                  Deploy to Vercel
                </Button>
              </div>
            </CardContent>
          </Card>
        </div>

        <Card>
          <CardHeader>
            <CardTitle>Extracted Components</CardTitle>
            <CardDescription>
              Components detected and generated from the source website
            </CardDescription>
          </CardHeader>
          <CardContent>
            <div className="text-sm text-muted-foreground text-center py-8">
              Component analysis in progress...
            </div>
          </CardContent>
        </Card>
      </div>
    </DashboardShell>
  )
}
