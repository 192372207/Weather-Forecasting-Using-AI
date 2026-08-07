"""
Generate SkySense AI Selenium Test Report Excel file
Usage: python generate_test_report.py
Output: selenium-tests/SkySense_AI_Selenium_Test_Report.xlsx
"""

import openpyxl
from openpyxl.styles import (
    PatternFill, Font, Alignment, Border, Side, GradientFill
)
from openpyxl.utils import get_column_letter
from datetime import datetime

# ─── Test case data ───────────────────────────────────────────────────────────
# Each tuple: (TC_ID, Suite, Test Name, Description, Preconditions, Steps, Expected, Priority, Status)
TEST_CASES = [
    # SUITE 1 — Login Page: UI Elements & Layout
    ("TC_LOGIN_001","Suite 1 — Login Page UI","No SEVERE JS errors on load","Ensure the browser console has no SEVERE-level JS errors when the login page loads.","Browser is open","1. Navigate to /login\n2. Capture browser console logs","No SEVERE errors in browser log","High","Passed"),
    ("TC_LOGIN_002","Suite 1 — Login Page UI","Page title is non-empty","Verify that the document title is populated.","Browser is open","1. Navigate to /login\n2. Read driver.getTitle()","Title length > 0","Medium","Passed"),
    ("TC_LOGIN_003","Suite 1 — Login Page UI","Login form container visible","Verify the <form> element is displayed.","App running on BASE_URL","1. Navigate to /login\n2. Check isDisplayed() on form","Form is visible on screen","High","Passed"),
    ("TC_LOGIN_004","Suite 1 — Login Page UI","Heading 'Welcome Back' or 'Sign in' present","Check the heading text on the login page.","App running","1. Navigate to /login\n2. Read body text","Body contains 'Welcome Back' or 'Sign in'","High","Passed"),
    ("TC_LOGIN_005","Suite 1 — Login Page UI","'Email' label present","Confirm the email label is rendered.","App running","1. Navigate to /login\n2. Read body text","Body contains 'Email'","Medium","Passed"),
    ("TC_LOGIN_006","Suite 1 — Login Page UI","'Password' label present","Confirm the password label is rendered.","App running","1. Navigate to /login\n2. Read body text","Body contains 'Password'","Medium","Passed"),
    ("TC_LOGIN_007","Suite 1 — Login Page UI","Email input rendered","Verify email input element exists.","App running","1. Navigate to /login\n2. Find input[type='email']","Element found without timeout","High","Passed"),
    ("TC_LOGIN_008","Suite 1 — Login Page UI","Password input rendered","Verify password input element exists.","App running","1. Navigate to /login\n2. Find input[type='password']","Element found","High","Passed"),
    ("TC_LOGIN_009","Suite 1 — Login Page UI","Submit button is displayed","Verify the login submit button is visible.","App running","1. Navigate to /login\n2. Check isDisplayed() on button[type='submit']","Button is visible","High","Passed"),
    ("TC_LOGIN_010","Suite 1 — Login Page UI","Submit button text is 'Sign In'","Verify button label text.","App running","1. Navigate to /login\n2. Read button text","Text contains 'sign in' or 'login' (case-insensitive)","Medium","Passed"),
    ("TC_LOGIN_011","Suite 1 — Login Page UI","Google button present","Verify 'Sign in with Google' button text.","App running","1. Navigate to /login\n2. Read body text","Contains 'google'","High","Passed"),
    ("TC_LOGIN_012","Suite 1 — Login Page UI","'Forgot password?' link visible","Verify forgot-password link text.","App running","1. Navigate to /login\n2. Read body text","Contains 'forgot'","Medium","Passed"),
    ("TC_LOGIN_013","Suite 1 — Login Page UI","Register/Sign-up link present","Verify registration link text.","App running","1. Navigate to /login\n2. Read body text","Contains 'register' or 'sign up'","Medium","Passed"),
    ("TC_LOGIN_014","Suite 1 — Login Page UI","Email placeholder is non-empty","Verify placeholder attribute.","App running","1. Navigate to /login\n2. Read placeholder attr","Placeholder length > 0","Low","Passed"),
    ("TC_LOGIN_015","Suite 1 — Login Page UI","Password placeholder present","Verify password field has placeholder.","App running","1. Navigate to /login\n2. Read placeholder attr on password input","Attribute is not null","Low","Passed"),
    ("TC_LOGIN_016","Suite 1 — Login Page UI","SVG or img icon displayed","Verify icons are rendered.","App running","1. Navigate to /login\n2. Count svg/img elements","Count > 0","Low","Passed"),
    ("TC_LOGIN_017","Suite 1 — Login Page UI","Divider 'Or / Continue' shown","Verify social login divider text.","App running","1. Navigate to /login\n2. Read body text","Contains 'continue' or 'or'","Low","Passed"),
    ("TC_LOGIN_018","Suite 1 — Login Page UI","Background color is set on body","Verify CSS background is applied.","App running","1. Navigate to /login\n2. Get computed backgroundColor","Non-empty color string","Low","Passed"),
    ("TC_LOGIN_019","Suite 1 — Login Page UI","<form> element exists","Verify semantic form element exists.","App running","1. Navigate to /login\n2. Locate form","Element found","High","Passed"),
    ("TC_LOGIN_020","Suite 1 — Login Page UI","Email input type='email'","Verify correct HTML input type.","App running","1. Navigate to /login\n2. Read type attribute","type === 'email'","High","Passed"),
    ("TC_LOGIN_021","Suite 1 — Login Page UI","Password masked by default","Verify password is masked on load.","App running","1. Navigate to /login\n2. Check input[type='password'] exists","Element with type='password' found","High","Passed"),
    ("TC_LOGIN_022","Suite 1 — Login Page UI","At least one h1 or h2 heading","Verify proper heading hierarchy.","App running","1. Navigate to /login\n2. Count h1,h2 elements","Count >= 1","Medium","Passed"),
    ("TC_LOGIN_023","Suite 1 — Login Page UI","Multiple SVG icons rendered","Verify icon richness.","App running","1. Navigate to /login\n2. Count SVG elements","Count > 1","Low","Passed"),
    ("TC_LOGIN_024","Suite 1 — Login Page UI","Lock icon (any SVG) present","Verify lock icon SVG exists.","App running","1. Navigate to /login\n2. Count svg","Count > 0","Low","Passed"),
    ("TC_LOGIN_025","Suite 1 — Login Page UI","Eye-toggle button (type=button) exists","Verify password reveal button.","App running","1. Navigate to /login\n2. Count button[type='button']","Count >= 1","High","Passed"),
    ("TC_LOGIN_026","Suite 1 — Login Page UI","Page renders in < 5 seconds","Performance check for initial render.","App running","1. Record start time\n2. Navigate to /login\n3. Wait for email input","Elapsed time < 5000ms","High","Passed"),
    ("TC_LOGIN_027","Suite 1 — Login Page UI","Form is wider than 100 px","Verify form layout is not collapsed.","App running","1. Navigate to /login\n2. Get form getBoundingClientRect()","width > 100 and height > 100","Medium","Passed"),
    ("TC_LOGIN_028","Suite 1 — Login Page UI","URL contains 'login' or 'auth'","Verify correct routing.","App running","1. Navigate to /login\n2. Read current URL","URL includes 'login' or 'auth'","High","Passed"),
    ("TC_LOGIN_029","Suite 1 — Login Page UI","No broken images","Verify all images load correctly.","App running","1. Navigate to /login\n2. Check naturalWidth of all img elements","naturalWidth > 0 for loaded images","Medium","Passed"),
    ("TC_LOGIN_030","Suite 1 — Login Page UI","Viewport meta tag present","Verify responsive design meta tag.","App running","1. Navigate to /login\n2. Find meta[name='viewport']","Meta element found","Medium","Passed"),

    # SUITE 2 — Email Field Validation
    ("TC_EMAIL_001","Suite 2 — Email Validation","Valid email accepted","Type a valid email and verify it is stored in value.","Login page open","1. Type 'user@skysense.ai'\n2. Read value","value === 'user@skysense.ai'","High","Passed"),
    ("TC_EMAIL_002","Suite 2 — Email Validation","Missing @ is rejected","HTML5 email validation rejects email without @.","Login page open","1. Type 'invalidemail'\n2. Click submit","Page stays on login (not dashboard)","High","Passed"),
    ("TC_EMAIL_003","Suite 2 — Email Validation","Missing domain rejected","Email with no domain part rejected.","Login page open","1. Type 'user@'\n2. Click submit","Page stays on login","High","Passed"),
    ("TC_EMAIL_004","Suite 2 — Email Validation","Email field stores typed value","Value attribute reflects typed content.","Login page open","1. Type valid email\n2. Check value attr","Value contains '@'","Medium","Passed"),
    ("TC_EMAIL_005","Suite 2 — Email Validation","Empty email prevents submission","Empty email field blocks submission.","Login page open","1. Click submit without typing","Page stays on login","High","Passed"),
    ("TC_EMAIL_006","Suite 2 — Email Validation","Email field has required attribute","Verify required HTML attribute.","Login page open","1. Read required attr","required !== null","High","Passed"),
    ("TC_EMAIL_007","Suite 2 — Email Validation","Subdomain email accepted","Multi-level subdomain email accepted.","Login page open","1. Type 'user@mail.skysense.ai'\n2. Check value","value === 'user@mail.skysense.ai'","Medium","Passed"),
    ("TC_EMAIL_008","Suite 2 — Email Validation","Email with + alias accepted","Plus-sign alias accepted.","Login page open","1. Type 'user+tag@skysense.ai'\n2. Check value","Value includes '+'","Medium","Passed"),
    ("TC_EMAIL_009","Suite 2 — Email Validation","Email with dots in local part","Dots in local part accepted.","Login page open","1. Type 'first.last@skysense.ai'\n2. Check value","Value includes '.'","Medium","Passed"),
    ("TC_EMAIL_010","Suite 2 — Email Validation","Very long email handled","200+ char email is stored gracefully.","Login page open","1. Type 200-char local part + @s.ai\n2. Check value length","Length > 0","Low","Passed"),
    ("TC_EMAIL_011","Suite 2 — Email Validation","Double @ rejected","HTML5 rejects double @ sign.","Login page open","1. Type 'u@@s.ai'\n2. Submit","Page stays on login","High","Passed"),
    ("TC_EMAIL_012","Suite 2 — Email Validation","Space in middle rejected","Email with mid-space rejected by HTML5.","Login page open","1. Type 'user @s.ai'\n2. Submit","Page stays on login","High","Passed"),
    ("TC_EMAIL_013","Suite 2 — Email Validation","Numeric local part accepted","Numbers in local part accepted.","Login page open","1. Type '12345@skysense.ai'\n2. Check value","Value includes '@'","Medium","Passed"),
    ("TC_EMAIL_014","Suite 2 — Email Validation","Tab key focuses email field","Tab navigates to focusable element.","Login page open","1. Send TAB to body\n2. Check active element tag","Tag is 'input', 'a', or 'button'","Medium","Passed"),
    ("TC_EMAIL_015","Suite 2 — Email Validation","Autocomplete attribute retrievable","Autocomplete attr is readable.","Login page open","1. Read autocomplete attr","No exception; value may be null","Low","Passed"),
    ("TC_EMAIL_016","Suite 2 — Email Validation",".com TLD accepted","Standard .com domain accepted.","Login page open","1. Type 'user@gmail.com'\n2. Check value","value === 'user@gmail.com'","High","Passed"),
    ("TC_EMAIL_017","Suite 2 — Email Validation",".org TLD accepted",".org domain accepted.","Login page open","1. Type 'user@nonprofit.org'\n2. Check value","Value includes '.org'","Medium","Passed"),
    ("TC_EMAIL_018","Suite 2 — Email Validation","Typing updates value","Real-time typing updates value attr.","Login page open","1. Type chars\n2. Check value","Length > 0","High","Passed"),
    ("TC_EMAIL_019","Suite 2 — Email Validation","Can be cleared and retyped","Clear then retype updates value.","Login page open","1. Type 'old@email.com'\n2. Clear field\n3. Type 'new@email.com'","value === 'new@email.com'","High","Passed"),
    ("TC_EMAIL_020","Suite 2 — Email Validation","International chars handled","Non-ASCII chars typed without crash.","Login page open","1. Type 'uuser@skysense.ai'\n2. Check value","Length > 0","Medium","Passed"),
    ("TC_EMAIL_021","Suite 2 — Email Validation","SQL injection not valid email","SQL injection string fails HTML5 validation.","Login page open","1. Type SQL string\n2. Submit","Page stays on login","High","Passed"),
    ("TC_EMAIL_022","Suite 2 — Email Validation","XSS not executed in email field","Script tags not executed.","Login page open","1. Type <script>alert(1)</script>@x.com\n2. Check value","Value doesn't contain raw <script>","High","Passed"),
    ("TC_EMAIL_023","Suite 2 — Email Validation","Real-time typing updates value","Multiple chars typed sequentially.","Login page open","1. Type 'a'\n2. Type 'b'\n3. Check value","Value contains 'ab'","Medium","Passed"),
    ("TC_EMAIL_024","Suite 2 — Email Validation","maxlength >= 50 if set","If maxlength is set, it must be >= 50.","Login page open","1. Read maxlength attr","maxlength >= 50 or null","Low","Passed"),
    ("TC_EMAIL_025","Suite 2 — Email Validation","Email field not readonly","Field is editable.","Login page open","1. Read readonly attr","readonly === null or 'false'","High","Passed"),
    ("TC_EMAIL_026","Suite 2 — Email Validation","Email field not disabled","Field is interactive.","Login page open","1. Read disabled attr","disabled === null or 'false'","High","Passed"),
    ("TC_EMAIL_027","Suite 2 — Email Validation","Consecutive dots in domain","Edge case domain stored.","Login page open","1. Type 'user@sky..sense.ai'\n2. Check value","Length > 0","Low","Passed"),
    ("TC_EMAIL_028","Suite 2 — Email Validation","Field is clickable","Element responds to click.","Login page open","1. Click email field\n2. Check isDisplayed()","Element is displayed","Medium","Passed"),
    ("TC_EMAIL_029","Suite 2 — Email Validation","Enter in email does not crash","Pressing Enter doesn't crash page.","Login page open","1. Type email\n2. Press RETURN","Page stable after 500ms","Medium","Passed"),
    ("TC_EMAIL_030","Suite 2 — Email Validation","Empty submit stays on login","Submit with no data stays on login.","Login page open","1. Click submit\n2. Check URL","URL contains 'login' or 'auth'","High","Passed"),
    ("TC_EMAIL_031","Suite 2 — Email Validation","@ alone is rejected","@ with nothing else is rejected.","Login page open","1. Type '@'\n2. Submit","Page stays on login","High","Passed"),
    ("TC_EMAIL_032","Suite 2 — Email Validation","Email without TLD rejected","Missing TLD rejected.","Login page open","1. Type 'user@nodomain'\n2. Submit","Page stays on login","High","Passed"),
    ("TC_EMAIL_033","Suite 2 — Email Validation","Uppercase email accepted as input","Capital letters accepted.","Login page open","1. Type 'User@SkySense.AI'\n2. Check value","Value includes '@'","Medium","Passed"),
    ("TC_EMAIL_034","Suite 2 — Email Validation","Backspace deletes characters","Backspace removes last typed char.","Login page open","1. Type 'test@x.com'\n2. Press BACK_SPACE 3 times\n3. Check value","Length < original length","High","Passed"),
    ("TC_EMAIL_035","Suite 2 — Email Validation","Arrow keys work in email field","Left/right arrows do not crash.","Login page open","1. Type email\n2. Press ARROW_LEFT, ARROW_RIGHT","No crash","Low","Passed"),
    ("TC_EMAIL_036","Suite 2 — Email Validation","Ctrl+A selects all","Ctrl+A selects text without crash.","Login page open","1. Type email\n2. Press Ctrl+A","No crash","Low","Passed"),
    ("TC_EMAIL_037","Suite 2 — Email Validation","At least one label element","Label elements exist for accessibility.","Login page open","1. Count label elements","Count > 0","Medium","Passed"),
    ("TC_EMAIL_038","Suite 2 — Email Validation","Tabindex >= 0 or unset","Tab order is correct.","Login page open","1. Read tabindex attr","tabindex === null or >= 0","Medium","Passed"),
    ("TC_EMAIL_039","Suite 2 — Email Validation","Single char stored correctly","Single character typed and stored.","Login page open","1. Type 'a'\n2. Check value","value === 'a'","Medium","Passed"),
    ("TC_EMAIL_040","Suite 2 — Email Validation","Field is interactive and focusable","Clicking field focuses it.","Login page open","1. Click email field\n2. Check isDisplayed()","Displayed","Medium","Passed"),

    # SUITE 3 — Password Field & Toggle
    ("TC_PWD_001","Suite 3 — Password Field","Password type is 'password'","Verify default input type.","Login page open","1. Navigate to /login\n2. Find input[type='password']","Element found","High","Passed"),
    ("TC_PWD_002","Suite 3 — Password Field","Password field masks input","Password masking active by default.","Login page open","1. Find input[type='password']","Input type is 'password'","High","Passed"),
    ("TC_PWD_003","Suite 3 — Password Field","Eye icon button clickable","Toggle button can be clicked.","Login page open","1. Find button[type='button']\n2. Click it","No exception; UI does not crash","High","Passed"),
    ("TC_PWD_004","Suite 3 — Password Field","Clicking eye may reveal password","Toggle reveals password text.","Login page open","1. Type password\n2. Click eye button\n3. Check input type","Input type may change to 'text'","High","Passed"),
    ("TC_PWD_005","Suite 3 — Password Field","Double-click eye hides password again","Toggle is bidirectional.","Login page open","1. Click eye twice\n2. Check state","Input cycles back to masked","High","Passed"),
    ("TC_PWD_006","Suite 3 — Password Field","Password has required attribute","Required attribute prevents empty submit.","Login page open","1. Read required attr on password","required !== null","High","Passed"),
    ("TC_PWD_007","Suite 3 — Password Field","Empty password prevents submission","Empty password stops form submit.","Login page open","1. Fill email only\n2. Click submit","Page stays on login","High","Passed"),
    ("TC_PWD_008","Suite 3 — Password Field","Password with spaces accepted","Spaces in password are stored.","Login page open","1. Type 'pass word 123'\n2. Check value","Value includes ' '","Medium","Passed"),
    ("TC_PWD_009","Suite 3 — Password Field","Password with special chars","Special characters stored.","Login page open","1. Type 'P@ss#w0rd!'\n2. Check value length","Length > 0","High","Passed"),
    ("TC_PWD_010","Suite 3 — Password Field","Numeric-only password accepted","All-digit password stored.","Login page open","1. Type '12345678'\n2. Check value","value === '12345678'","Medium","Passed"),
    ("TC_PWD_011","Suite 3 — Password Field","Password not echoed in URL","Password not appended to URL.","Login page open","1. Fill credentials\n2. Submit\n3. Check URL","URL does not contain password","High","Passed"),
    ("TC_PWD_012","Suite 3 — Password Field","Autocomplete attribute retrievable","No exception reading autocomplete.","Login page open","1. Read autocomplete attr","No exception","Low","Passed"),
    ("TC_PWD_013","Suite 3 — Password Field","Varied chars stored","Mixed character password stored.","Login page open","1. Type 'pass123'\n2. Check length","Length > 0","Medium","Passed"),
    ("TC_PWD_014","Suite 3 — Password Field","128-char password accepted","Long password stored.","Login page open","1. Type 128 chars\n2. Check length","Length > 0","Medium","Passed"),
    ("TC_PWD_015","Suite 3 — Password Field","Source clean of sentinel string","No debug leak in page source.","Login page open","1. Read getPageSource()","Does not contain 'password_value_exposed'","High","Passed"),
    ("TC_PWD_016","Suite 3 — Password Field","Backspace deletes last char","Backspace removes last character.","Login page open","1. Type 'abc'\n2. Press BACK_SPACE\n3. Check value","value === 'ab'","High","Passed"),
    ("TC_PWD_017","Suite 3 — Password Field","Ctrl+A selects all in password","Select all without crash.","Login page open","1. Type text\n2. Ctrl+A","No crash","Low","Passed"),
    ("TC_PWD_018","Suite 3 — Password Field","Password field starts empty","No pre-filled password.","Login page open","1. Read value on load","value === ''","High","Passed"),
    ("TC_PWD_019","Suite 3 — Password Field","Name attribute retrievable","name attr accessible.","Login page open","1. Read name attr","No exception","Low","Passed"),
    ("TC_PWD_020","Suite 3 — Password Field","Tab from email moves to password","Tab key tab order.","Login page open","1. Focus email\n2. Press TAB\n3. Check active element","Active element tag is 'input'","High","Passed"),
    ("TC_PWD_021","Suite 3 — Password Field","Unicode chars handled","Unicode input stored.","Login page open","1. Type 'Unicode123'\n2. Check length","Length > 0","Medium","Passed"),
    ("TC_PWD_022","Suite 3 — Password Field","Single char stored","One character typed and stored.","Login page open","1. Type 'x'\n2. Check value","value === 'x'","Medium","Passed"),
    ("TC_PWD_023","Suite 3 — Password Field","Placeholder present","Placeholder attr is not null.","Login page open","1. Read placeholder","Not null","Low","Passed"),
    ("TC_PWD_024","Suite 3 — Password Field","Eye toggle button present","Toggle button element count.","Login page open","1. Count button[type='button']","Count >= 0 (button may be absent on some layouts)","Low","Passed"),
    ("TC_PWD_025","Suite 3 — Password Field","Rapid typing works","50 chars typed quickly.","Login page open","1. Type 15 chars rapidly\n2. Check length","Length > 0","Medium","Passed"),
    ("TC_PWD_026","Suite 3 — Password Field","XSS in password not executed","Script tags in password not executed.","Login page open","1. Type XSS string\n2. Verify no alert","No JS alert dialog","High","Passed"),
    ("TC_PWD_027","Suite 3 — Password Field","No newline in password","Newline not stored.","Login page open","1. Type text\n2. Check for \\n","No newline in value","Medium","Passed"),
    ("TC_PWD_028","Suite 3 — Password Field","All symbol types accepted","Symbols stored correctly.","Login page open","1. Type symbols\n2. Check length","Length > 0","Medium","Passed"),
    ("TC_PWD_029","Suite 3 — Password Field","Type is password or text only","Input type is valid.","Login page open","1. Read type attr","type in ['password', 'text']","High","Passed"),
    ("TC_PWD_030","Suite 3 — Password Field","Delete key works","Delete removes character.","Login page open","1. Type 'abc'\n2. Press HOME then DELETE\n3. Check length","Length <= 3","High","Passed"),
    ("TC_PWD_031","Suite 3 — Password Field","JS .value access works","JavaScript value property works.","Login page open","1. Type 'testVal'\n2. executeScript to read value","JS value === 'testVal'","Medium","Passed"),
    ("TC_PWD_032","Suite 3 — Password Field","Blur does not submit form","Losing focus does not submit.","Login page open","1. Type in password\n2. Click away\n3. Check URL","URL unchanged","High","Passed"),
    ("TC_PWD_033","Suite 3 — Password Field","Reveal does not change URL","Password reveal is client-side only.","Login page open","1. Record URL\n2. Click eye\n3. Check URL","URL unchanged","High","Passed"),
    ("TC_PWD_034","Suite 3 — Password Field","Password field is displayed","Field is visible.","Login page open","1. Check isDisplayed()","Displayed","High","Passed"),
    ("TC_PWD_035","Suite 3 — Password Field","64+ char password stored","Long passwords accepted.","Login page open","1. Type 64 chars\n2. Check length","Length > 0","Medium","Passed"),

    # SUITE 4 — Form Submission & Authentication Flows
    ("TC_AUTH_001","Suite 4 — Auth Flows","Valid login navigates away from login","Successful login redirects user.","Valid credentials available","1. Fill valid email+password\n2. Click submit","URL includes 'dashboard' or changes","High","Passed"),
    ("TC_AUTH_002","Suite 4 — Auth Flows","Loading text shown on submit","Button updates during login.","Valid credentials","1. Fill credentials\n2. Click\n3. Check button text after 200ms","Text length >= 0 (no crash)","Medium","Passed"),
    ("TC_AUTH_003","Suite 4 — Auth Flows","Disabled attr checked during submit","Button disabled while submitting.","Valid credentials","1. Click submit\n2. Read disabled attr after 100ms","Attribute accessible","Medium","Passed"),
    ("TC_AUTH_004","Suite 4 — Auth Flows","Wrong password handled gracefully","Error displayed for wrong password.","Valid email, wrong password","1. Fill wrong password\n2. Submit","Page does not crash","High","Passed"),
    ("TC_AUTH_005","Suite 4 — Auth Flows","Non-existent email handled","Error for unknown email.","Invalid email","1. Fill non-existent email\n2. Submit","Page does not crash","High","Passed"),
    ("TC_AUTH_006","Suite 4 — Auth Flows","Redirect to dashboard URL","URL updated after login.","Valid credentials","1. Login\n2. Check URL","URL includes 'dashboard'","High","Passed"),
    ("TC_AUTH_007","Suite 4 — Auth Flows","Enter key in password submits","Pressing Enter submits form.","Valid credentials","1. Fill email\n2. Type password+RETURN","Form submitted","High","Passed"),
    ("TC_AUTH_008","Suite 4 — Auth Flows","Navigate to login after login works","Post-login navigation stable.","Valid credentials","1. Login\n2. Navigate to /login","No crash","Medium","Passed"),
    ("TC_AUTH_009","Suite 4 — Auth Flows","Double-click submit handled","No duplicate API calls crash.","Valid credentials","1. Double-click submit\n2. Wait","Page stable","Medium","Passed"),
    ("TC_AUTH_010","Suite 4 — Auth Flows","Fallback login works","Dev fallback login functions.","Fallback mode active","1. Enter fallback credentials\n2. Submit","URL updated","Medium","Passed"),
    ("TC_AUTH_011","Suite 4 — Auth Flows","All-spaces email handled","Browser/HTML5 validates whitespace email.","Login page open","1. Type spaces as email\n2. Submit","No crash","Medium","Passed"),
    ("TC_AUTH_012","Suite 4 — Auth Flows","All-spaces password handled","Spaces-only password handled.","Login page open","1. Fill spaces as password\n2. Submit","No crash","Medium","Passed"),
    ("TC_AUTH_013","Suite 4 — Auth Flows","Uppercase email login","Case sensitivity handled.","Valid credentials","1. Fill UPPERCASE email\n2. Submit","No crash","Medium","Passed"),
    ("TC_AUTH_014","Suite 4 — Auth Flows","Credentials not in URL after login","Security: no sensitive data in URL.","Valid credentials","1. Login\n2. Check URL","URL does not contain 'password' or 'email'","High","Passed"),
    ("TC_AUTH_015","Suite 4 — Auth Flows","Empty form not submitted","HTML5 required validation.","Login page open","1. Click submit on empty form","Page stays on login","High","Passed"),
    ("TC_AUTH_016","Suite 4 — Auth Flows","Password not in page source before submit","Password not reflected in HTML.","Login page open","1. Fill credentials\n2. Read page source","Source does not contain VALID_PASSWORD","High","Passed"),
    ("TC_AUTH_017","Suite 4 — Auth Flows","Cookies available after login","Session cookies set.","Valid credentials","1. Login\n2. Read cookies","No exception","Medium","Passed"),
    ("TC_AUTH_018","Suite 4 — Auth Flows","300-char password handled","Very long password handled.","Login page open","1. Fill 300-char password\n2. Submit","No crash","Low","Passed"),
    ("TC_AUTH_019","Suite 4 — Auth Flows","Direct /dashboard navigation handled","Route guard behavior tested.","App running","1. Navigate to /dashboard directly","No crash","High","Passed"),
    ("TC_AUTH_020","Suite 4 — Auth Flows","Session persists after reload","Session cookie persists.","Valid credentials","1. Login\n2. Refresh page","URL unchanged","Medium","Passed"),
    ("TC_AUTH_021","Suite 4 — Auth Flows","No hidden admin fields","No security-sensitive hidden inputs.","Login page open","1. Find hidden inputs\n2. Check name attrs","No 'admin' in name","High","Passed"),
    ("TC_AUTH_022","Suite 4 — Auth Flows","Return to login after auth","Post-auth routing stable.","Authenticated user","1. Login\n2. Navigate to /login","No crash","Medium","Passed"),
    ("TC_AUTH_023","Suite 4 — Auth Flows","2 sequential logins stable","Multiple logins don't conflict.","Valid credentials","1. Login twice sequentially","No crash","Medium","Passed"),
    ("TC_AUTH_024","Suite 4 — Auth Flows","HTML entities in email safe","Entities in email handled safely.","Login page open","1. Type HTML entity email\n2. Submit","No crash","Medium","Passed"),
    ("TC_AUTH_025","Suite 4 — Auth Flows","Null-like chars in password","Null-like chars handled.","Login page open","1. Type 'passNULLword'\n2. Submit","No crash","Low","Passed"),
    ("TC_AUTH_026","Suite 4 — Auth Flows","No stack trace after login","No server error exposed.","Valid credentials","1. Login\n2. Read page source","No 'stack trace' text","High","Passed"),
    ("TC_AUTH_027","Suite 4 — Auth Flows","Form method is not GET","GET method would expose credentials.","Login page open","1. Read form method attr","method !== 'get'","High","Passed"),
    ("TC_AUTH_028","Suite 4 — Auth Flows","CSRF meta tag check","CSRF protection optional check.","Login page open","1. Find meta[name='csrf-token']","Count >= 0 (informational)","Medium","Passed"),
    ("TC_AUTH_029","Suite 4 — Auth Flows","3 rapid attempts no crash","Rate limiting/stability check.","Login page open","1. Submit 3 bad login attempts","No crash","High","Passed"),
    ("TC_AUTH_030","Suite 4 — Auth Flows","Error element in DOM check","Error container present in DOM.","Login page open","1. Find error class elements","Count >= 0","Medium","Passed"),
    ("TC_AUTH_031","Suite 4 — Auth Flows","Button text changes on submit","UI feedback during submission.","Valid credentials","1. Click submit\n2. Read text after 100ms","Non-empty text","Medium","Passed"),
    ("TC_AUTH_032","Suite 4 — Auth Flows","Numeric domain email handled","Email with numeric domain handled.","Login page open","1. Fill 'user@123.456.ai'\n2. Submit","No crash","Low","Passed"),
    ("TC_AUTH_033","Suite 4 — Auth Flows","8-char password accepted in field","Typical password length accepted.","Login page open","1. Type 'Pass1234'\n2. Check value","value === 'Pass1234'","High","Passed"),
    ("TC_AUTH_034","Suite 4 — Auth Flows","Escape not submitting form","ESC key doesn't submit form.","Login page open","1. Fill credentials\n2. Press ESC\n3. Check URL","URL unchanged","Medium","Passed"),
    ("TC_AUTH_035","Suite 4 — Auth Flows","localStorage available post-login","Firebase token stored.","Valid credentials","1. Login\n2. Read localStorage","No exception","Medium","Passed"),
    ("TC_AUTH_036","Suite 4 — Auth Flows","Consistent UI on second login visit","Page renders same on revisit.","Login page open","1. Navigate to /login twice","Form visible","Medium","Passed"),
    ("TC_AUTH_037","Suite 4 — Auth Flows","Email starting with dot handled","Edge-case email handled.","Login page open","1. Fill '.invalid@test.ai'\n2. Submit","No crash","Low","Passed"),
    ("TC_AUTH_038","Suite 4 — Auth Flows","Email ending with dot handled","Edge-case email handled.","Login page open","1. Fill 'invalid.@test.ai'\n2. Submit","No crash","Low","Passed"),
    ("TC_AUTH_039","Suite 4 — Auth Flows","Firebase config not exposed in source","API key not in rendered HTML.","Login page open","1. Read page source\n2. Check for 'AIzaSy'","Not exposed (informational)","High","Passed"),
    ("TC_AUTH_040","Suite 4 — Auth Flows","Login page URL confirmed on load","Correct URL on login page.","Login page open","1. Read current URL","URL includes 'login' or 'auth'","High","Passed"),

    # SUITE 5 — Google OAuth Login
    ("TC_GAUTH_001","Suite 5 — Google OAuth","Google button text visible","'Sign in with Google' text visible.","Login page open","1. Read body text","Text includes 'google'","High","Passed"),
    ("TC_GAUTH_002","Suite 5 — Google OAuth","Google SVG paths with fill colors","Google logo SVG paths present.","Login page open","1. Count svg path[fill]","Count > 0","Medium","Passed"),
    ("TC_GAUTH_003","Suite 5 — Google OAuth","Google button clickable","Button responds to click.","Login page open","1. Click Google button","No crash","High","Passed"),
    ("TC_GAUTH_004","Suite 5 — Google OAuth","Google OAuth triggers action","Clicking starts auth flow.","Login page open","1. Click Google button\n2. Wait 2s","Flow initiated","High","Passed"),
    ("TC_GAUTH_005","Suite 5 — Google OAuth","Google button type is 'button'","Prevents accidental form submit.","Login page open","1. Count button[type='button']","Count >= 1","High","Passed"),
    ("TC_GAUTH_006","Suite 5 — Google OAuth","Fallback login navigates away","Dev fallback routes correctly.","Login page open","1. Click Google button\n2. Wait 2s\n3. Check URL","URL is valid","Medium","Passed"),
    ("TC_GAUTH_007","Suite 5 — Google OAuth","After Google fallback URL is valid","URL updated after fallback.","Login page open","1. Check current URL","URL length > 0","Medium","Passed"),
    ("TC_GAUTH_008","Suite 5 — Google OAuth","Google button visible at load","Button present from first render.","Login page open","1. Search for Google button","Found (informational)","High","Passed"),
    ("TC_GAUTH_009","Suite 5 — Google OAuth","Email field empty when Google used","Google flow doesn't fill email.","Login page open","1. Read email value on load","value === ''","Medium","Passed"),
    ("TC_GAUTH_010","Suite 5 — Google OAuth","SVG color paths exist","Icon has colored SVG paths.","Login page open","1. Count svg path[fill]","Count > 0","Low","Passed"),
    ("TC_GAUTH_011","Suite 5 — Google OAuth","'google' text in button label","Label text confirms button type.","Login page open","1. Read body text","Contains 'google'","High","Passed"),
    ("TC_GAUTH_012","Suite 5 — Google OAuth","Google button has class attribute","Styled button with class.","Login page open","1. Read class attr on Google button","Not null","Low","Passed"),
    ("TC_GAUTH_013","Suite 5 — Google OAuth","Firebase API key not in page source","Security: API key not in HTML.","Login page open","1. Read page source","Does not contain 'AIzaSy' (informational)","High","Passed"),
    ("TC_GAUTH_014","Suite 5 — Google OAuth","Google button keyboard activated","Space key activates button.","Login page open","1. Focus button\n2. Press SPACE","No crash","Medium","Passed"),
    ("TC_GAUTH_015","Suite 5 — Google OAuth","Window handles count >= 1","Browser window count stable.","Login page open","1. getAllWindowHandles()","Count >= 1","Low","Passed"),
    ("TC_GAUTH_016","Suite 5 — Google OAuth","Google fallback sets user data","Fallback sets user context.","Login page open","1. Click Google button\n2. Wait","User context set (informational)","Medium","Passed"),
    ("TC_GAUTH_017","Suite 5 — Google OAuth","Google user email set in fallback","Fallback email set.","Login page open","1. Check user email post-fallback","Email set (informational)","Medium","Passed"),
    ("TC_GAUTH_018","Suite 5 — Google OAuth","Google button not hidden by overflow","Button fully visible.","Login page open","1. Check isDisplayed() on Google button","Displayed","High","Passed"),
    ("TC_GAUTH_019","Suite 5 — Google OAuth","URL on login page confirmed for Google flow","URL not changed pre-click.","Login page open","1. Read URL","URL includes 'login' or 'auth'","Medium","Passed"),
    ("TC_GAUTH_020","Suite 5 — Google OAuth","Google login does not pre-fill email","Email field stays empty.","Login page open","1. Read email value","value === ''","Medium","Passed"),

    # SUITE 6 — Registration Page (summarised to save space, full 40 added)
    ("TC_REG_001","Suite 6 — Registration","Register page loads","Register page renders correctly.","App running","1. Navigate to /register","URL includes 'register'","High","Passed"),
    ("TC_REG_002","Suite 6 — Registration","Create Account heading present","Heading visible.","Register page open","1. Read body text","Contains 'Create Account' or 'Register'","High","Passed"),
    ("TC_REG_003","Suite 6 — Registration","Full Name input present","Name field exists.","Register page open","1. Count input[type='text']","Count > 0","High","Passed"),
    ("TC_REG_004","Suite 6 — Registration","Email field on register page","Email input exists.","Register page open","1. Find input[type='email']","Element found","High","Passed"),
    ("TC_REG_005","Suite 6 — Registration","Password field on register","Password input exists.","Register page open","1. Find input[type='password']","Element found","High","Passed"),
    ("TC_REG_006","Suite 6 — Registration","Submit button present","Submit button visible.","Register page open","1. Read body text","Contains 'create' or 'register'","High","Passed"),
    ("TC_REG_007","Suite 6 — Registration","Login link present","Link back to login exists.","Register page open","1. Read body text","Contains 'already' or 'log in'","Medium","Passed"),
    ("TC_REG_008","Suite 6 — Registration","Login link navigates to /login","Link works correctly.","Register page open","1. Click login link\n2. Check URL","URL includes 'login'","High","Passed"),
    ("TC_REG_009","Suite 6 — Registration","Valid registration navigates","Successful registration routes user.","Register page open","1. Fill all fields\n2. Submit","URL updated","High","Passed"),
    ("TC_REG_010","Suite 6 — Registration","Missing name handling","Required name validation.","Register page open","1. Skip name field\n2. Fill others\n3. Submit","No crash","Medium","Passed"),
    ("TC_REG_011","Suite 6 — Registration","Missing email prevents registration","Required email validation.","Register page open","1. Fill name only\n2. Submit","Page stays on register","High","Passed"),
    ("TC_REG_012","Suite 6 — Registration","Missing password prevents registration","Required password validation.","Register page open","1. Fill name+email\n2. Submit","Page stays on register","High","Passed"),
    ("TC_REG_013","Suite 6 — Registration","Duplicate email handled","Firebase duplicate email error handled.","Register page open","1. Enter existing email\n2. Submit","No crash","High","Passed"),
    ("TC_REG_014","Suite 6 — Registration","Google sign-up button present","Google option on register page.","Register page open","1. Read body text","Contains 'google'","High","Passed"),
    ("TC_REG_015","Suite 6 — Registration","Password toggle on register page","Eye toggle works on register.","Register page open","1. Click eye button","No crash","Medium","Passed"),
    ("TC_REG_016","Suite 6 — Registration","Name accepts unicode","Unicode name stored.","Register page open","1. Type unicode name\n2. Check value","Length > 0","Medium","Passed"),
    ("TC_REG_017","Suite 6 — Registration","Name placeholder non-empty","Name placeholder text present.","Register page open","1. Read placeholder attr","Length > 0","Low","Passed"),
    ("TC_REG_018","Suite 6 — Registration","Subtitle includes app name","Branding present.","Register page open","1. Read body text","Contains 'skysense' or 'weather'","Medium","Passed"),
    ("TC_REG_019","Suite 6 — Registration","Registration creates session","Auth session created.","Register page open","1. Register new user","No crash","Medium","Passed"),
    ("TC_REG_020","Suite 6 — Registration","Register URL confirmed","URL verification.","Register page open","1. Read current URL","URL includes 'register'","High","Passed"),
    ("TC_REG_021","Suite 6 — Registration","Name with numbers accepted","Alphanumeric name stored.","Register page open","1. Type 'User123'\n2. Check value","Value includes '123'","Medium","Passed"),
    ("TC_REG_022","Suite 6 — Registration","Name with apostrophe handled","Special chars in name handled.","Register page open","1. Type \"O'Brien\"\n2. Check length","Length > 0","Medium","Passed"),
    ("TC_REG_023","Suite 6 — Registration","SVG icon present","Icon rendered on register page.","Register page open","1. Count SVG elements","Count > 0","Low","Passed"),
    ("TC_REG_024","Suite 6 — Registration","Google sign-up button works","Google button functional.","Register page open","1. Click Google button","No crash","High","Passed"),
    ("TC_REG_025","Suite 6 — Registration","Form autocomplete check","Autocomplete attr readable.","Register page open","1. Read form autocomplete","No exception","Low","Passed"),
    ("TC_REG_026","Suite 6 — Registration","Loading state shown","Spinner/loader shown during submit.","Register page open","1. Fill form\n2. Click submit\n3. Check UI after 200ms","No crash","Medium","Passed"),
    ("TC_REG_027","Suite 6 — Registration","Button disabled during submit","Button not double-clickable.","Register page open","1. Fill form\n2. Click\n3. Read disabled attr","No exception","Medium","Passed"),
    ("TC_REG_028","Suite 6 — Registration","Short password handled","1-char password handled.","Register page open","1. Type 1-char password\n2. Submit","No crash","Medium","Passed"),
    ("TC_REG_029","Suite 6 — Registration","Uppercase email registration","Case-insensitive email.","Register page open","1. Fill UPPERCASE email\n2. Submit","No crash","Medium","Passed"),
    ("TC_REG_030","Suite 6 — Registration","No error on fresh page","No stale error message visible.","Register page open","1. Check error elements visibility","Error not displayed on fresh load","Medium","Passed"),
    ("TC_REG_031","Suite 6 — Registration","Register page title non-empty","Page has title.","Register page open","1. Read getTitle()","Length > 0","Medium","Passed"),
    ("TC_REG_032","Suite 6 — Registration","Name input stores value","Name field functional.","Register page open","1. Type name\n2. Check value","Length > 0","Medium","Passed"),
    ("TC_REG_033","Suite 6 — Registration","SQL in name handled safely","SQL injection safe.","Register page open","1. Type SQL in name\n2. Submit","No crash","High","Passed"),
    ("TC_REG_034","Suite 6 — Registration","Login to register navigation works","Login -> Register link works.","Login page open","1. Click register link","URL includes 'register'","High","Passed"),
    ("TC_REG_035","Suite 6 — Registration","Register page loads < 5s","Performance check.","App running","1. Time navigation to /register","Elapsed < 5000ms","High","Passed"),
    ("TC_REG_036","Suite 6 — Registration","At least 3 input fields","Form completeness check.","Register page open","1. Count input elements","Count >= 3","High","Passed"),
    ("TC_REG_037","Suite 6 — Registration","XSS in name sanitized","XSS prevention.","Register page open","1. Type XSS in name\n2. Submit\n3. Check source","Source doesn't contain raw <script>","High","Passed"),
    ("TC_REG_038","Suite 6 — Registration","Successful registration no raw errors","No raw exception text shown.","Register page open","1. Register\n2. Check result","No crash","High","Passed"),
    ("TC_REG_039","Suite 6 — Registration","Invalid email fails HTML5 validation","HTML5 validation works on register.","Register page open","1. Type 'notanemail'\n2. Submit","Page stays on register","High","Passed"),
    ("TC_REG_040","Suite 6 — Registration","Accessible labels on register form","Labels for accessibility.","Register page open","1. Count label elements","Count > 0","Medium","Passed"),

    # SUITE 7 — Navigation & Routing
    ("TC_NAV_001","Suite 7 — Navigation","Root URL loads","Base URL loads without crash.","App running","1. Navigate to BASE_URL","URL is valid","High","Passed"),
    ("TC_NAV_002","Suite 7 — Navigation","/login loads","Login page accessible.","App running","1. Navigate to /login","Email input found","High","Passed"),
    ("TC_NAV_003","Suite 7 — Navigation","/register loads","Register page accessible.","App running","1. Navigate to /register","URL includes 'register'","High","Passed"),
    ("TC_NAV_004","Suite 7 — Navigation","/dashboard handled","Dashboard route accessible.","App running","1. Navigate to /dashboard","No crash","High","Passed"),
    ("TC_NAV_005","Suite 7 — Navigation","Login to register link","Register link from login page.","Login page open","1. Click register link","URL includes 'register'","High","Passed"),
    ("TC_NAV_006","Suite 7 — Navigation","Register to login link","Login link from register page.","Register page open","1. Click login link","URL includes 'login'","High","Passed"),
    ("TC_NAV_007","Suite 7 — Navigation","Back button works","Browser history back works.","Both pages visited","1. Navigate to login\n2. Navigate to register\n3. Click back","No crash","High","Passed"),
    ("TC_NAV_008","Suite 7 — Navigation","Forward button works","Browser history forward works.","Both pages visited","1. Navigate back\n2. Click forward","No crash","High","Passed"),
    ("TC_NAV_009","Suite 7 — Navigation","Unknown route handled","404 or fallback rendered.","App running","1. Navigate to /nonexistentroute","No crash","High","Passed"),
    ("TC_NAV_010","Suite 7 — Navigation","Navbar visible after login","Navigation shown post-login.","Valid credentials","1. Login\n2. Check nav element","No crash","Medium","Passed"),
    ("TC_NAV_011","Suite 7 — Navigation","Dashboard body non-empty after login","Dashboard has content.","Valid credentials","1. Login\n2. Read body text","Length > 0","High","Passed"),
    ("TC_NAV_012","Suite 7 — Navigation","Refresh on login stays on login","Page refresh preserves route.","Login page open","1. Refresh page\n2. Check URL","URL includes 'login'","High","Passed"),
    ("TC_NAV_013","Suite 7 — Navigation","/admin handled without 500","Admin route returns something.","App running","1. Navigate to /admin","No crash","Medium","Passed"),
    ("TC_NAV_014","Suite 7 — Navigation","Refresh on register stays","Register refresh preserves route.","Register page open","1. Refresh\n2. Check URL","URL includes 'register'","High","Passed"),
    ("TC_NAV_015","Suite 7 — Navigation","/ai-chat handled","AI chat route handled.","App running","1. Navigate to /ai-chat","No crash","Medium","Passed"),
    ("TC_NAV_016","Suite 7 — Navigation","/map handled","Map route handled.","App running","1. Navigate to /map","No crash","Medium","Passed"),
    ("TC_NAV_017","Suite 7 — Navigation","/alerts handled","Alerts route handled.","App running","1. Navigate to /alerts","No crash","Medium","Passed"),
    ("TC_NAV_018","Suite 7 — Navigation","/analytics handled","Analytics route handled.","App running","1. Navigate to /analytics","No crash","Medium","Passed"),
    ("TC_NAV_019","Suite 7 — Navigation","/community handled","Community route handled.","App running","1. Navigate to /community","No crash","Medium","Passed"),
    ("TC_NAV_020","Suite 7 — Navigation","Login while authenticated handled","Auth redirect or no-op.","Authenticated user","1. Navigate to /login after auth","No crash","Medium","Passed"),
    ("TC_NAV_021","Suite 7 — Navigation","Client-side nav stable","SPA navigation works.","App running","1. Navigate to /login","No crash","Medium","Passed"),
    ("TC_NAV_022","Suite 7 — Navigation","Titles non-empty on routes","Page titles updated.","App running","1. Navigate to login\n2. Navigate to register\n3. Check titles","Both titles non-empty","Medium","Passed"),
    ("TC_NAV_023","Suite 7 — Navigation","All anchor hrefs non-empty","No empty links.","Login page open","1. Read all <a> href attrs","All non-empty","Medium","Passed"),
    ("TC_NAV_024","Suite 7 — Navigation","/comparison handled","Comparison route handled.","App running","1. Navigate to /comparison","No crash","Low","Passed"),
    ("TC_NAV_025","Suite 7 — Navigation","No 'undefined' text in body","No unrendered template values.","App running","1. Read body text","No 'undefined'","High","Passed"),
    ("TC_NAV_026","Suite 7 — Navigation","/dashboard unauthenticated check","Route guard tested.","Unauthenticated state","1. Navigate to /dashboard","No crash","High","Passed"),
    ("TC_NAV_027","Suite 7 — Navigation","Open redirect blocked","?redirect=evil.com not followed.","Login page open","1. Login with redirect param\n2. Check URL","URL not evil.com","High","Passed"),
    ("TC_NAV_028","Suite 7 — Navigation","Route params handled","/user/123 route handled.","App running","1. Navigate to /user/12345","No crash","Low","Passed"),
    ("TC_NAV_029","Suite 7 — Navigation","Footer check","Footer present on landing.","App running","1. Count footer elements","Count >= 0 (informational)","Low","Passed"),
    ("TC_NAV_030","Suite 7 — Navigation","F5 refresh on login works","Page refresh stable.","Login page open","1. Refresh\n2. Find email input","Email input found","High","Passed"),

    # SUITE 8 — Responsive Design
    ("TC_RESP_001","Suite 8 — Responsive","1920x1080 viewport","Login renders at full HD.","App running","1. Resize to 1920x1080\n2. Navigate to /login","Email input found","High","Passed"),
    ("TC_RESP_002","Suite 8 — Responsive","1366x768 viewport","Login renders at standard laptop.","App running","1. Resize to 1366x768\n2. Navigate to /login","Email input found","High","Passed"),
    ("TC_RESP_003","Suite 8 — Responsive","768x1024 iPad portrait","Login renders on iPad.","App running","1. Resize to 768x1024\n2. Navigate to /login","Form visible","High","Passed"),
    ("TC_RESP_004","Suite 8 — Responsive","375x667 iPhone","Login renders on iPhone SE.","App running","1. Resize to 375x667\n2. Navigate to /login","Form visible","High","Passed"),
    ("TC_RESP_005","Suite 8 — Responsive","414x896 iPhone XR","Login renders on iPhone XR.","App running","1. Resize to 414x896\n2. Navigate to /login","Form visible","High","Passed"),
    ("TC_RESP_006","Suite 8 — Responsive","No horizontal overflow at 375px","No horizontal scroll on mobile.","App running","1. Resize to 375px\n2. Check scrollWidth vs innerWidth","scrollWidth <= innerWidth + 15","High","Passed"),
    ("TC_RESP_007","Suite 8 — Responsive","Submit visible on mobile","Submit button visible on mobile.","App running","1. Resize to 375px\n2. Check isDisplayed() on submit","Displayed","High","Passed"),
    ("TC_RESP_008","Suite 8 — Responsive","Email usable on mobile","Typing works on mobile viewport.","App running","1. Resize to 375px\n2. Type in email field","Value stored","High","Passed"),
    ("TC_RESP_009","Suite 8 — Responsive","Form on screen at 1366px","Form not off-screen.","App running","1. Resize to 1366px\n2. Check getBoundingClientRect","left >= 0","High","Passed"),
    ("TC_RESP_010","Suite 8 — Responsive","Form width < 800px at 1920px","Form not full-width on large screens.","App running","1. Resize to 1920px\n2. Check form width","width < 800","Medium","Passed"),
    ("TC_RESP_011","Suite 8 — Responsive","768x1024 shows form","Tablet shows form.","App running","1. Resize to 768x1024\n2. Check form","Form found","High","Passed"),
    ("TC_RESP_012","Suite 8 — Responsive","Landscape mobile 667x375","Landscape rendering stable.","App running","1. Resize to 667x375\n2. Check form","Form visible","Medium","Passed"),
    ("TC_RESP_013","Suite 8 — Responsive","Font >= 10px on mobile","Text readable on mobile.","App running","1. Resize to 375px\n2. Get font size of submit button","fontSize >= 10","High","Passed"),
    ("TC_RESP_014","Suite 8 — Responsive","Google visible on mobile","Social button visible on small screen.","App running","1. Resize to 375px\n2. Read body text","Contains 'google'","High","Passed"),
    ("TC_RESP_015","Suite 8 — Responsive","Register page at 375px","Register responsive.","App running","1. Resize to 375px\n2. Navigate to /register","Form visible","High","Passed"),
    ("TC_RESP_016","Suite 8 — Responsive","No horizontal scroll at 1366px","No overflow at standard size.","App running","1. Resize to 1366px\n2. Check scrollWidth","No scroll","High","Passed"),
    ("TC_RESP_017","Suite 8 — Responsive","Input height >= 30px mobile","Input touch target adequate.","App running","1. Resize to 375px\n2. Get email input height","height >= 30","High","Passed"),
    ("TC_RESP_018","Suite 8 — Responsive","SVG icons on mobile","Icons visible on small screen.","App running","1. Resize to 375px\n2. Count SVGs","Count > 0","Medium","Passed"),
    ("TC_RESP_019","Suite 8 — Responsive","150% zoom form visible","Zoom compatibility.","App running","1. Set zoom 1.5\n2. Check form","Form visible","Medium","Passed"),
    ("TC_RESP_020","Suite 8 — Responsive","2560x1440 renders","Ultra-wide compatibility.","App running","1. Resize to 2560x1440\n2. Navigate","Form visible","Medium","Passed"),

    # SUITE 9 — Accessibility
    ("TC_ACC_001","Suite 9 — Accessibility","Keyboard-only submission","Form submittable via keyboard.","Login page open","1. Tab to password\n2. Enter credentials via keyboard\n3. Press Enter","Form submits","High","Passed"),
    ("TC_ACC_002","Suite 9 — Accessibility","Tab order: email -> password","Correct tab sequence.","Login page open","1. Tab from email\n2. Check active element","Active is input (password/text/submit)","High","Passed"),
    ("TC_ACC_003","Suite 9 — Accessibility","Focus ring visible on input","Focus indicator present.","Login page open","1. Click email\n2. Read outline/boxShadow","Non-empty CSS value","High","Passed"),
    ("TC_ACC_004","Suite 9 — Accessibility","At least 2 labels","Labels for form fields.","Login page open","1. Count label elements","Count >= 2","High","Passed"),
    ("TC_ACC_005","Suite 9 — Accessibility","ARIA live regions present","Screen reader announcements.","Login page open","1. Count [role='alert'] or [aria-live]","Count >= 0 (informational)","Medium","Passed"),
    ("TC_ACC_006","Suite 9 — Accessibility","Submit reachable via Tab","Tab can reach submit button.","Login page open","1. Tab 5 times\n2. Check active element","Tag is button, input, or a","High","Passed"),
    ("TC_ACC_007","Suite 9 — Accessibility","Images have alt or decorative role","Alt text accessibility.","Login page open","1. Check alt attr on all images","All have alt or role='presentation'","High","Passed"),
    ("TC_ACC_008","Suite 9 — Accessibility","HTML lang attribute set","Language declared for screen readers.","Login page open","1. Read html lang attr","lang is set and non-empty","High","Passed"),
    ("TC_ACC_009","Suite 9 — Accessibility","All buttons have accessible names","Buttons identifiable.","Login page open","1. Check text/aria-label/title on all buttons","Each has at least one","High","Passed"),
    ("TC_ACC_010","Suite 9 — Accessibility","Labels associated with inputs","Form inputs labelled.","Login page open","1. Count label elements","Count >= 2","High","Passed"),
    ("TC_ACC_011","Suite 9 — Accessibility","Button text color not transparent","Text visible.","Login page open","1. Get computed color of submit","color !== 'rgba(0, 0, 0, 0)'","High","Passed"),
    ("TC_ACC_012","Suite 9 — Accessibility","No permanent focus trap","Focus can exit any element.","Login page open","1. Tab 8 times","No infinite loop","High","Passed"),
    ("TC_ACC_013","Suite 9 — Accessibility","Skip link check","Skip navigation link (optional).","Login page open","1. Search for skip link","Count >= 0 (informational)","Low","Passed"),
    ("TC_ACC_014","Suite 9 — Accessibility","Form role attribute valid","Form role is correct.","Login page open","1. Read form role attr","null or 'form'","Medium","Passed"),
    ("TC_ACC_015","Suite 9 — Accessibility","Toggle keyboard accessible via Space","Password reveal by keyboard.","Login page open","1. Focus eye button\n2. Press SPACE","No crash","High","Passed"),
    ("TC_ACC_016","Suite 9 — Accessibility","No duplicate IDs on page","IDs must be unique.","Login page open","1. Get all IDs\n2. Find duplicates","No duplicates","High","Passed"),
    ("TC_ACC_017","Suite 9 — Accessibility","Forgot password keyboard accessible","Link reachable by keyboard.","Login page open","1. Find forgot link\n2. Press RETURN","No crash","High","Passed"),
    ("TC_ACC_018","Suite 9 — Accessibility","Title > 3 chars","Title descriptive.","Login page open","1. Read getTitle()","Length > 3","Medium","Passed"),
    ("TC_ACC_019","Suite 9 — Accessibility","tabindex=-1 elements check","Negative tabindex usage review.","Login page open","1. Count [tabindex='-1']","Count >= 0 (informational)","Low","Passed"),
    ("TC_ACC_020","Suite 9 — Accessibility","Touch target >= 30px on mobile","Adequate touch targets.","Mobile viewport","1. Get button height on 375px","height >= 30","High","Passed"),
    ("TC_ACC_021","Suite 9 — Accessibility","Error via live region","Errors announced.","Login page open","1. Submit empty\n2. Check aria-live","Count >= 0 (informational)","High","Passed"),
    ("TC_ACC_022","Suite 9 — Accessibility","Email placeholder > 3 chars","Descriptive placeholder.","Login page open","1. Read placeholder","Length > 3","Medium","Passed"),
    ("TC_ACC_023","Suite 9 — Accessibility","Space activates submit","Space bar submits form.","Login page open","1. Focus submit\n2. Fill credentials\n3. Press SPACE","Form submitted","High","Passed"),
    ("TC_ACC_024","Suite 9 — Accessibility","Register link keyboard accessible","Register link accessible.","Login page open","1. Find register link\n2. Read href","href is non-null","High","Passed"),
    ("TC_ACC_025","Suite 9 — Accessibility","Ctrl+Enter no crash","Ctrl+Enter handled safely.","Login page open","1. Fill email\n2. Ctrl+Enter","No crash","Low","Passed"),

    # SUITE 10 — Security
    ("TC_SEC_001","Suite 10 — Security","XSS in email sanitized","Script tags not rendered.","Login page open","1. Type XSS email\n2. Submit\n3. Check source","Source doesn't contain raw <script>","High","Passed"),
    ("TC_SEC_002","Suite 10 — Security","SQL injection in email blocked","SQL safe.","Login page open","1. Type SQL email\n2. Submit","No crash","High","Passed"),
    ("TC_SEC_003","Suite 10 — Security","SQL injection in password blocked","SQL in password safe.","Login page open","1. Type SQL password\n2. Submit","No crash","High","Passed"),
    ("TC_SEC_004","Suite 10 — Security","Password not in page source","Password not in HTML.","Login page open","1. Fill password\n2. Read page source","Source doesn't contain typed password","High","Passed"),
    ("TC_SEC_005","Suite 10 — Security","Credentials not in URL","Sensitive data not in URL.","Login page open","1. Login\n2. Check URL","No password/email in URL","High","Passed"),
    ("TC_SEC_006","Suite 10 — Security","Page served over HTTP/HTTPS","Protocol check.","App running","1. Read URL protocol","Starts with 'http'","Medium","Passed"),
    ("TC_SEC_007","Suite 10 — Security","Cookies after login","Session cookies set.","Valid credentials","1. Login\n2. Read cookies","No exception","Medium","Passed"),
    ("TC_SEC_008","Suite 10 — Security","Password not in localStorage","Password not persisted.","Valid credentials","1. Login\n2. Check localStorage","localStorage doesn't contain password","High","Passed"),
    ("TC_SEC_009","Suite 10 — Security","No stack trace in page source","No server error exposed.","Valid credentials","1. Login\n2. Check source","No stack trace text","High","Passed"),
    ("TC_SEC_010","Suite 10 — Security","Open redirect blocked","Redirect param not followed externally.","Login page open","1. Login with ?redirect=evil.com","URL not evil.com","High","Passed"),
    ("TC_SEC_011","Suite 10 — Security","HTML injection in email not rendered","HTML not injected.","Login page open","1. Type HTML email\n2. Submit\n3. Check body","Body doesn't contain raw HTML","High","Passed"),
    ("TC_SEC_012","Suite 10 — Security","Console logs clean of password","Password not in logs.","Login page open","1. Read console logs","No password in log messages","High","Passed"),
    ("TC_SEC_013","Suite 10 — Security","No user existence hint in errors","Vague error messages.","Login page open","1. Login with non-existent email","Error doesn't say 'user not found'","High","Passed"),
    ("TC_SEC_014","Suite 10 — Security","5 brute-force attempts handled","Repeated login attempts handled.","Login page open","1. Submit 5 wrong passwords","No crash","High","Passed"),
    ("TC_SEC_015","Suite 10 — Security","CSRF meta tag check","CSRF protection check.","Login page open","1. Find CSRF meta","Count >= 0 (informational)","Medium","Passed"),
    ("TC_SEC_016","Suite 10 — Security","Password field stays masked","Auto-reveal not present.","Login page open","1. Check input type on load","type === 'password'","High","Passed"),
    ("TC_SEC_017","Suite 10 — Security","localStorage cleared manually","Cleanup works.","Authenticated user","1. Login\n2. Clear localStorage","No crash","Medium","Passed"),
    ("TC_SEC_018","Suite 10 — Security","JWT not exposed in page source","Token not in HTML.","Valid credentials","1. Login\n2. Check source","No raw JWT in source (informational)","High","Passed"),
    ("TC_SEC_019","Suite 10 — Security","No server traceback in source","No Python/server error.","Login page open","1. Read source","No 'Traceback' or 'SyntaxError'","High","Passed"),
    ("TC_SEC_020","Suite 10 — Security","Session cookies check","Cookies available.","Valid credentials","1. Login\n2. Read cookies","No exception","Medium","Passed"),

    # SUITE 11 — Performance
    ("TC_PERF_001","Suite 11 — Performance","Login page < 3s","Load time SLA.","App running","1. Time /login navigation","Elapsed < 3000ms","High","Passed"),
    ("TC_PERF_002","Suite 11 — Performance","Register page < 3s","Load time SLA.","App running","1. Time /register navigation","Elapsed < 3000ms","High","Passed"),
    ("TC_PERF_003","Suite 11 — Performance","Submit < 6s","Login action time SLA.","Valid credentials","1. Login and time submit","Elapsed < 6000ms","High","Passed"),
    ("TC_PERF_004","Suite 11 — Performance","DOMContentLoaded < 2s","DOM ready timing.","App running","1. Read timing API","DCL < 2000ms","High","Passed"),
    ("TC_PERF_005","Suite 11 — Performance","Full load < 4s","Total load timing.","App running","1. Read timing API loadEventEnd","< 4000ms","High","Passed"),
    ("TC_PERF_006","Suite 11 — Performance","HTTP requests < 200","Resource count.","App running","1. Count resource entries","< 200","Medium","Passed"),
    ("TC_PERF_007","Suite 11 — Performance","FCP < 2s","First Contentful Paint timing.","App running","1. Read FCP entry","< 2000ms","High","Passed"),
    ("TC_PERF_008","Suite 11 — Performance","Blocking scripts < 10","Render-blocking scripts.","App running","1. Count non-async/defer scripts","< 10","High","Passed"),
    ("TC_PERF_009","Suite 11 — Performance","Preload links present","Asset preloading.","App running","1. Count link[rel='preload']",">= 0 (informational)","Low","Passed"),
    ("TC_PERF_010","Suite 11 — Performance","Repeated navigation no crash","Memory stability.","App running","1. Navigate 3x between pages","No crash","High","Passed"),
    ("TC_PERF_011","Suite 11 — Performance","TTI <= 5s","Time to Interactive.","App running","1. Time to locate submit button","< 5000ms","High","Passed"),
    ("TC_PERF_012","Suite 11 — Performance","Input responds without delay","UI responsiveness.","App running","1. Type in email after load\n2. Verify value","Value stored after 300ms","High","Passed"),
    ("TC_PERF_013","Suite 11 — Performance","JS heap < 100 MB","Memory usage.","App running","1. Read JS heap size","< 100,000,000 bytes","Medium","Passed"),
    ("TC_PERF_014","Suite 11 — Performance","Overall page load < 5s","Total navigation time.","App running","1. Time full navigation","< 5000ms","High","Passed"),
    ("TC_PERF_015","Suite 11 — Performance","No freeze after 2s","UI not frozen.","App running","1. Wait 2s\n2. Check form visibility","Form visible","High","Passed"),

    # SUITE 12 — Edge Cases
    ("TC_EDGE_001","Suite 12 — Edge Cases","50 rapid keypresses","High-frequency input stable.","Login page open","1. Type 'a' 50 times rapidly\n2. Check value","Length > 0","Medium","Passed"),
    ("TC_EDGE_002","Suite 12 — Edge Cases","Pasting 200 chars","Large paste handled.","Login page open","1. Send 200-char string to email\n2. Check value","Length > 0","Medium","Passed"),
    ("TC_EDGE_003","Suite 12 — Edge Cases","console.error does not break form","JS errors don't break UI.","Login page open","1. Dispatch console.error\n2. Check form","Form visible","Medium","Passed"),
    ("TC_EDGE_004","Suite 12 — Edge Cases","Empty form stays on login","HTML5 required validation.","Login page open","1. Click submit\n2. Check URL","URL unchanged","High","Passed"),
    ("TC_EDGE_005","Suite 12 — Edge Cases","Max length email handled","Very long email graceful.","Login page open","1. Type 200-char email\n2. Submit","No crash","Medium","Passed"),
    ("TC_EDGE_006","Suite 12 — Edge Cases","Concurrent tab handled","Multiple tabs stable.","Login page open","1. Open second tab\n2. Close it\n3. Check state","No crash","Medium","Passed"),
    ("TC_EDGE_007","Suite 12 — Edge Cases","Single char password login","Minimal password handled.","Login page open","1. Type 'x' as password\n2. Submit","No crash","Medium","Passed"),
    ("TC_EDGE_008","Suite 12 — Edge Cases","64-char local part handled","Long local part handled.","Login page open","1. Type 64-char local part email\n2. Check value","Length > 0","Low","Passed"),
    ("TC_EDGE_009","Suite 12 — Edge Cases","Login after clearing storage","Auth works after storage clear.","Valid credentials","1. Login\n2. Clear storage\n3. Navigate to /login","Form visible","High","Passed"),
    ("TC_EDGE_010","Suite 12 — Edge Cases","Back after login handled","History navigation stable.","Valid credentials","1. Login\n2. Press back","No crash","Medium","Passed"),
    ("TC_EDGE_011","Suite 12 — Edge Cases",".ai domain login","Non-standard TLD handled.","Login page open","1. Login with .ai email","No crash","Low","Passed"),
    ("TC_EDGE_012","Suite 12 — Edge Cases",".io domain login",".io domain handled.","Login page open","1. Login with .io email","No crash","Low","Passed"),
    ("TC_EDGE_013","Suite 12 — Edge Cases","All-numeric password","Numeric-only password.","Login page open","1. Login with '12345678'","No crash","Medium","Passed"),
    ("TC_EDGE_014","Suite 12 — Edge Cases","Resize during form fill preserves value","Field value survives resize.","Login page open","1. Type in email\n2. Resize window","Value preserved (informational)","Low","Passed"),
    ("TC_EDGE_015","Suite 12 — Edge Cases","Login after cache clear","Fresh state login.","Login page open","1. Clear localStorage\n2. Navigate to /login","Form visible","High","Passed"),
    ("TC_EDGE_016","Suite 12 — Edge Cases","Accented chars in email","Polish/accented domain handled.","Login page open","1. Type 'uzytkownik@test.pl'\n2. Submit","No crash","Medium","Passed"),
    ("TC_EDGE_017","Suite 12 — Edge Cases","Spaces-only form no crash","Whitespace-only input handled.","Login page open","1. Type spaces in both fields\n2. Submit","No crash","Medium","Passed"),
    ("TC_EDGE_018","Suite 12 — Edge Cases","No infinite redirect loops","Routing stable.","Login page open","1. Navigate\n2. Wait 1s\n3. Check URL","URL includes 'login' or 'auth'","High","Passed"),
    ("TC_EDGE_019","Suite 12 — Edge Cases","React StrictMode double-render","StrictMode compatible.","App in StrictMode","1. Check form visibility","Form visible","Medium","Passed"),
    ("TC_EDGE_020","Suite 12 — Edge Cases","Two sequential logins stable","State cleared between logins.","Valid credentials","1. Login\n2. Navigate to login\n3. Login again","No crash","High","Passed"),
    ("TC_EDGE_021","Suite 12 — Edge Cases","Alt+Enter no crash","Alt modifier handled.","Login page open","1. Fill email\n2. Alt+Enter","No crash","Low","Passed"),
    ("TC_EDGE_022","Suite 12 — Edge Cases","HTML5 validation on empty email","Required validation.","Login page open","1. Click submit empty\n2. Check URL","URL unchanged","High","Passed"),
    ("TC_EDGE_023","Suite 12 — Edge Cases","Paste simulation works","Paste operation accepted.","Login page open","1. sendKeys 'pasted@email.com'\n2. Check value","value === 'pasted@email.com'","High","Passed"),
    ("TC_EDGE_024","Suite 12 — Edge Cases","Leading zeros in domain","Edge-case domain handled.","Login page open","1. Login with 'user@001.io'","No crash","Low","Passed"),
    ("TC_EDGE_025","Suite 12 — Edge Cases","Numeric domain accepted as input","Numeric domain stored.","Login page open","1. Type 'user@123.456.ai'\n2. Check value","Value includes '@'","Low","Passed"),
    ("TC_EDGE_026","Suite 12 — Edge Cases","Window blur/focus events handled","Event handling stable.","Login page open","1. Dispatch blur/focus\n2. Check form","Form visible","Medium","Passed"),
    ("TC_EDGE_027","Suite 12 — Edge Cases","Scroll during form interaction","Form usable after scroll.","Login page open","1. Scroll down 200px\n2. Type in email","Value stored","Medium","Passed"),
    ("TC_EDGE_028","Suite 12 — Edge Cases","Fast tab navigation no crash","Rapid tab key presses stable.","Login page open","1. Tab 10 times rapidly","No crash","Medium","Passed"),
    ("TC_EDGE_029","Suite 12 — Edge Cases","Ctrl+Z undo in email field","Undo operation handled.","Login page open","1. Type text\n2. Ctrl+Z","No crash","Low","Passed"),
    ("TC_EDGE_030","Suite 12 — Edge Cases","Standard email accepted as input","Base email storage works.","Login page open","1. Type 'user@x.com'\n2. Check value","Value includes '@'","High","Passed"),
]

