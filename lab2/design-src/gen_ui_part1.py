# -*- coding: utf-8 -*-
"""生成二手交易系统 8 个 UI 界面的高保真 HTML 原型（360px 逻辑宽 × 2x 渲染）"""
import os

OUT = os.path.join(os.path.dirname(__file__), "ui")
os.makedirs(OUT, exist_ok=True)

BASE_CSS = """
* { margin:0; padding:0; box-sizing:border-box; font-family:"HarmonyOS Sans SC","MiSans","PingFang SC","Microsoft YaHei","Segoe UI",sans-serif; }
body { background:#E7EBF1; padding:56px 64px 64px; }
.title { font-size:44px; color:#171B26; font-weight:800; margin-bottom:10px; }
.sub { font-size:24px; color:#6B7484; margin-bottom:44px; line-height:1.6; }
.row { display:flex; gap:72px; align-items:flex-start; }
.frame { display:flex; flex-direction:column; }
.phone { width:720px; background:#F5F6FA; border:14px solid #171B26; border-radius:48px; overflow:hidden;
         box-shadow:0 28px 70px rgba(23,27,38,.20); position:relative; display:flex; flex-direction:column; }
.phone::before { content:""; position:absolute; top:0; left:50%; transform:translateX(-50%);
                  width:216px; height:26px; background:#171B26; border-radius:0 0 22px 22px; z-index:9; }
.statusbar { height:60px; display:flex; justify-content:space-between; align-items:center; padding:6px 40px 0;
             font-size:22px; color:#171B26; font-weight:700; background:inherit; flex:none; }
.caption { margin-top:26px; font-size:27px; color:#333B49; text-align:center; font-weight:700; }
.caption small { display:block; font-size:22px; color:#7A8291; font-weight:500; margin-top:6px; }
.screen { flex:1; display:flex; flex-direction:column; padding:16px 26px 0; }
.navbar { display:flex; align-items:center; gap:14px; padding:18px 6px 16px; }
.navbar .back { font-size:30px; color:#2A3140; }
.navbar .t { font-size:34px; font-weight:800; color:#171B26; flex:1; }
.navbar .act { font-size:25px; color:#FF6E2C; font-weight:700; }
.card { background:#fff; border-radius:26px; padding:26px; box-shadow:0 6px 18px rgba(23,27,38,.05); }
.hint { font-size:21px; color:#8A93A6; line-height:1.55; }
.pill { display:inline-flex; align-items:center; padding:6px 18px; border-radius:999px; font-size:21px; font-weight:700; }
.p-sale { background:#E5F7EC; color:#149A52; }
.p-reserved { background:#FFF0E0; color:#E0741F; }
.p-sold { background:#EDF0F4; color:#69738A; }
.p-review { background:#E6EFFF; color:#2C6BD8; }
.p-draft { background:#F0F2F6; color:#6C7689; }
.p-off { background:#F2F3F6; color:#9AA2B4; }
.p-violation { background:#FCEBEB; color:#D23030; }
.btn { display:flex; align-items:center; justify-content:center; border-radius:999px; font-weight:800; font-size:27px; padding:22px 0; }
.btn-primary { background:linear-gradient(92deg,#FF9A55,#FF6E2C); color:#fff; box-shadow:0 10px 22px rgba(255,110,44,.28); }
.btn-ghost { background:#fff; color:#FF6E2C; border:3px solid #FFC5A3; }
.btn-gray { background:#EEF0F4; color:#7A8291; }
.btn-danger { background:#fff; color:#D23030; border:3px solid #F3B9B9; }
.btn-disabled { background:#E9EBF0; color:#A6AEC0; box-shadow:none; }
.input { background:#F2F3F7; border-radius:20px; padding:24px 26px; font-size:27px; color:#2A3140; width:100%;
         border:3px solid transparent; outline:none; }
.input.error { border-color:#E5484D; background:#FEF7F7; }
.i-label { font-size:24px; color:#4A5264; font-weight:700; margin:22px 0 10px; }
.err-text { font-size:21px; color:#E5484D; margin-top:8px; }
.ok-text { font-size:21px; color:#149A52; margin-top:8px; }
.chip { padding:14px 26px; border-radius:999px; background:#F0F2F6; color:#4A5264; font-size:24px; font-weight:700; }
.chip.on { background:#FFE9DA; color:#FF5A1F; }
.pgrid { display:grid; grid-template-columns:1fr 1fr; gap:20px; }
.pcard { background:#fff; border-radius:24px; padding:16px 16px 20px; }
.pthumb { height:250px; border-radius:18px; display:flex; align-items:center; justify-content:center; font-size:110px; }
.ptitle { font-size:25px; font-weight:700; color:#252B39; margin:16px 2px 8px; line-height:1.35;
          overflow:hidden; text-overflow:ellipsis; display:-webkit-box; -webkit-line-clamp:2; -webkit-box-orient:vertical; }
.pprice { font-size:30px; color:#FF4D1C; font-weight:800; }
.pprice small { font-size:21px; font-weight:700; }
.pmeta { display:flex; justify-content:space-between; align-items:center; margin-top:12px; }
.seller { font-size:21px; color:#8A93A6; }
.tabbar { display:flex; background:#fff; border-top:2px solid #E8EBF1; padding:14px 0 30px; margin-top:auto; }
.tab { flex:1; display:flex; flex-direction:column; align-items:center; gap:6px; font-size:20px; color:#98A0B3; font-weight:600; }
.tab .ic { font-size:40px; }
.tab.on { color:#FF5A1F; }
.banner { border-radius:20px; padding:20px 24px; font-size:23px; line-height:1.5; }
.list-row { display:flex; gap:20px; padding:22px 4px; align-items:center; }
"""

