import { DashboardShell } from '@/components/dashboard/shell'
import { ProjectList } from '@/components/dashboard/project-list'

export default function DashboardPage() {
  return (
    <DashboardShell>
      <div className="flex flex-col gap-8">
        <div>
          <h2 className="text-3xl font-bold">Dashboard</h2>
          <p className="text-muted-foreground">
            Manage your web migration projects
          </p>
        </div>
        <ProjectList />
      </div>
    </DashboardShell>
  )
}
