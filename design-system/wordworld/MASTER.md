# 设计系统主文件（MASTER）

> **读取逻辑**：构建某个具体页面时，先检查 `design-system/pages/[页面名].md`。若存在，其规则**覆盖**本主文件；若不存在，严格遵循以下规则。

---

**项目**：WordWorld 单词世界
**生成时间**：2026-09-30
**类别**：儿童学习（小学英语单词）
**主题**：Claymorphism（黏土拟物风）

---

## 全局规则

### 色彩系统

| 角色 | 色值 | CSS 变量 |
|------|------|----------|
| 主色（学习蓝） | `#2563EB` | `--color-primary` |
| 主色上文字 | `#FFFFFF` | `--color-on-primary` |
| 辅助色（活力琥珀） | `#F59E0B` | `--color-secondary` |
| 辅助色上文字 | `#0F172A` | `--color-on-secondary` |
| 强调色（趣味粉） | `#EC4899` | `--color-accent` |
| 强调色上文字 | `#000000` | `--color-on-accent` |
| 页面背景 | `#EFF6FF` | `--color-background` |
| 主文字 | `#0F172A` | `--color-foreground` |
| 卡片 | `#FFFFFF` | `--color-card` |
| 卡片文字 | `#0F172A` | `--color-card-foreground` |
| 弱化底色 | `#F1F5FD` | `--color-muted` |
| 弱化文字 | `#475569` | `--color-muted-foreground` |
| 边框 | `#E4ECFC` | `--color-border` |
| 危险/错误 | `#DC2626` | `--color-destructive` |
| 危险色上文字 | `#FFFFFF` | `--color-on-destructive` |
| 焦点环 | `#2563EB` | `--color-ring` |

**色彩基调**：学习蓝 + 活力琥珀 + 趣味粉——饱和、明快、有能量。

### 自然拼读语义色（本项目硬约束，教学功能色）

这组颜色承载"五维记忆法 · 形"的教学语义，**不随风格偏好更改语义**，只允许微调色值以保持与新主题协调：

| 角色 | 色值 | CSS 变量 |
|------|------|----------|
| 元音字母 | `#FF6B6B` | `--vowel` |
| 辅音字母 | `#2563EB` | `--consonant` |
| 静音字母 | `#999999` | `--silent` |
| 音节分隔 | `#F59E0B` | `--syllable-sep` |

注意：元音红 `#FF6B6B` 与错误红 `#DC2626` 必须保持可区分（前者珊瑚红用于字母着色，后者深红仅用于错误反馈）。

### 字体

- **英文展示字体（标题、单词大字）**：Baloo 2 —— 圆润厚重，适合拼读字母块
- **英文正文字体（例句）**：Comic Neue —— Comic Sans 的现代化升级版
- **中文字体**：思源黑体（正文）、楷体（单词中文注释）、站酷快乐体（场景标题）；依赖系统字体栈，不在线加载中文字体
- **气质**：儿童、教育、活泼、友好、多彩、学习

```css
@import url('https://fonts.googleapis.com/css2?family=Baloo+2:wght@400;500;600;700&family=Comic+Neue:wght@300;400;700&display=swap');
```

> 小程序端注意：微信小程序不支持 wxss 远程 @import 字体，需改用 `wx.loadFontFace` 或打包字体子集；未加载时回退到 Comic Sans MS / 系统字体。

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

### 阴影与黏土效果（Claymorphism 核心特征）

| 令牌 | 值 | 用途 |
|------|-----|------|
| `--shadow-sm` | `0 1px 3px rgba(0,0,0,0.06)` | 轻微抬升 |
| `--shadow-md` | `0 4px 12px rgba(0,0,0,0.08)` | 卡片、按钮 |
| `--shadow-lg` | `0 8px 24px rgba(0,0,0,0.12)` | 弹层 |
| `--shadow-clay` | 内高光 + 内暗影 + 外投影（三重，见令牌文件） | 黏土卡片的立体感 |
| `--clay-border-width` | `3px` | 黏土元素粗描边 |
| `--clay-press` | `200ms ease-out` | 按压软反馈 |

---

## 组件规范

### 按钮（黏土胶囊）