def page(title, sub, frames_html):
    frames = "\n".join(
        f'<div class="frame">{phone}<div class="caption">{cap}<small>{small}</small></div></div>'
        for phone, cap, small in frames_html
    )
    return ("<!DOCTYPE html><html><head><meta charset='utf-8'>"
            f"<title>{title}</title><style>{BASE_CSS}</style></head><body>"
            f"<div class='title'>{title}</div><div class='sub'>{sub}</div>"
            f"<div class='row'>{frames}</div></body></html>")

def phone(inner, statusbg="#F5F6FA"):
    return (f'<div class="phone" style="background:{statusbg}">'
            '<div class="statusbar"><span>9:41</span><span>▮▮▯ &nbsp; ᯤ &nbsp; 🔋</span></div>'
            f'<div class="screen">{inner}</div></div>')

pages = {}

# ================= 界面 1：登录与注册 =================
login = """
<div style="padding:40px 8px 0; display:flex; flex-direction:column; align-items:center;">
  <div style="width:132px;height:132px;border-radius:36px;background:linear-gradient(135deg,#FF9A55,#FF5A1F);
              display:flex;align-items:center;justify-content:center;font-size:64px;box-shadow:0 14px 30px rgba(255,90,31,.30);">🛍️</div>
  <div style="font-size:44px;font-weight:800;color:#171B26;margin-top:22px;">校园二手集市</div>
  <div class="hint" style="margin-top:8px;">线下交易 · 状态透明 · 预约唯一</div>
</div>
<div class="card" style="margin-top:44px;padding:34px 30px;">
  <div class="i-label" style="margin-top:0;">手机号</div>
  <input class="input" value="138****6621">
  <div class="i-label">密码</div>
  <input class="input error" type="password" value="········">
  <div class="err-text">✕ 手机号或密码错误，请重试（登录失败已记录日志）</div>
  <div class="btn btn-primary" style="margin-top:34px;">登 录</div>
  <div style="text-align:center;margin-top:26px;font-size:24px;color:#7A8291;">
    还没有账号？<span style="color:#FF5A1F;font-weight:800;">立即注册</span>
  </div>
</div>
<div class="hint" style="text-align:center;margin:28px 0 40px;">🔒 密码仅以不可逆摘要保存，系统不保存明文</div>
"""

register = """
<div class="navbar"><div class="t" style="font-size:38px;padding-left:4px;">创建账号</div></div>
<div class="card" style="padding:34px 30px;">
  <div class="i-label" style="margin-top:0;">手机号 <span class="hint">（唯一，用于登录）</span></div>
  <input class="input" value="13812346621">
  <div class="ok-text">✓ 该手机号可以注册</div>
  <div class="i-label">用户名 <span class="hint">（可修改，允许与他人重复）</span></div>
  <input class="input" value="鸣骏Max">
  <div class="i-label">密码 <span class="hint">（至少 8 位）</span></div>
  <input class="input error" value="1234">
  <div class="err-text">✕ 密码长度不足 8 位</div>
  <div class="i-label">确认密码</div>
  <input class="input" type="password" value="········">
  <div class="i-label">选择角色</div>
  <div style="display:flex;gap:18px;">
    <div class="chip on" style="flex:1;text-align:center;">👤 买家</div>
    <div class="chip" style="flex:1;text-align:center;">🏪 卖家</div>
  </div>
  <div class="hint" style="margin-top:14px;">管理员账号由平台预置分配，不开放注册</div>
  <div class="btn btn-primary" style="margin-top:34px;">注 册</div>
</div>
<div class="hint" style="text-align:center;margin:28px 0 40px;">注册成功后按角色授予对应功能权限（REQ-001 / REQ-002）</div>
"""

