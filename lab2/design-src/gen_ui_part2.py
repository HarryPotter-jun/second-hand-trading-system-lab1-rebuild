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

# -*- coding: utf-8 -*-
# 界面 4-8 的定义体（由 gen_ui_part2.py 引用）
# part2 = part1 的头部（BASE_CSS + 辅助函数）+ 本文件内容拼接而成

pages = {}

# ================= 界面 4：商品发布与编辑（卖家） =================
publish = """
<div class="navbar"><div class="back">‹</div><div class="t">发布商品</div><div class="act">存草稿</div></div>
<div class="card" style="padding:30px;">
  <div class="i-label" style="margin-top:0;">商品图片（最多 9 张）</div>
  <div style="display:flex;gap:16px;">
    <div style="width:150px;height:150px;border-radius:20px;background:linear-gradient(135deg,#E8F1FF,#D9E7FF);
                display:flex;align-items:center;justify-content:center;font-size:56px;">💻</div>
    <div style="width:150px;height:150px;border-radius:20px;background:linear-gradient(135deg,#FFF1E0,#FFE3C2);
                display:flex;align-items:center;justify-content:center;font-size:56px;">🖨️</div>
    <div style="width:150px;height:150px;border-radius:20px;border:3px dashed #C9CFDB;color:#98A0B3;
                display:flex;align-items:center;justify-content:center;font-size:44px;font-weight:700;background:#FAFBFD;">＋</div>
  </div>
  <div class="i-label">标题</div>
  <input class="input" value="iPad Air 5 95新 深空灰 64G">
  <div class="i-label">描述</div>
  <input class="input" value="自用一学期，无磕碰，附原装充电线" style="padding-bottom:60px;">
  <div class="i-label">分类</div>
  <div style="display:flex;gap:14px;flex-wrap:wrap;">
    <div class="chip on">数码</div><div class="chip">图书</div><div class="chip">运动</div>
    <div class="chip">生活</div><div class="chip">票券</div>
  </div>
  <div class="i-label">成色</div>
  <div style="display:flex;gap:14px;flex-wrap:wrap;">
    <div class="chip">全新</div><div class="chip on">95新</div><div class="chip">9成新</div><div class="chip">8成新</div>
  </div>
  <div class="i-label">价格（元）</div>
  <input class="input error" value="0">
  <div class="err-text">✕ 价格必须大于 0 且不超过 1,000,000 元</div>
  <div class="i-label">取货方式</div>
  <div style="display:flex;gap:16px;">
    <div class="chip on" style="flex:1;text-align:center;">📍 校内自取</div>
    <div class="chip" style="flex:1;text-align:center;">📦 邮寄</div>
  </div>
</div>
<div style="display:flex;gap:18px;margin:28px 0 12px;">
  <div class="btn btn-ghost" style="flex:1;">保存草稿</div>
  <div class="btn btn-primary" style="flex:1;">提交审核</div>
</div>
<div class="hint" style="text-align:center;margin-bottom:36px;">
  提交前校验必填项 / 金额范围 / 60 秒内重复提交（REQ-011）；<br>提交成功后商品进入「待审核」
</div>
"""

