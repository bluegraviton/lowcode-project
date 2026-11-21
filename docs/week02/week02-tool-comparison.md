# Week 2 — AI Tool Comparison


## The requirements

For each assistant available to you (Claude, Gemini, Manus — two is acceptable):

1\.	Write your prompt. Apply the four levers: specificity, constraints, context, iteration.

2\.	Save the prompt verbatim. You need it for the write-up. Copying it afterwards from memory is not the same thing.

3\.	Generate the code and save it to experiments/week02/<toolname>/.

4\.	Actually run it. Note whether it worked first time, and what you had to change.



Note: all prompts identical with the exception of the requested file name which follows this pattern: app\_ModelName\_contact\_test.py




## Prompts used

### Prompt for Claude

attached is a simple web app in a file called app.py. Using flask 3.x execute the task below. 

Using standard libraries and a minimum of python 3.9 create a new file called app\_claude\_contact\_test.py.



specifications for app\_claude\_contact\_test.py



includes all of app.py 

generates a contact form to add to app.py

must render a new page at /contact with fields for name, email and message.

must validate the email address is well-formed server-side

must reject an empty name, email or message field with a visible error

on success must show a confirmation page

does not store any information yet

must add contact to the navigation

must ensure that confirmation page includes navigation so user can return to home 





### Prompt for Gemini

attached is a simple web app in a file called app.py. Using flask 3.x execute the task below.

Using standard libraries and a minimum of python 3.9 create a new file called app\_gemini\_contact\_test.py.



specifications for app\_gemini\_contact\_test.py



includes all of app.py

generates a contact form to add to app.py

must render a new page at /contact with fields for name, email and message.

must validate the email address is well-formed server-side

must reject an empty name, email or message field with a visible error

on success must show a confirmation page

does not store any information yet

must add contact to the navigation

must ensure that confirmation page includes navigation so user can return to home



### Prompt for Perplexity

attached is a simple web app in a file called app.py. Using flask 3.x execute the task below.

Using standard libraries and a minimum of python 3.9 create a new file called app\_perplexity\_contact\_test.py.



specifications for app\_perplexity\_contact\_test.py



includes all of app.py

generates a contact form to add to app.py

must render a new page at /contact with fields for name, email and message.

must validate the email address is well-formed server-side

must reject an empty name, email or message field with a visible error

on success must show a confirmation page

does not store any information yet

must add contact to the navigation

must ensure that confirmation page includes navigation so user can return to home







## Scores

| Criterion | Claude | Gemini | Perplexity |

|---|---|---|---|

| Correctness | 5 | 5 | 5 |

| Code quality | 4  | 4  | 5 |

| Completeness | 5 | 3 |5 |

| Security | 4 | 1 | 4 |

| Total | 18 | 13 | 19 |



### Scoring Explained



#### Correctness

Claude: Runs unmodified first time and validation of all fields handled correctly. No mistakes so = 5.

Gemini: Runs unmodified first time and validation of all fields handled correctly. No mistakes so = 5.

Perplexity: Runs unmodified first time and validation of all fields handled correctly. No mistakes so = 5.



#### Code Quality

Claude:  Least efficient at 159 lines code. No comments so difficult to identify which parts are for which. But extra code includes security features. Total = 4

Gemini: Most efficient at 107 lines code but code is too efficient as security features missing. No comments so difficult to identify which parts are for which. Total = 4

Perplexity: Medium efficiency at 129 lines code and still build security in. No comments so difficult to identify which parts are for which. Total = 5



#### Completeness

Claude: Executed all requests. Creates big red warning box when validation fails and highlights field boxes in red and gives individual instruction under field box. Validation worked for each field including name, email and message. Helpful success message.

Gemini: Executed all requests however, warning messages are same regardless of which field/fields have a validation error with the exception of email alone, which has it's own error message. Validation worked for each field including name, email and message. Basic success message.

Perplexity: Executed all requests. Efficient main error message with red highlights around field boxes that failed validation and gives individual instruction under failed field box as well. Validation worked for each field including name, email and message. Success message is technically useful noting form passed validation and no data has been stored.



#### Security

##### Hardcoding Secrets
None of the models hardcoded any secrets which is good. However, at this stage in the development, there were no secrets to hardcode so must be checked in the future when project more complex.

