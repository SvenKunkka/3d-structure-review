# 3D 结构图档评审 Skill

一个可复用的 Codex Skill：结合产品配置与本机 CAD，对 STEP/STP 或原生装配进行结构、开模前和注塑风险评审，并交付可追溯的报告与问题关闭清单。受力仿真、成品可靠性分析按用户当次要求启用。

**A Codex Skill for evidence-based structural and pre-tooling review of native CAD and STEP/STP assemblies.** Injection analysis, simulation, and reliability are selected according to the current request.

## 能做什么

- 核对输入版本、配置表、零件层级、单位与装配位姿。
- 使用本机 CAD 检查实体有效性、名义干涉、间隙、局部壁厚和关键剖面。
- 识别注塑厚薄区、筋柱、拔模、包胶及可能的成型风险，写明还需哪些模具和试模证据。
- 按需组织受力仿真与可靠性验证；明确材料、载荷、边界、试验条件及结论范围。
- 输出带对象位置、测量方法、复核结果和关闭条件的可编辑报告。

Skill 是评审流程和证据规则。它不会自行提供材料牌号、模具方案、载荷或求解器，也不会把局部几何测量当作模流或实物测试结果。

## 安装

将仓库作为一个完整目录放入 Codex 的 skills 目录：

```bash
git clone https://github.com/SvenKunkka/3d-structure-review.git
mkdir -p ~/.codex/skills
cp -R 3d-structure-review ~/.codex/skills/
```

如果本机已有同名 Skill，先检查并备份现有内容，再替换。入口是 [`SKILL.md`](SKILL.md)，可通过 `$3d-structure-review` 明确调用。`agents/openai.yaml` 设置了“3D结构图档评审”的显示名称，默认允许自动发现。

示例请求：

> 使用 $3d-structure-review，结合配置表和本机 CAD 评审这个 STEP 图档。本轮只做结构件注塑分析，输出 Word、PDF 和问题关闭清单。

## 文件

| 位置 | 内容 |
|---|---|
| [`SKILL.md`](SKILL.md) | 选择评审范围、执行顺序、独立复核与交付边界 |
| [`references/`](references/) | CAD、结构装配、注塑、仿真/可靠性、报告交付的按需参考 |
| [`scripts/source_guard.py`](scripts/source_guard.py) | 用标准库记录及核对输入文件的 SHA-256；不修改输入文件 |

输入文件基线工具：

```bash
python3 scripts/source_guard.py snapshot --manifest review/evidence/input_manifest.json --files model.stp requirements.xlsx
python3 scripts/source_guard.py verify --manifest review/evidence/input_manifest.json
```

上述工具只核对文件字节是否变化。真正的 CAD 导入、几何测量、图片检查与报告验收按 Skill 指引完成。

## 来源与边界

本 Skill 提炼自一次实际 CAD 结构及注塑评审，但不包含该产品的图档、配置表、面号、测量结果或私有报告。项目结论必须从当次输入重新核验。

许可证：[MIT](LICENSE)。
