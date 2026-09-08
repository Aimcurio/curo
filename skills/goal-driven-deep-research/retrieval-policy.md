# Goal-Driven Deep Research Retrieval Policy

## Objective

Tell a research-capable LLM what to retrieve, in what order, and under what evidence-quality expectations.

## Source priority

Prefer, when available:

1. primary sources;
2. official documentation and specifications;
3. original research papers, datasets, and source code;
4. authoritative institutional or vendor material;
5. high-quality secondary analysis;
6. community discussion for experience signals, discovery, and dissent—not as sole authority for high-stakes factual claims.

## Retrieval rules

- Retrieve only material relevant to a defined investigation question.
- Prefer recent sources when the subject is time-sensitive.
- Preserve publication/update dates when material freshness matters.
- Record source type and provenance.
- Use secondary sources to discover primary sources when possible.
- Do not inflate source count when multiple sources repeat the same underlying claim.
- Track source independence where practical.
- Distinguish missing evidence from negative evidence.
- If a source is inaccessible, record the limitation instead of inferring its contents.

## Required retrieval fields

Each evidence record should capture:

- evidence_id
- investigation_id
- source_uri or stable source identifier
- source_title
- source_type
- publisher_or_author
- published_or_updated_at when relevant
- retrieved_at when relevant
- claim_supported_or_challenged
- excerpt_or_summary
- provenance_notes
- independence_notes

## Retrieval stop condition

Stop retrieving for an investigation when:

- its evidence requirements are satisfied;
- contradiction search has been performed where required;
- additional retrieval is unlikely to materially change the decision;
- or the investigation is explicitly blocked/insufficient.