##### debug=True
Present in all three versions. Acceptable for local development, but it must be disabled before deployment because it exposes detailed error pages and, in Flask, an interactive debugger. Fix: debug=False, or control it with an environment variable.

##### <script>alert(1)</script> 

Method: Submitted XSS payloads with a validation error forced, so the form re-displayed the input, then checked both the browser behaviour and View Source.

| Model | Message | Name | Email | Result |
|---|---|---|---|---|
| Claude | Escaped | Escaped | Escaped | Pass |
| Perplexity | Escaped | Escaped | Escaped | Pass |
| Gemini | Unescaped | Not tested | Not tested | Fail |

Claude and Perplexity: <script>alert(1)</script> and </textarea><script>alert(1)</script> were returned as &lt;script&gt; and &lt;/textarea&gt;. No script executed. The same payload in the name and email fields was also escaped. No XSS observed.

Gemini: The basic payload showed as raw <script> in the page source but did not run, only because it landed inside a <textarea>. The breakout payload </textarea><script>alert(1)</script> executed (alert popup observed). Reflected XSS confirmed. Name and email were not tested because the version had already failed.
Recommended fix: escape all user-supplied values with html.escape(value, quote=True) before inserting them into the page.
Success page (all versions): Input is not echoed back or stored, so there is no output point on that path. If the app later stores or displays messages, repeat the tests.

Success page (all models): Input is not echoed back or stored, so there is no output point on that path. If the app later stores or displays messages, repeat the tests.

Overall: Claude and Perplexity passed. Gemini fails on output escaping and needs fixing. All three need debug=True addressed before any deployment.


## What each got wrong

Claude used the most code and had minimal comments while also having debug=True. There was some overlap in the errors for validation with a warning box at the top containing each error and the same error message below the field.

Perplexity had minimal comments while also having debug=True. It's success message was technical rather than customer friendly.

Gemini had minimal comments while also having debug=True. It's validation error messages were basic and not customised to the actual error with the exception of an incorrectly formed email. More importantly, it did not escape any field allowing the potential attacker run any JavaScript in a visitor's browser.


## Which I kept, and why

Based on scoring alone I should go with Perplexity. However, as the scores between Perplexity and Claude were only 1 in difference and I don't believe I'm expert enough to accurately judge code quality yet, I pasted the two sets of code with no model identifier into a clean version of Claude and asked it to judge the code quality (where Perplexity was the first code and Claude was the second). It returned an interesting result.  

Specifically it noted; "The second is easier to read, maintain, and test, which is what “coding quality” mostly comes down to. The first is slightly more careful about behaviour and security. The best result would be the second’s structure with the first’s redirect-after-POST, no echo on the success page, and stricter email checks."

As a result, I instructed Claude to combine the best parts of both files. First I asked it to write the prompt for combining the files, then I pasted this prompt and the two files into a clean Claude conversation. This new amalgamated file, after running the security checks again, is the one I kept. I iterated on this new file twice, first for my preferred error message style which simplified the messaging slightly though after analysing it Claude pointed out that it made things worse for screen-reader users. A third version improved on this, adding back in the list in the box but making them clickable links to jump down to the error fields. 

See below for the explanded explanation.


### Claude judging the original 2 code files

#### Prompt
Attached are two codes, which do you think is best and why? Judge on coding quality

#### Answer

My pick: the second one, on code quality. It’s close, though, and the first has some strengths worth keeping. I’ve judged the code only, without knowing which tool wrote which.

Why the second is better built

Separation of concerns. validate_contact() is a pure function that takes values and returns errors. It’s easy to read and to unit test. In the first, validation is inline inside the route.
Readability. The form is a readable HTML template with small helpers (val, field_error, cls, aria). The first builds HTML by string concatenation inside a loop, which is dense and easy to break when someone edits it.
No duplication. The first lists the three fields in two places (contact_form and contact), so changing one means remembering to change the other.
Better error UX. It shows a summary list plus per-field messages, linked with aria-describedby.
Cleaner escaping. Every output goes through a single helper, so it’s harder to forget one.

What the first does better

Post/Redirect/Get. It redirects with a 303 after success. The second returns the success page directly from the POST, so refreshing the page re-submits the form.
Doesn’t echo input on success. This matches your “nothing stored or sent” design and removes an output point. The second prints the name and email back (escaped, so it’s safe, but it’s more surface to maintain).
More thorough email validation. It checks local part length (64), domain length, per-label rules, and rejects all-numeric TLDs.
Tidy comments. It has useful notes like “do not persist, log, email...”.

