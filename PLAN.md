# Insurance Verification Caller for Outpatient Clinics

Source idea: https://www.ideabrowser.com/idea/insurance-verification-caller-for-outpatient-clinics

## 1. Problem

Outpatient clinics (PT/OT, behavioral health, dermatology, primary care, imaging, infusion, dental) burn 15–40 hours/week of front-desk time on insurance eligibility & benefits (E&B) verification. The work is:

- **Phone-bound.** 270/271 EDI returns coverage status but rarely the granularity clinics need (exact copay for CPT 99213, visit caps for PT, prior-auth requirements for a specific J-code, accumulators for the patient's plan year). Staff still call the payer.
- **Slow.** 20–45 min average per call; most of it is IVR navigation and hold music.
- **Error-prone.** A missed prior-auth or wrong copay turns into a denied claim or angry patient at the front desk.
- **Bursty.** Volume spikes with the next-day schedule, creating queue-of-shame backlogs that get punted or skipped.

Direct downstream cost: claim denials (5–15% of revenue at risk), patient collections friction, and staff turnover at the front desk.

## 2. ICP (initial customer profile)

Sweet spot for v1:
- Single-specialty outpatient groups, **3–25 providers**, **2–10 locations**.
- High-volume, recurring-visit specialties where re-verification matters: **physical therapy, behavioral health, allergy, infusion, women's health**.
- Already running on a modern PM/EHR with an API: **AthenaHealth, DrChrono, eClinicalWorks, NextGen, Modmed, Tebra (Kareo), Jane** (PT-heavy).
- Currently paying $400–$1,500/seat/month for an offshore VOB (verification of benefits) team, or burning internal FTE time.

Wedge: PT clinics on Jane or WebPT — homogeneous workflows, painful re-verification cadence, vocal community.

## 3. Solution

An AI voice agent that calls payer IVRs and live reps, runs the clinic's verification script, and returns a structured benefits summary back into the PM/EHR.

### Core user flow
1. Clinic submits a queue of patients to verify (CSV upload, EHR sync, or per-appointment trigger from tomorrow's schedule).
2. System matches each patient to the right payer phone tree + script template (specialty + plan + service type).
3. Voice agent dials, navigates IVR, authenticates as the provider, asks the script, captures answers.
4. Structured JSON benefits record is written back to the PM/EHR as a note/attachment, and surfaced in a dashboard with a confidence score and full call recording + transcript.
5. Low-confidence or refused calls are routed to a human-in-the-loop reviewer who can listen + correct in ~60 seconds.

### Output schema (per verification)
- Eligibility: active flag, effective/term dates, plan type, network tier
- Financial: deductible (ind/fam, met/remaining), OOP max (met/remaining), copay, coinsurance — by service code
- Authorization: prior-auth required (Y/N), reference #, referral required, visit limits + used
- Coordination of benefits: primary/secondary, Medicare crossover
- Provenance: payer rep name/ref #, call recording URL, transcript, call duration, confidence per field

## 4. Why now

- Sub-second streaming ASR + TTS + LLM tool-calling stacks (LiveKit Agents, Pipecat, Vapi, Bland) finally make IVR navigation + live-rep conversation tractable.
- Claude Sonnet 4.6 / Haiku 4.5 are fast and cheap enough to run as the in-call reasoning layer at <$1/call.
- Payer rep shortages mean even the payers prefer automated callers over staff who hang up after 30 min on hold.
- Post-No Surprises Act, clinics are under pressure to give patients accurate cost estimates pre-visit.

## 5. Technical architecture

```
┌──────────────────┐    ┌────────────────────────────────────────┐    ┌──────────────┐
│ Clinic dashboard │──▶│ API / job queue (FastAPI + Redis/BullMQ)│──▶│ Call runner  │
│ (Next.js)        │   │  - patient + payer + script templates   │   │ (LiveKit/    │
└──────────────────┘   │  - per-payer IVR map                    │   │  Pipecat)    │
        ▲              └────────────────────────────────────────┘    └──────┬───────┘
        │                              ▲                                    │
        │                              │ structured result                  ▼
        │              ┌───────────────┴───────────┐         ┌──────────────────────┐
        │              │ Postgres (encrypted)      │◀────────│ Telephony: Twilio /  │
        └──────────────│  + S3 recordings (KMS)    │         │  SignalWire          │
                       └───────────────────────────┘         │ ASR: Deepgram        │
                                  ▲                          │ TTS: Cartesia/11Labs │
                                  │                          │ LLM: Claude Sonnet   │
                  ┌───────────────┴────────────┐             │      4.6 + Haiku 4.5 │
                  │ EHR/PM integrations        │             └──────────────────────┘
                  │  Athena, DrChrono, Jane,   │
                  │  Tebra, Modmed (REST/FHIR) │
                  └────────────────────────────┘
```

Key design choices:
- **Two-model setup in-call.** Haiku 4.5 handles fast IVR DTMF / menu classification; Sonnet 4.6 handles live-rep dialogue and structured extraction. Keeps median latency <800 ms turn-to-turn.
- **Per-payer "playbooks"** stored as YAML: phone number, IVR map, auth prompts (NPI, TIN, provider DOB), question script, known quirks. Treated like first-class artifacts; versioned and A/B tested.
- **Deterministic finite-state script** wrapping the LLM. The LLM only chooses among allowed transitions — prevents hallucinated benefit values.
- **Confidence scoring per field** (rep restated value? transcript clarity? cross-checked against 271?). Threshold determines human review.
- **Re-dial + resume** on disconnect; max-attempt + cooldown per payer to avoid getting our number flagged.

## 6. Compliance & trust (non-negotiable, day 1)

- **HIPAA**: BAAs with Twilio, Deepgram, Anthropic, ElevenLabs/Cartesia, AWS. Encryption at rest (KMS) + in transit (TLS 1.2+). Per-tenant key isolation for recordings. Field-level PHI tagging in logs.
- **State two-party consent**: payer call recording disclosure script ("This call may be recorded for quality and compliance"). Per-state allowlist.
- **TCPA/identification**: agent identifies as automated assistant calling on behalf of <Clinic Name> when asked. Never claims to be human.
- **Audit log**: every call, transcript, prompt, model version, and write-back to EHR is immutable + exportable.
- **SOC 2 Type I in 6 months, Type II in 12** — table stakes for selling above 10-provider groups.

## 7. Roadmap

### MVP (weeks 0–10) — design partner pilot with 1–2 PT clinics
- CSV upload of patients to verify.
- Playbooks for top 5 payers in the pilot's market (UHC, Aetna, BCBS-state, Cigna, Medicare).
- Single specialty (PT). One service script.
- Twilio + LiveKit Agents + Claude + Deepgram + Cartesia.
- Dashboard: queue, results, transcript, recording, edit-and-approve.
- Output: PDF + JSON; manual paste-back into EHR is acceptable.
- Success metric: ≥80% of calls return a usable benefits record without human edit; <$2 fully-loaded cost per call.

### v1 (months 3–6) — first 10 paying clinics
- Multi-specialty playbooks (behavioral health, allergy).
- Top 25 payer IVR maps.
- EHR write-back: AthenaHealth + Jane first.
- Bulk scheduling: nightly run against tomorrow's appointments.
- Re-verification cadence rules.
- Human-in-the-loop reviewer console.
- 270/271 fast-path: skip the call when EDI gives a complete answer.

### v2 (months 6–12)
- Prior-authorization status checks (different script, same engine).
- Patient cost-estimate generator (No Surprises Act compliant).
- Denials triage: when a claim denies, auto-call the payer to get the reason code + remediation.
- Outbound patient calls: confirm appointments, collect updated insurance — same voice stack.
- SOC 2 Type II.

## 8. Pricing & monetization

- **Per-verification**: $4–$8 / completed verification (vs. $12–25 offshore, $25–40 in-house fully loaded).
- **Tiered subscription** + included verifications: e.g., $499/mo includes 100 verifications, $3 each over.
- **Enterprise**: per-provider seat ($99/provider/month) + volume discount per verification.

Unit economics target: gross margin 65–75% at scale (telephony + LLM + ASR/TTS = ~$0.80–$1.50 per call; ops + HITL ~$0.50; remainder is COGS overhead).

## 9. Go-to-market

1. **Design partners**: 2 PT clinics, free for 60 days in exchange for case study + payer playbook tuning.
2. **Specialty community wedge**: PT subreddits, APTA forums, Jane App user groups. "We did 1,200 verifications last month for $X — here's our case study."
3. **MSO / PE-backed groups**: 1 sale = 10–40 locations. Slower cycle, bigger ACV.
4. **Channel**: PT-focused billing companies (e.g., Therabill resellers, Raintree partners) — they upsell us to their book.

## 10. Key risks & mitigations

| Risk | Mitigation |
|------|------------|
| Payers detect + block automated callers | Voice diversity (multiple TTS voices), per-payer dial cadence limits, rotate Twilio numbers per-clinic, polite rate-limiting. Don't abuse rep time. |
| HIPAA breach | Vendor BAAs day 1; pen test before first paid customer; PHI minimization (don't send DOB to TTS unless needed). |
| Hallucinated benefit values | Deterministic FSM around the LLM; rep-confirmation step ("just to confirm, the copay is $40?"); confidence scoring + HITL fallback. |
| EHR integration drag | Start with CSV in / PDF + JSON out. Add Athena + Jane only after pilots confirm willingness to pay. |
| Regulatory shift on AI agents in healthcare | Conservative disclosure script; legal review per state; lobbying-by-proxy through clinic associations. |
| Incumbent move (Availity, Waystar, Infinx, Inbox Health) | Speed + specialty depth. Incumbents are EDI-first; we are phone-first and care about the long-tail benefit details they skip. |

## 11. Open questions to resolve before build

1. Which design-partner clinic + which 5 payers do we target first? (Drives playbook investment.)
2. Buy vs. build the voice runtime — LiveKit Agents (more control, more work) vs. Vapi/Bland (faster, less control over the IVR navigation policy)?
3. Where does the human reviewer sit — in-house team, or a customer-side workflow we just enable?
4. Do we record + store payer calls long-term, or transcribe-and-discard audio after N days to shrink HIPAA surface area?
5. Pricing anchor: per-verification (aligns to value, complex billing) vs. seat (predictable, less aligned)?

## 12. Definition of "MVP done"

- 1 design-partner clinic running ≥50 verifications/week through the system.
- ≥80% of calls return a complete, structurally-valid benefits record without human correction.
- Median call cost ≤ $2.
- Zero PHI incidents; full audit trail for every call.
- Clinic willing to be a named reference.
