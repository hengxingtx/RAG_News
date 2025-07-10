#! python3
# -*- encoding: utf-8 -*-
###############################################################
#          @Time    :   2025/07/07 18:50:00
#          @Author  :   heng
#          @Contact :   hengsblog@163.com
###############################################################
"""
@comment
"""
#! python3
# -*- encoding: utf-8 -*-
###############################################################
#          @File    :   model.py
#          @Time    :   2024/01/11 18:03:29
#          @Author  :   heng
#          @Version :   1.0
#          @Contact :   hengsblog@163.com
#
###############################################################
"""
@comment
"""
from typing import List, Optional, Dict, Any, ClassVar
from langchain.callbacks.manager import CallbackManagerForLLMRun
from langchain.llms.base import LLM
import requests
from pydantic import BaseModel, Field
from configs.logger_config import web_logger as logger
import json
from openai import OpenAI
import yaml
from utils_own.toolkit import format_json
import openai
import httpx
import time

with open("configs/config.yaml", "r") as f:
    config = yaml.safe_load(f)

openai_api_key = config["openai_api_key"]
qwen_api_key = config["qwen_api_key"]


class Qwen3(LLM):
    """qwen3 32b model"""

    api_url: str = Field(
        default="https://dashscope.aliyuncs.com/compatible-mode/v1",
        description="API 地址",
    )
    gpt_model_name: str = Field(default="gpt-4.1-mini")

    @property
    def _llm_type(self) -> str:
        return "custom"

    def get_from_llm(self, content: str) -> Dict[str, Any]:
        """
            从语言模型获取响应。

        Args:
            content (str): 输入内容，字符串类型。

        Returns:
            Dict[str, Any]: 返回一个字典，包含两个键值对："generated_text"（生成的文本）和"error"（错误信息，如果请求失败则为字符串类型）。

        Raises:
            无。
        """
        client = OpenAI(
            # 若没有配置环境变量，请用百炼API Key将下行替换为：api_key="sk-xxx",
            # api_key=os.getenv("DASHSCOPE_API_KEY"),
            api_key=qwen_api_key,
            base_url=self.api_url,
        )
        try:
            completion = client.chat.completions.create(
                # 模型列表：https://help.aliyun.com/zh/model-studio/getting-started/models
                model="qwen-plus-latest",
                messages=[
                    {"role": "system", "content": "You are a helpful assistant."},
                    {"role": "user", "content": content},
                ],
                stream=False,
                extra_body={"enable_thinking": False},
            )
            response = json.loads(completion.model_dump_json())
            result = response["choices"][0]["message"]["content"]
            return result
        except Exception as e:
            logger.info(f"error happend: {e}")
            logger.info(f"qwen3 模型被拦截，调用gpt4.1")
            return GPT4(model_name=self.gpt_model_name)._call(content)

    def _call(
        self,
        prompt: str,
        stop: Optional[List[str]] = None,
        run_manager: Optional[CallbackManagerForLLMRun] = None,
    ) -> str:
        """
            调用语言模型，获取响应。

        Args:
            prompt (str): 提示信息，一个字符串。
            stop (Optional[List[str]], optional): 不允许使用此参数，默认为None。
                Defaults to None.
            run_manager (Optional[CallbackManagerForLLMRun], optional): 运行回调管理器，默认为None。
                Defaults to None.

        Raises:
            ValueError: 如果stop参数不是None，则会引发ValueError异常。

        Returns:
            str: 返回答案，一个字符串。
        """
        if stop is not None:
            raise ValueError("stop kwargs are not permitted.")

        response = self.get_from_llm(prompt)
        logger.info(f"answer:{response}")
        return response


