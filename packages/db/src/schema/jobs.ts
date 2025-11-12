import { pgTable, uuid, text, timestamp, integer, jsonb } from 'drizzle-orm/pg-core'
import { projects } from './projects'

export const jobs = pgTable('jobs', {
  id: uuid('id').defaultRandom().primaryKey(),
  projectId: uuid('project_id').references(() => projects.id).notNull(),
  type: text('type').notNull(), // scrape, analyze, generate, deploy
  status: text('status').notNull().default('pending'), // pending, running, completed, failed
  progress: integer('progress').default(0),
  result: jsonb('result'),
  error: text('error'),
  createdAt: timestamp('created_at').defaultNow().notNull(),
  completedAt: timestamp('completed_at'),
})

export type Job = typeof jobs.$inferSelect
export type NewJob = typeof jobs.$inferInsert
