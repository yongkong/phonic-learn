# 设计系统主文件（MASTER）

> **读取逻辑**：构建某个具体页面时，先检查 `design-system/pages/[页面名].md`。若存在，其规则**覆盖**本主文件；若不存在，严格遵循以下规则。

---

**项目**：WordWorld 单词世界
**版本**：v2（2026-09-30 修订，v1 黏土拟物风已废弃）
**类别**：儿童学习（小学英语单词）
**目标用户**：7-12 岁学童（明确排除低龄幼儿园向视觉）
**主题**：Confident Play（自信游戏风）

> **v2 修订原因**：v1 黏土拟物（Claymorphism）+ Comic Neue 观感偏幼儿园，与 7+ 用户的自我认知不符。v2 保留游戏化机制（等级、金币、地图、勋章），视觉语言转为饱和克制、干净立体。

---

## 全局规则

### 色彩系统

| 角色 | 色值 | CSS 变量 |
|------|------|----------|
| 主色（自信靛蓝） | `#4F46E5` | `--color-primary` |
| 主色深（按钮底边） | `#4338CA` | `--color-primary-dark` |
| 主色浅底 | `#EEF2FF` | `--color-primary-soft` |
| 主色上文字 | `#FFFFFF` | `--color-on-primary` |
| 强调色（活力橙） | `#F97316` | `--color-accent` |
| 强调色深 | `#C2410C` | `--color-accent-dark` |
| 强调色上文字 | `#FFFFFF` | `--color-on-accent` |
| 成功色 | `#10B981` | `--color-success` |
| 危险/错误 | `#DC2626` | `--color-destructive` |
| 页面背景 | `#EEF2FF` | `--color-background` |
| 卡片 | `#FFFFFF` | `--color-card` |
| 主文字 | `#1E1B4B` | `--color-foreground` |
| 次级文字 | `#4E4B77` | `--color-muted-foreground` |
| 边框 | `#E2E5F5` | `--color-border` |
| 焦点环 | `#4F46E5` | `--color-ring` |

**色彩基调**：靛蓝 + 活力橙——饱和、自信、电竞感的大孩子配色；禁止大面积粉彩糖果色。

### 自然拼读语义色（本项目硬约束，教学功能色）

这组颜色承载"五维记忆法 · 形"的教学语义，**不随风格偏好更改语义**，只允许微调色值以保持与新主题协调：

| 角色 | 色值 | CSS 变量 |
|------|------|----------|
| 元音字母 | `#FF6B6B` | `--vowel` |
| 辅音字母 | `#4F46E5`（跟随主色） | `--consonant` |
| 静音字母 | `#9CA3AF` | `--silent` |
| 音节分隔 | `#F59E0B` | `--syllable-sep` |

注意：元音红 `#FF6B6B`（珊瑚红，用于字母着色）与错误红 `#DC2626`（仅用于错误反馈）必须保持可区分。

### 字体

- **英文展示字体（标题、单词大字、数字）**：Baloo 2 —— 圆润厚重但干练，适合字母块与游戏数值
- **英文/界面正文字体**：Nunito —— 圆角无衬线，类似 Duolingo 的亲和力，阅读效率高；**不使用** Comic Neue / Comic Sans（低龄感）
- **中文字体**：系统字体栈（PingFang SC / Microsoft YaHei）；单词中文注释可用楷体强调
- **气质**：自信、游戏、进阶、友好、利落

```css
@import url('https://fonts.googleapis.com/css2?family=Baloo+2:wght@500;600;700;800&family=Nunito:wght@400;600;700;800&display=swap');
```

> 小程序端注意：微信小程序不支持 wxss 远程 @import 字体，需改用 `wx.loadFontFace` 或打包字体子集；未加载时回退到系统字体。

### 间距（8px 栅格）

| 令牌 | 值 | 用途 |
|------|-----|------|
| `--space-xs` | `4px` | 紧凑间隙 |
| `--space-sm` | `8px` | 图标间距、行内间距 |
| `--space-md` | `12px` | 卡片间距 |
| `--space-lg` | `16px` | 标准内边距 |
| `--space-xl` | `20px` | 页面内边距 |
| `--space-2xl` | `24px` | 模块间距 |
| `--space-3xl` | `32px` | 大间距 |

### 圆角、阴影与"实体感"

| 令牌 | 值 | 用途 |
|------|-----|------|
| `--radius-sm/md/lg/xl` | `10 / 14 / 18 / 24px` | 圆角阶梯 |
| `--shadow-sm/md/lg` | 靛黑色调柔和投影 | 卡片、弹层的干净立体感 |
| `--edge-primary` | `0 3px 0 0 var(--primary-dark)` | 游戏实体按钮的"底边" |
| `--edge-accent` | `0 3px 0 0 var(--accent-dark)` | 橙色按钮底边 |
| 按压反馈 | `translateY(2px)` + 底边变薄 | **下沉**，不缩放、不位移邻居 |

