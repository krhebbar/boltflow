import { pgTable, uuid, text, timestamp, real } from 'drizzle-orm/pg-core'

export const componentPatterns = pgTable('component_patterns', {
  id: uuid('id').defaultRandom().primaryKey(),
  type: text('type').notNull(), // header, hero, footer, features, etc.
  htmlSample: text('html_sample'),
  cssSample: text('css_sample'),
  // Note: For pgvector, you would use: vector('embedding', { dimensions: 1536 })
  // For now, using text to store JSON array until pgvector is set up
  embedding: text('embedding'),
  confidenceThreshold: real('confidence_threshold').default(0.8),
  createdAt: timestamp('created_at').defaultNow().notNull(),
})

export type ComponentPattern = typeof componentPatterns.$inferSelect
export type NewComponentPattern = typeof componentPatterns.$inferInsert