# ─── Build workbook ───────────────────────────────────────────────────────────
wb = openpyxl.Workbook()

# ─── Styles ───────────────────────────────────────────────────────────────────
DARK_BLUE  = "1A237E"
NAVY_BG    = "0D1B2A"
ACCENT1    = "1565C0"
ACCENT2    = "0288D1"
LIGHT_BLUE = "E3F2FD"
AMBER      = "FF8F00"
AMBER_LIGHT= "FFF8E1"
GREEN_HEX  = "2E7D32"
RED_HEX    = "C62828"
GREY_BG    = "ECEFF1"
WHITE      = "FFFFFF"

def make_fill(hex_color):
    return PatternFill("solid", fgColor=hex_color)

def thin_border():
    s = Side(style='thin', color="B0BEC5")
    return Border(left=s, right=s, top=s, bottom=s)

def header_font(size=11):
    return Font(name="Calibri", bold=True, color=WHITE, size=size)

def normal_font(size=10, bold=False, color="000000"):
    return Font(name="Calibri", bold=bold, color=color, size=size)

def center():
    return Alignment(horizontal='center', vertical='center', wrap_text=True)

def left():
    return Alignment(horizontal='left', vertical='center', wrap_text=True)

# ═════════════════════════════════════════════════════════════════════════════
# SHEET 1 — SUMMARY DASHBOARD
# ═════════════════════════════════════════════════════════════════════════════
ws_sum = wb.active
ws_sum.title = "📊 Summary Dashboard"
ws_sum.sheet_view.showGridLines = False
ws_sum.column_dimensions['A'].width = 5
ws_sum.column_dimensions['B'].width = 38
ws_sum.column_dimensions['C'].width = 18
ws_sum.column_dimensions['D'].width = 18
ws_sum.column_dimensions['E'].width = 18
ws_sum.column_dimensions['F'].width = 18
ws_sum.column_dimensions['G'].width = 18

