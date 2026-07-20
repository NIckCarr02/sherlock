"""Base class for all OSINT integrations"""

from abc import ABC, abstractmethod
from typing import Dict, List, Any
import logging

logger = logging.getLogger(__name__)


class OSINTIntegration(ABC):
    """Abstract base class for OSINT tool integrations"""

    def __init__(self, name: str, config: Dict[str, Any] = None):
        """
        Initialize OSINT integration.
        
        Args:
            name: Integration tool name
            config: Configuration dictionary
        """
        self.name = name
        self.config = config or {}
        self.enabled = self.config.get('enabled', True)
        self.results = []

    @abstractmethod
    def search(self, query: str) -> Dict[str, Any]:
        """Execute search query.
        
        Args:
            query: Search query (username, email, domain, etc.)
            
        Returns:
            Standardized results dictionary
        """
        pass

    @abstractmethod
    def parse_results(self, raw_results: Any) -> Dict[str, Any]:
        """Parse and standardize results.
        
        Args:
            raw_results: Raw results from the tool
            
        Returns:
            Standardized results
        """
        pass

    def get_standardized_format(self) -> Dict[str, List]:
        """Return standardized result format."""
        return {
            'accounts': [],
            'emails': [],
            'domains': [],
            'social_media': [],
            'breaches': [],
            'metadata': {}
        }

    def log_result(self, result: Dict[str, Any]):
        """Log integration result."""
        logger.info(f"[{self.name}] Found results: {len(result.get('accounts', []))} accounts")
        self.results.append(result)

    def get_results(self) -> List[Dict[str, Any]]:
        """Get all accumulated results."""
        return self.results

    def clear_results(self):
        """Clear accumulated results."""
        self.results = []
