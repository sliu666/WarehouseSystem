# WarehouseSystem PR 审查演示

这是一个仅使用 Python 标准库的内存库存示例，每次运行后库存不会保留。

```powershell
python warehouse.py --receive 10 --ship 3
python -m unittest -v test_warehouse
```

## 配置 GitHub Actions

在 GitHub 仓库 **Settings → Secrets and variables → Actions** 中设置：

| 类型 | 名称 | 值 |
|---|---|---|
| Secret | `OCR_LLM_TOKEN` | 模型服务的访问令牌或 API Key |
| Variable | `OCR_LLM_URL` | 已验证的 Azure OpenAI Responses 端点，例如 `https://<resource>.services.ai.azure.com/openai/v1` |
| Variable | `OCR_LLM_MODEL` | Azure 模型部署名 |

先使用相同的模型配置运行 `ocr llm test`；不同端点的认证方式、协议和请求字段可能不同，按实际情况调整工作流。不要提交令牌。如果端点地址敏感，也应保存为 Secret 并将工作流中的 `vars.OCR_LLM_URL` 改为 `secrets.OCR_LLM_URL`。

OCR `1.13.3` 的 `llm_auth_header` 仅接受 `x-api-key` 或 `authorization`；Azure 的 `api-key` 应通过 `llm_extra_headers: api-key=${{ secrets.OCR_LLM_TOKEN }}` 传入，否则工作流会在配置阶段失败。

工作流使用自动提供的 `GITHUB_TOKEN` 发布评论，仓库及组织策略需允许 `contents: read` 和 `pull-requests: write`。将程序、测试和 `.github/workflows/ocr-review.yml` 先提交并推送到 PR 的目标分支；当前仓库的目标分支为 `master`。无需额外配置 checkout。工作流固定 OCR 版本为 `1.13.3`，正式使用时建议将 Action 标签替换为核验过的完整 commit SHA。

## 演示审查

1. 从已包含上述文件的目标分支创建同仓库测试分支。
2. 仅在测试分支中，将 `warehouse.py` 的 `if quantity > self.stock:` 临时改为 `if quantity >= self.stock:`。这会错误地拒绝出库全部库存；`python -m unittest -v test_warehouse` 中的 `test_ship_all_stock` 应失败。
3. 提交并推送测试分支，创建指向 `master` 的 PR。在 **Actions** 查看 `OpenCodeReview`，在 PR **Conversation** 查看摘要、在 **Files changed** 查看行级评论。AI 不保证发现该问题；结合测试、摘要和日志核对。
4. 恢复正确比较并再次推送，确认新提交触发审查、单测通过。演示结束后关闭 PR 或经人工确认后合并正确版本。

仅同仓库分支 PR 会运行此工作流，外部 fork 不在本示例范围内。同仓库条件不是完整隔离，只有可信贡献者才应使用，并应保护工作流及规则文件。日志和评论可能包含代码；请先确认代码发送及数据保留符合组织政策。此工作流可能因运行错误失败；若试点不应阻断合并，不要将其设为必需检查。