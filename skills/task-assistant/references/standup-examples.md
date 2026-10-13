# Standup examples (synthetic)

All names, dates and notes below are invented fixtures. Scenarios mirror the acceptance cases for the `task-assistant` standup. The confirmation rule in the skill's section 5 governs every write.

## 1. Complete linked chain

Fixtures: Task `draft-garden-plan` (`doing`, step 2 of 4, parent Project `garden-project`); Task `order-seeds` (`todo`, next action compare the saved seed list with stock, estimated at 20 minutes); and a daily log saying step 1 of `draft-garden-plan` was completed yesterday. Weekly plan `week-2030-w03` links the Project. Monthly plan `month-2030-01` links the weekly plan. Yearly plan `year-2030` links the monthly plan. Life direction `life-direction-sample` links the yearly plan.

> **Hermes:** Morning! Your planning path looks unbroken from today up to your life direction. Quick pulse, rough guesses welcome:
> - Time: under 1h / 1–3h / 3h+
> - Energy: low / steady / high
> - Since yesterday: finished something / got stuck / no big change / not sure
>
> **User:** About three hours. I finished step 1 yesterday.
>
> **Hermes:** Nice, a finished step and three hours is a good start. Two fits: continue `draft-garden-plan` with the bed layout (step 2 of 4), or knock out `order-seeds` in about 20 minutes. Which one gets today?
>
> **User:** Layout, I think.
>
> **Hermes:** Good pick. What would "layout done" look like by lunchtime: a sketch, or the full plan?
>
> **User:** Just a sketch.

No write yet. Focus and action are agreed but unconfirmed. The candidates' per-Task path (`draft-garden-plan` → `garden-project` → `week-2030-w03` → `month-2030-01` → `year-2030` → `life-direction-sample`, each link read) stays internal until the user asks or a Commitment is proposed.

If the user had said "I'll do the seeds later, around 3pm", Hermes would answer "Parked for 3pm, I'll nudge you then" and still write nothing.

## 2. Missing horizon notes

Fixtures: Task `renew-sample-licence` links `admin-project`. A weekly plan exists. No monthly or yearly note is indexed.

> **Hermes:** Morning! The trail runs up to this week's plan, then goes quiet: no monthly or yearly note in what I can see. That's not proof they don't exist, and I won't stretch a quarterly plan to fit. Is there one I should pull in first?

## 3. Blocked Task, stale link and changed capacity

Fixtures: Task `book-venue` is `blocked` ("waiting for quote"). Task `write-summary` links a weekly plan marked as last week's, and its Project lists a different parent Task. The user reports two hours, not four.

> **User:** Only two hours today, not four.
>
> **Hermes:** Two it is. `book-venue` is blocked on a quote, so it stays off the active list, and `write-summary` points at last week's plan with a Project naming a different parent Task. I won't guess which link is right. Should we pick something else for your two hours, or sort out that link first?

Hermes leaves both Tasks unchanged and does not repair the links.

## 4. Recorded execution differs from the plan

Fixtures: Task `draft-garden-plan` (`doing`, current step 2 of 4). Weekly plan `week-2030-w03` expects steps 2 and 3 done by Wednesday. Task `context` records "step 2 not started; waiting on soil survey" under a daily log dated 2030-01-14.

> **Hermes:** Reality and the calendar parted ways a bit: the week expected steps 2 and 3 by Wednesday, but yesterday's log says step 2 is waiting on the soil survey. Plans drift, no drama. Nudge the survey, pick something unblocked, or revisit the plan?
>
> **User:** Keep it, but only the survey request.

Hermes proposes the one-line Commitment for that action and waits. Nothing is written until the user explicitly confirms the exact proposal, as the skill's section 5 requires. Neither the Task nor the weekly plan is edited.

## 5. Explicit confirmation before persistence

> **Hermes:** To confirm: focus is `draft-garden-plan`. I would append this one line to that Task note and change nothing else:
> `- [commitment] 2030-01-15: owner=User; next action=draft the bed layout; time boundary=end of today; review point=tomorrow's standup`
> Shall I record it?
> **User:** Maybe.

No write. "Maybe" is not confirmation.

> **User:** Yes, record it.

If an atomic write capability is available that guards the Task checksum, `schema/task` convention, and any linked GitHub state in one transaction, Hermes appends the single observation with that targeted write and reads the note back. Status, frontmatter, priority and the plan notes stay unchanged. If the available tool (such as basic `edit_note`) only guards the Task checksum and cannot atomically guard schema and linked GitHub eligibility, Hermes writes nothing, preserves the proposal in conversation, and explains that persistence is unavailable until atomic multi-state guards exist.

If the user had not named a review point, Hermes would ask for it and write nothing until all four values are explicit.
