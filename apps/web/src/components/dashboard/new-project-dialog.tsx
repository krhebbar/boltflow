"use client"

import { useState } from "react"
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"

export function NewProjectDialog({ onClose }: { onClose?: () => void }) {
  const [url, setUrl] = useState("")
  const [maxPages, setMaxPages] = useState(10)
  const [loading, setLoading] = useState(false)

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    setLoading(true)

    try {
      // TODO: Connect to API
      const response = await fetch('/api/scraper/start', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ url, max_pages: maxPages, screenshot: true })
      })

      const data = await response.json()
      console.log('Migration started:', data)
      onClose?.()
    } catch (error) {
      console.error('Failed to start migration:', error)
    } finally {
      setLoading(false)
    }
  }

  return (
    <Card className="w-full max-w-2xl mx-auto">
      <CardHeader>
        <CardTitle>New Migration Project</CardTitle>
        <CardDescription>
          Enter the URL of the website you want to migrate to a modern stack
        </CardDescription>
      </CardHeader>
      <CardContent>
        <form onSubmit={handleSubmit} className="space-y-4">
          <div className="space-y-2">
            <label htmlFor="url" className="text-sm font-medium">
              Website URL
            </label>
            <Input
              id="url"
              type="url"
              placeholder="https://example.com"
              value={url}
              onChange={(e) => setUrl(e.target.value)}
              required
            />
          </div>

          <div className="space-y-2">
            <label htmlFor="maxPages" className="text-sm font-medium">
              Maximum Pages to Scrape
            </label>
            <Input
              id="maxPages"
              type="number"
              min={1}
              max={100}
              value={maxPages}
              onChange={(e) => setMaxPages(parseInt(e.target.value))}
              required
            />
            <p className="text-xs text-muted-foreground">
              Limit the number of pages to analyze (1-100)
            </p>
          </div>

          <div className="flex gap-3 pt-4">
            <Button type="submit" disabled={loading} className="flex-1">
              {loading ? "Starting Migration..." : "Start Migration"}
            </Button>
            {onClose && (
              <Button type="button" variant="outline" onClick={onClose}>
                Cancel
              </Button>
            )}
          </div>
        </form>
      </CardContent>
    </Card>
  )
}
