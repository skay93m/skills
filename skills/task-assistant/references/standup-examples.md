# Standup examples (synthetic)

All names, dates and notes below are invented fixtures. Scenarios mirror the acceptance cases for the `task-assistant` standup. The confirmation rule in the skill's section 5 governs every write.

## 1. Complete linked chain

Fixtures: Task `draft-garden-plan` (`doing`, step 2 of 4, parent Project `garden-project`). Weekly plan `week-2030-w03` links the Project. Monthly plan `month-2030-01` links the weekly plan. Yearly plan `year-2030` links the monthly plan. Life direction `life-direction-sample` links the yearly plan.

> **Hermes:** Three Tasks are ready: `draft-garden-plan` (step 2 of 4), `order-seeds`, `tidy-notes`. How much time and energy do you have today, and what moved yesterday?
> **User:** About three hours. I finished step 1 yesterday.
> **Hermes:** Then `draft-garden-plan` fits. Its path: garden-project, then `week-2030-w03` (lists the Project), then `month-2030-01` (links the week), then `year-2030` (links the month), then `life-direction-sample` (links the year). Each link comes from the cited note. Does that still read right? If so, would the next action be to draft the bed layout?
> **User:** Yes, layout only.

No write yet. Focus and action are agreed but unconfirmed.

## 2. Missing horizon notes

Fixtures: Task `renew-sample-licence` links `admin-project`. A weekly plan exists. No monthly or yearly note is indexed.

> **Hermes:** Path found: the Task, `admin-project`, then `week-2030-w03`. I found no monthly or yearly plan in the indexed notes and no link from the week upwards. That does not prove none exists. I will not use the quarterly plan in their place. Is there a monthly or yearly note I should read?

## 3. Blocked Task, stale link and changed capacity

Fixtures: Task `book-venue` is `blocked` ("waiting for quote"). Task `write-summary` links a weekly plan marked as last week's, and its Project lists a different parent Task. The user reports two hours, not four.

> **Hermes:** `book-venue` is blocked on a quote, so I am not offering it as work. Can you chase the quote, or leave it? `write-summary` links last week's plan, and its Project names another parent Task. I will not guess which is right. With two hours, which would you rather start?

Hermes leaves both Tasks unchanged and does not repair the links.

## 4. Explicit confirmation before persistence

> **Hermes:** To confirm: focus is `draft-garden-plan`. I would append this one line to that Task note and change nothing else:
> `- [commitment] 2030-01-15: owner=User; next action=draft the bed layout; time boundary=end of today; review point=tomorrow's standup`
> Shall I record it?
> **User:** Maybe.

No write. "Maybe" is not confirmation.

> **User:** Yes, record it.

Hermes appends the single observation with a targeted `edit_note` and reads the note back. Status, frontmatter, priority and the plan notes stay unchanged.

If the user had not named a review point, Hermes would ask for it and write nothing until all four values are explicit.