class GPT4(LLM):
    """openai的gpt4接口"""

    model_name: str = Field(default="gpt-4.1", description="使用的openai模型名称")
    api_url: str = Field(default="http://8.211.148.104:8021/duck/openai", description="API 地址")

    @property
    def _llm_type(self) -> str:
        """
        返回LLM类型，此处为自定义模型。

        Returns:
            str - "custom", 表示自定义模型。
        """
        return "custom"

    def call_openai_api(self, prompt: str):
        # API配置
        url = self.api_url

        # 请求头
        headers = {"Content-Type": "application/json", "Authorization": f"Bearer {openai_api_key}"}

        # 请求体
        data = {
            "model": self.model_name,
            # "model": "gpt-4.1-mini",
            # "model": "gpt-4.1-nano",
            "input": prompt,
        }

        try:
            # 发送POST请求
            response = requests.post(url, headers=headers, json=data)

            # 检查响应状态
            response.raise_for_status()

            # 打印响应结果
            print("状态码:", response.status_code)
            print(response.json())
            # 正确解析响应中的text内容
            response_json = response.json()
            for output_item in response_json["output"]:
                if output_item["type"] == "message" and "content" in output_item:
                    for content_item in output_item["content"]:
                        if content_item["type"] == "output_text":
                            return content_item["text"]
            # 如果没找到，返回空字符串或抛出异常
            return ""
        except requests.exceptions.RequestException as e:
            print(f"请求发生错误: {e}")
            return None

    def _call(
        self,
        prompt: str,
        stop: Optional[List[str]] = None,
        run_manager: Optional[CallbackManagerForLLMRun] = None,
    ) -> str:
        """
        调用该函数，生成一个基于给定提示的文本。
        """
        if stop is not None:
            raise ValueError("stop kwargs are not permitted.")

        response = self.call_openai_api(prompt)
        return response


class GPT4WithWeb(LLM):
    """openai的gpt4接口"""

    model_name: str = Field(default="gpt-4.1", description="使用的openai模型名称")
    api_url: str = Field(default="http://8.211.148.104:8021/duck/openai", description="API 地址")

    @property
    def _llm_type(self) -> str:
        """
        返回LLM类型，此处为自定义模型。

        Returns:
            str - "custom", 表示自定义模型。
        """
        return "custom"

    def call_openai_api(self, prompt: str):
        # API配置
        url = self.api_url

        client = OpenAI(
            api_key=openai_api_key,
        )

        max_retries = 3
        retry_count = 0

        while retry_count < max_retries:
            try:
                response = client.responses.create(
                    model=self.model_name,
                    tools=[{"type": "web_search_preview"}],
                    input=prompt,
                    # max_output_tokens=6000,
                    timeout=100,
                )

                # 打印响应结果
                print("状态码:", response.status_code)
                print(response.json())      # 打印响应结果
                # 正确解析响应中的text内容
                response_json = response.json()
                for output_item in response_json["output"]:
                    if output_item["type"] == "message" and "content" in output_item:
                        for content_item in output_item["content"]:
                            if content_item["type"] == "output_text":
                                return content_item["text"]
                # 如果没找到，返回空字符串
                return ""

            except requests.exceptions.RequestException as e:
                print(f"请求发生错误: {e}")
                retry_count += 1
                if retry_count >= max_retries:
                    return None
                wait_time = 2**retry_count
                print(f"请求错误，{wait_time}秒后第{retry_count}次重试")
                time.sleep(wait_time)

            except (openai.APIConnectionError, httpx.ConnectError) as e:
                retry_count += 1
                if retry_count >= max_retries:
                    print(f"连接错误，已尝试 {max_retries} 次重试，放弃: {e}")
                    return None

                wait_time = 2**retry_count  # 指数退避策略
                print(f"连接错误，{wait_time} 秒后进行第 {retry_count} 次重试: {e}")
                time.sleep(wait_time)

    def _call(
        self,
        prompt: str,
        stop: Optional[List[str]] = None,
        run_manager: Optional[CallbackManagerForLLMRun] = None,
    ) -> str:
        """
        调用该函数，生成一个基于给定提示的文本。
        """
        if stop is not None:
            raise ValueError("stop kwargs are not permitted.")

        response = self.call_openai_api(prompt)
        return response


