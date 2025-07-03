from datetime import datetime

def scale_resources(new_count, tier="App"):
    """
    Simulate scaling action for App or DB tier.
    
    :param new_count: Number of instances to scale to
    :param tier: Tier name ('App' or 'DB') for logging
    """
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    print(f"[{timestamp}] 🚀 Scaling {tier} Tier → {new_count} instances")