pages["界面1"] = page(
    "界面 1 · 用户注册与登录模块",
    "买家 / 卖家 / 管理员统一入口。手机号唯一标识账号，密码仅保存不可逆摘要；登录失败与注册校验错误均给出明确原因，并写入操作日志。",
    [(phone(login), "① 登录页（错误提示状态）", "登录失败提示原因，关键结果记录日志"),
     (phone(register), "② 注册页（表单校验状态）", "手机号唯一性、密码规则、角色选择")])

# ================= 界面 2：商品首页与组合查询 =================
home = """
<div style="padding:14px 2px 0;">
  <div style="display:flex;align-items:center;gap:14px;">
    <div style="flex:1;background:#fff;border-radius:999px;padding:20px 28px;font-size:25px;color:#98A0B3;
                box-shadow:0 6px 18px rgba(23,27,38,.05);">🔍 搜索商品关键词…</div>
    <div style="width:76px;height:76px;border-radius:24px;background:linear-gradient(135deg,#FF9A55,#FF5A1F);
                display:flex;align-items:center;justify-content:center;font-size:36px;">🎛️</div>
  </div>
  <div style="display:flex;gap:14px;margin:26px 0;flex-wrap:wrap;">
    <div class="chip on">全部</div><div class="chip">数码</div><div class="chip">图书</div>
    <div class="chip">运动</div><div class="chip">生活</div><div class="chip">票券</div>
  </div>
</div>
<div class="pgrid">
  <div class="pcard">
    <div class="pthumb" style="background:linear-gradient(135deg,#E8F1FF,#D5E5FF);">💻</div>
    <div class="ptitle">iPad Air 5 95新 带笔尖膜</div>
    <div class="pprice"><small>¥</small>2,399</div>
    <div class="pmeta"><span class="pill p-sale">在售</span><span class="seller">阿明 · 95新</span></div>
  </div>
  <div class="pcard">
    <div class="pthumb" style="background:linear-gradient(135deg,#FFF1E0,#FFE3C2);">🎸</div>
    <div class="ptitle">民谣吉他 入门款 赠琴包</div>
    <div class="pprice"><small>¥</small>329</div>
    <div class="pmeta"><span class="pill p-reserved">已预约</span><span class="seller">小林 · 9成新</span></div>
  </div>
  <div class="pcard">
    <div class="pthumb" style="background:linear-gradient(135deg,#E9F9EF,#D2F2DE);">📖</div>
    <div class="ptitle">算法导论 第三版 中文版</div>
    <div class="pprice"><small>¥</small>68</div>
    <div class="pmeta"><span class="pill p-sale">在售</span><span class="seller">学长书店 · 99新</span></div>
  </div>
  <div class="pcard">
    <div class="pthumb" style="background:linear-gradient(135deg,#F1EDFC,#E4DCF9);">🚲</div>
    <div class="ptitle">捷安特通勤自行车 已上锁</div>
    <div class="pprice"><small>¥</small>580</div>
    <div class="pmeta"><span class="pill p-sale">在售</span><span class="seller">骑行社 · 8成新</span></div>
  </div>
</div>
<div class="hint" style="text-align:center;margin:24px 0 8px;">普通用户列表自动过滤「已下架 / 违规下架」商品</div>
<div class="tabbar">
  <div class="tab on"><span class="ic">🏠</span>首页</div>
  <div class="tab"><span class="ic">❤️</span>收藏</div>
  <div class="tab"><span class="ic">➕</span>发布</div>
  <div class="tab"><span class="ic">👤</span>我的</div>
</div>
"""

