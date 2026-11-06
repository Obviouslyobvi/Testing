# Plan: Getting a grip on Gmail

**The one line:** Figure out which Gmail problem is worth a tool, then build that tool using the three parts every app is made of: presentation, logic, data.

*Written Nov 6, 2026 from a live look at the mailbox. Personal details are kept out of this file on purpose; the full version lives in the chat.*

## 1. Where things stand

| Measure | Count |
|---|---|
| Inbox threads | 31 |
| Inbox unread | 17 |
| Unread across the whole mailbox | 90,491 |
| Gmail filters | 760 |
| User-made labels | 45 |
| Largest label (sweepstakes) | 12,341 threads, 11,049 unread |
| Updates tab unread | 48,453 |
| Promotions tab unread | 26,966 |
| Sent messages, all time | 54,995 |

The inbox itself is small and under control. The weight is everywhere else: tens of thousands of unread messages sitting in categories and labels, most of them sweepstakes and newsletters that filters already route away.

## 2. What is already automated

A lot. This is not a mailbox starting from zero.

- **760 filters** kept current by a nightly script that emails a sync report to yourself.
- **Sports betting reports** emailed to yourself three times a day.
- **ChatGPT scheduled tasks** emailing in permit-watch results that update a spreadsheet.
- **Boomerang** labels for snoozed and returned mail.
- **A daily newsletter you publish**, which also lands in this inbox.
- **Two Google Takeout exports** finished this week. Something is already being pulled out of this account.

## 3. What is in the inbox right now

Grouped by what it is, not by who sent it:

- **Financial statements:** several brokerage and credit card notices.
- **Business threads:** a data sample test, a long-running partner thread, a few one-to-one contacts.
- **Household and family:** a pharmacy service shutting down, a public records request.
- **Tool and task notifications:** ChatGPT tasks, a browser automation tool, Google Takeout.
- **Paid studies:** several market research panels.

## 4. Three directions a first tool could take

**A. Morning inbox page.** One HTML page that groups the last day of mail the way section 3 does, with a comment box under each group so you can type "reply," "archive," or "ignore" and copy all of it back in one message. This is the review page from the crash course, pointed at your inbox.

**B. Label and filter map.** A visual of the 45 labels and 760 filters: which labels are dead (several hold a handful of messages), which overlap (three checkmark labels, two tax labels), which filters route to labels nobody reads. Built from a Takeout export, no live Gmail access needed.

**C. Outreach tracker.** Twelve cold emails went out on one day this week from three templates. A page listing each recipient, the template, the send date, and a follow-up date, with a box to note replies.

## 5. Proposed first build

Pick one of A, B, or C. Each one maps cleanly onto the course:

- **Presentation:** the HTML page.
- **Logic:** comment boxes and the copy button.
- **Data:** comments saved in browser storage so they survive a refresh.

Option A is the closest to the crash course and the most reusable. Option C is the most directly tied to money. Option B is the most work and needs the Takeout file.

## 6. Things I noticed along the way

- One recent sent email contains a credential in plain text. Worth rotating it and sending the new one another way.
- Mail for three different people lands in this one account.
- The sent-to-self reports sit unread and pile up unless something clears them.

## Three open questions for you

1. When you say "Gmail," which hurts most right now: too much coming in, finding things later, or keeping track of business conversations?
2. Does the tool need to handle more than one person's mail, or just yours?
3. The two Google Takeout exports from this week: are those for a Gmail project already in progress, and if so, what is it?
