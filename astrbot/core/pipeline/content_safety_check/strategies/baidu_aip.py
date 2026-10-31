"""Para usar este recurso, instale primeiro a dependência com pip install baidu-aip."""

from typing import Any, cast

from aip import AipContentCensor

from . import ContentSafetyStrategy


class BaiduAipStrategy(ContentSafetyStrategy):
    def __init__(self, appid: str, ak: str, sk: str) -> None:
        self.app_id = appid
        self.api_key = ak
        self.secret_key = sk
        self.client = AipContentCensor(self.app_id, self.api_key, self.secret_key)

    def check(self, content: str) -> tuple[bool, str]:
        res = self.client.textCensorUserDefined(content)
        if "conclusionType" not in res:
            return False, ""
        if res["conclusionType"] == 1:
            return True, ""
        if "data" not in res:
            return False, ""
        count = len(res["data"])
        parts = [f"A moderação de conteúdo do Baidu encontrou {count} violações:\n"]
        for i in res["data"]:
            # A API do Baidu retorna um dict dinâmico; convertemos i para dict antes de acessar os campos com get
            parts.append(f"{cast(dict[str, Any], i).get('msg', '')};\n")
        parts.append("\nAvaliação: " + res["conclusion"])
        info = "".join(parts)
        return False, info
