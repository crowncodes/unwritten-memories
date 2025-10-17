import neo4j, { Driver, Session } from 'neo4j-driver';
import { defineSecret } from 'firebase-functions/params';

const NEO4J_URI = defineSecret('NEO4J_URI');
const NEO4J_USER = defineSecret('NEO4J_USER');
const NEO4J_PASSWORD = defineSecret('NEO4J_PASSWORD');

let driver: Driver | null = null;

export function getDriver(): Driver {
  if (driver) return driver;
  const uri = NEO4J_URI.value();
  const user = NEO4J_USER.value();
  const password = NEO4J_PASSWORD.value();
  driver = neo4j.driver(uri, neo4j.auth.basic(user, password), { disableLosslessIntegers: true });
  return driver;
}

export async function runCypher<T = unknown>(query: string, params?: Record<string, unknown>): Promise<T[]> {
  const drv = getDriver();
  let session: Session | null = null;
  try {
    session = drv.session();
    const res = await session.run(query, params);
    return res.records.map((r) => (r.toObject() as unknown) as T);
  } finally {
    await session?.close();
  }
}


