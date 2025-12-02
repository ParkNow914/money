import fs from "fs-extra";
import path from "node:path";
import { randomUUID } from "node:crypto";

import { JobRecord } from "../types";

const jobsFile = path.resolve(process.cwd(), "data", "jobs.json");

async function ensureFile(): Promise<void> {
  await fs.ensureDir(path.dirname(jobsFile));
  if (!(await fs.pathExists(jobsFile))) {
    await fs.writeJson(jobsFile, []);
  }
}

export async function createJob(userId: string): Promise<JobRecord> {
  await ensureFile();
  const jobs = (await fs.readJson(jobsFile)) as JobRecord[];
  const now = new Date().toISOString();
  const job: JobRecord = {
    id: randomUUID(),
    status: "pending",
    createdAt: now,
    updatedAt: now,
    userId,
  };
  jobs.push(job);
  await fs.writeJson(jobsFile, jobs, { spaces: 2 });
  return job;
}

export async function updateJob(jobId: string, updates: Partial<JobRecord>): Promise<JobRecord | null> {
  await ensureFile();
  const jobs = (await fs.readJson(jobsFile)) as JobRecord[];
  const idx = jobs.findIndex((job) => job.id === jobId);
  if (idx === -1) return null;
  jobs[idx] = { ...jobs[idx], ...updates, updatedAt: new Date().toISOString() };
  await fs.writeJson(jobsFile, jobs, { spaces: 2 });
  return jobs[idx];
}

export async function getJob(jobId: string): Promise<JobRecord | null> {
  await ensureFile();
  const jobs = (await fs.readJson(jobsFile)) as JobRecord[];
  return jobs.find((job) => job.id === jobId) ?? null;
}
