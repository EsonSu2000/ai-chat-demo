from json import load
import time
import gradio as gr
import modelscope_studio.components.base as ms
import modelscope_studio.components.antd as antd
import modelscope_studio.components.pro as pro
import modelscope_studio.components.antdx as antdx
from components.my_setting import McpServersModal

from config import (
    primary_color,
    default_locale,
    default_theme,
    default_mcp_config,
    default_mcp_prompts,
    default_mcp_servers,
    bot_config,
    welcome_config,
)


def lighten_color(hex_color, factor=0.2):
    hex_color = hex_color.lstrip("#")

    # 解析RGB值
    r = int(hex_color[0:2], 16)
    g = int(hex_color[2:4], 16)
    b = int(hex_color[4:6], 16)

    # 向白色方向调整
    r = min(255, r + int((255 - r) * factor))
    g = min(255, g + int((255 - g) * factor))
    b = min(255, b + int((255 - b) * factor))

    # 转回十六进制
    return f"{r:02x}{g:02x}{b:02x}"


lighten_primary_color = lighten_color(primary_color, 0.4)
css = f"""
.user-message-content {{
    background-color: #{lighten_primary_color};
}}

"""
conversation_list = [
    {"key": f"item_{1}", "label": "新会话", "group": "今天"},
    {"key": f"item_{2}", "label": "会话j11112", "group": "今天"},
    {"key": f"item_{3}", "label": "会话z2132323", "group": "昨天"},
    {"key": f"item_{4}", "label": "会话z2132323333", "group": "昨天"},
    {"key": f"item_{5}", "label": "会话z2132323333", "group": "昨天"},
    {"key": f"item_{6}", "label": "会话z2132323333", "group": "昨天"},
    {"key": f"item_{7}", "label": "会话z2132323333", "group": "昨天"},
    {"key": f"item_{8}", "label": "会话z2132323333", "group": "昨天"},
    {"key": f"item_{9}", "label": "会话z2132323333", "group": "昨天"},
    {"key": f"item_{10}", "label": "会话z2132323333", "group": "昨天"},
    {"key": f"item_{11}", "label": "会话z2132323333", "group": "昨天"},
    {"key": f"item_{12}", "label": "会话z2132323333", "group": "昨天"},
    {"key": f"item_{13}", "label": "会话z2132323333", "group": "昨天"},
    {"key": f"item_{14}", "label": "会话z2132323333", "group": "昨天"},
    {"key": f"item_{15}", "label": "会话z2132323333", "group": "上周"},
    {"key": f"item_{16}", "label": "会话z2132323333", "group": "上周"},
    {"key": f"item_{17}", "label": "会话z2132323333", "group": "上周"},
    {"key": f"item_{18}", "label": "会话z2132323333", "group": "上周"},
    {"key": f"item_{19}", "label": "会话z2132323333", "group": "上周"},
]
active_conversation_key = conversation_list[0]["key"]


def new_chat_fn():
    print("新增会话")


def conversation_item_fn(e: gr.EventData):
    print("点击单个历史会话", e._data["payload"])


# 选择欢迎语句
def select_welcome_prompt(e: gr.EventData):
    print("选择欢迎语", e._data["payload"])
    return gr.update(value=e._data["payload"][0]["value"]["description"])


def chat_fn(message):  # chatbot, input, send_btn, input
    print("xxx", message)
    yield [], gr.update(value="", loading=True), gr.update(loading=True)
    time.sleep(2)
    yield [
        {
            "role": "assistant",
            "content": "你好，我是 MCP 助手，请问有什么可以帮助你的吗？",
        }
    ], gr.update(value="", loading=False), gr.update(loading=False)


def save_mcp_servers(mcp_servers_btn_value, browser_state_value):
    browser_state_value["mcp_servers"] = mcp_servers_btn_value["data_source"]
    return gr.update(value=browser_state_value)


