---
name: sk-supervised-ingest
---

# supervised-ingest-workflow

## Purpose

This procedure defines the repeatable supervised form of the Wiki's Ingest operation for external literature and source material. It is the sole current executable Wiki procedure for supervised ingestion. Historical knowledge may describe earlier approaches, but no other note, raw capture, scratchpad, transcript, research report, or retired skill may act as an ingest procedure.

Supervised ingestion is collaborative. The agent performs capture, provenance work, search, drafting, extraction, graph construction and mechanical verification. Syafiq supplies judgement where the source does not determine the answer and retains control over promotion into canonical knowledge.

The workflow deliberately separates source capture from canonical interpretation.

The purpose of ingestion is to extract a source's insights and key themes, consider them within what the Wiki already holds, and reflect on where they corroborate, conflict with, extend or leave gaps in existing knowledge, applying analytical frameworks where appropriate. The agent facilitates that reflection and Syafiq supplies the synthesis. The outcome is then persisted in the Wiki where it belongs, in `concepts/` or another folder depending on its nature. Supervised ingestion includes the human synthesis. Unsupervised ingestion, not yet drafted as a procedure, is intended to perform the same scoping without it and to leave a foundation from which an agent can later facilitate the reflection.

## Entry conditions
Start this workflow when an external source is to be ingested into the Wiki.

Source format is not restricted to Markdown. The agent may ingest a web page, document, PDF, image, audio, video, or other source only when its relevant content is directly inspectable through an available ordinary read or fetch capability.

### Source accessibility gate

Before analysing the source, determine whether usable content is already directly accessible.

Proceed when the source itself, or an already-existing authorised derivative such as a transcript, caption track, or text extraction, can be read directly.

Stop and flag the dependency to Syafiq when ingestion would require the agent to create the usable source representation first. The agent must not:

- generate a transcript from a YouTube or other video;
- transcribe an audio file;
- perform OCR on scanned or image-only material;
- reconstruct inaccessible text or media content;
- perform comparable conversion or preprocessing solely to make the source ingestible.

Syafiq may perform that preprocessing himself or use a more specialised tool, then provide or expose the resulting material for ingestion.

Where a derivative is used, keep it distinct from the primary source in provenance. A transcript of a video is supporting material, not the video itself.

Before substantive work, inspect the relevant Wiki guidance and search for existing notes, decisions and entities so that ingestion does not rediscover or duplicate existing knowledge.
## Step 1: Establish source identity and provenance

Identify the primary source and capture the provenance needed to identify and revisit it.

For a literature note, useful source metadata may include:

- source type;
- author or creator;
- title;
- platform or publication;
- publication date where established;
- source URL;
- access date.

Supporting material such as transcripts, captures or working notes must be identified separately from the primary source, for example through structured `supporting_materials` frontmatter.

Do not silently convert uncertain metadata into fact. Preserve uncertainty or verify it.

### Human gate

Ask Syafiq only where source identity or provenance is materially ambiguous and cannot be established from the available evidence.

## Step 2: Search before creating

Search the Wiki for:

- the source itself;
- existing literature notes covering the same material;
- concepts substantially discussed by the source;
- people, organisations, frameworks or other entities that may already exist;
- existing decisions or interpretations that should not be rediscovered.

Classify candidate entities as existing, genuinely new, or uncertain.

Do not create duplicate concept entities simply because the source uses different wording.

### Capture meaning before taxonomy

Final ontology is not an entry condition for ingestion.

When useful material does not yet have an obvious permanent home, capture the meaning, provenance, retrieval-worthy observations and semantic relations first. Do not require Syafiq to choose a final folder, note type, domain, project ownership or single canonical interpretation merely so that ingestion can proceed.

A source-derived idea may initially remain in a literature or raw note, or be represented as a provisional atomic concept when Syafiq has approved the underlying insight. It may relate simultaneously to several contexts, such as a dissertation, professional practice and a broader conceptual theme. Relations should preserve those connections without forcing one of them to become the idea's exclusive home.