myproducts = """
<div class="navbar"><div class="back">‹</div><div class="t">我发布的商品</div><div class="act">＋ 发布</div></div>
<div style="display:flex;gap:12px;margin:6px 0 18px;flex-wrap:wrap;">
  <div class="chip">全部 <span class="hint">12</span></div>
  <div class="chip on">待审核 <span>2</span></div>
  <div class="chip">在售 <span>5</span></div>
  <div class="chip">已预约 <span>1</span></div>
  <div class="chip">已售出 <span>4</span></div>
  <div class="chip">已下架 <span>2</span></div>
</div>
<div class="card" style="padding:10px 26px;">
  <div class="list-row" style="border-bottom:2px solid #F1F3F7;">
    <div style="width:120px;height:120px;border-radius:18px;background:linear-gradient(135deg,#E8F1FF,#D9E7FF);
                display:flex;align-items:center;justify-content:center;font-size:48px;flex:none;">💻</div>
    <div style="flex:1;">
      <div style="font-size:26px;font-weight:700;">iPad Air 5 95新</div>
      <div style="display:flex;gap:12px;margin-top:10px;align-items:center;">
        <span class="pill p-review">待审核</span><span class="hint">¥2,399 · 提交于 10-22</span>
      </div>
      <div class="hint" style="margin-top:8px;">编辑后需重新审核（REQ-003）</div>
    </div>
    <div class="chip">查看</div>
  </div>
  <div class="list-row" style="border-bottom:2px solid #F1F3F7;">
    <div style="width:120px;height:120px;border-radius:18px;background:linear-gradient(135deg,#E9F9EF,#D2F2DE);
                display:flex;align-items:center;justify-content:center;font-size:48px;flex:none;">📖</div>
    <div style="flex:1;">
      <div style="font-size:26px;font-weight:700;">算法导论 第三版</div>
      <div style="display:flex;gap:12px;margin-top:10px;align-items:center;">
        <span class="pill p-sale">在售</span><span class="hint">¥68 · 10-18 发布</span>
      </div>
    </div>
    <div style="display:flex;flex-direction:column;gap:10px;">
      <div class="chip">编辑</div><div class="chip">下架</div>
    </div>
  </div>
  <div class="list-row">
    <div style="width:120px;height:120px;border-radius:18px;background:linear-gradient(135deg,#FFF1E0,#FFE3C2);
                display:flex;align-items:center;justify-content:center;font-size:48px;flex:none;">🎸</div>
    <div style="flex:1;">
      <div style="font-size:26px;font-weight:700;">民谣吉他 入门款</div>
      <div style="display:flex;gap:12px;margin-top:10px;align-items:center;">
        <span class="pill p-reserved">已预约</span><span class="hint">¥329 · 待处理预约 1</span>
      </div>
      <div class="hint" style="margin-top:8px;color:#E0741F;">已预约商品须先处理预约方可下架</div>
    </div>
    <div class="chip" style="background:#F0F2F6;color:#B4BAC7;">编辑 🔒</div>
  </div>
</div>
<div class="hint" style="text-align:center;margin:24px 0 36px;">按状态筛选本人商品；已预约 / 已售出商品锁定关键信息编辑（REQ-005）</div>
"""

pages["界面4"] = page(
    "界面 4 · 商品发布与卖家商品管理模块",
    "发布表单覆盖必填字段（标题/描述/分类/成色/价格/图片/取货方式），提交前执行金额与重复提交校验；我的商品页按七种状态筛选，已预约商品锁定编辑并提示先处理预约。",
    [(phone(publish), "① 发布 / 编辑表单（校验状态）", "金额范围即时校验 + 取货方式选择"),
     (phone(myproducts), "② 我的商品（按状态筛选）", "七种状态标签 + 差异化操作")])

