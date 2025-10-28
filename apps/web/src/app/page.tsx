import Link from 'next/link'
import { Button } from '@/components/ui/button'

export default function Home() {
  return (
    <main className="flex min-h-screen flex-col items-center justify-center p-24">
      <div className="z-10 max-w-5xl w-full items-center justify-between font-mono text-sm">
        <div className="text-center space-y-6">
          <h1 className="text-6xl font-bold bg-gradient-to-r from-blue-600 to-purple-600 bg-clip-text text-transparent">
            ⚡ Boltflow
          </h1>
          <p className="text-2xl text-muted-foreground">
            AI-Driven Web Migration System
          </p>
          <p className="text-lg max-w-2xl mx-auto">
            Transform legacy websites into modern, production-ready applications
            using AI-powered analysis, component generation, and automated deployment.
          </p>
          <div className="flex gap-4 justify-center mt-8">
            <Link href="/dashboard">
              <Button size="lg">
                Get Started
              </Button>
            </Link>
            <Link href="/docs">
              <Button variant="outline" size="lg">
                View Documentation
              </Button>
            </Link>
          </div>
        </div>
      </div>
    </main>
  )
}
