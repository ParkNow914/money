import { Request, Response, NextFunction } from "express";

export interface UserContext {
  id: string;
  role: "user" | "admin" | "partner";
}

declare module "express-serve-static-core" {
  interface Request {
    user?: UserContext;
    fingerprint?: string;
  }
}

const ADMIN_KEY = process.env.ADMIN_API_KEY || "admin";

export function authMiddleware(req: Request, _res: Response, next: NextFunction): void {
  const adminKey = req.header("x-admin-key");
  if (adminKey && adminKey === ADMIN_KEY) {
    req.user = { id: "admin", role: "admin" };
    return next();
  }

  const partnerKey = req.header("x-api-key");
  if (partnerKey && partnerKey === ADMIN_KEY) {
    req.user = { id: `partner-${partnerKey}`, role: "partner" };
    return next();
  }

  const fallbackUser = req.header("x-user-id") || "anon";
  req.user = { id: fallbackUser, role: "user" };
  next();
}
