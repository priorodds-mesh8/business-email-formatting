# Behavioral review cases

Use these cases with the installed skill in your agent. They are a manual review set, not automated model scores. Do not send the outputs.

| Case | Input or request | What to check |
| --- | --- | --- |
| Dense request | Ask for an approved account list and report date range. State that data purchases are separate from the fee. | The inputs form a useful list. The fee exclusion remains. No deadline appears. |
| Short reply | Confirm Tuesday at 10 AM Central. | A short reply without forced headings or a new calendar claim. |
| Exact copy | Format only: “The fee is $12,000. Data purchases are separate. Start is conditional on approval.” | Every original word remains. The condition and exclusion stay clear. |
| Uncertain update | The export may be incomplete. The team has not confirmed the missing rows. | The result remains uncertain. The agent does not claim a confirmed defect. |
| Meeting recap | Morgan sends the account list by November 3. Sam sends the sample report by November 5. | Owners and dates stay attached to the correct actions. |
| Sensitive message | Apologize for a missed review and explain that a new date is not yet confirmed. | A natural acknowledgment and explanation. No invented date or forced bullet list. |
| Scope exclusion | Summarize a received email. | The skill does not impose an outgoing email template. |
| HTML tool | Format an approved request with two input items for a tool that accepts HTML. | Real paragraph and list elements, with no raw Markdown formatting markers. |
| Plain text tool | Use the same request with a text-only tool. | Blank lines and separate list items. The content matches the HTML version. |

Record the agent, version, input, output, and any failure. A good result in one host does not prove behavior in another.
