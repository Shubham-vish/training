"""Search executor agent node."""

from langchain_core.messages import SystemMessage, HumanMessage
from SharedCode.agent_utils.agent_utils import AgentContext, replace_state_placeholders
from SharedCode.services.content_fetching_service import enhance_search_results_with_content, get_content_for_ai_analysis
from typing import Optional, List, Dict, Any
import logging
import os

logger = logging.getLogger(__name__)

# Import search service with fallback
try:
    from SharedCode.services.search_service import SearchService
    SEARCH_SERVICE_AVAILABLE = True
except Exception as e:
    logger.warning(f"Search service not available: {e}")
    SEARCH_SERVICE_AVAILABLE = False

SEARCH_EXECUTOR_PROMPT = """
You are a research content analyzer tasked with processing and summarizing web search results for content creation.

Topic: __state__{topic}__state__
Content Type: __state__{content_type}__state__
Style: __state__{style}__state__

Global Custom Instructions (if provided):
__state__{global_custom_instruction}__state__

Search Queries Executed:
{queries_info}

Raw Search Results:
{search_results}

Your task is to analyze the search results and extract relevant, high-quality information that will be useful for creating content about the topic. 

For each search result, extract:
1. Key facts and insights relevant to the topic
2. Statistics, data points, or examples that could strengthen the content
3. Current trends or developments in the field
4. Expert opinions or authoritative sources
5. Interesting angles or perspectives on the topic

Present the information in a structured format that's easy for content creators to use. Focus on accuracy, relevance, and actionable insights.

If global custom instructions are provided, ensure the extracted information aligns with those requirements.
"""

