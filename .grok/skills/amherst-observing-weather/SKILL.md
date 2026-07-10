---
name: amherst-observing-weather
description: >
  Daily Amherst NH astronomy weather and evening go/no-go for Starwatch observing.
  Use for weather, tonight's sky, clear nights, or /weather /amherst-observing-weather.
  Canonical full skill also lives at ~/.grok/skills/amherst-observing-weather/.
metadata:
  short-description: "Amherst NH evening observing forecast"
---

# Amherst observing weather (Starwatch project)

Follow the full procedure in:

**`~/.grok/skills/amherst-observing-weather/SKILL.md`**

If that path is unavailable, use this summary:

1. Fetch NWS Amherst NH (03031 / 42.86N 71.63W) text forecast.  
2. Verdict: **GO** / **MARGINAL** / **SCRUB** for tonight (visual vs deep-sky if different).  
3. Table: clouds, precip, wind, fog/dew, action.  
4. Short lookahead 1–3 nights.  
5. On GO/MARGINAL, optional Starwatch reminder (align HC first, Pi on wall power).

Proactive daily briefs are scheduled separately; still run on demand when user asks.