# ================= 界面 5：买家预约与交易 =================
reservations = """
<div class="navbar"><div class="back">‹</div><div class="t">我的预约</div></div>
<div style="display:flex;gap:12px;margin:6px 0 18px;flex-wrap:wrap;">
  <div class="chip on">全部 <span>4</span></div><div class="chip">待确认 <span>1</span></div>
  <div class="chip">已确认 <span>1</span></div><div class="chip">已完成 <span>1</span></div>
  <div class="chip">已取消</div>
</div>
<div class="card" style="padding:24px 26px;margin-bottom:20px;">
  <div class="list-row" style="padding:0 0 18px;">
    <div style="width:110px;height:110px;border-radius:18px;background:linear-gradient(135deg,#FFF1E0,#FFE3C2);
                display:flex;align-items:center;justify-content:center;font-size:44px;flex:none;">🎸</div>
    <div style="flex:1;">
      <div style="font-size:26px;font-weight:700;">民谣吉他 入门款</div>
      <div class="hint" style="margin-top:8px;">¥329 · 2026-10-22 14:08 预约</div>
    </div>
    <span class="pill p-reserved">待确认</span>
  </div>
  <div class="hint" style="margin-bottom:16px;">卖家确认交付前，您可随时取消预约，商品将恢复在售</div>
  <div style="display:flex;gap:16px;">
    <div class="btn btn-danger" style="flex:1;padding:16px 0;font-size:24px;">取消预约</div>
    <div class="btn btn-disabled" style="flex:1;padding:16px 0;font-size:24px;">等待卖家确认</div>
  </div>
</div>
<div class="card" style="padding:24px 26px;margin-bottom:20px;border:3px solid #FFE3C2;">
  <div class="list-row" style="padding:0 0 18px;">
    <div style="width:110px;height:110px;border-radius:18px;background:linear-gradient(135deg,#E9F9EF,#D2F2DE);
                display:flex;align-items:center;justify-content:center;font-size:44px;flex:none;">🛴</div>
    <div style="flex:1;">
      <div style="font-size:26px;font-weight:700;">电动滑板车 九号F25</div>
      <div class="hint" style="margin-top:8px;color:#149A52;">卖家已确认交付 ✓ 请线下验收后确认收货</div>
    </div>
    <span class="pill p-reserved">已确认</span>
  </div>
  <div class="btn btn-primary" style="padding:18px 0;font-size:25px;">✓ 确认收货</div>
</div>
<div class="card" style="padding:24px 26px;margin-bottom:20px;opacity:.85;">
  <div class="list-row" style="padding:0;">
    <div style="width:110px;height:110px;border-radius:18px;background:linear-gradient(135deg,#F1EDFC,#E4DCF9);
                display:flex;align-items:center;justify-content:center;font-size:44px;flex:none;">🎧</div>
    <div style="flex:1;">
      <div style="font-size:26px;font-weight:700;">索尼 WH-1000XM4</div>
      <div class="hint" style="margin-top:8px;">¥899 · 双方已确认，交易完成</div>
    </div>
    <span class="pill p-sold">已完成</span>
  </div>
</div>
<div class="hint" style="text-align:center;margin-bottom:36px;">仅显示本人发起的预约；确认收货需在卖家确认交付之后（REQ-009 / REQ-010）</div>
"""

resv_detail = """
<div class="navbar"><div class="back">‹</div><div class="t">预约详情</div></div>
<div class="card">
  <div class="list-row" style="padding:0 0 20px;border-bottom:2px solid #F1F3F7;">
    <div style="width:120px;height:120px;border-radius:18px;background:linear-gradient(135deg,#E9F9EF,#D2F2DE);
                display:flex;align-items:center;justify-content:center;font-size:48px;flex:none;">🛴</div>
    <div style="flex:1;">
      <div style="font-size:27px;font-weight:700;">电动滑板车 九号F25</div>
      <div class="hint" style="margin-top:8px;">¥1,050 · 卖家 骑行社 · 校内自取</div>
    </div>
    <span class="pill p-reserved">已确认</span>
  </div>
  <div style="font-size:25px;font-weight:800;margin:24px 0 20px;">交易进度</div>
  <div class="step" style="margin-bottom:22px;">
    <div class="dot" style="background:#E5F7EC;color:#149A52;">✓</div>
    <div><div style="font-size:24px;font-weight:700;">提交预约</div>
         <div class="hint">10-21 09:12 · 商品转为「已预约」（版本 v5→v6）</div></div>
  </div>
  <div class="step" style="margin-bottom:22px;">
    <div class="dot" style="background:#E5F7EC;color:#149A52;">✓</div>
    <div><div style="font-size:24px;font-weight:700;">卖家确认预约</div>
         <div class="hint">10-21 15:40 · 预约转为「已确认」</div></div>
  </div>
  <div class="step" style="margin-bottom:22px;">
    <div class="dot" style="background:#E5F7EC;color:#149A52;">✓</div>
    <div><div style="font-size:24px;font-weight:700;">卖家确认交付</div>
         <div class="hint">10-23 18:02 · 线下已完成交付</div></div>
  </div>
  <div class="step">
    <div class="dot" style="background:#FF9A55;color:#fff;">4</div>
    <div><div style="font-size:24px;font-weight:700;color:#FF5A1F;">买家确认收货（待您操作）</div>
         <div class="hint">确认后商品转为「已售出」，预约转为「已完成」</div></div>
  </div>
</div>
<div class="btn btn-primary" style="margin-top:30px;">✓ 确认收货并完成交易</div>
<div class="btn btn-disabled" style="margin-top:16px;">取消预约（卖家已确认交付，不可取消）</div>
<div class="hint" style="text-align:center;margin:20px 0 36px;">确认操作原子完成：商品 / 预约 / 日志任一写入失败将整体回滚（REQ-019）</div>
"""