class Qwen3Thinking(LLM):
    """qwen3 32b model"""

    api_url: str = Field(
        default="https://dashscope.aliyuncs.com/compatible-mode/v1",
        description="API 地址",
    )
    gpt_model_name: str = Field(default="gpt-4.1-mini")

    @property
    def _llm_type(self) -> str:
        return "custom"

    def get_from_llm(self, content: str) -> Dict[str, Any]:
        """
            从语言模型获取响应。

        Args:
            content (str): 输入内容，字符串类型。

        Returns:
            Dict[str, Any]: 返回一个字典，包含两个键值对："generated_text"（生成的文本）和"error"（错误信息，如果请求失败则为字符串类型）。

        Raises:
            无。
        """
        client = OpenAI(
            # 若没有配置环境变量，请用百炼API Key将下行替换为：api_key="sk-xxx",
            # api_key=os.getenv("DASHSCOPE_API_KEY"),
            api_key=qwen_api_key,
            base_url=self.api_url,
        )
        try:
            full_response = ""
            completion = client.chat.completions.create(
                # 模型列表：https://help.aliyun.com/zh/model-studio/getting-started/models
                model="qwen-plus-latest",
                messages=[
                    {"role": "system", "content": "You are a helpful assistant."},
                    {"role": "user", "content": content},
                ],
                stream=True,
                extra_body={"enable_thinking": True},
            )
            for chunk in completion:
                if chunk.choices:
                    # 获取此块中的内容（如果有）
                    content = chunk.choices[0].delta.content
                    if content is not None:
                        full_response += content
                        # 可选：实时打印内容片段
                        # print(content, end="", flush=True)
            return full_response
        except Exception as e:
            logger.info(f"qwen3 模型被拦截，调用gpt4.1")
            logger.info(f"error happend: {e}")
            return GPT4(model_name=self.gpt_model_name)._call(content)

    def _call(
        self,
        prompt: str,
        stop: Optional[List[str]] = None,
        run_manager: Optional[CallbackManagerForLLMRun] = None,
    ) -> str:
        """
            调用语言模型，获取响应。

        Args:
            prompt (str): 提示信息，一个字符串。
            stop (Optional[List[str]], optional): 不允许使用此参数，默认为None。
                Defaults to None.
            run_manager (Optional[CallbackManagerForLLMRun], optional): 运行回调管理器，默认为None。
                Defaults to None.

        Raises:
            ValueError: 如果stop参数不是None，则会引发ValueError异常。

        Returns:
            str: 返回答案，一个字符串。
        """
        if stop is not None:
            raise ValueError("stop kwargs are not permitted.")

        response = self.get_from_llm(prompt)
        logger.info(f"answer:{response}")
        return response


