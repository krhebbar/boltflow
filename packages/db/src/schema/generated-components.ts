import { pgTable, uuid, text, timestamp } from 'drizzle-orm/pg-core'
import { jobs } from './jobs'

export const generatedComponents = pgTable('generated_components', {
  id: uuid('id').defaultRandom().primaryKey(),
  jobId: uuid('job_id').references(() => jobs.id).notNull(),
  componentType: text('component_type').notNull(),
  filename: text('filename').notNull(),
  content: text('content').notNull(),
  createdAt: timestamp('created_at').defaultNow().notNull(),
})

export type GeneratedComponent = typeof generatedComponents.$inferSelect
export type NewGeneratedComponent = typeof generatedComponents.$inferInsert