pages["界面5"] = page(
    "界面 5 · 买家预约与交易确认模块",
    "按预约状态（待确认 / 已确认 / 已取消 / 已拒绝 / 已完成）展示本人预约与可用操作；预约详情以时间线呈现交易四步，收货确认按钮受“卖家已交付”前置约束。",
    [(phone(reservations), "① 我的预约（多状态列表）", "按状态筛选 + 差异化操作按钮"),
     (phone(resv_detail), "② 预约详情（交易时间线）", "四步进度 + 前置条件约束")])

# ================= 界面 6：卖家预约处理与交付 =================
seller_resv = """
<div class="navbar"><div class="back">‹</div><div class="t">收到的预约</div><div class="act">历史</div></div>
<div class="banner" style="background:#E6EFFF;color:#2C6BD8;margin-bottom:20px;">
  📩 您有 <b>2</b> 个待确认预约。确认前买家可随时取消；确认交付后不可再拒绝或取消。
</div>
<div class="card" style="padding:24px 26px;margin-bottom:20px;">
  <div class="list-row" style="padding:0 0 18px;">
    <div style="width:110px;height:110px;border-radius:18px;background:linear-gradient(135deg,#FFF1E0,#FFE3C2);
                display:flex;align-items:center;justify-content:center;font-size:44px;flex:none;">🎸</div>
    <div style="flex:1;">
      <div style="font-size:26px;font-weight:700;">民谣吉他 入门款</div>
      <div class="hint" style="margin-top:8px;">¥329 · 买家 小柯 · 10-22 14:08</div>
    </div>
    <span class="pill p-reserved">待确认</span>
  </div>
  <div style="display:flex;gap:16px;">
    <div class="btn btn-danger" style="flex:1;padding:16px 0;font-size:24px;">拒绝预约</div>
    <div class="btn btn-primary" style="flex:1;padding:16px 0;font-size:24px;">确认预约</div>
  </div>
</div>
<div class="card" style="padding:24px 26px;margin-bottom:20px;">
  <div class="list-row" style="padding:0 0 18px;">
    <div style="width:110px;height:110px;border-radius:18px;background:linear-gradient(135deg,#F1EDFC,#E4DCF9);
                display:flex;align-items:center;justify-content:center;font-size:44px;flex:none;">🎨</div>
    <div style="flex:1;">
      <div style="font-size:26px;font-weight:700;">数位板 Wacom 小号</div>
      <div class="hint" style="margin-top:8px;">¥210 · 买家 阿澈 · 10-22 09:31</div>
    </div>
    <span class="pill p-reserved">待确认</span>
  </div>
  <div style="display:flex;gap:16px;">
    <div class="btn btn-danger" style="flex:1;padding:16px 0;font-size:24px;">拒绝预约</div>
    <div class="btn btn-primary" style="flex:1;padding:16px 0;font-size:24px;">确认预约</div>
  </div>
</div>
<div class="hint" style="text-align:center;margin-bottom:36px;">确认/拒绝后商品与预约状态原子同步更新；拒绝使商品恢复在售（REQ-024 / REQ-009）</div>
"""

