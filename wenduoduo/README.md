# Wenduoduo SDK

文多多SDK集成说明

## 使用方法

1. 引入SDK
```html
<script src="https://docmee.cn/sdk/docmee-ui-sdk-iframe.min.js"></script>
```

2. 初始化
```javascript
const docmeeUI = new DocmeeUI({
    token: 'your-token',
    container: document.querySelector("#container"),
    page: "creator",
    lang: "zh",
    mode: "light"
});
```

## 配置说明

- token: API访问令牌
- container: 容器元素
- page: 页面类型（creator/viewer）
- lang: 语言（zh/en）
- mode: 主题模式（light/dark）

## 注意事项

1. 确保容器元素具有合适的尺寸
2. 处理好错误回调
3. 注意跨域问题
