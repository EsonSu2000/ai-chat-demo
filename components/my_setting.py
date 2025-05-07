import modelscope_studio.components.antd as antd
from modelscope_studio.components.antd.typography import title
import modelscope_studio.components.base as ms
import gradio as gr
from config import max_mcp_server_count
import uuid


def McpServersModal(data_source: list[dict]):
    mcp_servers_state = gr.State({"mcp_servers": data_source})
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
        state_value["mcp_servers"] = [
            {**item, "disabled": not mcp_servers_switch_value}
            for item in state_value["mcp_servers"]
        ]
        return gr.update(value=state_value)

    mcp_servers_switch.change(
        change_mcp_servers_switch,
        inputs=[mcp_servers_switch, mcp_servers_state],
        outputs=[mcp_servers_state],
    )

    def change_mcp_server_switch(state_value, e: gr.EventData):
        print("change_mcp_server_switch", state_value)
        mpc = e._data["component"]["mcp"]
        enable = e._data["payload"][0]
        state_value["mcp_servers"] = [
            {**item, "enabled": enable} if item["name"] == mpc else item
            for item in state_value["mcp_servers"]
        ]
        return gr.update(value=state_value)

    mcp_server_switch.change(
        change_mcp_server_switch,
        inputs=[mcp_servers_state],
        outputs=[mcp_servers_state],
    )

    def apply_state_change(state_value):
        print("++++apply_state_change", state_value)
        disabled_tool_use = False
        enabled_server_count = 0
        for item in state_value["mcp_servers"]:
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
            for item in state_value["mcp_servers"]:
                if enabled_server_count >= max_mcp_server_count:
                    item["enabled"] = not item.get("enabled", False)
                else:
                    item["disabled"] = False
        return (
            gr.update(
                data_source=state_value["mcp_servers"],
                footer=(
                    "没有可用的 MCP Server"
                    if len(state_value["mcp_servers"]) == 0
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

    return mcp_servers_modal, mcp_servers_state, mcp_servers_list, mcp_servers_switch


# 我的设置
def MySettingModal(setting_data: list[dict]):
    with antd.Modal(
        width=800,
        footer=False,
        centered=True,
        styles=dict(footer=dict(display="none")),
    ) as my_setting_modal:
        with ms.Slot("title"):
            with antd.Flex(gap="small", align="center"):
                ms.Text("我的设置")
        with antd.Tabs(default_active_key="personal_center") as my_setting_tabs:
            with antd.Tabs.Item(label="个人中心", key="personal_center"):
                ms.Text("个人中心")
            with antd.Tabs.Item(label="模型配置", key="model_setting"):
                my_setting_state, model_setting_list = ModelSetting(setting_data)
            with antd.Tabs.Item(label="MCP服务设置", key="mcp_servers"):
                ms.Text("MCP Servers")
    my_setting_modal.cancel(
        fn=lambda: gr.update(open=False), outputs=[my_setting_modal]
    )

    return my_setting_modal, my_setting_state, model_setting_list


# 模型配置
def ModelSetting(data_source: list[dict]):
    my_setting_state = gr.State({"model_list": data_source})
    with ms.Div(elem_classes=["model-setting-card"]):
        with antd.List(
            data_source=data_source,
            header="大模型列表",
            bordered=True,
            elem_classes="model-setting-list",
        ) as model_setting_list:
            with ms.Slot(
                "renderItem",
                params_mapping="(item) =>({ text:{value:item.name},token:{value:item.token? item.token.split('').splice(0, 8).join('')+'**************': ''}, api_url: {value:item.api_url}, switch:{value: item.enabled,  model:item} })",
            ):
                with antd.List.Item():
                    with antd.Flex(
                        justify="space-between",
                        align="center",
                        elem_style=dict(width="100%"),
                    ):
                        with antd.Flex(gap="small", align="flex-start", vertical=True):
                            antd.Typography.Text(
                                as_item="text", elem_style=dict(fontSize="16px")
                            )
                            antd.Typography.Text(as_item="token")
                        with antd.Flex(gap="small", align="center"):
                            edit_btn = antd.Button("编辑", type="link")
                            del_btn = antd.Button("删除", type="link")
                            switch_btn = antd.Switch(as_item="switch", size="small")
        with antd.Flex(justify="center", elem_style=dict(marginTop="40px")):
            with antd.Button(
                "添加模型", type="primary", elem_style=dict(width="50%")
            ) as add_model_btn:
                with ms.Slot("icon"):
                    antd.Icon("PlusOutlined")
    model_item_form, edit_add_model_modal = edit_or_add_model()

    def edit_model_fn(e: gr.EventData):
        is_edit = e._data["component"]["value"] == "编辑"
        current_model = e._data["component"]["switch"]["model"] if is_edit else {}
        return gr.update(value=current_model), gr.update(open=True)

    edit_btn.click(
        edit_model_fn,
        outputs=[model_item_form, edit_add_model_modal],
        queue=False,
    )

    def add_model_fn():
        return gr.update(value={}), gr.update(open=True)

    add_model_btn.click(
        add_model_fn, outputs=[model_item_form, edit_add_model_modal], queue=False
    )

    # 新增或编辑保存
    def on_submit(state_value, form_data):

        if "id" not in form_data or form_data["id"] is None:
            form_data["id"] = str(uuid.uuid4())
            state_value["model_list"].append(form_data)
        else:
            state_value["model_list"] = [
                ({**form_data} if item["id"] == form_data["id"] else item)
                for item in state_value["model_list"]
            ]
        return gr.update(open=False), gr.update(value=state_value["model_list"])

    model_item_form.finish(
        on_submit,
        inputs=[my_setting_state, model_item_form],
        outputs=[edit_add_model_modal, my_setting_state],
    )

    def del_model_source(state_value, e: gr.EventData):
        current_model = e._data["component"]["switch"]["model"]
        state_value["model_list"] = [
            item
            for item in state_value["model_list"]
            if item["id"] != current_model["id"]
        ]
        return gr.update(value=state_value)

    del_btn.click(
        del_model_source,
        inputs=[my_setting_state],
        outputs=[my_setting_state],
    )

    def switch_model_source(state_value, e: gr.EventData):
        current_model = e._data["component"]["model"]
        enabled = e._data["payload"][0]
        state_value["model_list"] = [
            (
                {**item, "enabled": enabled}
                if item["id"] == current_model["id"]
                else item
            )
            for item in state_value["model_list"]
        ]
        return gr.update(value=state_value)

    switch_btn.change(
        switch_model_source,
        inputs=[my_setting_state],
        outputs=[my_setting_state],
    )

    def setting_data_source_change(state_value):
        # print("+++++++setting_data_source_change", state_value)
        return gr.update(data_source=state_value["model_list"])

    my_setting_state.change(
        setting_data_source_change,
        inputs=[my_setting_state],
        outputs=[model_setting_list],
    )
    return my_setting_state, model_setting_list


# 模型新增弹框
def edit_or_add_model():
    with antd.Modal(
        title="模型设置",
        width=420,
        footer=False,
        centered=True,
        styles=dict(footer=dict(display="none")),
    ) as edit_add_model_modal:
        # model_item_value = {"name": "", "model": "", "token": "", "api_url": ""}
        with antd.Form(layout="vertical") as model_item_form:
            antd.Form.Item(form_name="id", hidden=True)
            with antd.Form.Item(
                form_name="name",
                label="名称",
                tooltip="大模型名称，不要重复",
                rules=[{"required": True, "message": "名称不能为空"}],
            ):
                antd.Input()
            with antd.Form.Item(
                form_name="model",
                label="模型",
                tooltip="api具体调用的名称，例如：Pro/deepseek-ai/DeepSeek-V3",
                rules=[{"required": True, "message": "模型不能为空"}],
            ):
                antd.Input()
            with antd.Form.Item(
                form_name="token",
                label="API密钥",
                tooltip="各大模型提供的API key",
                rules=[{"required": True, "message": "API密钥不能为空"}],
            ):
                antd.Input.Password()
            with antd.Form.Item(
                form_name="api_url",
                label="API地址",
                tooltip="模型官方调用地址",
                rules=[{"required": True, "message": "API地址不能为空"}],
            ):
                antd.Input()
            with antd.Form.Item(label_col=24):
                with antd.Flex(justify="center"):
                    antd.Button(
                        "保存",
                        type="primary",
                        html_type="submit",
                        elem_style=dict(width="50%"),
                    )
    edit_add_model_modal.cancel(
        fn=lambda: gr.update(open=False), outputs=[edit_add_model_modal], queue=False
    )

    return model_item_form, edit_add_model_modal


# 切换模型
def SelectChatModel(data_source: list[dict]):
    model_chat_state = gr.State({"model_chat_list": data_source})
    selected_model = gr.State({"selected_model": data_source[0]})
    model_chat_select = antd.Select(
        options=data_source,
        value=data_source[0]["id"],
        field_names={"label": "name", "value": "id"},
        disabled=True,
    )

    def model_chat_state_change():
        print("++++model_chat_state_change++++")

    model_chat_state.change(
        model_chat_state_change,
        inputs=[model_chat_state],
    )

    def model_chat_select_change(state_value, e: gr.EventData):
        print("++++model_chat_select_change++++", e._data["payload"][1])
        _value = e._data["payload"][1]
        state_value["selected_model"] = _value
        return gr.update(value=_value["id"]), gr.update(value=state_value)

    model_chat_select.select(
        model_chat_select_change,
        inputs=[selected_model],
        outputs=[model_chat_select, selected_model],
        queue=False,
    )
    return model_chat_select, model_chat_state, selected_model