seller_deliver = """
<div class="navbar"><div class="back">‹</div><div class="t">交付确认</div></div>
<div class="card" style="padding:28px;">
  <div class="list-row" style="padding:0 0 20px;border-bottom:2px solid #F1F3F7;">
    <div style="width:110px;height:110px;border-radius:18px;background:linear-gradient(135deg,#E9F9EF,#D2F2DE);
                display:flex;align-items:center;justify-content:center;font-size:44px;flex:none;">🛴</div>
    <div style="flex:1;">
      <div style="font-size:26px;font-weight:700;">电动滑板车 九号F25</div>
      <div class="hint" style="margin-top:8px;">¥1,050 · 买家 鸣骏Max · 校内自取</div>
    </div>
    <span class="pill p-reserved">已确认</span>
  </div>
  <div style="font-size:25px;font-weight:800;margin:24px 0 8px;">双方确认进度</div>
  <div style="display:flex;gap:14px;margin:18px 0 10px;">
    <div style="flex:1;background:#E5F7EC;border-radius:18px;padding:18px;text-align:center;">
      <div style="font-size:34px;">✅</div><div style="font-size:22px;font-weight:700;color:#149A52;margin-top:6px;">您已确认交付</div>
      <div class="hint" style="font-size:19px;">10-23 18:02</div>
    </div>
    <div style="flex:1;background:#FFF7E8;border-radius:18px;padding:18px;text-align:center;">
      <div style="font-size:34px;">⏳</div><div style="font-size:22px;font-weight:700;color:#D98E04;margin-top:6px;">待买家确认收货</div>
      <div class="hint" style="font-size:19px;">等待对方操作</div>
    </div>
  </div>
  <div class="hint" style="margin-top:14px;">买家确认收货后：商品 →「已售出」，预约 →「已完成」（同一事务原子更新）</div>
</div>
<div class="banner" style="background:#EDF0F4;color:#69738A;margin-top:24px;">
  ℹ️ 您已确认交付，本预约不可再拒绝或取消；如线下出现问题请与买家协商后由买家操作。
</div>
<div class="card" style="margin-top:22px;padding:22px 26px;">
  <div style="font-size:24px;font-weight:800;margin-bottom:14px;">最近状态流转（自动记录）</div>
  <div class="hint" style="line-height:1.8;">
    10-21 09:12 · 买家预约成功 · 商品 在售→已预约 · v5→v6<br>
    10-21 15:40 · 您确认预约 · 预约 待确认→已确认<br>
    10-23 18:02 · 您确认交付 · 已写入交易确认记录
  </div>
</div>
<div class="hint" style="text-align:center;margin:24px 0 36px;">以上每次状态变化均写入操作日志，可供管理员追溯（REQ-014）</div>
"""

pages["界面6"] = page(
    "界面 6 · 卖家预约处理与交付确认模块",
    "待确认预约支持确认/拒绝两种处理；交付确认页以双方进度卡呈现“卖家交付 + 买家收货”双确认机制，确认交付后预约锁定，全部状态流转自动记录日志。",
    [(phone(seller_resv), "① 收到的预约（待处理）", "确认 / 拒绝 + 规则提示"),
     (phone(seller_deliver), "② 交付确认（双方进度）", "双确认进度卡 + 状态流转记录")])

