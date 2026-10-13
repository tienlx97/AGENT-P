# Routing policy — implemented Phase 3

Current implemented lane: explicit FE/BE selection, explicit Claude/Codex selection,
one bounded worker, independent worktree, no manager call and no automatic retry.
The native launch path now applies codingOfficePolicy.ts before dispatch.
The exact edit lane uses zero workers and scoped checks. Explicit tiers are accepted,
but elevated risk cannot be downgraded to XS/S.

The implemented non-model rules use these limits:

| Tier | Default work | Model workers | Automatic retry ceiling |
| --- | --- | --- | --- |
| XS | Unique exact edit or one local coder | 0–1 | 1 |
| S | Local component/validation change | 1 | 2 |
| M | Scoped API or multi-file change | Relevant coders; review by risk | 2 |
| L | Cross-repo contract/architecture change | Michael and only necessary specialists | 3 |

Explicit paths/repository intent decide FE or BE. Both means separate linked tasks,
not access to a combined checkout. Ambiguous repository or destructive scope is
held for human clarification. Auth, permission, privacy, payments, data deletion,
migrations and infrastructure override a small textual diff's low-risk classification.
The user-selected payment-stage feature is a cross-repo payment-domain change;
it is not XS even if the final UI diff is small.

No classification LLM is enabled. No entire roster is activated for copy changes.
No scheduled standup, heartbeat model call or idle animation model call is required.
Deterministic editing will require a specific file, exactly one matching UI context,
a dry-run, a restricted path and checks; the native exact button-label lane implements these checks.

Actual Phase 1 Codex read-only smoke attempts used approximately 31–35k total
tokens, including roughly 24–28k cached input. Native CLI context can exceed the
plan's illustrative XS cap before the edit begins. Do not claim a 3–6k XS budget
passed: the demonstrated deterministic XS edit used zero tokens. CLI runs have observed
token caps, item-step limits and wall-clock bounds; streamed total usage may arrive
only at turn completion, so token caps can overshoot before a stop is observed.
Invoice spend and unobserved model names remain `unknown`.

Observed CLI input includes large cached system/repository context: even a read-only smoke task used 31–35k total tokens. Final raw-token caps are calibrated to that evidence: XS 150k (exact edit still zero), S 500k, M 1.5m, L 3m across each continuation chain, with step limits 8/25/80/200 and times 60/180/600/1800 seconds. These are bounded raw counters, not promises of low subscription spend. Report cached and fresh work separately; the earlier Phase 4 500k cap and its overrun remain recorded unchanged in those historical runs. No classification model or automatic retries were enabled.

Continuation sums measured usage from all ancestor attempts, rejects unknown/cyclic history, and passes only the remaining token allowance to the next worker. Full code completion now requires a repository gate and fresh-input user acceptance.