def search_executor_node(
    ctx: AgentContext, 
    custom_user_message: Optional[str] = None,
    fetch_full_content: bool = True,  # New parameter to enable/disable content fetching
    max_pages_per_query: int = 2,     # Limit pages to fetch per query
) -> dict:
    """
    Execute web searches for queries and process results
    
    Args:
        ctx: Agent context containing state and model
        custom_user_message: Additional instructions from user
        fetch_full_content: Whether to fetch full webpage content (default: True)
        max_pages_per_query: Maximum number of pages to fetch per query (default: 2)
    """
    ctx.start_conversation("� Search Executor")
    
    try:
        # Get search queries from state
        queries = ctx.state.get('queries', [])
        if not queries:
            ctx.log_progress("⚠️ No search queries found")
            return {
                "content": ["No search queries available for execution"],
                "search_results": [],
                "lnode": "search_executor",
                "token_usage": {"total_tokens": 0, "prompt_tokens": 0, "completion_tokens": 0}
            }

        ctx.log_progress(f"🔍 Processing {len(queries)} queries | Content fetch: {'ON' if fetch_full_content else 'OFF'}", {
            "queries_count": len(queries),
            "queries": queries,
            "fetch_full_content": fetch_full_content,
            "max_pages_per_query": max_pages_per_query
        })
        
        all_search_results = []
        
        # Check if search service is available
        if not SEARCH_SERVICE_AVAILABLE:
            ctx.log_progress("📱 Using mock data (no API keys)", {
                "search_mode": "mock",
                "reason": "No API keys available",
                "queries_to_mock": len(queries)
            })
            # Create mock search results for testing
            for query in queries:
                mock_results = _create_mock_search_results(query)
                all_search_results.append({
                    "query": query,
                    "results": mock_results,
                    "status": "mock"
                })
        else:
            search_service = SearchService()
            ctx.log_progress("🌐 Real search service active", {
                "search_mode": "live",
                "service": "SearchService"
            })
        
            # Execute each search query
            for i, query in enumerate(queries):
                try:
                    # Try Tavily first, fallback to other services if needed
                    results = search_service.tavily_search(query, max_results=3)
                    search_source = "Tavily"
                    
                    if not results or not isinstance(results, dict) or 'results' not in results:
                        results = search_service.search_serpapi(query, num_results=3)
                        search_source = "SerpAPI"
                        
                        if isinstance(results, str):  # Error message
                            results = []
                            search_source = "Failed"
                    
                    result_count = len(results.get('results', []) if isinstance(results, dict) else results)
                    ctx.log_progress(f"📊 {search_source}: {result_count} results", {
                        "query": query,
                        "search_source": search_source,
                        "result_count": result_count,
                        "success": result_count > 0
                    })
                    
                    all_search_results.append({
                        "query": query,
                        "results": results,
                        "status": "success" if results else "failed"
                    })
                    
                    ctx.log_progress(f"✅ Found {len(results.get('results', []) if isinstance(results, dict) else results)} results for '{query}'", {
                        "query": query,
                        "search_source": search_source,
                        "result_count": result_count,
                        "results_structure": {
                            "type": type(results).__name__,
                            "keys": list(results.keys()) if isinstance(results, dict) else None,
                            "has_results": bool(results),
                            "format": "tavily" if isinstance(results, dict) and 'results' in results else "serpapi" if isinstance(results, list) else "unknown"
                        },
                        "sample_titles": [
                            item.get('title', 'No title')[:50] + "..." if len(item.get('title', '')) > 50 else item.get('title', 'No title')
                            for item in (results.get('results', [])[:2] if isinstance(results, dict) else results[:2] if isinstance(results, list) else [])
                        ] if results else []
                    })
                    
                except Exception as e:
                    all_search_results.append({
                        "query": query,
                        "results": [],
                        "status": "error",
                        "error": str(e)
                    })

        # Process and analyze search results with LLM
        if all_search_results:
            successful_searches = [r for r in all_search_results if r.get('status') == 'success' and r.get('results')]
            ctx.log_progress(f"📊 {len(successful_searches)}/{len(all_search_results)} successful", {
                "successful_searches": len(successful_searches),
                "total_searches": len(all_search_results),
                "success_rate": round((len(successful_searches) / len(all_search_results)) * 100, 1)
            })
            
            # Optionally fetch full content from top URLs
            if fetch_full_content:
                all_search_results = enhance_search_results_with_content(all_search_results, max_pages_per_query, ctx)
            
            # Prepare data for AI analysis
            queries_info = "\\n".join([f"- {q}" for q in queries])
            search_results_text = _format_search_results_for_analysis(all_search_results)
            
            # Truncate for AI analysis while preserving full content in state
            ai_analysis_text = get_content_for_ai_analysis(search_results_text)
            # Use prompt template from context or default
            prompt_template = ctx.prompts.get('search_executor', SEARCH_EXECUTOR_PROMPT)
            
            # First replace state placeholders
            base_prompt = replace_state_placeholders(prompt_template, ctx.state)
            
            # Then replace the custom format fields
            base_prompt = base_prompt.replace('{queries_info}', queries_info)
            base_prompt = base_prompt.replace('{search_results}', ai_analysis_text)  # Use truncated version for AI

            messages = [
                SystemMessage(content=base_prompt),
            ]

            if custom_user_message:
                messages.append(HumanMessage(content=f"Additional user instructions: {custom_user_message}"))

            response = ctx.model.invoke(messages)
            token_usage = response.response_metadata.get("token_usage", {})
            
            # Split response into content pieces
            content_pieces = [piece.strip() for piece in response.content.split('\\n\\n') if piece.strip()]
            ctx.log_progress(f"🤖 AI Analysis: {len(content_pieces)} sections | {token_usage.get('total_tokens', 0)} tokens", {
                "content_sections": len(content_pieces),
                "total_tokens": token_usage.get('total_tokens', 0),
                "prompt_tokens": token_usage.get('prompt_tokens', 0),
                "completion_tokens": token_usage.get('completion_tokens', 0),
                "analysis_length": len(response.content),
                "input_length": len(ai_analysis_text)
            })
            
        else:
            content_pieces = ["No search results were successfully retrieved"]
            token_usage = {"total_tokens": 0, "prompt_tokens": 0, "completion_tokens": 0}

        result = {
            "content": content_pieces,
            "search_results": all_search_results,  # Full content preserved here
            "queries_executed": queries,
            "lnode": "search_executor",
            "token_usage": token_usage,
            "research_results": response.content if 'response' in locals() else None  # Full AI analysis
        }

        # Calculate summary stats for logging
        total_results = sum(len(sr.get('results', {}).get('results', []) if isinstance(sr.get('results'), dict) else sr.get('results', [])) 
                          for sr in all_search_results)
        enhanced_urls = sum(1 for sr in all_search_results 
                          if sr.get('results') and isinstance(sr['results'], dict) and 'results' in sr['results']
                          for res in sr['results']['results'] if res.get('content_enhanced'))

        ctx.finalize_conversation({
            "summary": f"✅ Search complete: {len(content_pieces)} sections",
            "queries": len(queries),
            "results": len(all_search_results),
            "total_search_results": total_results,
            "enhanced_urls": enhanced_urls,
            "content_sections": len(content_pieces),
            "tokens_used": token_usage.get('total_tokens', 0)
        })

        return result
        
    except Exception as e:
        ctx.finalize_conversation({
            "summary": f"❌ Search failed: {str(e)}"
        })
        raise

