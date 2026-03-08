# backend/services/offline_extraction.py

from __future__ import annotations

import re
from typing import Dict, List, Tuple


# Broader feature areas (more realistic for app review triage)
FEATURE_RULES: Dict[str, List[str]] = {
    "Login/Account": [
        "login", "log in", "sign in", "signin", "sign-in",
        "signup", "sign up", "register", "registration",
        "password", "otp", "verification", "verify", "2fa", "two factor",
        "account", "profile", "username", "email", "phone number", "reset password",
        "code", "verification code", "one time password", "cant login", "can't login", "logged out"
    ],
    "Performance/Crashes": [
        "slow", "lag", "lags", "laggy", "freeze", "frozen", "hang", "stuck",
        "loading", "buffer", "buffering", "not responding",
        "crash", "crashes", "crashing", "keeps crashing",
        "bug", "bugs", "glitch", "glitches", "error", "errors",
        "failed to load", "won't load", "doesn't load", "does not load",
        "update", "after update", "new update", 
        "won't open", "cant open", "can't open", "black screen", 
        "white screen", "stuck on", "keeps loading"
    ],
    "UI/UX": [
        "ui", "ux", "interface", "layout", "design", "navigation", "menu",
        "button", "buttons", "scroll", "scrolling", "font", "theme",
        "dark mode", "light mode", "too small", "hard to use", "confusing",
    ],
    "Payments/Subscription": [
        "payment", "pay", "card", "debit", "credit", "billing",
        "charged", "charge", "overcharged", "refund", "refunds",
        "subscription", "subscribe", "renew", "renewal", "trial",
        "cancel subscription", "cancellation", "invoice", "receipt",
        "premium", "plan", "membership", "auto renewal", "cancel"
    ],
    "Notifications": [
        "notification", "notifications", "notify", "alert", "alerts",
        "reminder", "reminders", "push", "push notification",
    ],
    "Search/Discovery": [
        "search", "find", "filter", "filters", "sort", "sorting",
        "discover", "discovery", "recommendation", "recommendations",
        "results", "no results",
    ],
    "Ads": [
        "ads", "ad", "advert", "advertisement", "too many ads",
        "annoying ads", "pop up", "popup", "pop-up", "adverts", 
        "sponsored", "ads are", "too much ads"
    ],
    "Privacy/Security": [
        "privacy", "data", "permission", "permissions",
        "tracking", "track", "security", "secure",
        "scam", "fraud", "hack", "hacked", "phishing",
    ],
    "Content/Quality": [
        "content", "quality", "resolution", "stream", "streaming",
        "audio", "sound", "video", "music", "download", "offline",
        "subtitle", "captions", "buffering", "playback",
    ],
    "Customer Support": [
        "support", "customer support", "customer service",
        "help", "helpdesk", "ticket", "contact", "respond", "response",
        "no reply", "not replying", "unhelpful",
    ],
}


# Phrases indicating certain issue types
BUG_HINTS = [
    "crash", "crashing", "keeps crashing", "bug", "glitch", "error",
    "not working", "doesn't work", "does not work", "broken",
    "failed", "fails", "failure", "not responding", "stuck",
]
UX_HINTS = [
    "confusing", "hard to use", "difficult", "annoying", "frustrating",
    "bad ui", "ugly", "hate the new", "poor design", "not intuitive",
]
ENHANCEMENT_HINTS = [
    "please add", "feature request", "would be nice", "should have",
    "need a", "add option", "add feature", "i wish", "can you add",
]
PRAISE_HINTS = [
    "love", "great", "awesome", "amazing", "excellent", "fantastic",
    "good app", "very good", "perfect",
]


def _normalize(text: str) -> str:
    return re.sub(r"\s+", " ", (text or "").strip()).lower()


def feature_area_from_text(text: str) -> str:
    """
    Score-based classifier: counts how many keywords from each feature bucket appear in text.
    Returns the feature bucket with the highest score. If all scores are 0 -> 'Other'.
    """
    t = _normalize(text)
    best_area = "Other"
    best_score = 0

    for area, keywords in FEATURE_RULES.items():
        score = 0
        for kw in keywords:
            if kw in t:
                score += 1
        if score > best_score:
            best_area = area
            best_score = score
    
    if best_score == 0:
        return "Generic Issue"

    return best_area


def issue_type_from_text(text: str, rating: int | None = None) -> str:
    """
    Coarse issue type classification.
    Priority:
      - Praise (if strong praise hints OR rating >=4 and no strong negatives)
      - Bug (if bug hints)
      - UX (if UX hints)
      - Enhancement (if request hints)
      - Complaint otherwise (especially rating <=3)
    """
    t = _normalize(text)

    has_bug = any(h in t for h in BUG_HINTS)
    has_ux = any(h in t for h in UX_HINTS)
    has_req = any(h in t for h in ENHANCEMENT_HINTS)
    has_praise = any(h in t for h in PRAISE_HINTS)

    if has_praise and not (has_bug or has_ux or has_req):
        if rating is None or rating >= 4:
            return "Praise"
    
    if has_bug or has_ux or has_req:
        return "Complaint"
    
    if rating is not None and rating >= 4:
        return "Praise"
    
    return "Complaint"


def urgency_from_rating(rating: int | None) -> int:
    """
    Convert rating to urgency. This is simple and works surprisingly well.
    1-2 stars -> critical
    3 stars   -> medium
    4-5 stars -> low
    """
    if rating is None:
        return 3
    if rating <= 2:
        return 5
    if rating == 3:
        return 3
    return 1


def short_summary(text: str, max_len: int = 120) -> str:
    """
    A lightweight summary: just normalized, trimmed text.
    """
    s = re.sub(r"\s+", " ", (text or "").strip())
    return s[:max_len] + ("..." if len(s) > max_len else "")


def extract_offline(text: str, rating: int | None = None) -> Dict[str, object]:
    """
    Main function to be used by scripts:
      returns {feature_area, issue_type, urgency, short_summary}
    """
    area = feature_area_from_text(text)
    itype = issue_type_from_text(text, rating=rating)
    urg = urgency_from_rating(rating)
    summ = short_summary(text)

    return {
        "feature_area": area,
        "issue_type": itype,
        "urgency": int(urg),
        "short_summary": summ,
    }