# ================= 界面 7：个人中心与收藏 =================
profile = """
<div style="padding:26px 6px 0;display:flex;align-items:center;gap:24px;">
  <div style="width:128px;height:128px;border-radius:999px;background:linear-gradient(135deg,#FFD9BE,#FFB98C);
              display:flex;align-items:center;justify-content:center;font-size:58px;">🧑‍🎓</div>
  <div style="flex:1;">
    <div style="display:flex;align-items:center;gap:14px;">
      <span style="font-size:36px;font-weight:800;">鸣骏Max</span>
      <span class="pill p-review" style="font-size:19px;">买家</span>
      <span class="pill p-review" style="font-size:19px;background:#FFE9DA;color:#FF5A1F;">卖家</span>
    </div>
    <div class="hint" style="margin-top:10px;">手机号 138****6621 · 用户名可修改，允许重复</div>
  </div>
</div>
<div class="card" style="margin-top:26px;display:flex;padding:26px 0;">
  <div style="flex:1;text-align:center;border-right:2px solid #F1F3F7;">
    <div style="font-size:40px;font-weight:800;color:#171B26;">5</div><div class="hint">在售商品</div>
  </div>
  <div style="flex:1;text-align:center;border-right:2px solid #F1F3F7;">
    <div style="font-size:40px;font-weight:800;color:#171B26;">2</div><div class="hint">进行中预约</div>
  </div>
  <div style="flex:1;text-align:center;">
    <div style="font-size:40px;font-weight:800;color:#171B26;">9</div><div class="hint">收藏</div>
  </div>
</div>
<div class="card" style="margin-top:22px;padding:8px 26px;">
  <div class="list-row" style="border-bottom:2px solid #F1F3F7;">
    <span style="font-size:34px;">🏪</span><span style="flex:1;font-size:26px;font-weight:700;">我发布的商品</span><span class="hint">›</span>
  </div>
  <div class="list-row" style="border-bottom:2px solid #F1F3F7;">
    <span style="font-size:34px;">📮</span><span style="flex:1;font-size:26px;font-weight:700;">我发起的预约</span><span class="hint">›</span>
  </div>
  <div class="list-row" style="border-bottom:2px solid #F1F3F7;">
    <span style="font-size:34px;">❤️</span><span style="flex:1;font-size:26px;font-weight:700;">我的收藏</span><span class="hint">›</span>
  </div>
  <div class="list-row">
    <span style="font-size:34px;">✏️</span><span style="flex:1;font-size:26px;font-weight:700;">修改用户名</span><span class="hint">›</span>
  </div>
</div>
<div class="banner" style="background:#EDF0F4;color:#69738A;margin-top:22px;">
  ℹ️ 个人中心仅提供与交易直接相关的清单，不提供关注 / 粉丝 / 动态等社交功能（REQ-025）。
</div>
<div class="btn btn-gray" style="margin:26px 0 36px;">退出登录</div>
"""

favorites = """
<div class="navbar"><div class="back">‹</div><div class="t">我的收藏</div></div>
<div class="card" style="padding:10px 26px;">
  <div class="list-row" style="border-bottom:2px solid #F1F3F7;">
    <div style="width:120px;height:120px;border-radius:18px;background:linear-gradient(135deg,#E9F9EF,#D2F2DE);
                display:flex;align-items:center;justify-content:center;font-size:48px;flex:none;">📖</div>
    <div style="flex:1;">
      <div style="font-size:26px;font-weight:700;">算法导论 第三版 中文版</div>
      <div class="hint" style="margin-top:8px;">¥68 · 学长书店 · 99新</div>
      <div style="margin-top:10px;"><span class="pill p-sale">在售</span></div>
    </div>
    <div class="chip">♡ 取消</div>
  </div>
  <div class="list-row" style="border-bottom:2px solid #F1F3F7;">
    <div style="width:120px;height:120px;border-radius:18px;background:linear-gradient(135deg,#F1EDFC,#E4DCF9);
                display:flex;align-items:center;justify-content:center;font-size:48px;flex:none;">🎧</div>
    <div style="flex:1;">
      <div style="font-size:26px;font-weight:700;">索尼 WH-1000XM4</div>
      <div class="hint" style="margin-top:8px;">¥899 · 阿澈 · 95新</div>
      <div style="margin-top:10px;"><span class="pill p-sold">已售出</span></div>
    </div>
    <div class="chip">♡ 取消</div>
  </div>
  <div class="list-row">
    <div style="width:120px;height:120px;border-radius:18px;background:linear-gradient(135deg,#FFF1E0,#FFE3C2);
                display:flex;align-items:center;justify-content:center;font-size:48px;flex:none;">🖨️</div>
    <div style="flex:1;">
      <div style="font-size:26px;font-weight:700;">惠普喷墨打印机</div>
      <div class="hint" style="margin-top:8px;">¥150 · 打印室 · 8成新</div>
      <div style="margin-top:10px;"><span class="pill p-off">已下架</span></div>
    </div>
    <div class="chip" style="background:#F0F2F6;color:#B4BAC7;">♡ 取消</div>
  </div>
</div>
<div class="hint" style="text-align:center;margin:24px 0 36px;">
  商品售出 / 下架后收藏历史保留，状态实时同步（REQ-023）；<br>同一商品重复收藏不会产生第二条记录
</div>
"""