with gr.Blocks(
    css=css, css_paths="./assets/css/app.css", fill_width=True, fill_height=True
) as demo:
    browser_state = gr.BrowserState(
        {
            "mcp_config": default_mcp_config,
            "mcp_prompts": default_mcp_prompts,
            "mcp_servers": default_mcp_servers,
        },
        storage_key="mcp_config",
    )

    with ms.Application(), antdx.XProvider(locale=default_locale), ms.AutoLoading():
        mcp_servers_modal, mcp_servers_state = McpServersModal(
            data_source=default_mcp_servers
        )
        with antd.Layout(elem_style=dict(height="98vh")):
            with antd.LayoutSider(
                width=230,
                theme="light",
                elem_style=dict(paddingLeft="10px", height="100%"),
            ):
                with antd.Flex(
                    vertical=True, gap="middle", elem_style=dict(height="100%")
                ):
                    with ms.Div(
                        elem_style=dict(
                            flex=0,
                            height="60px",
                            padding=" 10px 0 0 0",
                            marginBottom="-10px",
                            textAlign="center",
                        ),
                    ):
                        with antd.Button(
                            "新增会话",
                            type="primary",
                            elem_style=dict(display="inline-block"),
                        ) as new_chat_btn:
                            with ms.Slot("icon"):
                                antd.Icon("PlusSquareOutlined")
                            # 新增会话 按钮点击事件
                            new_chat_btn.click(new_chat_fn)
                    with ms.Div(
                        elem_style=dict(flex=1, height="260px", overflow="auto"),
                        elem_classes=["conversation-list"],
                    ):
                        with antdx.Conversations(
                            default_active_key="item_1", groupable=True
                        ) as Conversations_btn:
                            for conversation in conversation_list:
                                antdx.ConversationsItem(
                                    label=conversation["label"],
                                    key=conversation["key"],
                                    group=conversation["group"],
                                )
                            Conversations_btn.active_change(conversation_item_fn)
                    with ms.Div(
                        elem_style=dict(
                            flex=0,
                            paddingRight="10px",
                            cursor="pointer",
                        ),
                    ):
                        with antd.Flex(
                            justify="space-between",
                            align="center",
                            gap="small",
                        ):
                            with antd.Flex(align="center"):
                                with antd.Avatar(
                                    size=50,
                                    elem_style=dict(marginRight="5px", flex="none"),
                                ):
                                    with ms.Slot("src"):
                                        antd.Image(
                                            "./assets/modelscope-mcp.png",
                                            preview=False,
                                            # width=80,
                                            # height=80,
                                        )
                                ms.Text("eson Su", elem_style=dict(fontSize="18px"))
                            antd.Icon(
                                "RightOutlined",
                            )

            with antd.Layout(elem_style=dict(padding="0 15px")):
                with antd.LayoutContent():
                    with antd.Flex(
                        vertical=True,
                        gap="middle",
                        elem_style=dict(height=1000, maxHeight="98vh"),
                    ):
                        with antd.Card(
                            elem_style=dict(
                                flex=1, height=0, display="flex", flexDirection="column"
                            ),
                            styles=dict(
                                body=dict(
                                    flex=1,
                                    height=0,
                                    display="flex",
                                    flexDirection="column",
                                )
                            ),
                        ):
                            chatbot = pro.Chatbot(
                                height=0,
                                bot_config=bot_config(),
                                welcome_config=welcome_config(default_mcp_prompts),
                                elem_style=dict(flex=1),
                            )
                        with antdx.Sender(actions=False, submit_type="enter") as input:
                            with ms.Slot("footer"):
                                with antd.Flex(
                                    gap="small",
                                    align="start",
                                    vertical=False,
                                    justify="space-between",
                                ):
                                    with antd.Flex(gap="small", align="center"):
                                        ms.Text("联网搜索")
                                        antd.Switch(checked=False)
                                        antd.Divider(type="vertical")
                                        with antd.Button(
                                            "MCP配置",
                                            type="text",
                                        ) as setting_btn:
                                            with ms.Slot("icon"):
                                                antd.Icon("SettingOutlined")
                                    with antd.Flex(gap="small", align="center"):
                                        with antd.Button(
                                            "发送",
                                            type="primary",
                                            loading=False,
                                            elem_style=dict(display="inline-block"),
                                        ) as send_btn:
                                            with ms.Slot("icon"):
                                                antd.Icon("SendOutlined")
    send_btn.click(
        fn=chat_fn,
        inputs=[input],
        outputs=[chatbot, input, send_btn],
    )
    # 发送消息
    input.submit(
        fn=chat_fn,
        inputs=[input, mcp_servers_state, chatbot],
        outputs=[chatbot, input, send_btn],
    )
    # 选择欢迎语
    chatbot.welcome_prompt_select(
        fn=select_welcome_prompt, outputs=[input], queue=False
    )
    # 点击设置按钮
    setting_btn.click(
        fn=lambda: gr.update(open=True), outputs=[mcp_servers_modal], queue=False
    )
    # 保存 MCP Servers
    mcp_servers_state.change(
        save_mcp_servers,
        inputs=[mcp_servers_modal, browser_state],
        outputs=[browser_state],
    )

demo.launch(ssr_mode=True)
