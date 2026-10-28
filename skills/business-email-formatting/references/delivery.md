# Email output and delivery

Read this file before an email draft or send tool call. Use the tool's current schema to identify the body format. Do not infer the format from a field named `body`.

## Plain text

- Separate paragraphs with a blank line: two newline characters.
- Put each list item on its own line. Use `- ` for bullets and `1. ` for numbered items.
- Use plain section labels only when needed. Do not send Markdown bold markers or heading hashes as decoration.
- Include a readable label and the destination URL when a link matters.
- Serialize the text once through the tool or JSON library. Do not replace real newlines with literal backslash-n text.

## HTML or rich text

- Use actual paragraph elements and real list elements: `p`, `ul`, `ol`, and `li`, or the editor's equivalent controls.
- Newlines in HTML source do not create paragraph spacing. Do not place one plain text block inside a single paragraph and expect separate paragraphs.
- Use descriptive semantic headings in long messages when supported. Keep their levels in order.
- Use `strong` for brief emphasis. Keep action labels explicit, since emphasis alone does not carry meaning for every reader.
- Keep body text left aligned and readable. Use simple spacing and the existing approved font or client default.
- Escape inserted text and attribute values if constructing HTML. Preserve the original destination of each link.
- Do not paste raw Markdown into an HTML body and assume that the client converts it.
- If the tool supports both HTML and plain text, give equivalent content in both. Do not add unsupported fields.

## Check before and after the tool

Check the final subject and body before the authorized action. Make sure the recipient, thread, and attachments still match the request. Keep commentary and review notes outside the email.

When the workflow creates a saved draft, inspect its body through readback or a client preview if available. Check that paragraphs remain separate, list items stay distinct, and links retain their destinations. If HTML is available, distinguish the source check from the rendered preview. Check a narrow view when a preview supports it.

If the workflow sends directly, check the final payload first. Use available post-send readback to confirm the result. Do not create an extra draft solely for this skill when the user already authorizes direct sending.

If a tool returns an uncertain result, inspect its state before retrying. Do not create a duplicate draft or send to repair an unconfirmed result. An after-send format fault does not authorize another send.

Report only checks that actually run. If no preview exists, report that limit when material. Do not block an otherwise authorized send solely because the tool has no preview.

## Same content in two formats

The following example uses fictional facts. It illustrates output structure, not a required email template.

Plain text:

```text
Hi Alex,

Please send these two inputs:

- The approved account list.
- The report date range.

I can finish the estimate after I receive both.

Thanks,
Sam
```

HTML body:

```html
<p>Hi Alex,</p>
<p>Please send these two inputs:</p>
<ul>
  <li>The approved account list.</li>
  <li>The report date range.</li>
</ul>
<p>I can finish the estimate after I receive both.</p>
<p>Thanks,<br>Sam</p>
```