```css
/* 主按钮：趣味粉或学习蓝，胶囊圆角，粗描边 + 黏土阴影 */
.btn-primary {
  background: var(--primary);
  color: #FFFFFF;
  padding: 14px 28px;
  border-radius: var(--radius-xl); /* 24px 胶囊 */
  border: var(--clay-border-width) solid var(--primary-dark);
  box-shadow: var(--clay-shadow-sm);
  font-weight: 700;
  transition: transform var(--clay-press), box-shadow var(--clay-press);
  cursor: pointer;
}

.btn-primary:active {
  transform: translateY(2px);   /* 软按压：下沉而不缩放 */
  box-shadow: var(--shadow-sm);
}

/* 次级按钮：描边样式 */
.btn-secondary {
  background: var(--surface);
  color: var(--primary);
  border: 3px solid var(--primary);
  padding: 14px 28px;
  border-radius: var(--radius-xl);
  font-weight: 700;
}
```

### 卡片（黏土块）

```css
.card {
  background: var(--surface);
  border-radius: var(--radius-lg); /* 16px */
  padding: 20px;
  border: var(--clay-border-width) solid var(--border);
  box-shadow: var(--clay-shadow);
  transition: transform 200ms ease-out, box-shadow 200ms ease-out;
}

.card:active {
  transform: translateY(2px);
  box-shadow: var(--shadow-md);
}
```

### 输入框

```css
.input {
  padding: 14px 18px;
  border: 3px solid var(--border);
  border-radius: var(--radius-md); /* 12px */
  background: var(--surface);
  font-size: 16px;
  transition: border-color 200ms ease-out;
}

.input:focus {
  border-color: var(--primary);
  outline: none;
  box-shadow: 0 0 0 3px rgba(37, 99, 235, 0.15);
}
```

### 弹窗

```css
.modal-overlay {
  background: rgba(15, 23, 42, 0.45);
  backdrop-filter: blur(4px);
}

.modal {
  background: var(--surface);
  border-radius: var(--radius-xl); /* 24px，黏土大圆角 */
  padding: 28px;
  border: var(--clay-border-width) solid var(--border);
  box-shadow: var(--shadow-xl);
  max-width: 500px;
  width: 90%;
}
```

---

## 风格指南

**主题**：Claymorphism（黏土拟物）

**关键词**：软 3D、厚重圆润、玩具感、活泼、泡泡感、粗描边（3-4px）、双重柔和阴影、大圆角（16-24px）

**最适用于**：教育应用、儿童应用、创意工具、轻松游戏

**关键效果**：内外双重阴影（柔和、无硬边线）、软按压反馈（200ms ease-out）、元素蓬松感、平滑过渡

**动效基调**（标准档）：列表入场可用 300-450ms stagger + `back.out(1.4)` 回弹缓动（像果冻一样Q弹）；数据密集处不用回弹。

> 生成结果中附带的"Trust & Authority + Conversion"落地页模式（Hero/社会证明/销售转化）面向 B2B 营销站，与本 App 无关，**不采用**。

---

## 反模式（禁止使用）

- ❌ 灰暗低饱和的颜色
- ❌ 毫无能量的静态界面
- ❌ **emoji 当图标** —— 一律用 SVG 图标（Lucide/Heroicons）
- ❌ **可点元素缺少按压反馈** —— 触摸软按压（下沉 2px + 阴影收缩）
- ❌ **布局位移式悬停** —— 避免引起周围内容跳动的变换
- ❌ **低对比度文字** —— 正文对比度至少 4.5:1
- ❌ **瞬变状态切换** —— 一律使用 150-300ms 过渡
- ❌ **不可见的焦点态** —— 键盘/无障碍焦点必须可见

---

## 本项目附加约束（儿童产品）

- **触控目标**：iOS ≥ 44pt / Android ≥ 48dp（小程序用 rpx 折算），相邻可点元素间距 ≥ 8px
- **正文行高**：1.5-1.75
- **字号偏大**：面向 6-12 岁儿童，正文不小于 16px，单词展示 48-72px
- **图标风格**：同一层级内填充/线性风格统一，圆角风格图标（与黏土风协调）
- **色彩不是唯一信息载体**：状态必须同时有文字或形状提示（如对错除了颜色还要有 ✓/✗ 图标）

## 交付前检查清单

- [ ] 没有用 emoji 充当图标（改用 SVG）
- [ ] 图标来自同一图标集、同一风格
- [ ] 所有可点元素有按压反馈（软按压 200ms）
- [ ] 触控目标 ≥ 44pt，间距 ≥ 8px
- [ ] 正文对比度 ≥ 4.5:1
- [ ] 焦点态可见，支持键盘导航
- [ ] 尊重 `prefers-reduced-motion`
- [ ] 自然拼读语义色未被风格覆盖
- [ ] 375px 小屏与横屏下无布局破损、无横向滚动
- [ ] 固定导航栏（tabBar）不遮挡内容