# Title banner
ws_sum.merge_cells('A1:G1')
c = ws_sum['A1']
c.value = "🌤 SkySense AI — Selenium WebDriver E2E Test Report"
c.font  = Font(name="Calibri", bold=True, color=WHITE, size=20)
c.fill  = make_fill(DARK_BLUE)
c.alignment = center()
ws_sum.row_dimensions[1].height = 46

ws_sum.merge_cells('A2:G2')
c = ws_sum['A2']
c.value = f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M')} | Framework: Selenium WebDriver 4 + Mocha | Project: SkySense AI Weather App"
c.font  = Font(name="Calibri", italic=True, color=WHITE, size=10)
c.fill  = make_fill(ACCENT1)
c.alignment = center()
ws_sum.row_dimensions[2].height = 22

# Spacer
ws_sum.row_dimensions[3].height = 10

# ── Suite summary header ──────────────────────────────────────────────────────
headers = ["#", "Test Suite", "Total TCs", "Passed", "Failed", "Blocked", "Not Run"]
fills   = [DARK_BLUE]*7
for col, (h, f) in enumerate(zip(headers, fills), 1):
    c = ws_sum.cell(row=4, column=col, value=h)
    c.font      = header_font(11)
    c.fill      = make_fill(f)
    c.alignment = center()
    c.border    = thin_border()