Repeated retrieval, reuse and later curation should provide evidence for whether an idea deserves promotion, merging, renaming, reclassification or a more stable canonical form. Organisational structure should emerge from demonstrated use rather than being guessed prematurely at capture time.

The agent remains responsible for search before create, provenance and duplicate prevention. Deferring taxonomy is not permission to create arbitrary new notes. It means uncertainty about final placement or ontology should be preserved explicitly rather than blocking capture or being resolved through unsupported inference.

### Human gate

For insight-bearing material, use the supervised conversation to deepen ingestion where useful. Distinguish clearly between source-derived claims, Syafiq's first-hand observations and any analytical connection developed together. Capture those layers with their provenance intact rather than flattening them into a single claim.

## Step 3: Create or update the literature note
The `raw/` folder is a lifecycle container, not a note type. Preserve the semantic type of any existing source-facing material. A `research-report`, `source-capture`, or `scratchpad` used as input to this workflow must not be retagged merely because it is being ingested.

Create or update a `type: literature-note` in `raw/` when the workflow needs a source-facing synthesis that explains the primary source. If the literature note is being actively developed through this workflow, set `ingest_status: partial`. An existing raw artefact that is merely waiting for this workflow may use `ingest_status: pending`.

The literature note should contain:

1. structured provenance in frontmatter;
2. readable free prose explaining the source;
3. retrieval-worthy observations;
4. typed directional relations to relevant entities.

Tags should be chosen for plausible future resurfacing, not merely because a word occurs in the source.

The literature note remains a source-facing artefact. It is not automatically a canonical statement of Syafiq's own beliefs or conclusions. Promotion creates or updates the appropriate durable Wiki notes while the literature note remains available as provenance. Do not relabel or discard a genuine human decision merely because it appears in `raw/`; preserve its provenance and assess current applicability against newer evidence.

At successful completion of the supervised ingest, set the literature note's `ingest_status` to `ingested`. Use `retained` when a raw artefact is deliberately kept for provenance or reference and no further ingestion is intended. Do not infer ingest completion merely because a note exists in `raw/`.
## Step 4: Write the free-prose account

Write enough prose for a reader to understand:

- what the source is about;
- how its argument, explanation or discussion develops;
- the important examples or methods it uses;
- relevant qualifications, scope and limitations.

Prefer attributed paraphrase. Preserve meaning and epistemic distinctions without reproducing unnecessary source text.

Free prose and observations must not collapse into the same function. Prose preserves meaning, context and nuance.

### Human gate

If the prose would require attributing a judgement to Syafiq, ask rather than infer it.

Straightforward factual or semantic corrections to the literature note can be applied directly and verified. Basic Memory version history supplies reversibility.

## Step 5: Extract observations as queryable properties

Select observations according to retrieval value rather than mechanically converting paragraphs into bullets.

For each proposed observation, ask:

1. Would an agent plausibly want to retrieve this without reading the whole note?
2. Does the category describe what kind of property this is?
3. Is the value supported by the source or by an explicit reviewed judgement?

Provisional observation roles that emerged from supervised literature ingestion include:

- `central_claim`;
- `method`;
- `framework`;
- `worked_example`;
- `intended_use`;
- `scope`;
- `limitation`.

These are candidate slots, not a fixed schema. Do not force every literature note to contain them.

A missing potentially useful observation is an incompleteness signal for review or later linting. It is not permission to manufacture content.

### Human gate

Where an observation requires personal interpretation, evaluative judgement, or information not established by the source, ask Syafiq. Do not infer merely to fill a slot.

## Step 6: Create relations as semantic graph routes

Create typed, directional relations that explain why an agent should traverse from the current note to the target entity.

Prefer the most precise predicate that the evidence supports.

Examples include:

- `presents [[Concept]]`;
- `applies [[Concept]]`;
- `illustrates [[Concept]]`;
- `critiques [[Claim]]`;
- `compares [[Concept]]`;
- `draws_on [[Source]]`.

