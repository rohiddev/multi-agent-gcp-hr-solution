import pytest
from retrieval import retrieve


class TestRetrieveStub:
    def test_retrieve_returns_results_for_hr_query(self):
        results = retrieve("How many PTO days do I have?", top_k=3)
        assert isinstance(results, list)
        assert len(results) <= 3
        for r in results:
            assert "content" in r
            assert "source" in r
            assert "score" in r

    def test_retrieve_honors_source_filter(self):
        results = retrieve("PTO", top_k=5, allowed_sources=["benefits"])
        # The stub keyword matcher may still match "PTO" in content, but if
        # allowed_sources is applied, it filters to only benefits docs.
        for r in results:
            assert "benefits" in r["source"]

    def test_retrieve_empty_query_returns_empty_or_stub(self):
        results = retrieve("", top_k=5)
        assert isinstance(results, list)

    def test_retrieve_top_k_limit(self):
        results = retrieve("policy", top_k=2)
        assert len(results) <= 2