def _format_search_results_for_analysis(search_results: List[Dict]) -> str:
    """Format search results for LLM analysis."""
    formatted_results = []
    
    for result_set in search_results:
        query = result_set["query"]
        results = result_set["results"]
        status = result_set["status"]
        
        formatted_results.append(f"\\n--- Results for: {query} ---")
        
        if status == "error":
            formatted_results.append(f"Error: {result_set.get('error', 'Unknown error')}")
            continue
            
        if not results:
            formatted_results.append("No results found")
            continue
            
        # Handle Tavily format
        if isinstance(results, dict) and 'results' in results:
            tavily_results = results['results'][:3]  # Limit to top 3
            for i, item in enumerate(tavily_results, 1):
                title = item.get('title', 'No title')
                content = item.get('content', 'No content')
                url = item.get('url', 'No URL')
                full_content = item.get('full_content', '')
                
                if full_content and item.get('content_enhanced'):
                    # Use structured content with clear indication
                    formatted_results.append(f"{i}. **{title}**\\n   Enhanced Content:\\n{full_content}\\n   Source: {url}\\n")
                else:
                    # Fallback to original snippet
                    snippet = content[:200] + "..." if len(content) > 200 else content
                    formatted_results.append(f"{i}. **{title}**\\n   Snippet: {snippet}\\n   Source: {url}\\n")
                
        # Handle SerpAPI format
        elif isinstance(results, list):
            for i, item in enumerate(results[:3], 1):  # Limit to top 3
                title = item.get('title', 'No title')
                snippet = item.get('snippet', 'No snippet')
                link = item.get('link', 'No URL')
                full_content = item.get('full_content', '')
                
                if full_content and item.get('content_enhanced'):
                    # Use structured content with clear indication
                    formatted_results.append(f"{i}. **{title}**\\n   Enhanced Content:\\n{full_content}\\n   Source: {link}\\n")
                else:
                    # Fallback to original snippet
                    formatted_results.append(f"{i}. **{title}**\\n   Snippet: {snippet}\\n   Source: {link}\\n")
        
        formatted_results.append("")  # Add spacing
    
    return "\\n".join(formatted_results)


def _create_mock_search_results(query: str) -> Dict:
    """Create mock search results for testing purposes."""
    mock_results = {
        "results": [
            {
                "title": f"Top insights on {query}",
                "content": f"Comprehensive analysis of {query} showing significant trends and developments in the industry. Recent studies indicate growing adoption rates and positive outcomes for businesses implementing these solutions.",
                "url": f"https://example.com/insights-{query.replace(' ', '-')}"
            },
            {
                "title": f"Best practices for {query}",
                "content": f"Industry experts share proven strategies for {query} implementation. Key factors include proper planning, stakeholder engagement, and continuous monitoring of performance metrics.",
                "url": f"https://example.com/best-practices-{query.replace(' ', '-')}"
            },
            {
                "title": f"Case study: {query} success story",
                "content": f"Real-world example of successful {query} implementation resulting in 40% efficiency improvement and significant cost savings. Detailed breakdown of approach and lessons learned.",
                "url": f"https://example.com/case-study-{query.replace(' ', '-')}"
            }
        ]
    }
    return mock_results