Avoid generic `relates_to` when a more informative relationship is established.

Do not overstate the relationship. Predicates such as `supports`, `validates`, `contradicts`, `derived_from` or `provides_evidence_for` require evidence for that stronger semantic claim.

Use the documented Basic Memory relation form:

```markdown
- relation_type [[Target]]
```

Do not make undocumented parser behaviour part of the Wiki contract.

### Human gate

If more than one materially different predicate is plausible and the source does not resolve the distinction, ask Syafiq rather than selecting a stronger interpretation silently.

## Step 7: Scope themes and reflect with Syafiq

The purpose of ingestion is not to transcribe a source. It is to extract the source's insights and key themes, consider them within what the Wiki already holds (which is why Step 2 queries existing notes), and reflect on where they corroborate, conflict with, extend or leave gaps in existing knowledge, applying an analytical framework where one is appropriate. The agent facilitates this reflection. Syafiq supplies the synthesis. Once a theme is resolved, the outcome is persisted in the Wiki in the place it belongs, which may be a concept note or another folder depending on its nature.

Reflection is expensive for Syafiq and must be bounded. The work therefore has three stages that must not be merged: the agent scopes and ranks all themes and persists that scoping, the agent resolves low-stakes themes by proposing a draft for Syafiq to accept, and the agent and Syafiq reflect one at a time on the few themes that need his judgement.

### 7a. Scope and rank the themes

After the source-facing literature note is coherent, the agent identifies the source's key themes and tensions, as themes rather than a flat list of claims. For each theme the agent searches the Wiki and records three things: what the source says, what the Wiki already holds, and whether the two appear to corroborate, conflict, extend or leave a gap.

The agent persists this scoping in the literature note itself, under a heading such as "Themes for supervised reflection", before any theme is discussed. The section must state that it is agent-proposed, name the creating model, state that it is unreviewed, and give each theme a status. The comparisons are the agent's reading of existing notes and must not be attributed to Syafiq.

The agent then ranks the themes by their consequence for the Wiki or for Syafiq's practice, and assigns each a handling:

- A theme that mainly corroborates what the Wiki already holds is resolved by a drafted insight (see 7b), not by an open reflection.
- A theme that conflicts with, extends or exposes a gap in existing knowledge is a candidate for reflection with Syafiq.
- At most three or four themes are reflected on per source. The remainder are recorded as parked, with the reason, and are not discussed in the session unless Syafiq asks.

Syafiq may reorder the ranking or promote a parked theme. Do not present several themes for discussion at the same time.

### 7b. Resolve one theme at a time

For each theme in turn, the agent surfaces the theme in a few sentences with its scoping evidence, then proposes a draft insight and a proposed destination. The destination is one of: the literature note only, an update to an existing note, or a new concept. The default is the literature note only.

For a corroboration theme, the agent states the draft insight and destination and Syafiq accepts, edits or rejects it. No open question is needed.

For a theme that needs Syafiq's judgement, the agent asks one multiple-choice question:

1. Offer two to four concrete options, each stating what choosing it would lead to.
2. Put the agent's recommended option first and mark it as recommended.
3. Make clear that Syafiq can add a comment or give his own answer instead of choosing.
4. Use the client's structured multiple-choice question where one exists. Otherwise use lettered options in text.

Do not ask open-ended or abstract counterfactual questions such as what would have been lost had the source never existed. Give Syafiq facts or a draft to react to and ask him to choose between defined alternatives. Ask one question only, and wait for the response.

Record the response and outcome under that theme in the literature note before moving to the next theme. Give each theme a final status of resolved or parked.

Where an analytical framework such as the idea compass is applied, it must be the Wiki's own defined version of that framework. The agent must not invent a framework's prompts. If no definition can be found in the Wiki, ask Syafiq where it is defined.