filter_panel = """
<div class="navbar"><div class="back">‹</div><div class="t">筛选条件</div><div class="act">重置</div></div>
<div class="card" style="padding:30px;">
  <div class="i-label" style="margin-top:0;">分类</div>
  <div style="display:flex;gap:14px;flex-wrap:wrap;">
    <div class="chip on">数码</div><div class="chip">图书</div><div class="chip">运动</div>
    <div class="chip">生活</div><div class="chip">票券</div>
  </div>
  <div class="i-label">价格区间（元）</div>
  <div style="display:flex;align-items:center;gap:16px;">
    <input class="input" style="text-align:center;" value="100">
    <span style="color:#98A0B3;font-size:26px;">—</span>
    <input class="input error" style="text-align:center;" value="50">
  </div>
  <div class="err-text">✕ 价格区间下限不能大于上限</div>
  <div class="i-label">商品状态</div>
  <div style="display:flex;gap:14px;flex-wrap:wrap;">
    <div class="chip on">在售</div><div class="chip">已预约</div><div class="chip">已售出</div>
  </div>
  <div class="hint" style="margin-top:10px;">已下架 / 违规下架商品对普通用户不可见</div>
  <div class="i-label">发布时间</div>
  <div style="display:flex;gap:14px;flex-wrap:wrap;">
    <div class="chip on">最新发布</div><div class="chip">最早发布</div><div class="chip">近 7 天</div>
  </div>
</div>
<div class="banner" style="background:#E6EFFF;color:#2C6BD8;margin-top:24px;">
  当前组合条件预计匹配 <b>23</b> 件商品
</div>
<div class="btn btn-primary" style="margin-top:28px;">应用筛选</div>
<div class="hint" style="text-align:center;margin:24px 0 40px;">多条件组合查询（REQ-007）；无匹配时返回空列表并明确提示</div>
"""

pages["界面2"] = page(
    "界面 2 · 商品浏览与组合查询模块",
    "首页以双列卡片展示在售商品：缩略图、标题、价格、成色、状态标签与卖家昵称。筛选面板支持关键词、分类、价格区间、商品状态与发布时间的任意组合，价格区间非法时即时校验。",
    [(phone(home), "① 商品首页（浏览）", "分类快捷入口 + 商品卡片流"),
     (phone(filter_panel), "② 组合筛选面板（校验状态）", "价格区间即时校验，组合条件预估结果")])

# ================= 界面 3：商品详情 =================
detail_onsale = """
<div class="navbar"><div class="back">‹</div><div class="t">商品详情</div><div class="act">···</div></div>
<div style="height:430px;border-radius:24px;background:linear-gradient(135deg,#E8F1FF,#D9E7FF);
            display:flex;align-items:center;justify-content:center;font-size:170px;position:relative;">
  💻
  <div style="position:absolute;bottom:20px;right:24px;background:rgba(23,27,38,.55);color:#fff;
              border-radius:999px;padding:8px 20px;font-size:21px;">1 / 4</div>
</div>
<div style="display:flex;align-items:center;gap:16px;margin:26px 4px 10px;">
  <span class="pill p-sale">在售</span>
  <span class="hint">版本 v5 · 2026-10-20 发布</span>
</div>
<div style="font-size:34px;font-weight:800;color:#171B26;line-height:1.4;">iPad Air 5 95新 深空灰 64G 带笔尖膜</div>
<div style="font-size:46px;color:#FF4D1C;font-weight:800;margin:14px 0 20px;"><small style="font-size:26px;">¥</small> 2,399</div>
<div class="card" style="padding:6px 26px;">
  <div class="list-row" style="border-bottom:2px solid #F1F3F7;"><span class="hint">成色</span><b style="font-size:25px;">95 新</b></div>
  <div class="list-row" style="border-bottom:2px solid #F1F3F7;"><span class="hint">分类</span><b style="font-size:25px;">数码</b></div>
  <div class="list-row" style="border-bottom:2px solid #F1F3F7;"><span class="hint">取货方式</span><b style="font-size:25px;">校内自取（南门快递点）</b></div>
  <div class="list-row"><span class="hint">卖家</span>
    <span style="display:flex;align-items:center;gap:12px;"><span style="font-size:34px;">🧑‍🎓</span><b style="font-size:25px;">阿明</b></span>
  </div>
</div>
<div class="hint" style="margin:14px 6px 0;">🔒 仅展示卖家公开昵称，手机号等资料不可见（REQ-022）</div>
<div class="card" style="margin-top:22px;">
  <div style="font-size:26px;font-weight:800;margin-bottom:10px;">商品描述</div>
  <div class="hint" style="font-size:23px;">自用一学期，无磕碰，屏幕贴膜，电池健康 96%。附原装充电线，可现场验机。价格可小刀。</div>
</div>
<div style="display:flex;gap:18px;margin:26px 0 30px;">
  <div style="width:104px;height:88px;border-radius:22px;background:#fff;border:3px solid #F0E4DC;
              display:flex;align-items:center;justify-content:center;font-size:36px;">🤍</div>
  <div style="width:104px;height:88px;border-radius:22px;background:#fff;border:3px solid #F0E4DC;
              display:flex;align-items:center;justify-content:center;font-size:36px;">🚩</div>
  <div class="btn btn-primary" style="flex:1;">立即预约</div>
</div>
<div class="hint" style="text-align:center;margin-bottom:36px;">预约请求将携带当前版本号 v5；多人同时预约时以首个成功请求为准</div>
"""

