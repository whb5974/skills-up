---
name: brand-voice-guard
description: Ensure content matches brand voice guidelines. Check tone, style, terminology, and messaging consistency across documents and communications.
---

# Brand Voice Guard Skill

## Capabilities

- Analyze text for brand voice compliance
- Check tone consistency (formal, casual, friendly, professional)
- Verify terminology usage
- Identify off-brand messaging
- Suggest improvements for brand alignment
- Compare content against brand guidelines

## Configuration

Create a brand voice configuration file:

```yaml
# brand-voice.yaml
brand:
  name: "Your Brand"
  tone:
    - professional
    - friendly
    - helpful
  
  style:
    - clear
    - concise
    - active_voice
  
  forbidden_terms:
    - "cheap"
    - "guaranteed"
  
  preferred_terms:
    "customers": "clients"
    "buy": "invest"
  
  messaging_pillars:
    - "Quality first"
    - "Customer-centric"
    - "Innovation"
```

## Usage

When the user asks to check brand voice:

1. Load brand guidelines (if available)
2. Analyze the content
3. Check for:
   - Tone alignment
   - Terminology consistency
   - Messaging alignment
   - Style guidelines
4. Provide feedback and suggestions

## Example Analysis

```python
def analyze_brand_voice(text, guidelines):
    issues = []
    suggestions = []
    
    # Check forbidden terms
    for term in guidelines.get('forbidden_terms', []):
        if term.lower() in text.lower():
            issues.append(f"Found forbidden term: '{term}'")
    
    # Check preferred terms
    for preferred, replacement in guidelines.get('preferred_terms', {}).items():
        if preferred.lower() in text.lower():
            suggestions.append(f"Consider using '{replacement}' instead of '{preferred}'")
    
    # Check tone indicators
    tone_score = calculate_tone_score(text, guidelines.get('tone', []))
    
    return {
        'issues': issues,
        'suggestions': suggestions,
        'tone_score': tone_score,
        'compliant': len(issues) == 0
    }
```

## Notes

- Brand guidelines should be provided by the user
- Tone analysis can use sentiment analysis libraries
- Keep a glossary of approved terminology
- Consider industry-specific compliance requirements
