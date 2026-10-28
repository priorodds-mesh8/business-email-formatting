---
name: business-email-formatting
description: Format business email drafts and replies with short paragraphs, useful lists, clear requests, and output suited to the email tool. Use when composing, rewriting, reviewing, or preparing business email for delivery. Do not apply to email summaries, mailbox search, or unrelated prose.
license: MIT
metadata:
  version: "1.0.0"
---

# Business email formatting

Make the email easy to scan and act on. Preserve the writer's meaning and the reader's context.

## Scope and language

Apply this skill to the email body and subject, including drafts shown only in chat. An explicit user format takes priority.

Follow the user's existing voice and language rules. This skill controls layout, not vocabulary or voice. If STE100 or anti-slop is installed, use it under the user's configured precedence. Neither skill is required. Without a separate style guide, use plain words, short sentences, active voice, and one idea per sentence.

Do not change approved copy merely to apply a preferred template. For format-only edits, preserve wording unless the user also requests a rewrite. Keep names, amounts, dates, links, commitments, exclusions, and uncertainty intact. Do not invent an owner, deadline, attachment, approval, or result.

## Choose the structure

Infer the audience, purpose, and relationship from the request and thread. Ask only when a missing fact changes the substance. Use the smallest useful structure.

| Message | Default structure |
| --- | --- |
| Short reply | Answer, needed context, next step if any. No headings by default. |
| Request | Request near the start, brief reason, required inputs, known deadline. |
| Update | Overall status, material changes, risks, next action. |
| Meeting recap | Decisions, open questions, actions with known owners and dates. |
| Proposal follow-up | Recommendation, relevant terms or changes, decision request. |
| Sensitive message | Brief acknowledgment, clear explanation, next step. Use lists only when helpful. |
| Cold outreach | Relevant context, useful offer, one primary response request. No forced headings or bullets. |

Read [examples.md](references/examples.md) when the format is unclear or a dense draft needs a structural rewrite. The examples show conditional choices, not fixed wording.

## Layout rules

- State the purpose, result, or request within the first two sentences. Allow a brief acknowledgment when the situation needs care.
- Keep one topic per paragraph. Default to one to three short sentences with visible space between paragraphs.
- Use bullets for parallel facts, deliverables, options, or actions when a list improves scanning. Two to five items per group is a useful default, not a quota.
- Use numbers for ordered steps or questions that need separate answers. Keep each item focused on one point.
- Add two or three key takeaways only when a substantial message needs an overview. Do not repeat the same summary at the end.
- Use short descriptive section labels when the message has distinct sections. Omit empty sections and headings that add no value.
- Bold short labels or a material decision or deadline sparingly. Keep the meaning clear without bold or color.
- Prefer one primary request. If the reader must do several things, group the related actions in a list.
- Use the shortest complete message. Do not force a universal word limit or compress several ideas into one sentence.
- Keep the layout in one column. Avoid layout tables, deep nesting, decorative banners, and images of text. Use a simple data table only when it improves the actual comparison.
- Give links descriptive text in rich text. Retain usable destination URLs in plain text. Do not invent missing links.
- State the topic and real action in a new subject. Preserve the existing subject for a direct reply unless the topic changes.

These counts are house defaults. Adjust them to preserve meaning, the user's chosen format, and natural correspondence.

## Output and delivery

For a chat-only draft, use readable paragraphs and lists. Put a new subject outside the body. Do not add research notes or format explanations inside the email.

Before a draft or send tool call, read [delivery.md](references/delivery.md). Match the supported body format and preserve paragraph and list structure. A string is acceptable when it contains the correct separators or markup.

This skill grants no permission to send, create drafts, change recipients, or alter sender settings. Follow the user's existing task authority. Do not request permission again for an action already authorized.

## Final check

Before delivery, check the actual email:

1. Can the reader find the purpose and required action quickly?
2. Do paragraphs separate topics, and do lists group related items?
3. Does the layout fit this message without forced takeaways or headings?
4. Are the original facts, qualifications, and commitments intact?
5. Does the intended output preserve the spacing, links, and list structure?

For factual uncertainty, preserve the qualification. For a format failure, correct the body before the authorized action. Never claim a client preview passed without inspecting it.