detail_conflict = """
<div class="navbar"><div class="back">‹</div><div class="t">商品详情</div><div class="act">···</div></div>
<div style="height:430px;border-radius:24px;background:linear-gradient(135deg,#FFF1E0,#FFE3C2);
            display:flex;align-items:center;justify-content:center;font-size:170px;">🎸</div>
<div style="display:flex;align-items:center;gap:16px;margin:26px 4px 10px;">
  <span class="pill p-reserved">已预约</span>
  <span class="hint">版本 v6 · 2026-10-22 发布</span>
</div>
<div style="font-size:34px;font-weight:800;color:#171B26;line-height:1.4;">民谣吉他 入门款 赠琴包变调夹</div>
<div style="font-size:46px;color:#FF4D1C;font-weight:800;margin:14px 0 20px;"><small style="font-size:26px;">¥</small> 329</div>
<div class="banner" style="background:#FFF0E0;color:#B45A10;">
  ⚠️ 该商品已被预约。详情仅对<b>商品卖家</b>与<b>预约买家</b>继续开放，用于双方确认交易进度。
</div>
<div class="card" style="margin-top:22px;">
  <div style="font-size:26px;font-weight:800;margin-bottom:10px;">我的预约状态</div>
  <div style="display:flex;align-items:center;gap:12px;">
    <span class="pill p-reserved">待确认</span>
    <span class="hint">2026-10-22 14:08 提交 · 等待卖家确认</span>
  </div>
</div>
<div style="position:relative;margin-top:30px;">
  <div style="filter:blur(2px) saturate(.8);opacity:.55;pointer-events:none;">
    <div class="card">
      <div style="font-size:26px;font-weight:800;margin-bottom:10px;">商品描述</div>
      <div class="hint" style="font-size:23px;">买来练了一个月，手感很好，闲置转让。赠送琴包、变调夹和两套备用弦……</div>
    </div>
    <div style="display:flex;gap:18px;margin:26px 0 10px;">
      <div style="width:104px;height:88px;border-radius:22px;background:#fff;border:3px solid #F0E4DC;
                  display:flex;align-items:center;justify-content:center;font-size:36px;">🤍</div>
      <div class="btn btn-disabled" style="flex:1;">立即预约</div>
    </div>
  </div>
  <div style="position:absolute;left:50%;top:38%;transform:translate(-50%,-50%);width:560px;">
    <div class="card" style="padding:36px 30px;text-align:center;box-shadow:0 30px 60px rgba(23,27,38,.28);">
      <div style="font-size:64px;">⚡</div>
      <div style="font-size:30px;font-weight:800;margin:14px 0 10px;">商品状态已变化</div>
      <div class="hint" style="font-size:23px;">该商品刚被其他买家预约（版本 v5 → v6），<br>为避免覆盖他人预约，本次请求未写入。</div>
      <div style="display:flex;gap:16px;margin-top:28px;">
        <div class="btn btn-ghost" style="flex:1;padding:18px 0;">返回列表</div>
        <div class="btn btn-primary" style="flex:1;padding:18px 0;">刷新最新状态</div>
      </div>
    </div>
  </div>
</div>
<div class="hint" style="text-align:center;margin:22px 0 36px;">旧页面 / 并发请求冲突提示（REQ-012）</div>
"""

pages["界面3"] = page(
    "界面 3 · 商品详情模块（含预约入口与冲突反馈）",
    "详情页展示商品完整公开信息与卖家昵称；预约按钮携带版本号提交。左图为在售状态；右图演示并发冲突：商品刚被他人预约，旧版本请求被拒绝并提示刷新，详情对无关用户收起。",
    [(phone(detail_onsale), "① 在售商品详情", "完整公开信息 + 卖家公开昵称 + 预约入口"),
     (phone(detail_conflict), "② 已预约状态与版本冲突弹层", "仅交易双方可见；旧版本请求被拒绝")])

os.makedirs(OUT, exist_ok=True)
for name, html in pages.items():
    with open(os.path.join(OUT, f"{name}.html"), "w", encoding="utf-8") as f:
        f.write(html)
    print("written", name)
