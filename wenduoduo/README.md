# AIPPT 生成器

## 简介
基于AI的智能PPT生成工具，只需输入主题即可快速生成专业PPT。

## 特点
- 一键生成PPT
- 智能排版
- 专业模板
- 在线预览

## 使用方法
访问：https://suihong123.github.io/aippt


#生成 PPT 回调
请求方式： POST
请求头（签名方式）：
x-signature： MD5(uid + pptId + apiKey)
请求 body（application/json）：
{
  "event": "ppt_generate",
  "data": {
    "uid": "xxx", // 第三方用户ID
    "pptId": "xxx", // PPT ID
    "name": "xxx", // 名称
    "subject": "xxx", // 主题
    "coverUrl": "https://xxx.png", // 封面
    "fileUrl": "https://xxx.pptx", // PPT文件
    "createTime": "2024-01-01 10:00:00" // 创建时间
  }
}

标准响应格式（application/json）：
{
  "ok": true,
  "msg": "操作成功"
}
响应结果中 ok 字段为 true 则表示集成方收到回调事件，否则为处理失败，失败后系统会在 2 分钟后重试、15 分钟后重试、1 小时后重试、4 小时后重试，最多重试 4 次。

配置服务回调或修改回调地址时，系统会发送测试请求，验证接口地址是否能正常工作，测试请求数据：
{
  "event": "ppt_generate",
  "data": {
    "uid": "test",
    "pptId": "test", // pptId 为 test 时，为系统测试请求（忽略业务处理，请直接响应 {"ok":true} 数据）
    "name": "test",
    "subject": "test",
    "coverUrl": "https://docmee.cn/xxx.png",
    "fileUrl": "https://docmee.cn/xxx.pptx",
    "createTime": "2024-01-01 10:00:00"
  }
}
上传 PPT 模板回调
请求方式： POST

请求头（签名方式）：

x-signature： MD5(uid + templateId + apiKey)

请求 body（application/json）：

{
  "event": "template_upload",
  "data": {
    "uid": "xxx", // 第三方用户ID
    "templateId": "xxx", // PPT模板ID
    "coverUrl": "https://xxx.png", // 封面
    "fileUrl": "https://xxx.pptx", // PPT文件
    "createTime": "2024-01-01 10:00:00" // 创建时间
  }
}
标准响应格式（application/json）：

{
  "ok": true,
  "msg": "操作成功"
}
响应结果中 ok 字段为 true 则表示集成方收到回调事件，否则为处理失败，失败后系统会在 2 分钟后重试、15 分钟后重试、1 小时后重试、4 小时后重试，最多重试 4 次。

## 快速开始

### 安装
1. 克隆仓库
```bash
git clone https://github.com/suihong123/aippt.git
```

### 本地运行
```bash
# 使用任意HTTP服务器
http-server
```

### 部署
推送到GitHub后自动部署到GitHub Pages