Keep three provenance layers distinct in what is recorded: the source's claims, the Wiki's existing positions, and Syafiq's first-hand responses or jointly developed analysis. The deepening rule in Step 2 applies here.

### 7c. Persist the outcome where it belongs

When a theme is resolved, the agent persists the outcome at the destination Syafiq chose. The options include:

- recording the response and final status in the literature note only, which is the default;
- linking to an existing entity, or updating it with genuinely new information;
- creating a concept note in `concepts/`;
- placing the outcome in another folder that suits its nature, for example a record of a conflict between sources or with existing positions.

Some folders that this stage may call for, such as one for contradictions, have not been created. The agent must not create a new folder without Syafiq's explicit authorisation, and must follow the AGENTS.md placement rules (inspect the destination index, keep folders shallow, use lowercase kebab-case).

Canonical concept notes should represent durable understanding, not merely repeat what a single source says. Leave an idea only in the literature note when it is not yet worth promoting.

### Human gate

The theme resolution in 7b is itself the principal human gate of supervised ingestion. Promotion of a genuinely new source-derived idea into a canonical concept note requires Syafiq's judgement or clear prior approval. The agent may prepare the proposal, search evidence and suggest the relation structure, but should not silently convert source claims into Syafiq's canonical knowledge.

### Supervised and unsupervised ingestion

Supervised ingestion includes Syafiq's synthesis at 7b. Unsupervised ingestion, which has not yet been drafted as a procedure, is expected to perform the scoping and ranking at 7a without human synthesis and to leave the scoped themes, with their provenance, as a foundation from which an agent can later facilitate the reflection with Syafiq.


## Step 8: Preserve agent-authored analysis correctly

If the agent creates a separate raw note containing its own analysis, synthesis, working theory or workflow findings, record the specific model in semantic frontmatter, for example:

```yaml
author: GPT-5.6 Sol
agent_model: GPT-5.6 Sol
authorship: agent-analysis
```

Never attribute agent-generated raw analysis to Syafiq.

Basic Memory-managed `created_by` and `updated_by` fields are account provenance and are not semantic authorship.

## Step 9: Mutate safely and verify

For every write or edit:

1. read the current note and obtain the current checksum where available;
2. make the bounded mutation;
3. reread the persisted note;
4. verify the intended content, frontmatter and Markdown structure;
5. correct straightforward structural artefacts immediately.

Use CriticMarkup for minor edits where reviewing the proposed wording in context is useful. Do not use it for straightforward structural fixes or straightforward semantic fixes.

Do not assume an overwrite removed stale metadata. Verification is mandatory.

## Step 10: Maintain navigation and activity records

After creating or materially changing notes:

- maintain the relevant folder index where the note should be discoverable;
- append an appropriate activity entry to the relevant log;
- preserve append-only log history;
- check that intended links and paths resolve.

Do not treat an activity log as canonical knowledge.

## Step 11: Report unresolved items

Before declaring the ingest complete, surface any unresolved items, including:

- uncertain provenance;
- observations that require Syafiq's interpretation;
- ambiguous relation predicates;
- proposed canonical entities awaiting judgement;
- missing properties that may be useful but cannot be established;
- source limitations or evidence gaps.

Do not fill these merely to make the note appear complete.

## Definition of done

A supervised literature ingest is complete when:

- the primary source is correctly identified;
- supporting material is distinguished from the source;
- search-before-create has been performed;
- the literature note contains sufficient readable prose;
- retrieval-worthy observations have been extracted without forced slot filling;
- graph relations use meaningful directional predicates;
- the source's themes have been scoped against existing Wiki knowledge, and the scoping has been persisted in the literature note before any theme is discussed;
- every scoped theme has a recorded final status of resolved or parked, with no more than three or four themes reflected on with Syafiq one at a time;
- any new canonical entities have been explicitly reviewed or otherwise clearly authorised;
- all writes have been reread and verified;
- relevant navigation and activity records are maintained;
- unresolved interpretive questions are explicitly surfaced rather than silently resolved.