pages["界面7"] = page(
    "界面 7 · 个人中心与收藏模块",
    "个人中心聚合角色标签、交易统计与本人业务清单入口；收藏列表实时同步商品当前状态（在售可预约、已售出/已下架仅保留历史），不提供社交化功能。",
    [(phone(profile), "① 个人中心主页", "双角色标签 + 交易统计 + 业务清单入口"),
     (phone(favorites), "② 我的收藏（状态同步）", "收藏历史保留，状态实时同步")])

# ================= 界面 8：管理员工作台 =================
review = """
<div class="navbar"><div class="t">审核工作台</div><div class="hint">管理员 · 胡老师</div></div>
<div style="display:flex;gap:12px;margin:6px 0 18px;">
  <div class="chip on">待审核 <span>2</span></div><div class="chip">举报 <span>3</span></div>
  <div class="chip">日志</div><div class="chip">统计</div>
</div>
<div class="card" style="padding:24px 26px;margin-bottom:20px;">
  <div class="list-row" style="padding:0 0 16px;">
    <div style="width:110px;height:110px;border-radius:18px;background:linear-gradient(135deg,#E8F1FF,#D9E7FF);
                display:flex;align-items:center;justify-content:center;font-size:44px;flex:none;">💻</div>
    <div style="flex:1;">
      <div style="font-size:26px;font-weight:700;">iPad Air 5 95新 深空灰</div>
      <div class="hint" style="margin-top:8px;">¥2,399 · 卖家 阿明 · 10-22 提交</div>
    </div>
    <span class="pill p-review">待审核</span>
  </div>
  <div class="banner" style="background:#F7F8FA;color:#4A5264;margin-bottom:16px;">
    图片 4 张 · 描述完整 · 价格合法 · 非 60 秒重复提交 ✓
  </div>
  <div style="display:flex;gap:16px;">
    <div class="btn btn-danger" style="flex:1;padding:16px 0;font-size:24px;">驳回</div>
    <div class="btn btn-primary" style="flex:1;padding:16px 0;font-size:24px;">通过并上架</div>
  </div>
</div>
<div class="card" style="padding:24px 26px;margin-bottom:20px;border:3px solid #F3B9B9;">
  <div class="list-row" style="padding:0 0 16px;">
    <div style="width:110px;height:110px;border-radius:18px;background:linear-gradient(135deg,#FCEBEB,#F8D9D9);
                display:flex;align-items:center;justify-content:center;font-size:44px;flex:none;">🎫</div>
    <div style="flex:1;">
      <div style="font-size:26px;font-weight:700;">演唱会门票两张（代排）</div>
      <div class="hint" style="margin-top:8px;">¥1,800 · 卖家 黄牛一号 · 10-22 提交</div>
    </div>
    <span class="pill p-review">待审核</span>
  </div>
  <div class="i-label" style="margin-top:0;color:#D23030;">驳回原因（必填）</div>
  <input class="input error" value="疑似违规代拍，不符合平台规则">
  <div style="display:flex;gap:16px;margin-top:18px;">
    <div class="btn btn-gray" style="flex:1;padding:16px 0;font-size:24px;">取消</div>
    <div class="btn btn-danger" style="flex:1;padding:16px 0;font-size:24px;">确认驳回</div>
  </div>
  <div class="hint" style="margin-top:12px;">驳回后商品退回「草稿」，卖家修改后可重新提交</div>
</div>
<div class="hint" style="text-align:center;margin-bottom:36px;">仅管理员可审核；非待审核状态商品不可进入审核流（REQ-004）</div>
"""

