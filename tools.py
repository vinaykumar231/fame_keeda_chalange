# ---------------------- Tools ----------------------

def trend_fetcher(brand, platform):
    return [f"#{brand}On{platform}", f"#{platform}Buzz", "#TrendingNow"]

def persona_classifier(goal, product):
    if goal.lower() == "brand awareness":
        return "Young, urban audience looking for lifestyle upgrades"
    return "Fitness-conscious individuals aged 25–35"

def creative_angle(brand, product, goal):
    return [
        f"{brand} makes {product} for the bold and fearless.",
        "Show off your unique style with comfort.",
        "Run the world, one step at a time."
    ]
