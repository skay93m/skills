# Repair prompt template

Use this when a Sourcery review contains `BLOCKING` findings and you want an agent to plan the repair. Copy the template, paste the blocking findings, and send it.

```
Diagnose and plan repairs for the blocking findings below from a pull request review. Do not edit any file until I approve the plan.

For each finding:
1. Confirm it in the diff, quoting the file and line.
2. State the cause.
3. Propose the smallest change that fixes it, and list the files it touches.
4. Say how to verify the fix.

Standard used by the review: <paste the stamp line from the Sourcery comment>

Blocking findings (copy each "BLOCKING [ID]:" comment with its file and line):
<paste here>
```

Include only `BLOCKING` findings. Leave `NON-BLOCKING` findings out unless you decide to act on them.
