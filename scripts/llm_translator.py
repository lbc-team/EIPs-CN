import openai
import os
import json
from spliter import split_text

from dotenv import load_dotenv

load_dotenv(".env")

from config import OPENROUTER_MODEL_GEMINI_20_FLASH, OPENROUTER_PREFIX, LLM_MODEL_DEEPSEEK_R1, LLM_MODEL_GPT_4O_MINI

TRANSLATE_PROMPT = """
用户将提供给你一段 以太坊改进提案(EIP) 相关的英文 md 文档内容，请你将内容翻译成中文，注意只做翻译，不要删减内容，不要添加解释和演绎。
输出格式保持 MD 格式。

你必须严格遵循以下规则：
1. 保持所有 MD 特有的标记和组件不变，比如 <ComponentName>、{expression} 等
2. 遇到 Rust、Solana、Anchor、JavaScript、SDK、Kit 等专业术语时，保留英文原文
3. 翻译后的内容必须保持原文的结构，包括标题、段落、列表、表格、空行等和原文一致
4. 代码块处理规则：
   - 只翻译代码注释，代码本身保持不变
   - 所有的 json 代码，保持原文不变
   - 所有的 HTML 标记代码， 如 <Tabs> <Tab> <Callout>，保持原文不变
   - 保持代码块的语言标记，如 ```rust、```typescript、```javascript
   - 保持单行代码标记，如 `code`

5. 格式转换规则：
   - 保持所有链接标记 [text](url) 的格式不变，仅翻译其中的文本内容
   - 原文中的 frontmatter（文档元数据）不翻译 title description 等标记，仅翻译其对应的文本内容
6. 翻译完成后仔细检查
   - 是否完整保留了所有 MD 是否完整，检查代码块、HTML 标记、等是否和原文一致， 不一致请修复。
   - 检查所有专业术语，是否翻译恰当，没有合适的翻译，请保持英文。
"""

class LLMTranslator:
    def __init__(self, model=OPENROUTER_MODEL_GEMINI_20_FLASH):
        self.model = model

        # 初始化客户端，API密钥从环境变量读取
        if model.startswith("gpt-"):
            api_key=os.getenv("OPENAI_API_KEY")
            base_url=os.getenv("OPENAI_BASE_URL")

            self.client = openai.OpenAI(api_key=api_key, base_url=base_url)
        elif model.startswith("deepseek"):
            api_key = os.getenv("ALI_AI_API_KEY")
            base_url = os.getenv("ALI_AI_BASE_URL")

            self.client = openai.OpenAI(api_key=api_key, base_url=base_url)
        elif model.startswith(OPENROUTER_PREFIX):
            api_key = os.getenv("OPENROUTER_API_KEY")
            base_url = os.getenv("OPENROUTER_BASE_URL")

            colIndex = model.find(":")
            self.model = model[colIndex+1:]
            print(f"使用 OpenRouter 模型: {self.model}")
            self.client = openai.OpenAI(api_key=api_key, base_url=base_url)

    def simple_translate(self, text):
        system_prompt = "你是一个精通中文的与英文的计算机技术专家，请将以下英文内容翻译成中文，仅返回翻译后的中文内容，不要添加任何解释。"

        request_params = {
            "model": self.model,
            "temperature": 1, 
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": text}
            ]
        }

        if self.model == LLM_MODEL_DEEPSEEK_R1:
            request_params["stream"] = True
            response = self.client.chat.completions.create(**request_params)
            
            # print(response.choices[0].message.reasoning_content)
            # print(response.choices[0].message.content)

            responseContent = ""
            for chunk in response:
                answer_chunk = chunk.choices[0].delta.content
                # print(answer_chunk)
                if answer_chunk and answer_chunk != "":
                    responseContent += answer_chunk
            return responseContent
        else:
            response = self.client.chat.completions.create(**request_params)
            return response.choices[0].message.content



    def translate_markdown(self, markdown_text):

        translated_text = ""
        chunks = split_text(markdown_text)

        for chunk in chunks:
            translated_chunk = self.translate(chunk)
            translated_text += translated_chunk

        return translated_text

    def translate(self, markdown_text):
        request_params = {
            "model": self.model,
            "temperature": 1.1, 
            "messages": [
                {"role": "system", "content": TRANSLATE_PROMPT},
                {"role": "user", "content": markdown_text}
            ]
        }

        if self.model == LLM_MODEL_DEEPSEEK_R1:
            request_params["stream"] = True
            response = self.client.chat.completions.create(**request_params)
            
            # print(response.choices[0].message.reasoning_content)
            # print(response.choices[0].message.content)

            print("等待 DEEPSEEK R1 大模型返回翻译结果...")
            responseContent = ""
            for chunk in response:
                if chunk and chunk.choices[0].delta.content:
                    answer_chunk = chunk.choices[0].delta.content
                    # print(answer_chunk)
                    if answer_chunk and answer_chunk != "":
                        responseContent += answer_chunk
            return responseContent
        else:
            response = self.client.chat.completions.create(**request_params)
            return response.choices[0].message.content