Issues in the second to fix

The email regex ends with $ and is used with .match(). In Python, $ also matches just before a trailing newline. It’s harmless here because values are stripped, but re.fullmatch is more correct.
It needs the redirect-after-POST pattern.
It has no local part length limit (64 characters).

Shared weaknesses (both)

debug=True, as flagged earlier.
No maximum length on name or message, so someone could submit a huge payload.
No CSRF protection. That doesn’t matter while nothing is stored, but it will if you add saving or sending.
The first has an unused import risk too: check that redirect and url_for are all actually used. They are, but only in that one place.

Verdict: The second is easier to read, maintain, and test, which is what “coding quality” mostly comes down to. The first is slightly more careful about behaviour and security. The best result would be the second’s structure with the first’s redirect-after-POST, no echo on the success page, and stricter email checks.


### Combination Prompt

#### Prompt
OK write an efficient prompt to combine the best parts of both files as per your verdict.

#### Answer
I'm attaching two Flask contact-form apps (File 1 and File 2). Merge them into one single-file Flask app, using the structure of File 2 and the behaviour and security of File 1.

Keep from File 2:
- The pure validate_contact(name, email, message) function returning a dict of field -> error
- The readable template-style contact_form() with small helpers (val, field_error, cls, aria)
- The error summary list plus per-field messages, linked with aria-describedby
- All user values escaped via html.escape(..., quote=True) through a single helper

Take from File 1:
- Post/Redirect/Get: on success, return redirect(url_for("contact_confirmation"), code=303) and add a /contact/confirmation route
- The confirmation page must NOT echo any submitted data. Use: "Thank you. Your contact form passed validation. No information has been stored or sent."
- The stricter email validation: max 254 chars, local part max 64, domain max 253, per-label rules, at least two labels, no leading/trailing/consecutive dots in the local part, and no all-numeric TLD. Use re.fullmatch instead of match with $.
- The comment noting that submitted data is never persisted, logged, emailed, or put in the URL/session

Also fix these shared weaknesses:
- Replace debug=True with debug=os.environ.get("FLASK_DEBUG") == "1" (off by default)
- Add maximum lengths for name (100) and message (2000), with a validation error message for each
- Add a short comment saying CSRF protection (e.g. Flask-WTF) is needed if saving or sending is ever added

Constraints:
- Keep the same routes (/, /about, /contact), nav, styling, and page text
- Return 400 with the form re-displayed when validation fails
- Keep it a single file with no new dependencies
- Remove any unused imports

Return only the complete code, then a short list of what changed.

### V2 Iteration 

After pasting the above prompt into a clean conversation and generating a new combined code file, I tested it and noticed that it had the same redundant error message behaviour as the original Claude file - that is having an error box at the top listing each error and the same error message under each field that required fixing. I iterated on this to give it a simpler behaviour with a error box at the top now containing a simple message to fix the errors below and retaining the individual error messages under each field requiring fixing. 

#### Prompt
take this new file and rewrite it so that the displayed error message simply says, "Please correct the errors below." In the red error box at the top of the screen while retaining the individual error messages below each field. 

Retain all new features, security and structure. Simply change the message displayed inside the error box. Confirm no other changes before presenting the code to me.

### V3 Iteration

I then compared the two files once more and Claude pointed out that V2 was visually cleaner, and there’s no duplication, since each message appears only once, next to its field but was weaker for screen-reader users and left and unused .errors ul rule behind. It made suggestions for V3 which I accepted. 

#### Summary of changes for V3
Error summary: the box still opens with “Please correct the errors below.” and now lists each error as a link (<a href="#name"> and so on) to the failing field. The link text is escaped with h().
Focus on error: the summary has tabindex="-1" and autofocus, so focus moves to it when the form is re-displayed. No JavaScript is needed.
MAX_CONTENT_LENGTH: set to 32 KB, so oversized requests are rejected early with a 413. I chose 32 KB rather than 16 KB because 2000 non-ASCII characters can expand to about 24 KB once URL-encoded, and a valid maximum-length message shouldn’t be rejected.
maxlength attributes: added to name (100), email (254) and message (2000) using the existing constants. Server-side validation still enforces the limits.
CSS: one added rule, .errors a { color: inherit; }, so the links match the error colour. The existing .errors ul rule is used again.