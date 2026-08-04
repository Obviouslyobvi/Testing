# Test Results — 90-Minute Focus Matrix (AI Edition)

Three tests run on 2026-07-02 against Claude (the prompt is plain markdown with no
platform-specific features, so behavior on ChatGPT/Gemini should track closely;
spot-check there before launch).

## Test A — Paste-in prompt, live multi-turn (happy path)
Persona: Etsy seller, 7-item messy brain dump, energy 3, 90 minutes, phone/Instagram/snack distractions.

- Asked exactly one question per turn, all six questions, zero preamble. ✅
- Matrix scored all 7 tasks; picked product photos (high impact + this-week deadline + energy match) with the waiting customer message folded into Sprint 1. ✅
- Timeline, if–then plans, and Parking Lot all personalized to stated distractions; no invented details. ✅
- **Check-back-in loop:** after a simulated report-back ("stalled in sprint 3 re-editing, snuck phone in break 2"), it correctly diagnosed perfectionism vs. energy, added forced-choice timers, restructured breaks, and pre-planned the next session. ✅

## Test B — SKILL.md file (scripted scenario)
Persona: nonprofit worker, grant report due tomorrow, energy 4, 90 minutes.

- 5/6 audit items passed (one question per turn; four sections in order; sensible pick; 411/450 words; no invented details).
- ⚠️ Flag: markdown pipe table degrades in plain-text clients → fixed by adding a one-task-per-line fallback to both files.

## Test C — Edge case (vague user, low energy, 40 minutes)
Persona: office worker, "idk, stuff for work I guess," energy 2 at 3pm, 40 minutes, open office.

- 6/6 audit items passed:
  - Used exactly 1 of the 2 allowed clarifying follow-ups on the vague brain dump.
  - Scaled to 40 minutes with correct arithmetic (3+11+2+11+2+7+4 = 40), Launch and Shutdown kept.
  - Deep work (performance reviews) scored Poor at energy 2 per the rubric.
  - Deadline-vs-energy tension resolved explicitly (urgent report won; mismatch mitigated with mechanical punch-list steps).

## Known limits
- Word-count margin is tight (~440/450) on multi-distraction users; acceptable.
- The prompt reinterprets impossible rewards ("leaving on time" at 3:40) gracefully rather than literally — desired behavior.
- Free-tier ChatGPT/Gemini were not directly exercised in this environment; the prompt uses no tables-only or platform-specific features after the fallback fix, but do one manual paste-test in each before selling.