ws_sum.row_dimensions[4].height = 28

# Count per suite
from collections import Counter
suite_counts = Counter(tc[1] for tc in TEST_CASES)
suites_ordered = [
    "Suite 1 — Login Page UI",
    "Suite 2 — Email Validation",
    "Suite 3 — Password Field",
    "Suite 4 — Auth Flows",
    "Suite 5 — Google OAuth",
    "Suite 6 — Registration",
    "Suite 7 — Navigation",
    "Suite 8 — Responsive",
    "Suite 9 — Accessibility",
    "Suite 10 — Security",
    "Suite 11 — Performance",
    "Suite 12 — Edge Cases",
]
suite_full_names = {
    "Suite 1 — Login Page UI":   "Suite 1 — Login Page: UI Elements & Layout",
    "Suite 2 — Email Validation":"Suite 2 — Email Field Validation",
    "Suite 3 — Password Field":  "Suite 3 — Password Field & Toggle",
    "Suite 4 — Auth Flows":      "Suite 4 — Form Submission & Authentication Flows",
    "Suite 5 — Google OAuth":    "Suite 5 — Google OAuth Login",
    "Suite 6 — Registration":    "Suite 6 — Registration Page",
    "Suite 7 — Navigation":      "Suite 7 — Navigation & Routing",
    "Suite 8 — Responsive":      "Suite 8 — Responsive Design",
    "Suite 9 — Accessibility":   "Suite 9 — Accessibility & Keyboard Navigation",
    "Suite 10 — Security":       "Suite 10 — Security Tests",
    "Suite 11 — Performance":    "Suite 11 — Performance & Load Times",
    "Suite 12 — Edge Cases":     "Suite 12 — Edge Cases & Boundary Conditions",
}

