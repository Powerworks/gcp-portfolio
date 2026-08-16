import { defineCollection, z } from 'astro:content';

const projects = defineCollection({
  type: 'content',
  schema: z.object({
    title: z.string(),
    subtitle: z.string(),
    category: z.enum(['Architecture', 'AI']),
    client: z.string().optional(),
    repoUrl: z.string().url().optional(),
    tech: z.array(z.string()),
    order: z.number().optional(), // We'll use this to control layout order safely
  }),
});

const experience = defineCollection({
  type: 'content',
  schema: z.object({
    title: z.string(),
    company: z.string(),
    location: z.string(),
    startDate: z.string(),
    endDate: z.string(),
    current: z.boolean(),
    tech: z.array(z.string()),
  }),
});

export const collections = { projects, experience };