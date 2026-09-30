// tabBar 图标生成脚本：Lucide 风格线性 SVG（MASTER v2）→ 81×81 PNG（微信 tabBar 推荐尺寸）
// 幂等：重跑直接覆盖。改图标只需改 ICONS 表后 `node scripts/gen-tab-icons.mjs`。
import { mkdir, writeFile } from 'node:fs/promises'
import path from 'node:path'
import sharp from 'sharp'

const OUT_DIR = path.resolve(process.cwd(), 'src/static/tab')
const SIZE = 81 // 微信小程序 tabBar 图标推荐 81×81，同时满足 H5 3x retina
const STROKE = 2.2

// MASTER v2 色板
const COLORS = {
  inactive: '#767397', // --fg-tertiary
  active: '#4F46E5', // --primary / selectedColor
}

// 四个 tab 的 Lucide 路径（stroke 2.2、圆帽、圆角连接）
const ICONS = {
  // 学习：翻开的书
  study: [
    'M12 7v14',
    'M3 18a1 1 0 0 1-1-1V4a1 1 0 0 1 1-1h5a4 4 0 0 1 4 4 4 4 0 0 1 4-4h5a1 1 0 0 1 1 1v13a1 1 0 0 1-1 1h-5a4 4 0 0 0-4 4 4 4 0 0 0-4-4z',
  ],
  // 练习：铅笔
  practice: [
    'M17 3a2.85 2.83 0 1 1 4 4L7.5 20.5 2 22l1.5-5.5z',
    'm15 5 4 4',
  ],
  // 作文：文稿
  essay: [
    'M15 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V7z',
    'M14 2v4a2 2 0 0 0 2 2h4',
    'M10 9H8',
    'M16 13H8',
    'M16 17H8',
  ],
  // 我的：单人
  profile: [
    'M19 21v-2a4 4 0 0 0-4-4H9a4 4 0 0 0-4 4v2',
    'M12 11a4 4 0 1 0 0-8 4 4 0 0 0 0 8z',
  ],
}

function svgFor(paths, color) {
  const body = paths.map((p) => `<path d="${p}"/>`).join('')
  return `<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg" width="${SIZE}" height="${SIZE}" viewBox="0 0 24 24"
     fill="none" stroke="${color}" stroke-width="${STROKE}" stroke-linecap="round" stroke-linejoin="round">
  ${body}
</svg>
`
}

async function main() {
  await mkdir(OUT_DIR, { recursive: true })
  let count = 0
  for (const [name, paths] of Object.entries(ICONS)) {
    for (const [variant, color] of Object.entries(COLORS)) {
      const svg = svgFor(paths, color)
      const base = variant === 'active' ? `${name}-active` : name
      await writeFile(path.join(OUT_DIR, `${base}.svg`), svg, 'utf8')
      await sharp(Buffer.from(svg), { density: 300 }).png().toFile(path.join(OUT_DIR, `${base}.png`))
      count++
    }
  }
  console.log(`generated ${count} tab icons (${SIZE}x${SIZE}) in ${path.relative(process.cwd(), OUT_DIR)}`)
}

main().catch((e) => {
  console.error(e)
  process.exit(1)
})
