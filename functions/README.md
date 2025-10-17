# Genkit Flows – How to add, run, test and deploy

This guide explains how to create new Genkit flows in the `functions/` workspace, run them locally with the Genkit Developer UI, call them from Flutter or HTTP, and deploy to Firebase Functions.

## 1) Project layout and runtime

```
functions/
  src/
    genkit-sample.ts         # example flow + onCall wrapper (Dev UI entry)
    index.ts                 # Firebase Functions bootstrap (reserved)
  genkit.json                # Genkit config (plugins, default model, log level)
  package.json               # scripts (genkit:start, build, deploy, ...)
  tsconfig.json
```

- Node runtime: Node 22 (see `package.json` → engines.node)
- Default model and plugins: configured in `genkit.json` (e.g. `googleai/gemini-2.0-flash-exp`)
- Dev UI entry: `npm run genkit:start` runs `genkit start -- tsx --watch src/genkit-sample.ts`
  - The file passed to Genkit must import or define the flows you want to test.

## 2) Prerequisites

- Node.js 20+ (22 recommended as configured)
- Install deps inside `functions/`:

```bash
cd functions
npm ci
```

- Google AI API key (Gemini). For local dev, set an env var:

```bash
export GOOGLE_GENAI_API_KEY=YOUR_KEY
```

For production (Cloud Functions), store it as a secret once per project:

```bash
firebase functions:secrets:set GOOGLE_GENAI_API_KEY
```

Then grant the secret to any exported `onCallGenkit` function (see examples below).

## 3) Creating a new flow

Add a new TypeScript module under `src/`, define a flow, and (optionally) export a Firebase callable function via `onCallGenkit`.

Minimal template (structured output ready):

```ts
// src/my-new-flow.ts
import { genkit, z } from "genkit";
import { googleAI } from "@genkit-ai/google-genai";
import { onCallGenkit } from "firebase-functions/https";
import { defineSecret } from "firebase-functions/params";

// Access secret in production (optional for local dev env vars)
const apiKey = defineSecret("GOOGLE_GENAI_API_KEY");

const ai = genkit({
  plugins: [googleAI()],
  // Optional: set/override defaults here
});

// Example structured schema with Zod
const OutputSchema = z.object({
  title: z.string(),
  summary: z.string(),
});

export const myNewFlow = ai.defineFlow(
  {
    name: "myNewFlow",
    inputSchema: z.object({ topic: z.string() }),
    outputSchema: OutputSchema,
  },
  async (input) => {
    const { output } = await ai.generate({
      prompt: `Write a short brief about ${input.topic}`,
      output: { schema: OutputSchema },
    });
    if (!output) throw new Error("Model did not return structured output");
    return output;
  }
);

// Optional: expose as a callable Firebase Function
export const myNew = onCallGenkit({
  // enforceAppCheck: true,           // enable if you use App Check
  // authPolicy: hasClaim("email_verified"), // require specific claims if needed
  secrets: [apiKey],
}, myNewFlow);
```

Important:
- Use unique `name` for each flow.
- Keep flows lightweight; push heavy logic into helpers.
- To appear in Dev UI, ensure your flow file is imported by the entry file (`src/genkit-sample.ts` or a central `src/flows.ts`).

## 4) Structured output with Zod (recommended)

```ts
const RecipeSchema = z.object({
  title: z.string(),
  ingredients: z.array(z.string()),
});

const { output } = await ai.generate({
  prompt: "Generate a simple recipe.",
  output: { schema: RecipeSchema },
});
```

- Guarantees typed output.
- Add `.describe()` to fields to steer the model.
- Consider `z.coerce.number()` for numeric fields to reduce schema failures.

## 5) Streaming flows

```ts
const streamFlow = ai.defineFlow(
  {
    name: "streamFlow",
    inputSchema: z.string(),
    streamSchema: z.string(),
    outputSchema: z.string(),
  },
  async (topic, { sendChunk }) => {
    const { stream, response } = ai.generateStream({
      prompt: `Live brainstorm on ${topic}`,
    });

    for await (const chunk of stream) sendChunk(chunk.text);
    return (await response).text;
  }
);
```

- `onCallGenkit` automatically streams to the client.

## 6) Running locally with the Dev UI

Start the UI from `functions/`:

```bash
npm run genkit:start
```

- Browser opens at `http://localhost:4000`.
- The file after `--` (currently `src/genkit-sample.ts`) must import your new flow module:

