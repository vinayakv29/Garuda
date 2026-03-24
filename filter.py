import re

# garuda filter - main logic file
# idea is simple - each bad word gets a score (1, 2 or 3)
# if total score of a message crosses 2 then we flag it
# mild words like damn/hell only matter if message sounds aggressive

# 3 = very bad, 2 = medium bad, 1 = borderline
BAD_WORDS = {
    # level 3 - clearly abusive, always block
    "bhenchod": 3,
    "dick": 3,
    "madarchod": 3,
    "randi": 3,
    "chutiya": 3,
    "bhosdike": 3,
    "gaandu": 3,
    "lodu": 3,
    "fuck": 3,
    "fucking": 3,
    "fucker": 3,
    "motherfucker": 3,
    "bitch": 3,
    "cunt": 3,
    "bastard": 3,
    "asshole": 3,
    "dickhead": 3,
    "faggot": 3,
    "whore": 3,
    "slut": 3,
    "retard": 3,
    "nigger": 3,
    "nigga": 3,
    "bc": 3,
    "mf": 3,
    "mfc": 3,
    "kill yourself": 3,
    "kys": 3,

    # level 2 - insulting but not the worst
    "harami": 2,
    "kamine": 2,
    "kutte": 2,
    "saale": 2,
    "kamina": 2,
    "ullu": 2,
    "bewakoof": 2,
    "idiot": 2,
    "stupid": 2,
    "moron": 2,
    "loser": 2,
    "dumb": 2,
    "dumbass": 2,
    "jackass": 2,
    "prick": 2,
    "jerk": 2,
    "creep": 2,
    "freak": 2,
    "ass": 2,
    "wtf": 2,
    "stfu": 2,
    "shut up": 2,
    "go to hell": 2,

    # level 1 - only a problem if used with aggression
    "damn": 1,
    "hell": 1,
    "crap": 1,
}

# these phrases sound bad but are just normal frustration
# no one should get flagged for these in a college setting
SAFE_PHRASES = {
    "shit yaar", "yaar shit", "shit man", "man shit",
    "what the hell", "oh hell", "what the heck",
    "damn it", "oh damn", "oh crap", "crap yaar",
}

# if these words appear, mild words get treated as moderate
AGGRESSION_WORDS = [
    "you are", "you're", "ur", "tum", "teri", "tera",
    "go", "get out", "die", "hate you", "hate u",
]


def prep_text(text):
    # lowercase and fix basic leet speak substitutions
    text = text.lower().strip()
    text = text.replace("@", "a").replace("3", "e").replace("0", "o").replace("1", "i")
    text = re.sub(r"\s+", " ", text)
    return text


def is_safe_phrase(text):
    cleaned = prep_text(text)
    for phrase in SAFE_PHRASES:
        if phrase in cleaned:
            return True
    return False


def is_aggressive(text):
    cleaned = prep_text(text)
    for word in AGGRESSION_WORDS:
        if word in cleaned:
            return True
    return False


class GarudaFilter:
    def __init__(self):
        self.word_list = BAD_WORDS

    def analyze(self, message: str) -> dict:
        # empty message - nothing to do
        if not message or not message.strip():
            return {
                "original": message,
                "filtered": message,
                "is_toxic": False,
                "severity": 0,
                "severity_label": "clean",
                "flagged_words": [],
                "score": 0,
                "reason": "Empty message"
            }

        cleaned = prep_text(message)
        detected = []
        points = 0
        aggressive = is_aggressive(message)

        for word, level in self.word_list.items():
            pattern = r'\b' + re.escape(word) + r'\b'
            if re.search(pattern, cleaned):
                actual_level = level
                # bump up mild words if message has aggressive tone
                if level == 1 and aggressive:
                    actual_level = 2
                detected.append({
                    "word": word,
                    "level": actual_level
                })
                points += actual_level

        # check if its just casual frustration - let it pass
        if is_safe_phrase(message) and points <= 2:
            return {
                "original": message,
                "filtered": message,
                "is_toxic": False,
                "severity": 0,
                "severity_label": "clean",
                "flagged_words": [],
                "score": 0,
                "reason": "Casual expression - not flagged"
            }

        # score under 2 means its fine
        is_bad = points >= 2
        censored_msg = self._censor(message, detected)

        if points == 0:
            tag = "clean"
        elif points <= 2:
            tag = "mild"
        elif points <= 5:
            tag = "moderate"
        else:
            tag = "severe"

        return {
            "original": message,
            "filtered": censored_msg if is_bad else message,
            "is_toxic": is_bad,
            "severity": points,
            "severity_label": tag,
            "flagged_words": [d["word"] for d in detected],
            "score": points,
            "reason": f"Found {len(detected)} problematic term(s)" if detected else "No issues found"
        }

    def _censor(self, message: str, detected: list) -> str:
        output = message
        for item in detected:
            w = item["word"]
            # keep first and last letter, hide the middle
            if len(w) > 2:
                hidden = w[0] + "*" * (len(w) - 2) + w[-1]
            else:
                hidden = "*" * len(w)
            pat = re.compile(r'\b' + re.escape(w) + r'\b', re.IGNORECASE)
            output = pat.sub(hidden, output)
        return output
