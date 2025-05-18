import os
import shutil
import json
import secrets
import requests
import gradio as gr
from dotenv import load_dotenv
from parser.json_parser import json2dict, dict2json

# 加载环境变量
load_dotenv()
# 加载主播选项
options_dict = json2dict("introduction.json")
options = list(options_dict.keys())

# Raw路径
RAW_PATH = os.path.join(os.getenv("KB_BASE_PATH"), "raw")

from gradio.themes import Monochrome


def list_existing_files():
    API_URL = "http://127.0.0.1:8090/list-files"
    response = requests.get(API_URL)
    if response.status_code == 200:
        return list(response.json())
    return []


def save_uploaded_file(file_obj):
    # 定义你的目标路径（例如：当前目录下的 uploaded_files 文件夹）
    custom_dir = RAW_PATH
    os.makedirs(custom_dir, exist_ok=True)  # 确保目录存在
    # 生成目标路径
    target_path = os.path.join(custom_dir, os.path.basename(file_obj.name))
    # 将文件从临时路径复制到自定义路径
    shutil.copy(file_obj.name, target_path)

    # 删除临时文件（Gradio 上传的临时路径）
    if os.path.exists(file_obj.name):  # 检查文件是否存在（避免异常）
        os.remove(file_obj.name)  # 删除临时文件
    file_path = f"raw/{os.path.basename(file_obj.name)}"
    return file_path, file_path


with gr.Blocks(title="☝️🤓💡切片神器", theme=Monochrome()) as demo:
    gr.Markdown("# ☝️🤓💡切片剪辑神器")
    # 处理按钮
    process_btn = gr.Button("✅开始处理", interactive=False)
    uploaded_file_state = gr.State("")
    with gr.Column():
        # 文件上传选项卡
        with gr.Tab("上传新文件") as upload_tab:
            upload_input = gr.File(label="上传视频文件")
            # 初始化保存按钮为隐藏状态
            save_btn = gr.Button("保存文件", visible=False)

        # 现有文件选项卡
        with gr.Tab("选择现有文件") as existing_tab:
            existing_files = gr.Dropdown(
                choices=[],
                label="选择已存在的文件",
                interactive=True
            )
            existing_tab.select(
                fn=lambda: gr.update(choices=list_existing_files()),  # 关键：每次切换时重新获取文件列表
                outputs=existing_files  # 更新下拉菜单的选项
            )
            pass
            

        # 结果显示
        file_path_output = gr.Textbox(label="文件路径")
        save_btn.click(
            fn=save_uploaded_file,
            inputs=upload_input,
            outputs=[file_path_output, uploaded_file_state]
        )

        existing_files.change(
            fn=lambda x: x,  # 直接返回选中的文件路径
            inputs=existing_files,
            outputs=file_path_output  # 输出到文件路径显示框
        )

        # 上传选项卡切换事件：显示最近上传的文件路径
        upload_tab.select(
            fn=lambda x: x,
            inputs=uploaded_file_state,
            outputs=file_path_output
        )

        # 现有文件选项卡切换事件：显示选中的文件
        existing_tab.select(
            fn=lambda x: x,
            inputs=existing_files,
            outputs=file_path_output
        )

        # 当文件上传内容变化时显示保存按钮
        upload_input.change(
            # 使用gr.update()返回组件更新状态
            fn=lambda x: gr.update(visible=True) if x is not None else gr.update(visible=False),
            inputs=upload_input,
            outputs=save_btn  # 直接指向按钮组件本身
        )
        # end of gr column
    with gr.Column():
        # 主播选择
        streamer_introduction = gr.State("")
        streamer_select = gr.Dropdown(
            interactive=True,
            choices=options,
            value=options[0],
            label="选择主播ID",

        )
        # -----------------------
        streamer_select.change(
            fn=lambda x: options_dict[x],  # 添加处理函数：返回选中的值
            inputs=streamer_select,  # 指定输入为下拉框组件
            outputs=streamer_introduction  # 输出到文本框
        )


        # 条件检查函数
        def check_process_conditions(file_path, streamer_info):
            return gr.update(interactive=bool(file_path and streamer_info))


        # 监听文件路径变化
        file_path_output.change(
            fn=check_process_conditions,
            inputs=[file_path_output, streamer_introduction],
            outputs=process_btn
        )

        # 监听主播介绍变化
        streamer_introduction.change(
            fn=check_process_conditions,
            inputs=[file_path_output, streamer_introduction],
            outputs=process_btn
        )


        # 处理按钮点击事件
        def submit_root_processor(file_path, streamer_info):
            API_URL = "http://127.0.0.1:8090/submit"
            response = requests.post(
                API_URL,
                json={
                    'task_id': secrets.token_hex(4),
                    'raw_path': file_path,
                    'introduction': streamer_info
                }
            )
            if response.status_code == 200:
                return response.json()
            else:
                return {}


        process_result = gr.State([])

        process_btn.click(
            fn=submit_root_processor,
            inputs=[file_path_output, streamer_introduction],
            outputs=process_result
        )

    with gr.Column() as result_links:
        # 此处修改：使用Markdown组件来显示结果
        result_display = gr.Markdown()


    def update_result_columns(results):
        # 此处修改：生成组合的Markdown内容
        if not results:
            return ""

        output = []
        for idx, res in enumerate(results, 1):
            content = "\n".join([f"- {k}: {v}\n" for k, v in res.items()])
            output.append(f"""\n### 切片结果 {idx}\n{content}""")

        return "处理结束" + "\n\n".join(output)


    # 此处修改：更新change事件指向Markdown组件
    process_result.change(
        fn=update_result_columns,
        inputs=process_result,
        outputs=result_display
    )

if __name__ == "__main__":
    demo.launch(
        server_name="127.0.0.1",
        server_port=7860
    )
