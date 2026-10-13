# Standup examples (synthetic)

All names, dates and notes below are invented fixtures. Scenarios mirror the acceptance cases for the `task-assistant` standup. The confirmation rule in the skill's section 5 governs every write.

## 1. Complete linked chain

Fixtures: Task `draft-garden-plan` (`doing`, step 2 of 4, parent Project `garden-project`); Task `order-seeds` (`todo`, next action compare the saved seed list with stock, estimated at 20 minutes); and a daily log saying step 1 of `draft-garden-plan` was completed yesterday. Weekly plan `week-2030-w03` links the Project. Monthly plan `month-2030-01` links the weekly plan. Yearly plan `year-2030` links the monthly plan. Life direction `life-direction-sample` links the yearly plan.

> **Hermes:** 🌅 **Morning stand-up**
>
> **Planning path:** `draft-garden-plan` → `garden-project` → `week-2030-w03` → `month-2030-01` → `year-2030` → `life-direction-sample` (each link verified in the note named).
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
> - `draft-garden-plan` — `doing`, step 2 of 4. Next: draft the bed layout. It continues yesterday's completed step and fits your three-hour window (Task and daily log).
> - `order-seeds` — `todo`. Next: compare the saved seed list with stock. The Task estimates 20 minutes, so it fits your available time if you want a shorter option.
>
> The first option follows the verified planning path above. Shall we make it today's focus, or would you rather choose the 20-minute task?
> **User:** Yes, layout only.

No write yet. Focus and action are agreed but unconfirmed.

## 2. Missing horizon notes

Fixtures: Task `renew-sample-licence` links `admin-project`. A weekly plan exists. No monthly or yearly note is indexed.

> **Hermes:** Path found: the Task, `admin-project`, then `week-2030-w03`. I found no monthly or yearly plan in the indexed notes and no link from the week upwards. That does not prove none exists. I will not use the quarterly plan in their place. Is there a monthly or yearly note I should read?

## 3. Blocked Task, stale link and changed capacity

Fixtures: Task `book-venue` is `blocked` ("waiting for quote"). Task `write-summary` links a weekly plan marked as last week's, and its Project lists a different parent Task. The user reports two hours, not four.

> **Hermes:** `book-venue` is blocked on a quote, so I am not offering it as work. Can you chase the quote, or leave it? `write-summary` links last week's plan, and its Project names another parent Task. I will not guess which is right. With two hours, which would you rather start?

Hermes leaves both Tasks unchanged and does not repair the links.

## 4. Recorded execution differs from the plan

Fixtures: Task `draft-garden-plan` (`doing`, current step 2 of 4). Weekly plan `week-2030-w03` expects steps 2 and 3 done by Wednesday. Task `context` records "step 2 not started; waiting on soil survey" under a daily log dated 2030-01-14.

> **Hermes:** `week-2030-w03` expects steps 2 and 3 done by Wednesday. The Task's own daily log (2030-01-14) says step 2 has not started and is waiting on a soil survey, so the evidence differs from the plan. I will not guess the cause or update either note. How would you like to proceed: keep this Task as today's focus, pick another, or leave the plan question for you to review?
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
