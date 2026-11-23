# MP Hardening Plan — decisions & work items

> Source: 12-question user interview (2026-11-25) after the full MP audit.
> Status: **APPROVED — awaiting session claim.** New dedicated MP session
> (not folded into Session A/B/C).

## Locked decisions

| # | Topic | Decision |
|---|-------|----------|
| 1 | Platform gate | Show MP button disabled with **"Android only"** hint on non-Android builds (desktop/web) — no dead-end lobby flow |
| 2 | Cross-platform MP | **Deferred** ("later") — Android-only is current scope |
| 3 | Host migration | **No promotion** — host leave = session ends; peer restores own run. Document as accepted limitation |
| 4 | Peer edit trust | **Keep open trust** — full mutual inventory editing, no guardrails |
| 5 | Dead code | **Cut both now** — `sessionEvents` log + `sendPeerRemove` API (incl. their tests) |
| 6 | Reconnect UX | **Escalating hint + Leave MP button** in the banner after prolonged unreachability |
| 7 | Transport security | **Simple shared-secret check** — per-session token in `MpHello`, validated on `MpSnapshot`; backward-compatible (absent token = legacy peer, allowed) |
| 8 | Quick-add MP seam test | **Session B as planned** — not in this batch |
| 9 | Work landing | **New MP hardening session** — this doc is its spec |
| 10 | Extra MP UI (RTT chip etc.) | **No extra UI** — chrome stays minimal |

## Work items

### MP-1 — Platform gate (small)
- `lib/screens/main_menu_screen.dart` (~line 270): Multiplayer button → on
  `!Platform.isAndroid && !kIsWeb-android` show disabled state + "ANDROID ONLY"
  subtitle instead of pushing `MpLobbyScreen`.
- Helper: single `bool get isMpSupported` (probably in `mp_link.dart` or a
  small util) so lobby/connect can also guard deep-links.
- Verify: `flutter test` widget test asserting disabled state on
  `debugDefaultTargetPlatformOverride = TargetPlatform.windows` (and web if
  testable); Android path unchanged.

### MP-2 — Shared-secret session token (medium)
- `MpSession`: generate a random token at session start (`Random.secure()`),
  expose to `MpSync.setSessionMeta`-style path or hello params.
- `MpHello`: add optional `sessionToken` field (wire-compatible — old peers
  ignore it; `fromJson` defaults `''`).
- `MpSnapshot`: add optional `token` echo field; receiver compares against
  stored peer token **only when peer hello carried one** — mismatch → drop
  snapshot + surface sync error (don't kill session on first mismatch? decide
  during impl: drop-and-count, error after N).
- Rationale (documented): blocks non-app/random injectors; an accepted peer
  sees the hello anyway, so this is hygiene not real auth — user accepted
  "simple" scope explicitly.
- Tests: `mp_protocol_v3`/`mp_wire_contract` style — token round-trips,
  mismatch drops, absent-token legacy peer still works.

### MP-3 — Dead code cut (small)
- Remove `MpSession.sessionEvents` + `logEvent` + call sites
  (`player_page._transferDirect`, `mp_session` internal logs ~518/653/750).
- Remove `sendPeerRemove` (zero callers). Keep `sendPeerClear` (used).
- Remove `MpEvent` class + `mp_session_experience_test` event-log group IF
  nothing else uses `MpEvent` — verify with grep first.
- `mp.is_paired` stays in `MpStore` cleanup list (hygiene for old installs).

### MP-4 — Reconnect banner Leave MP (small)
- `lib/widgets/mp_reconnect_banner.dart`: after elapsed ≥ threshold
  (suggest 120s, tune with existing escalation cadence), show a "LEAVE MP"
  action → `session.cancel()` (same path as menu Leave MP).
- Keep manual cancel primary; button is an accelerant not a replacement.

### MP-5 — Docs
- `docs/TECHNICAL_REFERENCE.md` MP section: threat model note (plaintext
  Nearby Connections accepted; session token = injector hygiene; proximity +
  acceptance prompt is the real gate) + host-migration limitation +
  Android-only scope.
- `AGENT_STATUS.md` session log row on completion.

## Verify
- `flutter analyze` 0 issues
- MP suites: `test/mp_*` + `test/widget/mp_*` + `paradox_widgets_test`
- Full `flutter test` green
- `VERSION_HISTORY.md` Unreleased entry (user-visible: Android-only label,
  reconnect leave button; internal: token + dead-code cut)

## Explicitly out of scope
- iOS/desktop/web transport, host promotion, >2 players, RTT UI, chat,
  payload signing/HMAC, quick-add MP seam test (Session B).
