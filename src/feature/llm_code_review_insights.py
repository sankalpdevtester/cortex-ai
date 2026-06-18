import re
from typing import Dict, List

class CodeReviewInsights:
    @staticmethod
    def generate_insights(review: str) -> Dict[str, List[str]]:
        insights = {
            'security_vulnerabilities': [],
            'performance_optimizations': [],
            'code_smells': [],
        }

        security_vulnerabilities = re.findall(r'Security vulnerability: (.*)', review)
        performance_optimizations = re.findall(r'Performance optimization: (.*)', review)
        code_smells = re.findall(r'Code smell: (.*)', review)

        insights['security_vulnerabilities'] = security_vulnerabilities
        insights['performance_optimizations'] = performance_optimizations
        insights['code_smells'] = code_smells

        return insights