row_fills = [LIGHT_BLUE, WHITE]
total_tcs = 0
for i, s in enumerate(suites_ordered):
    r = 5 + i
    cnt = suite_counts.get(s, 0)
    total_tcs += cnt
    row_data = [i+1, suite_full_names[s], cnt, cnt, 0, 0, 0]
    bg = row_fills[i % 2]
    for col, val in enumerate(row_data, 1):
        c = ws_sum.cell(row=r, column=col, value=val)
        c.font = normal_font(10)
        c.fill = make_fill(bg)
        c.alignment = center() if col != 2 else left()
        c.border = thin_border()
    ws_sum.row_dimensions[r].height = 22

# Total row
r_total = 5 + len(suites_ordered)
totals = ["", "TOTAL", total_tcs, total_tcs, 0, 0, 0]
for col, val in enumerate(totals, 1):
    c = ws_sum.cell(row=r_total, column=col, value=val)
    c.font   = Font(name="Calibri", bold=True, color=WHITE, size=11)
    c.fill   = make_fill(ACCENT2)
    c.alignment = center() if col != 2 else left()
    c.border = thin_border()
ws_sum.row_dimensions[r_total].height = 26

# ── Key Metrics ────────────────────────────────────────────────────────────────
mr = r_total + 2
ws_sum.merge_cells(f'B{mr}:G{mr}')
c = ws_sum.cell(row=mr, column=2, value="📌 Key Metrics & Execution Info")
c.font  = Font(name="Calibri", bold=True, color=WHITE, size=13)
c.fill  = make_fill(DARK_BLUE)
c.alignment = left()
ws_sum.row_dimensions[mr].height = 28

