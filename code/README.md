# 校园二手集市（实验三桌面程序）

## 启动

双击 `启动校园二手集市.bat`，或在本目录运行：

```powershell
python web_desktop.py
```

程序使用 pywebview、HTML/CSS 和 SQLite；无需网络、在线服务或浏览器标签页。

## 演示账号

| 角色 | 手机号 | 密码 |
|---|---|---|
| 买家 | 13800000001 | buyer123 |
| 卖家 | 13800000002 | seller123 |
| 管理员 | 13800000003 | admin123 |

`web_desktop.py` 是高 DPI 桌面 WebView 主入口，加载同目录 `ui/index.html` 的原创界面。`market_service.py` 提供注册登录、商品状态机、预约交易、收藏、举报、审核、统计和操作日志等业务服务。