```ts
// src/genkit-sample.ts
import "./my-new-flow";      // ensure flow is registered
// (existing sample flow definitions can remain)
```

## 7) Calling flows

### From Flutter (Firebase Callable)

```dart
import 'package:cloud_functions/cloud_functions.dart';

final HttpsCallable callable =
    FirebaseFunctions.instance.httpsCallable('myNew');

final result = await callable.call({'topic': 'card-based games'});
print(result.data); // typed JSON from OutputSchema
```

- Make sure you deployed the callable function (see Deploy section).
- For streaming in Flutter, use HTTPS functions with server-sent events or polling; callable functions return final payloads.

### From HTTP (Dev/testing)

If you expose a plain HTTP endpoint (e.g. via `express`), you can also invoke flows from HTTP. With `onCallGenkit`, prefer the Firebase Functions client shown above.

## 8) Secrets & environment

- Local dev: `GOOGLE_GENAI_API_KEY` env var.
- Prod: create secret once:

```bash
firebase functions:secrets:set GOOGLE_GENAI_API_KEY
```

Then list it in the function wrapper:

```ts
export const myNew = onCallGenkit({ secrets: [apiKey] }, myNewFlow);
```

## 9) Observability

- `enableFirebaseTelemetry()` is used (see `src/genkit-sample.ts`) for metrics, traces, logs.
- `genkit.json` → `logLevel: "debug"` (set to `info`/`warn` in prod as needed).
- Use the Dev UI to inspect runs, traces, and streamed chunks.

## 10) Deployment (Firebase Functions)

Build and deploy from `functions/`:

```bash
npm run deploy
```

or:

```bash
npm run build
firebase deploy --only functions
```

Checklist before deploy:
- [ ] New flow file exported via `onCallGenkit` (if you need a callable)
- [ ] Secret configured and attached to function(s)
- [ ] Dev UI entry imports your flow during local testing
- [ ] Lints/build are clean

## 11) Model selection

- Global default can be set in `genkit.json` → `model`.
- Per-call overrides:

```ts
import { googleAI } from "@genkit-ai/google-genai";

await ai.generate({
  model: googleAI.model('gemini-2.5-flash'),
  prompt: '...'
});
```

or a string ID:

```ts
await ai.generate({
  model: 'googleai/gemini-2.5-flash',
  prompt: '...'
});
```

## 12) Common pitfalls

- Flow not showing in Dev UI → the entry file doesn’t import your module.
- 401/permission errors → secret not granted or missing API key.
- Callable name mismatch → exported function name must match the client.
- Type errors in output → relax schema with `z.coerce.*` or retry logic.
- Streaming not visible → ensure `streamSchema` is set and `sendChunk` is called.

## 13) Example: add and test a new flow quickly

1) Create `src/my-new-flow.ts` with the template above.
2) Add `import "./my-new-flow";` to `src/genkit-sample.ts`.
3) Run `npm run genkit:start` and open Dev UI → run `myNewFlow`.
4) Deploy with `npm run deploy` and call from Flutter via callable `myNew`.

## 14) Using @google/genai (advanced, optional)

When you need lower-level access to Google AI capabilities that are not yet surfaced by Genkit plugins, you can use the official `@google/genai` SDK inside your functions or helpers. Keep Genkit flows as your orchestration boundary and call `@google/genai` for narrow, advanced tasks; return typed results back through the flow using Zod schemas.

- When to prefer Genkit
  - Flow orchestration, structured I/O with Zod, streaming via `defineFlow` + `sendChunk`, Dev UI previews, tracing/telemetry, Firebase Functions integration and secrets.

- When to consider `@google/genai`
  - Specialized modules such as `files` (file upload/management), `chats` (stateful sessions), `live` (realtime), `models` (model metadata), `tokens` (token counting), `tunings` (tuning operations), and `music` (audio). See the official modules reference for APIs and usage.

- Reference
  - Official modules docs: [@google/genai Modules](https://googleapis.github.io/js-genai/release_docs/modules.html)

Guidance
- Keep your flow function small; push the low-level `@google/genai` calls into a `src/helpers/` module and import that from the flow. This keeps flows testable and observable while enabling advanced features.
- Continue to return typed outputs to callers (Flutter, HTTP) using Genkit’s `outputSchema` to enforce structure even when using low-level APIs internally.

---

Questions or improvements? Add more flows under `src/` and import them into the Dev UI entry. Keep structured output and streaming where it adds value.