Completion of ingestion does not mean the source has been accepted as true or promoted into Syafiq's own worldview. It means the source has been represented faithfully and usefully enough for later query, comparison, reflection and linting.

## Observations

- [purpose] Defines the sole current executable procedure for supervised ingestion of external sources into the Wiki.
- [trigger] Use when an external source is to be ingested into the Wiki.
- [access_boundary] Proceed only when the relevant source content, or an already-existing authorised derivative, is directly inspectable; if transcription, OCR, reconstruction or comparable preprocessing is required, stop and flag the dependency to Syafiq.
- [authority_boundary] The agent performs capture, provenance work, search, drafting, extraction, graph construction and verification; Syafiq retains interpretive judgement and authority over promotion into canonical knowledge.
- [provenance_rule] Keep the primary source distinct from supporting derivatives such as transcripts, caption tracks, text extractions and working notes.
- [search_rule] Search the Wiki for the source, existing entities, relevant decisions and prior interpretations before creating new notes or concepts.
- [taxonomy_rule] Capture meaning, provenance, observations and semantic relations before forcing final taxonomy; folder, note type and exclusive project ownership may remain provisional until repeated use and later curation provide evidence for a stable form.
- [deepening_rule] For insight-bearing material, supervised ingestion may deepen the source through discussion with Syafiq; preserve source-derived claims, Syafiq's first-hand observations and jointly developed analysis as distinct provenance layers.
- [observation_rule] Extract observations for retrieval value and source support; do not force-fill expected properties or invent missing information.
- [relation_rule] Use evidence-supported, typed directional relations that explain why an agent should traverse the edge; ask Syafiq when materially different predicates remain plausible.
- [promotion_rule] A genuinely new source-derived idea must not become canonical knowledge without Syafiq's judgement or clear prior approval.
- [authorship_rule] Agent-authored raw analysis must identify the specific creating model as semantic author and must not attribute authorship to Syafiq.
- [verification_rule] Every mutation must follow read current state, make the bounded change, reread and verify.
- [completion_rule] Completion means the source has been represented faithfully and usefully with unresolved interpretive issues surfaced; it does not mean the source has been accepted as true or adopted into Syafiq's worldview.
- [ingestion_purpose] Ingestion extracts a source's insights and key themes, considers them within existing Wiki knowledge, and reflects on corroboration, conflict, extension and gaps, applying analytical frameworks where appropriate; it is not transcription.
- [facilitation_rule] The agent facilitates the reflection and Syafiq supplies the synthesis.
- [scoping_rule] Before any theme is discussed, the agent scopes the themes against existing Wiki notes, ranks them by consequence, and persists that scoping in the literature note, labelled as agent-proposed, model-attributed and unreviewed.
- [bounding_rule] Reflect with Syafiq on at most three or four themes per source, prioritising conflicts, extensions and gaps; resolve mainly corroborating themes with a drafted insight for him to accept, edit or reject; record the remainder as parked with a reason.
- [reflection_rule] Take themes one at a time: surface the theme, propose a draft insight and destination, and where his judgement is needed ask one multiple-choice question with the recommended option first and room for his comments. Record the outcome and a final status of resolved or parked before moving on. Never present several themes at once.
- [prompt_rule] Do not ask open-ended or abstract counterfactual questions; give Syafiq facts or a draft to react to and defined alternatives to choose between.
- [framework_rule] Use only the Wiki's own defined version of an analytical framework such as the idea compass; if it cannot be found, ask where it is defined rather than inventing its prompts.
- [persistence_rule] Persist each reflected outcome where it belongs, for example the literature note, an existing entity, `concepts/` or another suitable folder; do not create a new folder without Syafiq's explicit authorisation.
- [unsupervised_relation] Unsupervised ingestion, not yet drafted, is expected to scope themes without human synthesis and leave a foundation for later agent-facilitated reflection.

## Relations
- governed_by [[AGENTS.md]]