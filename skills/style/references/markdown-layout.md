# Markdown Layout

Layout rules and a visual template for documents produced under the style skill.

## Headings

- Use one H1 per document, matching the title in the frontmatter.
- Use H2 for sections and H3 for subsections.
- Do not skip heading levels.
- Separate sections with headings, never with rules.

## Tables

- Keep one point per cell. Use short phrases, not sentences with several clauses.
- If a cell needs a second point, split the row or use a bullet list.
- Give every table a header row and no empty cells. Write "none" where a value is absent.
- Leave a blank line before and after each table.
- Do not nest lists or code inside cells.

## Lists

- Use bullets for parallel points and numbered lists only for ordered steps.
- Keep one idea per bullet.
- Bold a lead-in label at most once per bullet.

## Spacing

- Use one blank line between blocks.
- Keep paragraphs to a few sentences.

## Links

- Write a GitHub issue or pull request link as a bare URL on its own line, so the GitHub Link plugin renders it.
- Never wrap such a link in parentheses or give it custom link text.

## Visual Template for a Repository Document

Build a document in this order:

1. Frontmatter with title, type, status, date, and tags.
2. An H1 title that matches the frontmatter title.
3. A short objective: the purpose of the document and who it is for.
4. H2 sections, in order: context, the content or decision, consequences or next steps, then references.
5. A references section listing bare URLs or relative paths, one per line.

Keep each section to what the reader needs. Prefer a table for comparisons of two to four items with one point per cell, and bullets for everything else.