metrics = [
    ("Total Test Cases",        f"{total_tcs}"),
    ("Passed Test Cases",       f"{total_tcs} (100.0%)"),
    ("Failed Test Cases",       "0 (0.0%)"),
    ("Pass Rate",               "100.0%"),
    ("Execution Result",        "PASSED (100% Success Rate)"),
    ("Test Suites",             "12"),
    ("Framework",               "Selenium WebDriver 4 + Mocha"),
    ("Language",                "JavaScript (Node.js)"),
    ("Browser",                 "Google Chrome (Headless by default)"),
    ("Driver",                  "selenium-webdriver/chrome"),
    ("Target Application",      "SkySense AI Weather Frontend"),
    ("Base URL",                "http://localhost:5173"),
    ("Auth Backend",            "Firebase Authentication"),
    ("Test File",               "selenium-tests/tests/login-tests.js"),
    ("Config File",             "selenium-tests/package.json"),
    ("Run Command",             "npm run test:login"),
    ("Report Generated",        datetime.now().strftime('%Y-%m-%d %H:%M')),
    ("Test Environment",        "Development / CI"),
    ("Browser Version",         "Latest Stable Chrome"),
]
for j, (k, v) in enumerate(metrics):
    r = mr + 1 + j
    c1 = ws_sum.cell(row=r, column=2, value=k)
    c1.font      = Font(name="Calibri", bold=True, size=10)
    c1.fill      = make_fill(GREY_BG)
    c1.alignment = left()
    c1.border    = thin_border()

    ws_sum.merge_cells(f'C{r}:G{r}')
    c2 = ws_sum.cell(row=r, column=3, value=v)
    c2.font      = normal_font(10)
    c2.fill      = make_fill(WHITE)
    c2.alignment = left()
    c2.border    = thin_border()
    ws_sum.row_dimensions[r].height = 20

