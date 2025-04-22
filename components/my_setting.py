import dis
from gc import enable
from fastapi import Query
import modelscope_studio.components.antd as antd
import modelscope_studio.components.base as ms
import gradio as gr
from config import max_mcp_server_count


def McpServersModal(data_source: list[dict]):
    mcp_servers_state = gr.State({"data_source": data_source})
    with antd.Modal(
        # open=open,
        width=420,
        footer=False,
        centered=True,
        styles=dict(footer=dict(display="none")),
    ) as mcp_servers_modal:
        with ms.Slot("title"):
            with antd.Flex(gap="small", align="center"):
                ms.Text("MCP Servers")
                mcp_servers_switch = antd.Switch(True)
                antd.Typography.Text(
                    f"最大 MCP Server 连接数：{max_mcp_server_count}",
                    type="secondary",
                    elem_style=dict(fontSize=12, fontWeight="normal"),
                )
        with antd.List(
            data_source=data_source, pagination=dict(pageSize=10, hideOnSinglePage=True)
        ) as mcp_servers_list:
            with ms.Slot(
                "renderItem",
                params_mapping="(item) => ({ text: { value: item.name, disabled: item.disabled }, tag: { style: { display: item.internal ? undefined: 'none' } }, switch: { value: item.enabled, mcp: item.name, disabled: item.disabled }})",
            ):
                with antd.List.Item():
                    with antd.Flex(
                        justify="space-between", elem_style=dict(width="100%")
                    ):
                        with antd.Flex(gap="small"):
                            antd.Typography.Text(as_item="text")
                            antd.Tag("官方示例", color="green", as_item="tag")
                        mcp_server_switch = antd.Switch(as_item="switch")

    def change_mcp_servers_switch(mcp_servers_switch_value, state_value):
        state_value["data_source"] = [
            {**item, "disabled": not mcp_servers_switch_value}
            for item in state_value["data_source"]
        ]
        return gr.update(value=state_value)

    mcp_servers_switch.change(
        change_mcp_servers_switch,
        inputs=[mcp_servers_switch, mcp_servers_state],
        outputs=[mcp_servers_state],
    )

    def change_mcp_server_switch(state_value, e: gr.EventData):
        mpc = e._data["component"]["mcp"]
        enable = e._data["payload"][0]
        state_value["data_source"] = [
            {**item, "enabled": enable} if item["name"] == mpc else item
            for item in state_value["data_source"]
        ]
        return gr.update(value=state_value)

    mcp_server_switch.change(
        change_mcp_server_switch,
        inputs=[mcp_servers_state],
        outputs=[mcp_servers_state],
    )

    def apply_state_change(state_value):
        print("apply_state_change", state_value)
        disabled_tool_use = False
        enabled_server_count = 0
        for item in state_value["data_source"]:
            if item.get("enabled"):
                if enabled_server_count >= max_mcp_server_count:
                    item["enabled"] = False
                else:
                    enabled_server_count += 1
                    if item.get("disabled"):
                        disabled_tool_use = True
                    else:
                        has_tool_use = True
        if not disabled_tool_use:
            for item in state_value["data_source"]:
                if enabled_server_count >= max_mcp_server_count:
                    item["enabled"] = not item.get("enabled", False)
                else:
                    item["disabled"] = False
        return (
            gr.update(
                data_source=state_value["data_source"],
                footer=(
                    "没有可用的 MCP Server"
                    if len(state_value["data_source"]) == 0
                    else ""
                ),
            ),
            gr.update(value=not disabled_tool_use),
            gr.update(value=state_value),
        )

    mcp_servers_state.change(
        apply_state_change,
        inputs=[mcp_servers_state],
        outputs=[mcp_servers_list, mcp_servers_switch, mcp_servers_state],
    )
    mcp_servers_modal.cancel(
        fn=lambda: gr.update(open=False), outputs=[mcp_servers_modal]
    )

    return mcp_servers_modal, mcp_servers_state


# 我的设置
def mySetting():
    with antd.Modal(
        width=600,
        footer=False,
        centered=True,
        styles=dict(footer=dict(display="none")),
    ) as my_setting_modal:
        with ms.Slot("title"):
            with antd.Flex(gap="small", align="center"):
                ms.Text("我的设置")
        with antd.Tabs(default_active_key="personal_center") as my_setting_tabs:
            with antd.Tabs.Pane(title="个人中心", key="personal_center"):
                ms.Text("个人中心")
            with antd.Tabs.Pane(title="模型配置", key="mcp_servers"):
                ms.Text("模型配置")
            with antd.Tabs.Pane(title="MCP服务设置", key="mcp_servers"):
                ms.Text("MCP Servers")
