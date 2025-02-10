import requests
from bs4 import BeautifulSoup
from dataclasses import dataclass

def flaky(e: BeautifulSoup):
    return e.text if e else ''

@dataclass(frozen=True)
class OllamaSearchResult:
    model_name: str
    desc: str
    model_sizes: list[str]
    pull_count: str
    capability: str
    link: str

    def display(self) -> tuple:
        return (
            self.model_name,
            f'{self.desc[:120]}...' if len(self.desc) > 120 else self.desc,
            ','.join(self.model_sizes),
            self.pull_count,
            self.capability,
        )

class OllamaSearchClient:
    def __init__(self):
        self._base_url = 'https://ollama.com/search'
    
    def search(self, q: str):
        results = []
        response = requests.get(self._base_url, params={'q': q})
        response.raise_for_status()

        soup = BeautifulSoup(response.text, 'html.parser')
        search_resutls = soup.select('#searchresults > ul > li')
        if search_resutls:
            for result in search_resutls:
                link = result.find_next('a')['href'] or ''
                model_name = flaky(result.find('span', { 'x-test-search-response-title': '' }))
                desc = flaky(result.find('p'))
                capability = flaky(result.find('span', { 'x-test-capability': '' }))
                model_sizes = [ flaky(span) for span in result.find_all('span', { 'x-test-size': '' }) ]
                pull_count = flaky(result.find('span', {'x-test-pull-count': ''}))

                results.append(OllamaSearchResult(
                    desc=desc,
                    link=link,
                    capability=capability,
                    model_name=model_name,
                    model_sizes=model_sizes,
                    pull_count=pull_count
                ))
        return results


if __name__ == '__main__':
    client = OllamaSearchClient()
    search = client.search('llama')

    for node in search:
        print(node)