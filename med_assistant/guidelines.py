"""
Clinical Practice Guidelines Query & Navigation Engine for MD Medicine Specialists.
Structures and queries international evidence-based guidelines across Cardiology, Nephrology,
Critical Care, and Pulmonology.
"""

from typing import Dict, Any, List, Optional
from med_assistant.mock_data import GUIDELINES_DATA

class GuidelineEngine:
    """Specialist clinical guideline knowledge retrieval and structuring engine."""

    def __init__(self, guidelines_data: Optional[List[Dict[str, Any]]] = None):
        self.guidelines = guidelines_data if guidelines_data is not None else GUIDELINES_DATA

    def get_all_guidelines(self) -> List[Dict[str, Any]]:
        """Returns all structured guidelines."""
        return self.guidelines

    def filter_by_specialty(self, specialty: str) -> List[Dict[str, Any]]:
        """Filters guidelines by clinical specialty."""
        if not specialty or specialty.lower() == "all":
            return self.guidelines
        spec_lower = specialty.lower()
        return [g for g in self.guidelines if spec_lower in g.get("specialty", "").lower()]

    def search_guidelines(self, query: str) -> List[Dict[str, Any]]:
        """
        Searches guidelines across title, society, drug classes, recommendations, and clinical pearls.
        """
        if not query or not query.strip():
            return self.guidelines

        q = query.lower().strip()
        results = []

        for g in self.guidelines:
            # Check top-level fields
            if (q in g.get("name", "").lower() or
                q in g.get("specialty", "").lower() or
                q in g.get("society", "").lower() or
                q in g.get("device_therapy", "").lower()):
                results.append(g)
                continue

            # Check individual pillars
            pillar_match = False
            for p in g.get("pillars", []):
                if (q in p.get("drug_class", "").lower() or
                    q in p.get("recommendation", "").lower() or
                    q in p.get("starting_dose", "").lower() or
                    q in p.get("target_dose", "").lower() or
                    q in p.get("pearls", "").lower()):
                    pillar_match = True
                    break
            
            if pillar_match:
                results.append(g)

        return results

    def get_guideline_by_id(self, guideline_id: str) -> Optional[Dict[str, Any]]:
        """Retrieves a specific guideline by its unique ID."""
        for g in self.guidelines:
            if g.get("id") == guideline_id:
                return g
        return None

    def get_specialties(self) -> List[str]:
        """Returns distinct list of represented medical specialties."""
        return sorted(list(set(g["specialty"] for g in self.guidelines if "specialty" in g)))
