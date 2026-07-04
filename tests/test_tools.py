"""Tests for agent tool schemas and client."""

from fastapi.testclient import TestClient

from starwatch.agent.tools import AGENT_TOOLS, StarwatchAgentClient
from starwatch.server.app import app


class TestAgentTools:
    def test_tool_count(self):
        assert len(AGENT_TOOLS) == 6

    def test_tool_names(self):
        names = {t["function"]["name"] for t in AGENT_TOOLS}
        assert names == {
            "telescope_status",
            "telescope_slew",
            "telescope_track",
            "telescope_park",
            "telescope_unpark",
            "telescope_abort",
        }

    def test_slew_schema_has_target(self):
        slew = next(t for t in AGENT_TOOLS if t["function"]["name"] == "telescope_slew")
        assert "target" in slew["function"]["parameters"]["properties"]


class TestAgentClient:
    def test_dispatch_status(self):
        with TestClient(app) as http:
            with StarwatchAgentClient(client=http) as agent:
                result = agent.dispatch("telescope_status", {})
                assert "connected" in result

    def test_dispatch_slew(self):
        with TestClient(app) as http:
            with StarwatchAgentClient(client=http) as agent:
                agent.dispatch("telescope_unpark", {})
                result = agent.dispatch("telescope_slew", {"target": "M45"})
                assert result["ok"] is True

    def test_unknown_tool(self):
        with StarwatchAgentClient() as agent:
            try:
                agent.dispatch("nonexistent_tool", {})
                raise AssertionError("should have raised")
            except ValueError as e:
                assert "Unknown tool" in str(e)