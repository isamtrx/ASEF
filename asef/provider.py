"""LLM provider abstraction.

Supports two backends:
- ``anthropic`` (default): uses ``ANTHROPIC_API_KEY`` and the Anthropic SDK.
- ``github``: uses ``GITHUB_TOKEN`` and the GitHub Models inference endpoint
  (OpenAI-compatible at https://models.inference.ai.azure.com).

Set ``ASEF_PROVIDER=github`` to switch backends.
"""

from __future__ import annotations

import json
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import Any

# ---------------------------------------------------------------------------
# Data classes (provider-agnostic)
# ---------------------------------------------------------------------------


@dataclass
class ToolCall:
    """A tool invocation requested by the model."""

    tool_id: str
    name: str
    input: dict[str, Any]


@dataclass
class LLMResponse:
    """Normalized response returned by any provider."""

    text: str
    tool_calls: list[ToolCall]
    tokens_in: int
    tokens_out: int
    _raw: Any = field(repr=False, default=None)  # provider-specific raw value


# ---------------------------------------------------------------------------
# Abstract base
# ---------------------------------------------------------------------------


class LLMProvider(ABC):
    """Abstract LLM backend.

    Implementations must keep the *messages* list in their own native format.
    The agent loop only calls the three abstract methods below and never
    inspects message internals directly.
    """

    @abstractmethod
    def complete(
        self,
        model: str,
        system: str,
        messages: list[dict[str, Any]],
        tools: list[dict[str, Any]],
        max_tokens: int = 4096,
    ) -> LLMResponse:
        """Send a completion request and return a normalized response."""

    @abstractmethod
    def append_assistant(
        self,
        messages: list[dict[str, Any]],
        response: LLMResponse,
    ) -> None:
        """Append the assistant turn to *messages* in provider-native format."""

    @abstractmethod
    def append_tool_results(
        self,
        messages: list[dict[str, Any]],
        results: list[dict[str, Any]],
    ) -> None:
        """Append tool results to *messages*.

        Each entry in *results* is a dict with keys:
        - ``tool_id``: the tool call id
        - ``content``: the string result
        - ``is_error``: bool
        """


# ---------------------------------------------------------------------------
# Anthropic implementation
# ---------------------------------------------------------------------------


class AnthropicProvider(LLMProvider):
    """Anthropic Messages API backend."""

    def __init__(self, api_key: str) -> None:
        from anthropic import Anthropic

        self._client = Anthropic(api_key=api_key)

    def complete(
        self,
        model: str,
        system: str,
        messages: list[dict[str, Any]],
        tools: list[dict[str, Any]],
        max_tokens: int = 4096,
    ) -> LLMResponse:
        resp = self._client.messages.create(
            model=model,
            max_tokens=max_tokens,
            system=system,
            tools=tools,
            messages=messages,
        )
        text = "\n".join(b.text for b in resp.content if b.type == "text").strip()
        calls = [
            ToolCall(tool_id=b.id, name=b.name, input=b.input)
            for b in resp.content
            if b.type == "tool_use"
        ]
        return LLMResponse(
            text=text,
            tool_calls=calls,
            tokens_in=resp.usage.input_tokens,
            tokens_out=resp.usage.output_tokens,
            _raw=resp.content,
        )

    def append_assistant(self, messages: list[dict[str, Any]], response: LLMResponse) -> None:
        messages.append({"role": "assistant", "content": response._raw})

    def append_tool_results(
        self, messages: list[dict[str, Any]], results: list[dict[str, Any]]
    ) -> None:
        messages.append(
            {
                "role": "user",
                "content": [
                    {
                        "type": "tool_result",
                        "tool_use_id": r["tool_id"],
                        "content": r["content"],
                        "is_error": r["is_error"],
                    }
                    for r in results
                ],
            }
        )


# ---------------------------------------------------------------------------
# GitHub Models implementation
# ---------------------------------------------------------------------------


class GitHubModelsProvider(LLMProvider):
    """GitHub Models via the OpenAI-compatible inference endpoint.

    Authenticates with a ``GITHUB_TOKEN`` (personal access token or
    GitHub Actions ``GITHUB_TOKEN`` secret). Does NOT require an
    Anthropic API key.
    """

    DEFAULT_ENDPOINT = "https://models.inference.ai.azure.com"

    def __init__(self, github_token: str, endpoint: str = "") -> None:
        from openai import OpenAI

        self._client = OpenAI(
            base_url=endpoint or self.DEFAULT_ENDPOINT,
            api_key=github_token,
        )

    def complete(
        self,
        model: str,
        system: str,
        messages: list[dict[str, Any]],
        tools: list[dict[str, Any]],
        max_tokens: int = 4096,
    ) -> LLMResponse:
        # Messages are already in OpenAI format; prepend system message.
        oai_messages = [{"role": "system", "content": system}] + messages
        kwargs: dict[str, Any] = {
            "model": model,
            "messages": oai_messages,
            "max_tokens": max_tokens,
        }
        if tools:
            kwargs["tools"] = _to_openai_tools(tools)
            kwargs["tool_choice"] = "auto"

        resp = self._client.chat.completions.create(**kwargs)
        choice = resp.choices[0]
        msg = choice.message
        text = msg.content or ""
        calls: list[ToolCall] = []
        if msg.tool_calls:
            for tc in msg.tool_calls:
                calls.append(
                    ToolCall(
                        tool_id=tc.id,
                        name=tc.function.name,
                        input=json.loads(tc.function.arguments),
                    )
                )
        usage = resp.usage
        return LLMResponse(
            text=text,
            tool_calls=calls,
            tokens_in=usage.prompt_tokens if usage else 0,
            tokens_out=usage.completion_tokens if usage else 0,
            _raw=msg,
        )

    def append_assistant(self, messages: list[dict[str, Any]], response: LLMResponse) -> None:
        msg = response._raw
        entry: dict[str, Any] = {"role": "assistant", "content": msg.content}
        if msg.tool_calls:
            entry["tool_calls"] = [
                {
                    "id": tc.id,
                    "type": tc.type,
                    "function": {
                        "name": tc.function.name,
                        "arguments": tc.function.arguments,
                    },
                }
                for tc in msg.tool_calls
            ]
        messages.append(entry)

    def append_tool_results(
        self, messages: list[dict[str, Any]], results: list[dict[str, Any]]
    ) -> None:
        for r in results:
            messages.append(
                {
                    "role": "tool",
                    "tool_call_id": r["tool_id"],
                    "content": r["content"],
                }
            )


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def _to_openai_tools(tools: list[dict[str, Any]]) -> list[dict[str, Any]]:
    """Convert Anthropic tool schema format to OpenAI function-calling format."""
    return [
        {
            "type": "function",
            "function": {
                "name": t["name"],
                "description": t.get("description", ""),
                "parameters": t.get("input_schema", {}),
            },
        }
        for t in tools
    ]


def make_provider(config: Any) -> LLMProvider:
    """Factory: instantiate the provider configured in *config*."""
    if config.provider == "github":
        if not config.github_token:
            raise RuntimeError(
                "GITHUB_TOKEN is not set. Export it in your shell or add it "
                "to .env when using ASEF_PROVIDER=github."
            )
        return GitHubModelsProvider(config.github_token, config.github_models_endpoint)

    # Default: Anthropic
    if not config.anthropic_api_key:
        raise RuntimeError(
            "ANTHROPIC_API_KEY is not set. Copy .env.example to .env and fill "
            "in your key, or export it in your shell. "
            "Alternatively set ASEF_PROVIDER=github and GITHUB_TOKEN."
        )
    return AnthropicProvider(config.anthropic_api_key)
