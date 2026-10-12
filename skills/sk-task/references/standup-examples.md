# Standup examples (synthetic)

All names, dates and notes below are invented fixtures. Scenarios mirror the acceptance cases for the `sk-task` standup. Hermes writes nothing until the confirmation turn in example 4.

## 1. Complete linked chain

Fixtures: Task `draft-garden-plan` (`doing`, step 2 of 4, parent Project `garden-project`). Weekly plan `week-2030-w03` links the Project. Monthly plan `month-2030-01` links the weekly plan. Yearly plan `year-2030` links the monthly plan. Life direction `life-direction-sample` links the yearly plan.

> **Hermes:** Three Tasks are ready: `draft-garden-plan` (step 2 of 4), `order-seeds`, `tidy-notes`. How much time and energy do you have today, and what moved yesterday?
> **Syafiq:** About three hours. I finished step 1 yesterday.
> **Hermes:** Then `draft-garden-plan` fits. Its path: garden-project, then `week-2030-w03` (lists the Project), then `month-2030-01` (links the week), then `year-2030` (links the month), then `life-direction-sample` (links the year). Each link comes from the cited note. Does that still read right? If so, would the next action be to draft the bed layout?
> **Syafiq:** Yes, layout only.

No write yet. Focus and action are agreed but unconfirmed.

## 2. Missing horizon notes

Fixtures: Task `renew-sample-licence` links `admin-project`. A weekly plan exists. No monthly or yearly note is indexed.

> **Hermes:** Path found: the Task, `admin-project`, then `week-2030-w03`. I found no monthly or yearly plan in the indexed notes and no link from the week upwards. That does not prove none exists. I will not use the quarterly plan in their place. Is there a monthly or yearly note I should read?

## 3. Blocked Task, stale link and changed capacity

Fixtures: Task `book-venue` is `blocked` ("waiting for quote"). Task `write-summary` links a weekly plan marked as last week's, and its Project lists a different parent Task. Syafiq reports two hours, not four.

> **Hermes:** `book-venue` is blocked on a quote, so I am not offering it as work. Can you chase the quote, or leave it? `write-summary` links last week's plan, and its Project names another parent Task. I will not guess which is right. With two hours, which would you rather start?

Hermes leaves both Tasks unchanged and does not repair the links.

## 4. Explicit confirmation before persistence

> **Hermes:** To confirm: focus is `draft-garden-plan`, today, 2030-01-15. Next action: draft the bed layout. Time boundary: today. Review point: tomorrow's standup. I will add this dated Commitment to that Task note only, changing no status, priority or plan. Shall I record it?
> **Syafiq:** Maybe.

No write. "Maybe" is not confirmation.

> **Syafiq:** Yes, record it.

Hermes checks that the Task note already uses a supported Commitment convention. If it does, Hermes makes one targeted edit and reads the note back. If not, Hermes writes nothing and reports the smallest decision needed from Syafiq.
