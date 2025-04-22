import json
from modelscope_studio.components.pro.chatbot import (
    ChatbotWelcomeConfig,
    ChatbotUserConfig,
    ChatbotBotConfig,
    ChatbotActionConfig,
)

primary_color = "#999999"

default_locale = "zh_CN"

default_theme = {
    "token": {
        "colorPrimary": primary_color,
    }
}
default_mcp_config = json.dumps({"mcpServers": {}}, indent=4, ensure_ascii=False)
# for internal
default_mcp_prompts = {
    # "arxiv": ["查找最新的5篇关于量子计算的论文并简要总结", "根据当前时间，找到近期关于大模型的论文，得到研究趋势"],
    "高德地图": [
        "北京今天天气怎么样",
        "基于今天的天气，帮我规划一条从北京到杭州的路线",
    ],
    "time": [
        "帮我查一下北京时间",
        "现在是北京时间 2025-04-01 12:00:00，对应的美西时间是多少？",
    ],
    "fetch": [
        "从中国新闻网获取最新的新闻",
        "获取 https://www.example.com 的内容，并提取为Markdown格式",
    ],
}
default_mcp_servers = [
    {"name": mcp_name, "enabled": True, "internal": True}
    for mcp_name in default_mcp_prompts.keys()
]


def bot_config(disabled_actions=None):
    return ChatbotBotConfig(
        actions=[
            "copy",
            "edit",
            ChatbotActionConfig(
                action="retry",
                popconfirm=dict(
                    title="重新生成消息",
                    description="重新生成消息会删除所有后续消息。",
                    okButtonProps=dict(danger=True),
                ),
            ),
            ChatbotActionConfig(
                action="delete",
                popconfirm=dict(
                    title="删除消息",
                    description="确认删除该消息?",
                    okButtonProps=dict(danger=True),
                ),
            ),
        ],
        disabled_actions=disabled_actions,
    )


def welcome_config(prompts: dict, loading=False):
    return ChatbotWelcomeConfig(
        icon="./assets/mcp.png",
        title="你好，我是智能聊天机器人",
        styles=dict(icon=dict(borderRadius="50%", overflow="hidden")),
        description="我可以帮你写代码、读文件、写作各种创意内容，请把你的任务交给我吧~",
        prompts=dict(
            title="用例生成中..." if loading else None,
            wrap=True,
            styles=dict(item=dict(flex="1 0 200px")),
            items=[
                {
                    "label": mcp_name,
                    "children": [{"description": prompt} for prompt in prompts],
                }
                for mcp_name, prompts in prompts.items()
            ],
        ),
    )
