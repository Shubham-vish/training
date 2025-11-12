# Agent Design Principles


1. **Planner**
   - Why: Just produces a strategy document that other nodes use as text
   - Output: Single `content_outline` string
   - Simple text output.

2. **Script Generator**
   - Why: Just produces the final script text
   - Output: Single `script` string
   - Simple text output.

3. **Research Planner** 
   - Why: Produces list of queries needed by Search Executor
   - Fields: `research_queries` (List[str]), `research_objectives`, `key_areas`, `information_sources`
   - Structured output.

4. **Search Executor**
   - Why: Produces key insights list for display + research summary text
   - Fields: `key_insights` (List[str]), `research_summary` (str)
   - Structured output.

5. **Reflection** 
   - Why: Produces quality scores needed for routing decision
   - Fields: `engagement`, `accuracy`, `structure`, `actionability`, `audience_fit` (all float), `critique` (str)
   - Structured output.

6. **Hashtag Generator**
   - Why: Produces list of hashtags
   - Fields: `hashtags` (List[str]), `seo_keywords` (List[str]), `rationale` (str)
   - Structured output.

7. **CTA Generator**
   - Why: Produces list of engagement hooks
   - Fields: `cta` (str), `engagement_hooks` (List[str])
   - Structured output.


## Code Organization

### Each Node Has:
1. **Pydantic Model** (if needed) - Define structured output at top of file
2. **Display Function** - Private function `_display_xxx()` for presentation logic
3. **Node Function** - Clean, simple main function that:
   - Gets LLM client
   - Calls `generate_response()` or `generate_structured()`
   - Updates state
   - Calls display function

### Example Structure:
```python
# Structured Output (if needed)
class OutputModel(BaseModel):
    field1: Type = Field(description="...")
    
# Display Logic
def _display_results(data, execution_time):
    # Rich formatting, panels, tables
    pass

# Main Node Function (SIMPLE!)
def node_function(state):
    start_time = time.time()
    llm_client = get_llm_client()
    
    result = llm_client.generate_structured(...)  # or generate_response()
    
    execution_time = time.time() - start_time
    updates = {...}
    state.add_agent_execution(...)
    
    _display_results(result, execution_time)
    return updates
```