class Qwen3WithWeb(LLM):
    """qwen3 32b model"""

    api_url: str = Field(
        default="https://dashscope.aliyuncs.com/compatible-mode/v1",
        description="API 地址",
    )
    gpt_model_name: str = Field(default="gpt-4.1-mini")

    @property
    def _llm_type(self) -> str:
        return "custom"

    def get_from_llm(self, content: str) -> Dict[str, Any]:
        """
            从语言模型获取响应。

        Args:
            content (str): 输入内容，字符串类型。

        Returns:
            Dict[str, Any]: 返回一个字典，包含两个键值对："generated_text"（生成的文本）和"error"（错误信息，如果请求失败则为字符串类型）。

        Raises:
            无。
        """
        client = OpenAI(
            # 若没有配置环境变量，请用百炼API Key将下行替换为：api_key="sk-xxx",
            # api_key=os.getenv("DASHSCOPE_API_KEY"),
            api_key=qwen_api_key,
            base_url=self.api_url,
        )
        try:
            completion = client.chat.completions.create(
                # 模型列表：https://help.aliyun.com/zh/model-studio/getting-started/models
                model="qwen-plus-latest",
                messages=[
                    {"role": "system", "content": "You are a helpful assistant."},
                    {"role": "user", "content": content},
                ],
                stream=False,
                extra_body={"enable_search": True},
            )
            response = json.loads(completion.model_dump_json())

            result = response["choices"][0]["message"]["content"]
            return result
        except Exception as e:
            logger.info(f"qwen3 模型被拦截，调用gpt4.1")
            logger.info(f"error happend: {e}")
            return GPT4(model_name=self.gpt_model_name)._call(content)

    def _call(
        self,
        prompt: str,
        stop: Optional[List[str]] = None,
        run_manager: Optional[CallbackManagerForLLMRun] = None,
    ) -> str:
        """
            调用语言模型，获取响应。

        Args:
            prompt (str): 提示信息，一个字符串。
            stop (Optional[List[str]], optional): 不允许使用此参数，默认为None。
                Defaults to None.
            run_manager (Optional[CallbackManagerForLLMRun], optional): 运行回调管理器，默认为None。
                Defaults to None.

        Raises:
            ValueError: 如果stop参数不是None，则会引发ValueError异常。

        Returns:
            str: 返回答案，一个字符串。
        """
        if stop is not None:
            raise ValueError("stop kwargs are not permitted.")

        response = self.get_from_llm(prompt)
        print(f"answer:{response}")
        return response