> v1 的黏土双重内阴影（inset 高光/暗影）已废弃；v2 的立体感来自按钮底边（hard edge）+ 柔和外投影。

---

## 组件规范

### 按钮（游戏实体按钮）

```css
.btn-primary {
  background: var(--primary);
  color: #FFFFFF;
  padding: 14px 28px;
  border-radius: var(--radius-pill);
  box-shadow: 0 3px 0 0 var(--primary-dark); /* 实体底边 */
  font-weight: 800;
  transition: transform 200ms ease-out, box-shadow 200ms ease-out;
}

.btn-primary:active {
  transform: translateY(2px);      /* 按下去 */
  box-shadow: 0 1px 0 0 var(--primary-dark); /* 底边变薄 */
}
```

### 卡片

```css
.card {
  background: var(--surface);
  border-radius: var(--radius-lg);   /* 18px */
  padding: 16px;
  border: 1px solid var(--border);
  box-shadow: 0 1px 2px rgba(30,27,75,.05), 0 2px 8px rgba(30,27,75,.06);
}
```

### 输入框

```css
.input {
  padding: 14px 16px;
  border: 2px solid var(--border-strong);
  border-radius: var(--radius-md);
  font-size: 16px;
  font-weight: 600;
}

.input:focus {
  border-color: var(--primary);
  outline: none;
  box-shadow: 0 0 0 4px rgba(79, 70, 229, 0.14);
}
```

### 弹窗

```css
.modal-overlay {
  background: rgba(30, 27, 75, 0.45);
  backdrop-filter: blur(4px);
}

.modal {
  background: var(--surface);
  border-radius: var(--radius-xl); /* 24px */
  padding: 28px;
  box-shadow: 0 12px 32px rgba(30, 27, 75, 0.16);
  max-width: 500px;
  width: 90%;
}
```

### 图标

- 一律使用**线性 SVG 图标**（Lucide 风格：stroke 2-2.4px、圆帽、圆角连接），同层级线性和填充不混用
- 禁止 emoji 充当图标
- 品牌插画（场景图、水果道具）用扁平几何 SVG，色值取自色板

---

## 风格指南

**主题**：Confident Play（自信游戏风）

**关键词**：游戏化、干净立体、饱和克制、实体按钮、利落圆角、大孩子气质

**最适用于**：7+ 教育应用、答题闯关、成长激励系统、轻竞技

**动效基调**（标准档）：入场 300-450ms fade + 轻位移；正确反馈 pop 回弹；错误反馈 shake；进度条平滑增长；尊重 `prefers-reduced-motion`。

---

## 反模式（禁止使用）

- ❌ 粉彩糖果色 / 大面积马卡龙色块（低龄感）
- ❌ Comic Sans / Comic Neue 等低龄字体
- ❌ emoji 当图标 —— 一律用线性 SVG
- ❌ 黏土内阴影、球状膨胀（v1 已废弃）
- ❌ 可点元素缺少按压反馈 —— 实体按钮必须"按下去"
- ❌ 布局位移式悬停 —— 避免引起周围内容跳动
- ❌ 低对比度文字 —— 正文对比度至少 4.5:1
- ❌ 瞬变状态切换 —— 一律使用 150-300ms 过渡
- ❌ 不可见的焦点态 —— 键盘/无障碍焦点必须可见

---

## 本项目附加约束（儿童产品）

- **触控目标**：iOS ≥ 44pt / Android ≥ 48dp（小程序用 rpx 折算），相邻可点元素间距 ≥ 8px
- **正文行高**：1.5-1.8
- **字号偏大**：正文不小于 16px，单词展示 48-64px
- **图标风格**：同一层级内填充/线性统一；圆角风格与整体协调
- **色彩不是唯一信息载体**：状态必须同时有文字或形状提示（对错配 ✓/✗ 图标）
- **游戏数值可见**：等级、XP、金币、连击天数等成长信息要显性展示，激励 7+ 用户持续进阶

## 交付前检查清单

- [ ] 没有用 emoji 充当图标（改用 SVG）
- [ ] 图标来自同一图标集、同一描边风格
- [ ] 所有可点元素有按压反馈（下沉 2px）
- [ ] 触控目标 ≥ 44pt，间距 ≥ 8px
- [ ] 正文对比度 ≥ 4.5:1
- [ ] 焦点态可见，支持键盘导航
- [ ] 尊重 `prefers-reduced-motion`
- [ ] 自然拼读语义色未被风格覆盖
- [ ] 375px 小屏与横屏下无布局破损、无横向滚动
- [ ] 固定导航栏（tabBar）不遮挡内容
