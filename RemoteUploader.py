import os
import shutil
import time
from pprint import pprint

import gradio as gr
import yaml

with open('config.yaml', 'r', encoding='utf-8') as f:
    config = yaml.load(f, yaml.FullLoader)

print("启动参数:")
pprint(config)

web_ui_path = config['web_ui_path']


def path_concat(path):
    return os.path.join(web_ui_path, path)


path = {
    "Stable Diffusion 模型": path_concat("models/Stable-diffusion/"),
    "嵌入式 (Embedding) 模型": path_concat("embeddings/"),
    "超网络 (HyperNetwork) 模型": path_concat("models/hypernetworks/"),
    "变分自编码器 (VAE) 模型": path_concat("models/VAE/"),
    "LORA 模型 (原生)": path_concat("models/Lora/"),
    "LoRA 模型 (插件)": path_concat("extensions/sd-webui-additional-networks/models/lora/")
}


def movefile(src_file, dst_path):
    _, f_name = os.path.split(src_file)
    shutil.move(src_file, os.path.join(dst_path, f_name))


def timestamp():
    return time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())


def upload(upload_path, file_obj):
    if upload_path is None:
        text = f"[{timestamp()}] 错误: 未指定模型的上传类型"
        print(text)
        return text
    try:
        movefile(file_obj.name, path[upload_path])
        _, f_name = os.path.split(file_obj.name)
        text = f"[{timestamp()}] 已载入 {f_name} 到 {upload_path} 合集"
        print(text)
        return text
    except (Exception, BaseException):
        text = f"[{timestamp()}] 上传失败"
        print(text)
        return text


demo = gr.Interface(
    upload,
    [
        gr.Radio(list(path.keys()), label="上传类型"),
        gr.File(label="模型文件")
    ],
    gr.Textbox(label="系统消息"),
    title="远程上传模型",
    description="@ BiliBili 一块小熊饼干r <br> ( Version: 1.0 ) <br> 上传完成后请返回 Web UI 并重新刷新模型列表",
    allow_flagging='never'
)

print("\n服务:")
demo.launch(server_name=config['server_name'], server_port=config['server_port'])
