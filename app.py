from typing import TypedDict, Annotated
from langchain_core.messages import BaseMessage, HumanMessage, SystemMessage
from langchain_openai import ChatOpenAI
from langgraph.graph import StateGraph, END
from dotenv import load_dotenv
import operator
import os

load_dotenv()

# ─────────────────────────────────────────
# 1. LLM Model
# ─────────────────────────────────────────
llm = ChatOpenAI(
    model="gpt-3.5-turbo",
    temperature=0,  # 0 = consistent, predictable responses
    api_key=os.getenv("OPENAI_API_KEY")
)

# ─────────────────────────────────────────
# 2. State Definition
# ─────────────────────────────────────────
class SupportState(TypedDict):
    messages: Annotated[list[BaseMessage], operator.add]
    should_escalate: bool
    issue_type: str
    user_tier: str  # "vip" or "standard"


# ─────────────────────────────────────────
# 3. Nodes
# ─────────────────────────────────────────
def check_user_tier_node(state: SupportState):
    """Uses LLM to classify if user is VIP or standard"""
    prompt = [
        SystemMessage(
            content=(
                "You are a customer service classifier. "
                "Classify the customer into exactly one tier: vip or standard. "
                "A customer is VIP if they mention: vip, premium, priority, executive, or platinum. "
                "Return only one word: vip or standard."
            )
        ),
        HumanMessage(content=state["messages"][0].content),
    ]
    response = llm.invoke(prompt)
    tier = response.content.strip().lower()

    # Safety check — if LLM returns something unexpected
    if tier not in ["vip", "standard"]:
        tier = "standard"

    return {"user_tier": tier}


def vip_agent_node(state: SupportState):
    """Handles VIP customers — fast lane, no escalation"""
    prompt = [
        SystemMessage(
            content=(
                "You are a premium VIP support agent with 10 years experience. "
                "Be extra helpful, concise and make the customer feel valued."
            )
        ),
    ] + state["messages"]

    response = llm.invoke(prompt)
    return {
        "messages": [response],
        "should_escalate": False,
    }


def standard_agent_node(state: SupportState):
    """Handles standard customers — may escalate"""
    prompt = [
        SystemMessage(
            content=(
                "You are a standard support agent. "
                "Be helpful and professional. "
                "If the issue seems complex, recommend escalation."
            )
        ),
    ] + state["messages"]

    response = llm.invoke(prompt)
    return {
        "messages": [response],
        "should_escalate": True,
    }


# ─────────────────────────────────────────
# 4. Routing Function
# ─────────────────────────────────────────
def route_by_tier(state: SupportState) -> str:
    """Decides which path to take based on user tier"""
    if state.get("user_tier") == "vip":
        return "vip_path"
    return "standard_path"


# ─────────────────────────────────────────
# 5. Build Graph
# ─────────────────────────────────────────
def build_graph():
    print("--Building Graph")
    workflow = StateGraph(SupportState)

    workflow.add_node("check_tier", check_user_tier_node)
    workflow.add_node("vip_agent", vip_agent_node)
    workflow.add_node("standard_agent", standard_agent_node)

    workflow.set_entry_point("check_tier")

    workflow.add_conditional_edges(
        "check_tier",
        route_by_tier,
        {
            "vip_path": "vip_agent",
            "standard_path": "standard_agent",
        },
    )

    workflow.add_edge("vip_agent", END)
    workflow.add_edge("standard_agent", END)

    return workflow.compile()


# ─────────────────────────────────────────
# 6. Main
# ─────────────────────────────────────────
def main() -> None:
    graph = build_graph()

    # VIP run
    print("─── VIP Run ───")
    vip_result = graph.invoke({
        "messages": [HumanMessage(content="I'm a premium customer, please check my order")],
        "should_escalate": False,
        "issue_type": "",
        "user_tier": "",
    })
    print(f"  user_tier:       {vip_result.get('user_tier')}")
    print(f"  should_escalate: {vip_result.get('should_escalate')}")
    print(f"  response:        {vip_result['messages'][-1].content}")

    print()

    # Standard run
    print("─── Standard Run ───")
    standard_result = graph.invoke({
        "messages": [HumanMessage(content="Check my order status")],
        "should_escalate": False,
        "issue_type": "",
        "user_tier": "",
    })
    print(f"  user_tier:       {standard_result.get('user_tier')}")
    print(f"  should_escalate: {standard_result.get('should_escalate')}")
    print(f"  response:        {standard_result['messages'][-1].content}")


if __name__ == "__main__":
    main()