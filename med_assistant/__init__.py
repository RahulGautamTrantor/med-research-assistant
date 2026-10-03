"""
Medical Research Assistant - Specialist Clinical Intelligence Engine for MD Medicine.
"""

from med_assistant.case_processor import CaseStudyProcessor
from med_assistant.paper_summarizer import PaperSummarizer
from med_assistant.guidelines import GuidelineEngine
from med_assistant.mock_data import SAMPLE_CASES, SAMPLE_PAPERS, GUIDELINES_DATA

__version__ = "1.0.0"

__all__ = [
    "CaseStudyProcessor",
    "PaperSummarizer",
    "GuidelineEngine",
    "SAMPLE_CASES",
    "SAMPLE_PAPERS",
    "GUIDELINES_DATA"
]