admin_ops = """
<div class="navbar"><div class="t">举报 · 日志 · 统计</div><div class="hint">管理员</div></div>
<div style="display:flex;gap:12px;margin:6px 0 18px;">
  <div class="chip">审核</div><div class="chip on">举报 <span>3</span></div>
  <div class="chip">日志</div><div class="chip">统计</div>
</div>
<div class="card" style="padding:24px 26px;margin-bottom:20px;">
  <div style="display:flex;align-items:center;gap:14px;margin-bottom:14px;">
    <span style="font-size:34px;">🚩</span><span style="font-size:26px;font-weight:800;">待处理举报</span>
    <span class="pill p-violation" style="margin-left:auto;">待处理</span>
  </div>
  <div style="font-size:24px;font-weight:700;">演唱会门票两张（代排）</div>
  <div class="hint" style="margin:10px 0 16px;">举报人 匿名用户 · 原因：疑似黄牛代拍 · 10-22 21:40 提交<br>该用户对同一商品无其他待处理举报 ✓</div>
  <div style="display:flex;gap:16px;">
    <div class="btn btn-gray" style="flex:1;padding:16px 0;font-size:24px;">驳回举报</div>
    <div class="btn btn-danger" style="flex:1;padding:16px 0;font-size:24px;">确认违规并下架</div>
  </div>
</div>
<div class="card" style="padding:24px 26px;margin-bottom:20px;">
  <div style="display:flex;align-items:center;gap:14px;margin-bottom:18px;">
    <span style="font-size:34px;">📊</span><span style="font-size:26px;font-weight:800;">商品统计</span>
  </div>
  <div style="display:flex;gap:14px;">
    <div style="flex:1;background:#F5F6FA;border-radius:18px;padding:16px;text-align:center;">
      <div style="font-size:32px;font-weight:800;">156</div><div class="hint" style="font-size:19px;">全部商品</div>
    </div>
    <div style="flex:1;background:#E5F7EC;border-radius:18px;padding:16px;text-align:center;">
      <div style="font-size:32px;font-weight:800;color:#149A52;">89</div><div class="hint" style="font-size:19px;">在售</div>
    </div>
    <div style="flex:1;background:#FFF0E0;border-radius:18px;padding:16px;text-align:center;">
      <div style="font-size:32px;font-weight:800;color:#E0741F;">12</div><div class="hint" style="font-size:19px;">已预约</div>
    </div>
    <div style="flex:1;background:#EDF0F4;border-radius:18px;padding:16px;text-align:center;">
      <div style="font-size:32px;font-weight:800;color:#69738A;">32</div><div class="hint" style="font-size:19px;">已售出</div>
    </div>
  </div>
  <div class="hint" style="margin-top:14px;">按分类：数码 45 · 图书 38 · 生活 31 · 运动 27 · 票券 15（空分组计 0）</div>
</div>
<div class="card" style="padding:24px 26px;">
  <div style="display:flex;align-items:center;gap:14px;margin-bottom:14px;">
    <span style="font-size:34px;">🗂️</span><span style="font-size:26px;font-weight:800;">操作日志查询</span>
  </div>
  <div style="display:flex;gap:12px;margin-bottom:14px;flex-wrap:wrap;">
    <div class="chip">操作者</div><div class="chip">对象类型</div><div class="chip">操作类型</div><div class="chip on">时间段</div>
  </div>
  <div class="hint" style="line-height:1.9;border-top:2px solid #F1F3F7;padding-top:14px;">
    10-23 18:02 · 卖家 骑行社 · 确认交付 · 滑板车 · <b style="color:#149A52;">成功</b><br>
    10-22 14:08 · 买家 小柯 · 发起预约 · 民谣吉他 · <b style="color:#149A52;">成功</b><br>
    10-22 14:09 · 买家 阿澈 · 发起预约 · 民谣吉他 · <b style="color:#D23030;">失败（已被预约）</b>
  </div>
</div>
<div class="hint" style="text-align:center;margin:22px 0 36px;">非管理员访问统计 / 日志被拒绝；成功与失败的关键操作均被记录（REQ-015 / REQ-016）</div>
"""

pages["界面8"] = page(
    "界面 8 · 管理员工作台模块（审核 / 举报 / 日志 / 统计）",
    "审核页执行「通过上架 / 驳回退草稿」决策，驳回必填原因；运营页处理举报（驳回或违规下架）、按状态与分类查看统计、按四类条件检索成功与失败的操作日志。",
    [(phone(review), "① 商品审核", "通过 / 驳回决策 + 驳回原因必填"),
     (phone(admin_ops), "② 举报 · 统计 · 日志", "单层处置 + 汇总统计 + 日志检索")])

for name, html in pages.items():
    with open(os.path.join(OUT, f"{name}.html"), "w", encoding="utf-8") as f:
        f.write(html)
    print("written", name)
