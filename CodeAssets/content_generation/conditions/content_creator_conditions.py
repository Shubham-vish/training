def should_revise(state: dict) -> str:
    """Conditional edge function to decide if we need to critique or move to hook creation"""
    if state.get("revision_number", 0) < state.get("max_revisions", 2):
        return "research_critique"
    else:
        return "hook_creator"

def after_hook_creator(state: dict) -> str:
    """Always proceed to hashtag generation after hook creation"""
    return "hashtag_generator"