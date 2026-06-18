from src.utils.cache import Cache
from src.feature.llm_review_engine import LLMReviewEngine

class LLMCache:
    def __init__(self, cache: Cache):
        self.cache = cache
        self.llm_review_engine = LLMReviewEngine(cache)

    def get_review(self, code: str, language: str) -> str:
        review = self.cache.get(f"llm_review_{code}_{language}")
        if review is None:
            review = self.llm_review_engine.review_code(code, language)["review"]
            self.cache.set(f"llm_review_{code}_{language}", review)
        return review

    def get_tests(self, code: str, language: str) -> List[str]:
        tests = self.cache.get(f"llm_tests_{code}_{language}")
        if tests is None:
            tests = self.llm_review_engine.generate_tests(code, language)
            self.cache.set(f"llm_tests_{code}_{language}", tests)
        return tests

    def get_vulnerabilities(self, code: str, language: str) -> List[str]:
        vulnerabilities = self.cache.get(f"llm_vulnerabilities_{code}_{language}")
        if vulnerabilities is None:
            vulnerabilities = self.llm_review_engine.detect_vulnerabilities(code, language)
            self.cache.set(f"llm_vulnerabilities_{code}_{language}", vulnerabilities)
        return vulnerabilities

    def get_optimizations(self, code: str, language: str) -> List[str]:
        optimizations = self.cache.get(f"llm_optimizations_{code}_{language}")
        if optimizations is None:
            optimizations = self.llm_review_engine.suggest_optimizations(code, language)
            self.cache.set(f"llm_optimizations_{code}_{language}", optimizations)
        return optimizations

    def get_insights(self, code: str, language: str) -> Dict:
        insights = self.cache.get(f"llm_insights_{code}_{language}")
        if insights is None:
            insights = self.llm_review_engine.get_insights(code, language)
            self.cache.set(f"llm_insights_{code}_{language}", insights)
        return insights