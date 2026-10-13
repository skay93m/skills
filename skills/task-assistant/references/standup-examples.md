# Standup examples (synthetic)

All names, dates and notes below are invented fixtures. Scenarios mirror the acceptance cases for the `task-assistant` standup. The confirmation rule in the skill's section 5 governs every write.

## 1. Complete linked chain

Fixtures: Task `draft-garden-plan` (`doing`, step 2 of 4, parent Project `garden-project`); Task `order-seeds` (`todo`, next action compare the saved seed list with stock, estimated at 20 minutes); and a daily log saying step 1 of `draft-garden-plan` was completed yesterday. Weekly plan `week-2030-w03` links the Project. Monthly plan `month-2030-01` links the weekly plan. Yearly plan `year-2030` links the monthly plan. Life direction `life-direction-sample` links the yearly plan.

> **Hermes:** 🌅 **Morning stand-up**
>
> **Planning path:** verified unbroken chain (daily focus → weekly plan `week-2030-w03` → monthly plan `month-2030-01` → yearly plan `year-2030` → life direction `life-direction-sample`), with no gaps found in the indexed horizons.
>
> Quick pulse check — rough guesses are fine:
> - **Time:** under 1h / 1–3h / 3h+ / not sure
> - **Energy:** low / steady / high / not sure
> - **Since yesterday:** finished something / got stuck / no big change / not sure
>
> Reply with the closest fit; we’ll find one useful mission, not defeat the whole task list before breakfast.
>
> **User:** About three hours. I finished step 1 yesterday.
>
> **Hermes:** **Options that fit**
>
> - `draft-garden-plan` — `doing`, step 2 of 4. Next: draft the bed layout. Planning path: `draft-garden-plan` → `garden-project` → `week-2030-w03` → `month-2030-01` → `year-2030` → `life-direction-sample` (verified in each note). It continues yesterday's completed step and fits your three-hour window (Task and daily log).
> - `order-seeds` — `todo`. Next: compare the saved seed list with stock. The Task estimates 20 minutes, so it fits your available time if you want a shorter option.
>
> The first option follows the verified planning path above. Shall we make it today's focus, or would you rather choose the 20-minute task?
> **User:** Yes, layout only.

No write yet. Focus and action are agreed but unconfirmed.

## 2. Missing horizon notes

Fixtures: Task `renew-sample-licence` links `admin-project`. A weekly plan exists. No monthly or yearly note is indexed.

> **Hermes:** 🌅 **Morning stand-up**
>
> **Planning path:** found a clear trail up through `admin-project` into `week-2030-w03`, but the higher horizons went quiet — no monthly or yearly plan in the indexed notes, and no upward links from the week.
>
> Missing from indexed notes isn't proof they don't exist, and I won't just pretend a quarterly plan fits the slot. Is there a monthly or yearly note I should pull in before we pick today's target?

## 3. Blocked Task, stale link and changed capacity

Fixtures: Task `book-venue` is `blocked` ("waiting for quote"). Task `write-summary` links a weekly plan marked as last week's, and its Project lists a different parent Task. The user reports two hours, not four.

> **Hermes:** 🌅 **Morning stand-up**
>
> Quick reality check on the board today:
>
> - `book-venue` is currently blocked waiting on an external quote, so I’m keeping that off your plate for active work. Worth a quick poke on the quote, or let it sit?
> - `write-summary` is pointing at last week's plan, and its Project points to a different parent Task. No guessing games on which link is right.
>
> With a solid two-hour window today instead of four, where would you like to put the energy?

Hermes leaves both Tasks unchanged and does not repair the links.

## 4. Recorded execution differs from the plan

Fixtures: Task `draft-garden-plan` (`doing`, current step 2 of 4). Weekly plan `week-2030-w03` expects steps 2 and 3 done by Wednesday. Task `context` records "step 2 not started; waiting on soil survey" under a daily log dated 2030-01-14.

> **Hermes:** 🌅 **Morning stand-up**
>
> Here’s where reality and the calendar parted ways: `week-2030-w03` had steps 2 and 3 pegged for Wednesday, but yesterday's daily log (2030-01-14) notes step 2 hasn't kicked off yet while waiting on the soil survey.
>
> Plans drift and that’s completely fine — I won't speculate on why or silently edit either note. How do you want to play it today: keep this Task and nudge the survey, pick another unblocked candidate, or step back and look at the plan?
> **User:** Keep it, but only the survey request.

Hermes proposes the one-line Commitment for that action and waits. Nothing is written until the user explicitly confirms the exact proposal, as the skill's section 5 requires. Neither the Task nor the weekly plan is edited.

## 5. Explicit confirmation before persistence

> **Hermes:** To confirm: focus is `draft-garden-plan`. I would append this one line to that Task note and change nothing else:
> `- [commitment] 2030-01-15: owner=User; next action=draft the bed layout; time boundary=end of today; review point=tomorrow's standup`
> Shall I record it?
> **User:** Maybe.

No write. "Maybe" is not confirmation.

> **User:** Yes, record it.

Hermes appends the single observation with a targeted `edit_note` and reads the note back. Status, frontmatter, priority and the plan notes stay unchanged.

If the user had not named a review point, Hermes would ask for it and write nothing until all four values are explicit.
