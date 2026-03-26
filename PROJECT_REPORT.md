# Garuda - Project Report
## BYOP Submission | AI/ML Course | VIT Bhopal

---

## 1. The Problem

College group chats - whether on WhatsApp, Discord or any internal platform - often have toxic messages. Slurs, directed insults, harassment. Most of the time nobody moderates it. I wanted to build something that could automatically detect and filter these messages without needing a human to watch the chat 24/7.

The tricky part is that a filter can't be too strict. College students use a lot of words in frustration that are not actually harmful. The challenge was building something that understands that difference.

---

## 2. Why I chose this

I noticed this problem firsthand in college group chats. A lot of messages that go out are either genuinely toxic or come very close to it. Existing tools like YouTube's filter or Discord's Automod are either too aggressive or not adapted to Hinglish (Hindi + English mixed) which is what Indian students actually use.

So I decided to build one myself, specifically for this context.

---

## 3. What I built

Garuda is a web application with:
- A Python Flask backend that exposes a REST API
- A custom filter engine (`filter.py`) that does all the detection logic
- A frontend chat interface where you can test messages live

---

## 4. How the filter works

### Scoring system
Every word in my word list has a score assigned to it - 1 for mild, 2 for moderate, 3 for severe. When a message comes in, I add up the scores of all matching words. If the total is 2 or more, the message gets flagged.

### Whitelisting
Some words appear in common frustrated expressions that are not actually toxic. I maintain a list of such phrases. If a message matches one of these and the score is still low, it passes through without being flagged.

### Aggression context
Mild words (score 1) on their own don't matter much. But if the message also has words like "you are", "ur", "teri" etc. that suggest the message is directed at someone, I bump up the score of those mild words to 2. This captures cases where someone is being aggressive but using softer words.

### Leet speak handling
Before checking anything, I run the text through a normalization step that converts common leet substitutions - @ to a, 3 to e, 0 to o etc. This prevents simple bypass attempts.

### Censorship
Flagged words get replaced with partial asterisks - first and last letter are kept, middle is hidden. So it's clear something was filtered but the message is still somewhat readable.

---

## 5. Technical decisions I made

**Rule-based instead of ML model**
I considered training a classifier but decided against it. The main reason is data - getting a properly labeled dataset of toxic messages ethically is hard. A rule-based approach also gives me full control and transparency which makes more sense for this use case. I can see exactly why something got flagged.

**Hinglish support**
Pure English filters would miss half the actual toxic content in Indian college chats. I made sure the word list includes common Hindi abusive terms alongside English ones.

**Threshold of 2**
Setting the threshold at 2 instead of 1 means a single mild word won't get someone flagged. This reduces false positives a lot.

---

## 6. Challenges

**Context is hard**
Words mean different things depending on how they're used. "Idiot" directed at someone is very different from "I did such an idiot thing today". My aggression context detection helps but it's not perfect.

**Spelling variations**
People type the same word in 10 different ways. The leet speak normalization handles some of it but not all. A better approach would be fuzzy matching or character-level n-grams.

**Whitelist vs being too lenient**
Making the whitelist too big would let genuinely toxic messages through. I kept it focused on the most common casual expressions only.

---

## 7. What I learned

- How to build a complete web app with Flask from scratch
- How text preprocessing works - normalization, pattern matching, tokenization concepts
- The complexity of content moderation - it's not just about blocking words, context matters a lot
- How to design and expose a REST API
- Frontend-backend communication using fetch and JSON
- That building for a specific cultural context (Hinglish, Indian college environment) requires you to think beyond generic solutions

---

## 8. What could be improved

- Train an actual ML classifier on labeled data for better generalization
- Add a feedback button so users can report wrong decisions, and use that to improve over time
- Support for detecting toxic intent even when no bad words are used (sarcasm, passive aggression)
- Admin panel with logs and moderation history
- Integration with existing platforms like Discord or Slack via webhooks

---

## 9. Conclusion

Garuda is a focused, practical solution to a real problem I observed in my own college environment. It applies text processing and classification concepts from the course to build something that actually works and could realistically be deployed. The filter is not perfect but it handles the most common cases well and is designed to be extended further.

---

*Name: Vinayak Vishwkarma*
*REG No: 25BCE10258*
*Course: Fundamentals in AI/ML*
*GitHub: https://github.com/vinayakv29/Garuda*