def main():
    """main"""
    prompt = """
    <INSTRUCTIONS>
    目标：仔细阅读文章，梳理每段正文的逻辑，优化并精简输入的文章, 且文章为模型生成，可能有事实性错误，
    你需要通过互联网查询文章引言部分的实体是否有误，如果实体有错误，需要对原文错误进行修改。使全文来源准确。
    </INSTRUCTIONS>

    【修改要求】
    1. 要求语言严谨、结构清晰、内容真实可信，论据充实严谨，体现出权威性。
    2. 保持文章大纲不变
    3. 保持原文第一部分一是、二是、三是的书写格式，内容可精简 。
    4. 精简文章正文部分，精简描述并保留最可以论证原文主题的观点及事件，每段正文不超过300字。
    5. 仔细审查全文事件，涉及的事件不能有重复，若有重复则只保留一个。
    6. 除了事件详情部分，在分析研判、对策建议及其他大章节下，如果出现`中国`，则用`我国`代替。

    <keywords>
    马斯克成立美国党
    </keywords>

    <article>
    {'chapters': [{'overview': '2024年7月4日，美国科技大亨埃隆·马斯克在其社交媒体平台"X"上宣布成立名为"美国党"的新政党，称该决定基于一项超124.9万人参与的网络民调结果，其中65.4%的支持者认同打破当前民主党和共和党主导的政治格局。马斯克批评美国政府浪费严重、腐败成风，正将国家推向破产边缘，并强调新政党旨在"将自由归还民众"。此举与其此前支持特朗普及共和党的立场形成明显反差。此前在2024年美国总统大选期间，马斯克曾公开挺特朗普，但因反对"大而美"税收和支出法案而逐渐疏远。6月30日其公开抨击该法案并预告次日成立新政党，7月4日法案签署后不久即正式宣布。根据美国法律规定，新政党需完成包括召开代表大会、选举临时官员等程序方能具备选举资格，目前尚不清楚"美国党"是否已启动相关流程。马斯克回应网友提问时表示，新政党计划于"明年"参与选举。具体情况如下:'}, {'title': '一、事件详情', 'sections': [{'title': '（一）马斯克发起成立"美国党"并获得65.4%网民支持', 'content': '一是马斯克在社交媒体宣布成立"美国党"。当地时间7月5日，美国企业家埃隆·马斯克在其拥有的社交媒体平台X上发布消息称，"今天，'美国党'的成立还给你们自由"，这一表态是在其7月4日发起的网络投票结果支持率占优后作出的。据相关数据显示，在约124.9万网民参与的投票中，65.4%的支持者希望摆脱民主党与共和党的两党体制，建立新政党。马斯克强调，此举旨在打破当前"因浪费和贪污而破产"的政治格局。二是马斯克提出新政党参选计划及面临挑战。尽管"美国党"的具体行动纲领尚未公布，但马斯克在社交媒体回应网友时表示，新政党计划在明年参与包括2026年中期选举或2028年总统选举在内的重要选举活动。然而，根据美国法律，新政党要获得选举资格需经历复杂的认证程序，包括召开代表大会、选举临时官员及向联邦选举委员会申请资质等。此外，专家分析指出，无论是法律门槛还是经济成本，以及可能遭遇民主党和共和党的联合抵制，均使"美国党"短期内难以撼动美国现有的两党格局。'}, {'title': '（二）马斯克与特朗普因"大而美"法案公开决裂', 'content': '一是马斯克与特朗普因"大而美"法案产生激烈分歧。自6月30日起，马斯克公开批评美国总统特朗普力推的"大而美"税收和支出法案，并表示如果该法案通过，他将在次日即7月4日启动成立"美国党"的程序。随后，特朗普于当地时间7月4日正式签署该法案使其生效，与此同时，马斯克在法案签署前数小时再次发起关于成立新政党的网络民意调查，进一步强化了其对现有两党体制的不满。二是"大而美"法案最终获通过并签署生效。根据背景信息，当地时间7月3日，该法案在众议院以微弱优势通过，随后美国总统特朗普于7月4日美国国庆日将其签署生效，标志着该法案正式成为法律。三是马斯克提出针对特定共和党议员的选举策略。据社交媒体平台X上的帖文显示，马斯克计划通过"美国党"聚焦2-3个参议院席位以及8-10个众议院选区，在明年中期选举中对支持"大而美"法案的共和党议员发起挑战，试图使其在党内初选中失利。四是马斯克的举动引发共和党内部不满。据美国《国会山报》5日报道，在特朗普及其盟友试图挽救中期选举不利局面之际，马斯克的一系列公开表态引起了共和党内部的无视与批评，有共和党策略师警告称，此举可能导致马斯克同时失去民主党和共和党的支持，陷入孤立境地。'}, {'title': '（三）马斯克计划通过夺取关键席位撬动国会政治格局', 'content': '一是马斯克提出具体策略，计划在参议院争取2或3个席位，在众议院争取8到10个选区席位，利用国会两党现有微弱优势影响立法进程。据背景资料描述，共和党在参议院的优势仅体现为副总统万斯的关键投票权，若马斯克掌握数个席位即可成为两党争夺的对象。二是马斯克回应网友关于新政党参与选举的时间表时明确表示将在"明年"参加2026年中期选举。尽管根据美国法律，新政党需完成包括召开党团会议、选举临时官员和政党名称指定等复杂资质认证程序，但马斯克已通过社交媒体获得超过百万网民支持，其新政党动向引发广泛关注。三是美国乔治敦大学政治学教授汉斯·诺埃尔分析指出，基于美国"赢者通吃"的选举人团制度，第三方政党难以通过获得20%-30%选民票数而在议会中取得实质性席位，这使得马斯克新政党面临结构性挑战。尽管如此，作为世界首富且曾深度参与美国政治的特殊人物，马斯克仍被认为可能对现有两党格局产生一定影响。'}, {'title': '（四）特朗普威胁审查马斯克企业并驱逐其出境引发舆论震动', 'content': '一是面对马斯克成立"美国党"的挑战，美国总统特朗普在公开场合表示，将让马斯克曾领导的政府效率部（DOGE）对其企业补贴进行严格审查，并暗示可能驱逐马斯克回南非老家。此外，特朗普还透露曾爆料马斯克在白宫吸毒。这一系列强硬表态反映出特朗普政府对马斯克成立新政党的强烈不满。二是马斯克的表态已在共和党内部引发无视与不满，有策略师警告称，此举可能导致马斯克失去两党支持，陷入孤立境地。三是"美国党"初期战略聚焦关键席位争夺。根据马斯克在社交媒体上的披露，新成立的"美国党"将聚焦2-3个参议院席位以及8-10个众议院选区，试图通过这些关键席位在国会中形成影响力。这一策略不同于传统政党追求多数席位的做法，显示出马斯克希望通过精准打击影响立法进程。也有网友指出，创建新党可能分散共和党选票，反而有利于民主党扩大优势。'}]}, {'title': '二、分析研判', 'sections': [{'title': '（一）美国政党结构面临挑战，两党制稳定性或受冲击', 'content': '马斯克宣布成立"美国党"，声称该党将代表所谓"80%的中间选民"，试图打破长期以来共和党和民主党轮流执政的政治格局。尽管其短期内难以撼动美国既有的政治架构，但其行为本身已对传统两党制构成象征性挑战。美国现行选举制度具有明显的"赢者通吃"特征，这使得第三方政党很难通过获得一定比例的选票而逐步壮大。然而，马斯克作为全球首富和科技巨头领导者，凭借强大的个人影响力和资金支持，可能在一定程度上突破制度壁垒，推动新政党进入国会选举竞争。这种由超级富豪主导的政治力量崛起，不仅加剧了美国政党的碎片化趋势，也削弱了传统大党的代表性与凝聚力，动摇了美国政治体系的稳定性。对中国而言，美国国内政治秩序的动荡可能影响其对外政策的一致性和可预测性，尤其是在中美战略博弈背景下，需警惕美方因内部政治压力而采取更具攻击性的对华政策。'}, {'title': '（二）马斯克新党可能加剧美国内部政治极化与治理困境', 'content': '马斯克的新党"美国党"虽自称代表"中间路线"，但在实际操作中更可能通过煽动民众对现有体制的不满来获取政治资本，这将进一步加剧美国社会的政治极化现象。特朗普时期的"MAGA"主义已使美国政治呈现高度分裂状态，而马斯克作为曾深度参与保守派议程的企业家，其新政党很可能延续甚至放大这一趋势。此外，马斯克在社交媒体平台上的言论极具煽动性，容易引导舆论走向极端，进而激化不同政治立场群体之间的对立情绪。如果"美国党"在未来选举中取得一定席位，其议员可能利用少数关键票左右立法进程，导致政府决策效率进一步下降，甚至引发更多政治僵局。对中国来说，这种内耗型政治生态可能促使美国政府在外交事务上寻求外部"替罪羊"，从而增加中美关系的不确定性与风险。'}, {'title': '（三）中美博弈背景下，马斯克政坛转向对华科技政策影响深远', 'content': '马斯克自2024年起逐步从特朗普盟友转变为批评者，并最终成立新政党，显示出其政治立场的独立性和灵活性。然而，他在科技领域的重大利益（如特斯拉、SpaceX等）使其对美国对华技术限制政策尤为敏感。若"美国党"在国会取得一定影响力，马斯克或将推动放松对华高科技出口管制，以维护自身企业的全球供应链稳定和市场拓展需求。另一方面，马斯克也可能利用其在美国政治中的特殊地位，在中美科技博弈中扮演"调停者"角色，试图缓和两国紧张关系。但同时，他仍可能受到美国国家安全审查机制的压力，特别是在涉及与中国企业合作的技术项目时。因此，中国应密切关注马斯克及其新政党在科技政策方面的动向，既要防范其可能配合美国遏制战略的风险，也要把握其在特定领域推动务实合作的潜在机遇。'}, {'title': '（四）美国政商勾连机制或被进一步暴露，影响国际形象认知', 'content': '马斯克成立"美国党"的举动再次凸显美国政商勾连机制的深层问题。作为特斯拉和SpaceX的CEO，他不仅拥有巨额财富，还长期与联邦政府保持密切合作关系，其企业接受大量政府补贴和合同，且在政策制定过程中具有显著话语权。此次成立新政党并试图影响国会选举，暴露出美国精英阶层通过资本操控政治议程的现象日益严重。这种"富人政治"模式不仅损害民主制度的公平性，也在国际社会上削弱了美国所谓"自由民主"的道义感召力。尤其在中美意识形态与制度竞争加剧的背景下，美国政商合流的负面案例将被广泛传播，进一步动摇发展中国家对西方制度的信任。中国应借此机会加强国际叙事引导，揭示美式民主的本质缺陷，增强国际社会对中国发展模式和治理理念的理解与认同。'}]}, {'title': '三、对策建议', 'sections': [{'title': '（一）密切跟踪马斯克新政党动向，评估其对在美中企影响', 'content': '马斯克宣布成立"美国党"并迅速获得大量网民支持，标志着其从科技与商业领域向政治领域的深度拓展。该政党若逐步获得政策影响力，可能重塑美国传统政治格局，并对涉及外资的产业政策产生潜在调整。尤其值得关注的是，马斯克作为特斯拉和SpaceX的掌舵人，其政党立场可能直接影响联邦政府在新能源、航天、人工智能等关键领域的监管方向。对于在美运营的中国企业而言，需高度关注该政党的政策主张及其对国会立法议程的影响，特别是有关外资审查、技术出口限制和市场竞争规则等方面的变化。建议通过专业团队加强信息监测，建立动态风险评估机制，提前识别政策转向带来的合规挑战与市场风险，确保企业在美业务稳健运行。'}, {'title': '（二）强化对美舆情引导，塑造有利于我方的国际叙事环境', 'content': '马斯克成立"美国党"的事件不仅引发国内舆论高度关注，也在国际社会掀起波澜。由于其在科技与资本市场的巨大影响力，该事件可能被西方媒体用来渲染所谓"自由主义创新力量"，进一步强化对中国体制的负面叙事。对此，应主动布局对外传播策略，借助多语种平台和新媒体渠道，客观阐释中国企业的全球化发展理念与合作共赢立场。同时，针对可能出现的误解或偏见，及时组织专家解读相关政策背景，提升国际公众对中国的认知准确性。还可通过民间交流、企业社会责任活动等方式增强情感共鸣，构建更具韧性的国际舆论生态，为中美经贸关系稳定发展营造良好氛围。'}, {'title': '（三）利用美方内部矛盾深化对话，争取科技与经贸合作空间', 'content': '马斯克与特朗普因"大而美"法案公开决裂，反映出当前美国政坛内部意见分歧加剧，特别是在科技政策、移民改革和财政刺激等领域存在较大张力。这种分裂状态为中国提供了可资利用的战略窗口期。应积极把握美国两党及新兴政治力量之间的博弈态势，推动与美国地方州政府、高校科研机构以及非政治性行业协会的合作。在清洁能源、人工智能伦理治理、太空探索等双方利益交汇点上，倡导设立联合工作组或技术标准协调机制，促进规则互认与资源共享。此外，在双边经贸谈判中，可适时提出降低关税壁垒、放宽高科技产品出口限制等议题，争取实现互利共赢的新突破。'}, {'title': '（四）提升应对能力，防范潜在的政治干预与经济反制风险', 'content': '随着马斯克涉足政坛，其旗下企业可能面临更多来自美国政府的审查压力，同时也可能将部分政治争议投射到国际投资领域，给在美中企带来不确定性。因此，必须提高预判能力和应急响应水平，建立健全跨部门联动的风险预警体系，重点防范可能的政治干预、金融制裁或供应链脱钩行为。鼓励企业完善合规管理体系，优化全球资源配置结构，避免过度依赖单一市场。同时，推动国内产业链自主可控能力建设，提升关键技术自给率。在必要时可通过WTO等多边机制发声，坚决维护我国企业合法权益，展现负责任大国形象。'}]}]}
    </article>

    保持原json格式输出修改后的文章
    """
    result = GPT4WithWeb()._call(prompt)
    print(result)
    result_json = format_json(result)
    print(result_json)


if __name__ == "__main__":
    main()
