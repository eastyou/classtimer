# classtimer

[![CI](https://github.com/eastyou/classtimer/actions/workflows/ci.yml/badge.svg)](https://github.com/eastyou/classtimer/actions/workflows/ci.yml)
[![License: MIT](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)
[![Python](https://img.shields.io/badge/python-3.9%2B-brightgreen.svg)](pyproject.toml)

给课堂用的全屏倒计时：生成一个单文件 HTML，双击就能用，带 1/3/5/10 分钟预设、开始/暂停/重置、结束提示音和键盘快捷键。**零依赖，不联网，不需要安装任何软件。**

上课做练习、小组讨论、测验时，投屏一个醒目的大号倒计时，比反复看手机更方便。老师也可以把预设改成自己的课堂节奏。

## 特性

- **大号显示**：自适应屏幕，投屏后远处也能看清
- **预设时间**：默认 1、3、5、10 分钟，可自定义
- **开始 / 暂停 / 继续 / 重置**：暂停后继续，不会丢时间
- **结束提醒**：数字变红闪烁，并用 Web Audio 发出三声提示音，不需要音频文件
- **键盘操作**：空格开始/暂停，`R` 重置，数字键 `1~9` 选择预设
- **单文件离线**：所有 CSS 和 JS 都内嵌，断网也能用
- **17 个单元测试**：预设解析、HTML 输出与命令行

## 安装

```bash
pip install "git+https://github.com/eastyou/classtimer.git"
```

或者不安装，直接运行：

```bash
git clone https://github.com/eastyou/classtimer.git
cd classtimer
python3 -m classtimer -o timer.html
```

## 快速开始

```console
$ classtimer -o 课堂计时.html
已生成 课堂计时.html：预设 1、3、5、10 分钟
```

双击打开，按 `F11` 进入全屏（macOS 用 `Ctrl + Cmd + F`），点击预设时间，再按空格开始。

自定义预设和标题：

```console
$ classtimer -o 英语课计时.html --presets 2,5,15 --title 英语课堂
已生成 英语课计时.html：预设 2、5、15 分钟
```

## 参数

| 参数 | 说明 |
| --- | --- |
| `-o, --output` | 输出文件，默认 `timer.html` |
| `--title` | 页面标题，默认「课堂计时」 |
| `--presets` | 预设分钟数，逗号分隔，默认 `1,3,5,10` |

预设规则：

- 每个预设为 1~180 的整数分钟
- 最多 9 个预设（对应数字键 1~9）
- 重复的预设会自动去重

### 退出码

| 退出码 | 含义 |
| --- | --- |
| `0` | 成功 |
| `1` | 文件写入失败 |
| `2` | 参数不合法 |

## 使用建议

- 投屏时把浏览器缩放调到 100%，全屏后效果最好
- 结束提示音依赖浏览器音频权限；点击过「开始」后一般即可正常播放
- 页面只在本机运行，不请求任何网络资源，也不会上传任何数据

## 说明与边界

- 计时基于系统时间差，电脑休眠后恢复时可能直接跳到剩余时间，属于预期行为
- 提示音使用 Web Audio 实时合成，部分浏览器在静音模式下不会发声
- 页面没有暂停历史记录，刷新后回到第一个预设

## 常见问题

**需要联网吗？**
不需要。HTML 里没有任何外部链接。

**可以放到教室电脑上吗？**
可以，直接把生成的 HTML 拷到 U 盘，双击打开即可。

**能改成考试专用的大屏吗？**
把预设改成 `--presets 45,60,90`，再按 `F11` 全屏即可。

## 开发与测试

```bash
python3 -m unittest discover -s tests -v
```

CI 覆盖 Python 3.9 ~ 3.13 与 Linux/macOS/Windows；计时器本身在浏览器中运行，CI 负责校验页面结构与预设注入。

## License

[MIT](LICENSE) © 2026 eastyou
