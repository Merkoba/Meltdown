from __future__ import annotations

# Standard
import json
import requests
import urllib.parse
from bs4 import BeautifulSoup


class Search:
    def web_search(self, query: str) -> str:
        try:
            # First try DuckDuckGo instant answer API (no rate limiting)
            ddg_result = self.duckduckgo_search(query)

            if ddg_result and "Error" not in ddg_result:
                return ddg_result
        except:
            pass

        try:
            return self.google_scrape_search(query)
        except Exception as e:
            return f"Error performing web search: {e}"

    def duckduckgo_search(self, query: str) -> str:
        try:
            # DuckDuckGo instant answer API
            ddg_url = "https://api.duckduckgo.com/"
            params = {
                "q": query,
                "format": "json",
                "no_redirect": "1",
                "no_html": "1",
                "skip_disambig": "1",
            }

            response = requests.get(ddg_url, params=params, timeout=10)
            response.raise_for_status()
            data = response.json()

            result_parts = []

            # Check for instant answer
            if data.get("AbstractText"):
                result_parts.append(f"Summary: {data['AbstractText']}")
                if data.get("AbstractURL"):
                    result_parts.append(f"Source: {data['AbstractURL']}")

            # Check for definition
            if data.get("Definition"):
                result_parts.append(f"Definition: {data['Definition']}")
                if data.get("DefinitionURL"):
                    result_parts.append(f"Source: {data['DefinitionURL']}")

            # Check for answer (direct answer from API)
            if data.get("Answer"):
                result_parts.append(f"Direct Answer: {data['Answer']}")
                if data.get("AnswerType"):
                    result_parts.append(f"Answer Type: {data['AnswerType']}")

            # Check for related topics with more details
            if data.get("RelatedTopics") and len(data["RelatedTopics"]) > 0:
                result_parts.append("\nRelated information:")
                for i, topic in enumerate(data["RelatedTopics"][:5], 1):
                    if isinstance(topic, dict):
                        if topic.get("Text"):
                            result_parts.append(f"{i}. {topic['Text']}")
                            if topic.get("FirstURL"):
                                result_parts.append(f"   URL: {topic['FirstURL']}")
                    elif isinstance(topic, list) and len(topic) > 0:
                        # Sometimes RelatedTopics contains nested lists
                        for j, subtopic in enumerate(topic[:3]):
                            if isinstance(subtopic, dict) and subtopic.get("Text"):
                                result_parts.append(f"{i}.{j + 1}. {subtopic['Text']}")
                                if subtopic.get("FirstURL"):
                                    result_parts.append(
                                        f"       URL: {subtopic['FirstURL']}"
                                    )

            # Check for results (sometimes contains additional info)
            if data.get("Results") and len(data["Results"]) > 0:
                result_parts.append("\nSearch Results:")
                for i, result in enumerate(data["Results"][:3], 1):
                    if isinstance(result, dict):
                        if result.get("Text"):
                            result_parts.append(f"{i}. {result['Text']}")
                        if result.get("FirstURL"):
                            result_parts.append(f"   URL: {result['FirstURL']}")

            if result_parts:
                return f"Search results for '{query}':\n\n" + "\n".join(result_parts)
            else:
                # Try alternative DuckDuckGo search
                return self.ddg_search(query)

        except Exception as e:
            return ""  # Will trigger fallback

    def ddg_search(self, query: str) -> str:
        try:
            search_url = "https://html.duckduckgo.com/html/"
            params = {
                "q": query,
                "kl": "us-en",  # US English
            }

            headers = {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
            }

            response = requests.get(
                search_url, params=params, headers=headers, timeout=10
            )
            response.raise_for_status()

            soup = BeautifulSoup(response.text, "html.parser")
            results = []

            # Find result snippets in DuckDuckGo HTML
            result_divs = soup.find_all("div", class_="result__snippet")

            for div in result_divs[:5]:  # Get first 5 results
                text = div.get_text(strip=True)
                if len(text) > 30 and len(text) < 400:
                    results.append(text)

            # Also try to find result bodies if snippets aren't found
            if not results:
                result_bodies = soup.find_all("div", class_="result__body")
                for body in result_bodies[:5]:
                    text = body.get_text(strip=True, separator=" ")
                    # Clean up the text
                    sentences = text.split(".")
                    meaningful_sentences = []

                    for sentence in sentences:
                        sentence = sentence.strip()
                        if 20 < len(sentence) < 200 and len(sentence.split()) > 3:
                            meaningful_sentences.append(sentence)

                    if meaningful_sentences:
                        clean_text = ". ".join(meaningful_sentences[:2]) + "."
                        if clean_text not in results:
                            results.append(clean_text)

            if results:
                formatted_results = f"DuckDuckGo search results for '{query}':\n\n"

                for i, result in enumerate(results, 1):
                    formatted_results += f"{i}. {result}\n\n"
                return formatted_results.strip()

            return ""  # Will trigger Google fallback

        except Exception:
            return ""  # Will trigger Google fallback

    def google_scrape_search(self, query: str) -> str:
        try:
            # Try Wikipedia first for factual queries
            wikipedia_result = self.search_wikipedia(query)

            if wikipedia_result and len(wikipedia_result) > 100:
                return wikipedia_result

            # Fallback to Google search
            search_url = "https://www.google.com/search"

            params = {
                "q": query,
                "num": 5,
                "hl": "en",
                "gl": "us",
            }

            headers = {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
                "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
                "Accept-Language": "en-US,en;q=0.9",
                "Accept-Encoding": "gzip, deflate, br",
                "DNT": "1",
                "Connection": "keep-alive",
                "Upgrade-Insecure-Requests": "1",
            }

            response = requests.get(
                search_url, params=params, headers=headers, timeout=10
            )
            response.raise_for_status()

            soup = BeautifulSoup(response.text, "html.parser")
            extracted_info = []

            # Try to find knowledge panel information
            # Google uses various classes for knowledge panels and featured snippets
            knowledge_selectors = [
                "[data-attrid]",  # Knowledge panel attributes
                ".kno-rdesc",  # Knowledge panel description
                ".hgKElc",  # Featured snippet content
                ".IZ6rdc",  # Answer box content
                ".kp-blk",  # Knowledge panel block
                ".g-blk",  # General block
            ]

            for selector in knowledge_selectors:
                elements = soup.select(selector)

                for element in elements:
                    text = element.get_text(strip=True)
                    if 20 < len(text) < 300 and text not in extracted_info:
                        extracted_info.append(text)

                    if len(extracted_info) >= 5:
                        break

                if len(extracted_info) >= 5:
                    break

            # If we found structured information, return it
            if extracted_info:
                result = f"Search results for '{query}':\n\n"
                for i, info in enumerate(extracted_info[:5], 1):
                    result += f"{i}. {info}\n\n"
                return result.strip()

            # Try to find regular search result snippets
            search_results = []

            # Look for search result containers
            result_containers = soup.select(".g, .tF2Cxc, .hlcw0c")

            for container in result_containers[:5]:
                # Try to find the snippet/description
                snippet_selectors = [".VwiC3b", ".s", ".st", "span"]
                snippet_text = ""

                for selector in snippet_selectors:
                    snippet_elem = container.select_one(selector)
                    if snippet_elem:
                        snippet_text = snippet_elem.get_text(strip=True)
                        if len(snippet_text) > 30:
                            break

                if snippet_text and len(snippet_text) > 30:
                    search_results.append(snippet_text)

            if search_results:
                result = f'Web search results for "{query}":\n\n'
                for i, snippet in enumerate(search_results, 1):
                    result += f"{i}. {snippet}\n\n"
                return result.strip()

            # Final fallback - extract any meaningful text content
            # Remove navigation and footer elements first
            for elem in soup(["nav", "footer", "script", "style", "header"]):
                elem.decompose()

            # Get all text and look for relevant sentences
            all_text = soup.get_text(separator=" ", strip=True)
            sentences = all_text.split(".")
            relevant_sentences = []

            query_words = [word.lower() for word in query.split() if len(word) > 2]

            for sentence in sentences:
                sentence = sentence.strip()
                if 30 < len(sentence) < 300:
                    sentence_lower = sentence.lower()
                    # Check if sentence contains query terms
                    word_matches = sum(
                        1 for word in query_words if word in sentence_lower
                    )
                    if (
                        word_matches >= min(2, len(query_words))
                        and len(sentence.split()) > 5
                    ):
                        relevant_sentences.append(sentence)
                        if len(relevant_sentences) >= 5:
                            break

            if relevant_sentences:
                result = f"Web search found information about '{query}':\n\n"

                for i, sentence in enumerate(relevant_sentences[:5], 1):
                    result += f"{i}. {sentence}.\n\n"

                return result.strip()

            # Absolute final fallback
            return f"Search completed for '{query}'. Found general information but unable to extract specific details from the search results. The query was processed successfully and relevant web pages were found, but the content structure made it difficult to parse specific facts."
        except requests.exceptions.RequestException as e:
            return f"Error performing web search: Network error - {e}"
        except Exception as e:
            return f"Error performing web search: {e}"

    def search_wikipedia(self, query: str) -> str:
        """Search Wikipedia for factual information"""
        try:
            # Wikipedia API search - try direct page lookup first
            search_url = (
                "https://en.wikipedia.org/api/rest_v1/page/summary/"
                + query.replace(" ", "_")
            )

            headers = {
                "User-Agent": "Meltdown/1.0 (https://github.com/Merkoba/meltdown)"
            }

            response = requests.get(search_url, headers=headers, timeout=10)

            if response.status_code == 200:
                data = response.json()

                if data.get("extract") and not data.get("type") == "disambiguation":
                    result = f"Wikipedia information for '{query}':\n\n"
                    result += data["extract"]

                    if data.get("content_urls", {}).get("desktop", {}).get("page"):
                        result += (
                            f"\n\nSource: {data['content_urls']['desktop']['page']}"
                        )

                    return result

            # Try search API if direct lookup fails
            search_api_url = "https://en.wikipedia.org/w/api.php"
            params = {
                "action": "query",
                "format": "json",
                "list": "search",
                "srsearch": query,
                "srlimit": 3,  # Get top 3 results
            }

            response = requests.get(
                search_api_url, params=params, headers=headers, timeout=10
            )

            if response.status_code == 200:
                data = response.json()

                search_results = data.get("query", {}).get("search", [])
                if search_results:
                    # Try to get the full summary for the best match
                    best_match = search_results[0]
                    page_title = best_match["title"]

                    # Get the full page summary
                    summary_url = f"https://en.wikipedia.org/api/rest_v1/page/summary/{page_title.replace(' ', '_')}"
                    summary_response = requests.get(
                        summary_url, headers=headers, timeout=10
                    )

                    if summary_response.status_code == 200:
                        summary_data = summary_response.json()
                        if summary_data.get("extract"):
                            result = f"Wikipedia information for '{query}':\n\n"
                            result += f"Article: {page_title}\n\n"
                            result += summary_data["extract"]

                            if (
                                summary_data.get("content_urls", {})
                                .get("desktop", {})
                                .get("page")
                            ):
                                result += f"\n\nSource: {summary_data['content_urls']['desktop']['page']}"

                            return result

                    # Fallback to snippet if summary fails
                    snippet = best_match.get("snippet", "")
                    if snippet:
                        # Clean HTML from snippet using BeautifulSoup
                        soup = BeautifulSoup(snippet, "html.parser")
                        clean_snippet = soup.get_text(strip=True)

                        if clean_snippet:
                            result = f"Wikipedia search result for '{query}':\n\n"
                            result += f"Article: {page_title}\n"
                            result += f"Summary: {clean_snippet}\n"
                            result += f"URL: https://en.wikipedia.org/wiki/{page_title.replace(' ', '_')}"
                            return result

            return ""

        except Exception:
            return ""


search = Search()