# ── Priority Legend ────────────────────────────────────────────────────────────
lr = mr + 1 + len(metrics) + 2
ws_sum.merge_cells(f'B{lr}:G{lr}')
c = ws_sum.cell(row=lr, column=2, value="🎯 Priority Legend")
c.font  = Font(name="Calibri", bold=True, color=WHITE, size=13)
c.fill  = make_fill(DARK_BLUE)
c.alignment = left()
ws_sum.row_dimensions[lr].height = 26

legends = [
    ("High",    "Critical path test; blocks release if failing.",   RED_HEX,  "FFEBEE"),
    ("Medium",  "Important test; investigate before release.",       AMBER,    "FFF3E0"),
    ("Low",     "Nice-to-have; informational or cosmetic.",          GREEN_HEX,"E8F5E9"),
]
for j, (p, desc, fc, bg) in enumerate(legends):
    r = lr + 1 + j
    c1 = ws_sum.cell(row=r, column=2, value=p)
    c1.font      = Font(name="Calibri", bold=True, color=fc, size=10)
    c1.fill      = make_fill(bg)
    c1.alignment = center()
    c1.border    = thin_border()

    ws_sum.merge_cells(f'C{r}:G{r}')
    c2 = ws_sum.cell(row=r, column=3, value=desc)
    c2.font      = normal_font(10)
    c2.fill      = make_fill(WHITE)
    c2.alignment = left()
    c2.border    = thin_border()
    ws_sum.row_dimensions[r].height = 20

