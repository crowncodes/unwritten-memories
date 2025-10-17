interface CacheRecord<T> {
  value: T;
  expiresAt: number;
}

const cache = new Map<string, CacheRecord<unknown>>();

export function cacheGet<T = unknown>(key: string): T | null {
  const rec = cache.get(key);
  if (!rec) return null;
  if (rec.expiresAt < Date.now()) {
    cache.delete(key);
    return null;
  }
  return rec.value as T;
}

export function cacheSet<T = unknown>(key: string, value: T, ttlMs: number): void {
  cache.set(key, { value, expiresAt: Date.now() + ttlMs });
}


