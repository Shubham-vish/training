"""Temperature configuration for content generation nodes."""

# Optimal temperature settings for different content types
NODE_TEMPERATURE_CONFIG = {
    # Creative Content Generation (Higher temperatures for more creativity)
    'script_generation': 0.9,      # Scripts need high creativity and natural flow
    'hook_generation': 1.0,        # Hooks need maximum creativity to capture attention
    'hashtag_generation': 0.7,     # Hashtags need balance of creativity and relevance
    'cta_generation': 0.6,         # CTAs need some creativity but stay focused
    'carousel_generation': 0.8,    # Carousels need creative but structured content
    'story_generation': 0.9,       # Stories need high creativity and engagement
    
    # Analytical Content Generation (Lower temperatures for accuracy)
    'search_executor': 0.3,        # Search needs focused, accurate analysis
    'content_analyzer': 0.2,       # Analysis needs precision and consistency
    'trend_analyzer': 0.4,         # Trend analysis needs some creativity for insights
}

def get_model_with_temperature(base_model, node_type: str):
    """
    Apply dynamic temperature to a model based on node type.
    
    Args:
        base_model: The base LLM model instance
        node_type: The type of content generation node
        
    Returns:
        Model configured with appropriate temperature for the node type
    """
    temperature = NODE_TEMPERATURE_CONFIG.get(node_type, 0.5)  # Default to 0.5
    
    return base_model.with_config({
        'llm': {'temperature': temperature}
    })

def log_temperature_usage(ctx: 'AgentContext', node_type: str):
    """Log the temperature being used for a specific node."""
    temperature = NODE_TEMPERATURE_CONFIG.get(node_type, 0.5)
    
    ctx.log_progress(
        "🌡️ Temperature Configuration",
        data={
            'node_type': node_type,
            'temperature': temperature,
            'reasoning': get_temperature_reasoning(node_type)
        }
    )

def get_temperature_reasoning(node_type: str) -> str:
    """Get the reasoning behind temperature choice for a node type."""
    reasoning_map = {
        'script_generation': 'High creativity needed for engaging, natural-sounding scripts',
        'hook_generation': 'Maximum creativity required to capture attention and stand out',
        'hashtag_generation': 'Balanced creativity for relevant but varied hashtags',
        'cta_generation': 'Moderate creativity while maintaining clear, action-oriented focus',
        'carousel_generation': 'Creative but structured content for visual storytelling',
        'story_generation': 'High creativity for compelling narrative and engagement',
        'search_executor': 'Low creativity for focused, accurate search result analysis',
        'content_analyzer': 'Minimal creativity for precise, consistent content analysis',
        'trend_analyzer': 'Moderate creativity for insightful trend interpretation'
    }
    
    return reasoning_map.get(node_type, 'Default balanced setting for content generation')