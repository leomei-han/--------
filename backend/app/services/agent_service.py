from __future__ import annotations


class AgentService:
    def overview(self) -> dict:
        return {
            "knowledge_agents": [
                "需求分析助手",
                "数据采集助手",
                "算法实验助手",
                "测试文档助手",
            ],
            "collaboration_flow": [
                "将课程要求拆成数据、算法、前端、文档四条并行工作流",
                "记录任务分工、阶段目标和验收脚本",
                "为周报、PPT 和报告提供自动化草稿入口",
            ],
        }
