# ---------------------- Prompts ----------------------

def generate_prompt(brand, product, goal, platform, trends, persona, creative_ideas):
    return f"""
You are an AI marketing strategist.

Generate a campaign brief based on:
- Brand: {brand}
- Product: {product}
- Goal: {goal}
- Platform: {platform}

Here are internal insights:
- Trends: {', '.join(trends)}
- Target Persona: {persona}
- Creative Angles: {', '.join(creative_ideas)}

Now generate:
- 1 engaging caption
- 2-3 creative hooks
- Relevant hashtags
- CTA (Call To Action)
- Tone of voice
Return everything in JSON format.
"""