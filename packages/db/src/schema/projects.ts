import { pgTable, uuid, text, timestamp, integer } from 'drizzle-orm/pg-core'
import { users } from './users'

export const projects = pgTable('projects', {
  id: uuid('id').defaultRandom().primaryKey(),
  userId: uuid('user_id').references(() => users.id).notNull(),
  name: text('name').notNull(),
  url: text('url').notNull(),
  status: text('status').notNull().default('pending'), // pending, scraping, analyzing, generating, completed, failed
  maxPages: integer('max_pages').default(50),
  createdAt: timestamp('created_at').defaultNow().notNull(),
  updatedAt: timestamp('updated_at').defaultNow().notNull(),
})

export type Project = typeof projects.$inferSelect
export type NewProject = typeof projects.$inferInsert
