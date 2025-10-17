export interface AuthContext {
  uid?: string;
  token?: Record<string, unknown>;
  rawToken?: string;
}

export interface RoutingContext {
  tier?: 'free' | 'premium';
  model?: string;
  thinkingEnabled?: boolean;
  manyShotEnabled?: boolean;
}

export interface RequestMetaContext {
  requestId?: string;
  promptHash?: string;
  cardId?: string;
  interactionId?: string;
  locationId?: string;
}

export interface RetrievalContext {
  topK?: number;
  filters?: Record<string, unknown>;
  snippets?: Array<{ id: string; text: string; score?: number }>;
}

export interface SafetyContext {
  enabled?: boolean;
  categories?: string[];
}

export interface BudgetContext {
  maxInputTokens?: number;
  maxOutputTokens?: number;
}

export interface PromptHints {
  suggestions?: string[];
}

export interface LifebondContext {
  auth?: AuthContext;
  session?: Record<string, unknown>;
  routing?: RoutingContext;
  requestMeta?: RequestMetaContext;
  retrieval?: RetrievalContext;
  safety?: SafetyContext;
  budgets?: BudgetContext;
  promptHints?: PromptHints;
}

export function buildContext(base?: Partial<LifebondContext>, overrides?: Partial<LifebondContext>): LifebondContext {
  return {
    auth: { ...(base?.auth || {}), ...(overrides?.auth || {}) },
    session: { ...(base?.session || {}), ...(overrides?.session || {}) },
    routing: { ...(base?.routing || {}), ...(overrides?.routing || {}) },
    requestMeta: { ...(base?.requestMeta || {}), ...(overrides?.requestMeta || {}) },
    retrieval: { ...(base?.retrieval || {}), ...(overrides?.retrieval || {}) },
    safety: { ...(base?.safety || {}), ...(overrides?.safety || {}) },
    budgets: { ...(base?.budgets || {}), ...(overrides?.budgets || {}) },
    promptHints: { ...(base?.promptHints || {}), ...(overrides?.promptHints || {}) },
  };
}


