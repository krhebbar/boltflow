import { pgTable, uuid, text, timestamp, jsonb } from 'drizzle-orm/pg-core'
import { jobs } from './jobs'

export const scrapedPages = pgTable('scraped_pages', {
  id: uuid('id').defaultRandom().primaryKey(),
  jobId: uuid('job_id').references(() => jobs.id).notNull(),
  url: text('url').notNull(),
  html: text('html'),
  css: text('css'),
  screenshot: text('screenshot'),
  metadata: jsonb('metadata'),
  scrapedAt: timestamp('scraped_at').defaultNow().notNull(),
})

export type ScrapedPage = typeof scrapedPages.$inferSelect
export type NewScrapedPage = typeof scrapedPages.$inferInsert