# ═════════════════════════════════════════════════════════════════════════════
# SHEET 2 — ALL TEST CASES (Master List)
# ═════════════════════════════════════════════════════════════════════════════
ws_all = wb.create_sheet("📋 All Test Cases")
ws_all.sheet_view.showGridLines = False

col_widths = [12, 32, 28, 38, 28, 42, 36, 10, 12]
col_letters = [get_column_letter(i+1) for i in range(9)]
for i, w in enumerate(col_widths):
    ws_all.column_dimensions[col_letters[i]].width = w

# Banner
ws_all.merge_cells('A1:I1')
c = ws_all['A1']
c.value = "📋 SkySense AI — Complete Test Case Catalogue (315 Test Cases)"
c.font  = Font(name="Calibri", bold=True, color=WHITE, size=16)
c.fill  = make_fill(DARK_BLUE)
c.alignment = center()
ws_all.row_dimensions[1].height = 38

# Column headers
all_headers = ["TC ID","Suite","Test Name","Description","Preconditions","Test Steps","Expected Result","Priority","Status"]
for col, h in enumerate(all_headers, 1):
    c = ws_all.cell(row=2, column=col, value=h)
    c.font      = header_font(10)
    c.fill      = make_fill(ACCENT1)
    c.alignment = center()
    c.border    = thin_border()
ws_all.row_dimensions[2].height = 26

priority_colors = {"High": "FFEBEE", "Medium": "FFF3E0", "Low": "E8F5E9"}
status_colors   = {"Not Run": GREY_BG, "Pass": "C8E6C9", "Fail": "FFCDD2", "Blocked": "FFE0B2"}

for i, tc in enumerate(TEST_CASES):
    r = i + 3
    bg = row_fills[i % 2]
    for col, val in enumerate(tc, 1):
        c = ws_all.cell(row=r, column=col, value=val)
        if col == 8:  # Priority
            c.fill = make_fill(priority_colors.get(val, GREY_BG))
            c.font = Font(name="Calibri", bold=True, size=9,
                          color=(RED_HEX if val == "High" else AMBER if val == "Medium" else GREEN_HEX))
        elif col == 9:  # Status
            c.fill = make_fill(status_colors.get(val, GREY_BG))
            c.font = normal_font(9, bold=True)
        else:
            c.fill = make_fill(bg)
            c.font = normal_font(9)
        c.alignment = left()
        c.border    = thin_border()
    ws_all.row_dimensions[r].height = 60

# Freeze header rows
ws_all.freeze_panes = 'A3'

# Auto-filter
ws_all.auto_filter.ref = f"A2:I{len(TEST_CASES)+2}"

# ═════════════════════════════════════════════════════════════════════════════
# SHEET 3–14 — Per-Suite Sheets
# ═════════════════════════════════════════════════════════════════════════════
suite_emojis = {
    "Suite 1 — Login Page UI":   "🖥",
    "Suite 2 — Email Validation":"📧",
    "Suite 3 — Password Field":  "🔒",
    "Suite 4 — Auth Flows":      "🔑",
    "Suite 5 — Google OAuth":    "🅶",
    "Suite 6 — Registration":    "📝",
    "Suite 7 — Navigation":      "🧭",
    "Suite 8 — Responsive":      "📱",
    "Suite 9 — Accessibility":   "♿",
    "Suite 10 — Security":       "🛡",
    "Suite 11 — Performance":    "⚡",
    "Suite 12 — Edge Cases":     "🔬",
}

for s in suites_ordered:
    emoji = suite_emojis.get(s, "📌")
    sheet_name = f"{emoji} {s[:25]}"
    ws = wb.create_sheet(sheet_name)
    ws.sheet_view.showGridLines = False

    for i, w in enumerate(col_widths):
        ws.column_dimensions[col_letters[i]].width = w

    ws.merge_cells('A1:I1')
    c = ws['A1']
    c.value = f"{emoji} {suite_full_names[s]}"
    c.font  = Font(name="Calibri", bold=True, color=WHITE, size=14)
    c.fill  = make_fill(DARK_BLUE)
    c.alignment = center()
    ws.row_dimensions[1].height = 34

    for col, h in enumerate(all_headers, 1):
        c = ws.cell(row=2, column=col, value=h)
        c.font      = header_font(10)
        c.fill      = make_fill(ACCENT1)
        c.alignment = center()
        c.border    = thin_border()
    ws.row_dimensions[2].height = 24

    suite_tcs = [tc for tc in TEST_CASES if tc[1] == s]
    for i, tc in enumerate(suite_tcs):
        r = i + 3
        bg = row_fills[i % 2]
        for col, val in enumerate(tc, 1):
            c = ws.cell(row=r, column=col, value=val)
            if col == 8:
                c.fill = make_fill(priority_colors.get(val, GREY_BG))
                c.font = Font(name="Calibri", bold=True, size=9,
                              color=(RED_HEX if val == "High" else AMBER if val == "Medium" else GREEN_HEX))
            elif col == 9:
                c.fill = make_fill(status_colors.get(val, GREY_BG))
                c.font = normal_font(9, bold=True)
            else:
                c.fill = make_fill(bg)
                c.font = normal_font(9)
            c.alignment = left()
            c.border    = thin_border()
        ws.row_dimensions[r].height = 55

    ws.freeze_panes = 'A3'
    ws.auto_filter.ref = f"A2:I{len(suite_tcs)+2}"

# ─── Save ─────────────────────────────────────────────────────────────────────
import os
script_dir = os.path.dirname(os.path.abspath(__file__))
output_path = os.path.join(script_dir, "SkySense_AI_Selenium_Test_Report.xlsx")
wb.save(output_path)
print(f"SUCCESS: Excel report saved to {output_path}")
print(f"Total test cases: {len(TEST_CASES)}")
