"""如需修改配置，请在 `data/cmd_config.json` 中修改或者在管理面板中可视化修改。"""

import os
import platform

from astrbot import __version__
from astrbot.core.computer.booters.cua_defaults import CUA_DEFAULT_CONFIG
from astrbot.core.utils.astrbot_path import get_astrbot_data_path

from .agent_runner import get_agent_runner_config_default


def get_local_permission_defaults(system: str | None = None) -> dict:
    """Return fresh Local permission defaults for the operating system.

    Args:
        system: Operating system name, or None to use the current system.

    Returns:
        Per-role policies. Windows disables member access and gives admins
        unrestricted access because workspace isolation is unavailable.
    """
    windows = (system or platform.system()).lower() == "windows"
    return {
        "member": {
            "allow_execution": False,
            "allow_network": False,
            "filesystem_scope": "none" if windows else "workspace",
        },
        "admin": {
            "allow_execution": True,
            "allow_network": True,
            "filesystem_scope": "host" if windows else "workspace",
        },
    }


VERSION = __version__

DB_PATH = os.path.join(get_astrbot_data_path(), "data_v4.db")
PERSONAL_WECHAT_CONFIG_METADATA = {
    "weixin_oc_base_url": {
        "description": "Base URL",
        "type": "string",
        "hint": "Padrão: https://ilinkai.weixin.qq.com",
    },
    "weixin_oc_bot_type": {
        "description": "bot_type (parâmetro de login por QR)",
        "type": "string",
        "hint": "Padrão: 3",
        "invisible": True,
    },
    "weixin_oc_qr_poll_interval": {
        "description": "Intervalo de consulta do status do QR (segundos)",
        "type": "int",
        "hint": "Intervalo de consulta do status do código QR, em segundos.",
        "invisible": True,
    },
    "weixin_oc_long_poll_timeout_ms": {
        "description": "Tempo limite da consulta longa de getUpdates (ms)",
        "type": "int",
        "hint": "Tempo limite da API de consulta de mensagens.",
    },
    "weixin_oc_api_timeout_ms": {
        "description": "Tempo limite das requisições HTTP (ms)",
        "type": "int",
        "hint": "Tempo limite geral das requisições à API.",
    },
    "weixin_oc_token": {
        "description": "Token após o login (opcional)",
        "type": "string",
        "hint": "Preenchido após o login por QR; pode ser informado manualmente em cenários avançados.",
        "secret": True,
        "invisible": True,
    },
    "weixin_oc_account_id": {"invisible": True},
    "weixin_oc_sync_buf": {"invisible": True},
    "weixin_oc_context_tokens": {"invisible": True},
}

WEBHOOK_SUPPORTED_PLATFORMS = [
    "qq_official_webhook",
    "weixin_official_account",
    "wecom",
    "wecom_ai_bot",
    "slack",
    "lark",
    "line",
]

# 默认配置
DEFAULT_CONFIG = {
    "config_version": 4,
    "platform_settings": {
        "unique_session": False,
        "rate_limit": {
            "time": 60,
            "count": 30,
            "strategy": "stall",  # stall, discard
        },
        "reply_prefix": "",
        "forward_threshold": 1500,
        "enable_id_white_list": True,
        "id_whitelist": [],
        "id_whitelist_log": True,
        "wl_ignore_admin_on_group": True,
        "wl_ignore_admin_on_friend": True,
        "reply_with_mention": False,
        "reply_with_quote": False,
        "path_mapping": [],
        "segmented_reply": {
            "enable": False,
            "only_llm_result": True,
            "interval_method": "random",
            "interval": "1.5,3.5",
            "log_base": 2.6,
            "words_count_threshold": 150,
            "split_mode": "regex",  # regex 或 words
            "regex": ".*?[。？！~…]+|.+$",
            "split_words": [
                "。",
                "？",
                "！",
                "~",
                "…",
            ],  # 当 split_mode 为 words 时使用
            "content_cleanup_rule": "",
        },
        "no_permission_reply": True,
        "empty_mention_waiting": True,
        "empty_mention_waiting_need_reply": True,
        "friend_message_needs_wake_prefix": False,
        "ignore_bot_self_message": False,
        "ignore_at_all": False,
    },
    "provider_sources": [],  # provider sources
    "provider": [],  # models from provider_sources
    "provider_settings": {
        "enable": True,
        "default_image_caption_provider_id": "",
        "image_caption_prompt": "Descreva a imagem em português do Brasil.",
        "provider_pool": ["*"],  # "*" 表示使用所有可用的提供者
        "wake_prefix": "",
        "web_search": False,
        "websearch_provider": "tavily",
        "websearch_tavily_key": [],
        "websearch_bocha_key": [],
        "websearch_brave_key": [],
        "websearch_baidu_app_builder_key": "",
        "websearch_firecrawl_key": [],
        "websearch_exa_key": [],
        "websearch_anysearch_key": [],
        "web_search_link": False,
        "display_reasoning_text": False,
        "identifier": False,
        "group_name_display": False,
        "datetime_system_prompt": True,
        "persona_pool": ["*"],
        "prompt_prefix": "{{prompt}}",
        "streaming_response": False,
        "show_tool_use_status": False,
        "show_tool_call_result": False,
        "buffer_intermediate_messages": False,
        "max_quoted_fallback_images": 20,
        "quoted_message_parser": {
            "max_component_chain_depth": 4,
            "max_forward_node_depth": 6,
            "max_forward_fetch": 32,
            "warn_on_action_failure": False,
        },
        "unsupported_streaming_strategy": "realtime_segmenting",
        "reachability_check": False,
        "file_extract": {
            "enable": False,
            "provider": "moonshotai",
            "moonshotai_api_key": "",
        },
        "proactive_capability": {
            "add_cron_tools": True,
        },
        "computer_use_runtime": "none",
        "computer_use_local_permissions": get_local_permission_defaults(),
        "computer_use_require_admin": True,
        "sandbox": {
            "booter": "shipyard_neo",
            "shipyard_endpoint": "",
            "shipyard_access_token": "",
            "shipyard_ttl": 3600,
            "shipyard_max_sessions": 10,
            "shipyard_neo_endpoint": "",
            "shipyard_neo_access_token": "",
            "shipyard_neo_profile": "python-default",
            "shipyard_neo_ttl": 3600,
            "cua_image": CUA_DEFAULT_CONFIG["image"],
            "cua_os_type": CUA_DEFAULT_CONFIG["os_type"],
            "cua_idle_timeout": CUA_DEFAULT_CONFIG["idle_timeout"],
            "cua_telemetry_enabled": CUA_DEFAULT_CONFIG["telemetry_enabled"],
            "cua_local": CUA_DEFAULT_CONFIG["local"],
            "cua_api_key": CUA_DEFAULT_CONFIG["api_key"],
        },
        "image_compress_options": {
            "max_size": 1280,
        },
    },
    "agent_runner": {
        "runner_type": "local",
        "config": get_agent_runner_config_default("local"),
    },
    # SubAgent orchestrator mode:
    # - main_enable = False: disabled; main LLM mounts tools normally (persona selection).
    # - main_enable = True: enabled; main LLM keeps its own tools and includes handoff
    #   tools (transfer_to_*). remove_main_duplicate_tools can remove tools that are
    #   duplicated on subagents from the main LLM toolset.
    "subagent_orchestrator": {
        "main_enable": False,
        "remove_main_duplicate_tools": False,
        "router_system_prompt": (
            "Você é um roteador de tarefas. Converse naturalmente, reconheça a intenção do usuário "
            "e delegue ao subagente mais adequado usando as ferramentas transfer_to_*. "
            "Evite usar ferramentas de domínio diretamente. Se nenhum subagente for adequado, responda diretamente em português do Brasil."
        ),
        "agents": [],
    },
    "provider_stt_settings": {
        "enable": False,
        "provider_id": "",
    },
    "provider_tts_settings": {
        "enable": False,
        "provider_id": "",
        "dual_output": False,
        "use_file_service": False,
        "trigger_probability": 1.0,
    },
    "provider_ltm_settings": {
        "group_icl_enable": False,
        "group_message_max_cnt": 1000,
        "image_caption": False,
        "image_caption_provider_id": "",
        "group_message_history_enable": False,
        "group_message_history_max_cnt": 700,
        "active_reply": {
            "enable": False,
            "method": "possibility_reply",
            "possibility_reply": 0.1,
            "whitelist": [],
        },
    },
    "content_safety": {
        "also_use_in_response": False,
        "internal_keywords": {"enable": True, "extra_keywords": []},
        "baidu_aip": {"enable": False, "app_id": "", "api_key": "", "secret_key": ""},
    },
    "admins_id": ["astrbot"],
    "t2i": False,
    "t2i_word_threshold": 150,
    "t2i_strategy": "remote",
    "t2i_endpoint": "",
    "t2i_use_file_service": False,
    "t2i_active_template": "base",
    "http_proxy": "",
    "no_proxy": ["localhost", "127.0.0.1", "::1", "10.*", "192.168.*"],
    "dashboard": {
        "enable": True,
        "username": "astrbot",
        "password": "",
        "pbkdf2_password": "",
        "password_storage_upgraded": False,
        "password_change_required": False,
        "jwt_secret": "",
        "host": "0.0.0.0",
        "port": 6185,
        "disable_access_log": True,
        "trust_proxy_headers": False,
        "auth_rate_limit": {
            "enable": True,
            "average_interval": 1.0,
            "max_burst": 3,
        },
        "totp": {
            "enable": False,
            "secret": "",
            "recovery_code_hash": "",
        },
        "ssl": {
            "enable": False,
            "cert_file": "",
            "key_file": "",
            "ca_certs": "",
        },
    },
    "platform": [],
    "platform_specific": {
        # 平台特异配置：按平台分类，平台下按功能分组
        "lark": {
            "pre_ack_emoji": {"enable": False, "emojis": ["Typing"]},
        },
        "telegram": {
            "pre_ack_emoji": {"enable": False, "emojis": ["✍️"]},
        },
        "discord": {
            "pre_ack_emoji": {"enable": False, "emojis": ["🤔"]},
        },
    },
    "wake_prefix": ["/"],
    "log_level": "INFO",
    "log_file_enable": False,
    "log_file_path": "logs/astrbot.log",
    "log_file_max_mb": 20,
    "temp_dir_max_size": 1024,
    "trace_enable": False,
    "trace_log_enable": False,
    "trace_log_path": "logs/astrbot.trace.log",
    "trace_log_max_mb": 20,
    "pip_install_arg": "",
    "pypi_index_url": "https://mirrors.aliyun.com/pypi/simple/",
    "persona": [],  # deprecated
    "timezone": "Asia/Shanghai",
    "callback_api_base": "",
    "default_kb_collection": "",  # 默认知识库名称, 已经过时
    "plugin_set": ["*"],  # "*" 表示使用所有可用的插件, 空列表表示不使用任何插件
    "kb_names": [],  # 默认知识库名称列表
    "kb_fusion_top_k": 20,  # 知识库检索融合阶段返回结果数量
    "kb_final_top_k": 5,  # 知识库检索最终返回结果数量
    "kb_agentic_mode": False,
    "disable_builtin_commands": False,
    "disable_metrics": False,
}


"""
AstrBot v3 时代的配置元数据，目前仅承担以下功能：

1. 保存配置时，配置项的类型验证
2. WebUI 展示提供商和平台适配器模版

WebUI 的配置文件在 `CONFIG_METADATA_3` 中。

未来将会逐步淘汰此配置元数据。
"""
CONFIG_METADATA_2 = {
    "platform_group": {
        "metadata": {
            "platform": {
                "description": "Adaptadores de plataformas",
                "type": "list",
                "config_template": {
                    "QQ 官方机器人(Websocket, 推荐)": {
                        "id": "default",
                        "type": "qq_official",
                        "enable": True,
                        "appid": "",
                        "secret": "",
                        "enable_group_c2c": True,
                        "enable_guild_direct_message": True,
                        "use_markdown": True,
                    },
                    "QQ 官方机器人(Webhook)": {
                        "id": "default",
                        "type": "qq_official_webhook",
                        "enable": True,
                        "appid": "",
                        "secret": "",
                        "use_markdown": True,
                        "is_sandbox": False,
                        "unified_webhook_mode": True,
                        "webhook_uuid": "",
                        "callback_server_host": "0.0.0.0",
                        "port": 6196,
                    },
                    "OneBot v11": {
                        "id": "default",
                        "type": "aiocqhttp",
                        "enable": True,
                        "ws_reverse_host": "0.0.0.0",
                        "ws_reverse_port": 6199,
                        "ws_reverse_token": "",
                    },
                    "飞书(Lark)": {
                        "id": "lark",
                        "type": "lark",
                        "enable": True,
                        "app_id": "",
                        "app_secret": "",
                        "domain": "https://open.feishu.cn",
                        "lark_connection_mode": "socket",  # webhook, socket
                        "webhook_uuid": "",
                        "lark_encrypt_key": "",
                        "lark_verification_token": "",
                    },
                    "个人微信": {
                        "id": "weixin_personal",
                        "type": "weixin_oc",
                        "enable": True,
                        "weixin_oc_base_url": "https://ilinkai.weixin.qq.com",
                        "weixin_oc_bot_type": "3",
                        "weixin_oc_qr_poll_interval": 1,
                        "weixin_oc_long_poll_timeout_ms": 35_000,
                        "weixin_oc_api_timeout_ms": 120_000,
                    },
                    "企业微信 (智能机器人)": {
                        "id": "wecom_ai_bot",
                        "type": "wecom_ai_bot",
                        "hint": "Se algum campo estiver incorreto, crie novamente",
                        "enable": True,
                        "wecom_ai_bot_connection_mode": "long_connection",  # long_connection, webhook
                        "wecom_ai_bot_name": "",
                        "wecomaibot_ws_bot_id": "",
                        "wecomaibot_ws_secret": "",
                        "wecomaibot_token": "",
                        "wecomaibot_encoding_aes_key": "",
                        "wecomaibot_init_respond_text": "",
                        "wecomaibot_friend_message_welcome_text": "",
                        "msg_push_webhook_url": "",
                        "only_use_webhook_url_to_send": False,
                        "wecomaibot_ws_url": "wss://openws.work.weixin.qq.com",
                        "wecomaibot_heartbeat_interval": 30,
                        "unified_webhook_mode": True,
                        "webhook_uuid": "",
                        "callback_server_host": "0.0.0.0",
                        "port": 6198,
                    },
                    "企业微信应用 & 微信客服": {
                        "id": "wecom",
                        "type": "wecom",
                        "enable": True,
                        "corpid": "",
                        "secret": "",
                        "token": "",
                        "encoding_aes_key": "",
                        "kf_name": "",
                        "api_base_url": "https://qyapi.weixin.qq.com/cgi-bin/",
                        "unified_webhook_mode": True,
                        "webhook_uuid": "",
                        "callback_server_host": "0.0.0.0",
                        "port": 6195,
                    },
                    "微信公众平台": {
                        "id": "weixin_official_account",
                        "type": "weixin_official_account",
                        "enable": True,
                        "appid": "",
                        "secret": "",
                        "token": "",
                        "encoding_aes_key": "",
                        "api_base_url": "https://api.weixin.qq.com/cgi-bin/",
                        "unified_webhook_mode": True,
                        "webhook_uuid": "",
                        "callback_server_host": "0.0.0.0",
                        "port": 6194,
                        "active_send_mode": False,
                    },
                    "钉钉(DingTalk)": {
                        "id": "dingtalk",
                        "type": "dingtalk",
                        "enable": True,
                        "client_id": "",
                        "client_secret": "",
                        "card_template_id": "",
                    },
                    "Telegram": {
                        "id": "telegram",
                        "type": "telegram",
                        "enable": True,
                        "telegram_token": "",
                        "start_message": "Hello, I'm AstrBot!",
                        "telegram_api_base_url": "https://api.telegram.org/bot",
                        "telegram_file_base_url": "https://api.telegram.org/file/bot",
                        "telegram_command_register": True,
                        "telegram_command_auto_refresh": True,
                        "telegram_command_register_interval": 300,
                        "telegram_polling_restart_delay": 5.0,
                    },
                    "Discord": {
                        "id": "discord",
                        "type": "discord",
                        "enable": True,
                        "discord_token": "",
                        "discord_proxy": "",
                        "discord_command_register": True,
                        "discord_activity_name": "",
                        "discord_allow_bot_messages": False,
                    },
                    "Misskey": {
                        "id": "misskey",
                        "type": "misskey",
                        "enable": True,
                        "misskey_instance_url": "https://misskey.example",
                        "misskey_token": "",
                        "misskey_default_visibility": "public",
                        "misskey_local_only": False,
                        "misskey_enable_chat": True,
                        # download / security options
                        "misskey_allow_insecure_downloads": False,
                        "misskey_download_timeout": 15,
                        "misskey_download_chunk_size": 65536,
                        "misskey_max_download_bytes": None,
                        "misskey_enable_file_upload": True,
                        "misskey_upload_concurrency": 3,
                        "misskey_upload_folder": "",
                    },
                    "Slack": {
                        "id": "slack",
                        "type": "slack",
                        "enable": True,
                        "bot_token": "",
                        "app_token": "",
                        "signing_secret": "",
                        "slack_connection_mode": "socket",  # webhook, socket
                        "unified_webhook_mode": True,
                        "webhook_uuid": "",
                        "slack_webhook_host": "0.0.0.0",
                        "slack_webhook_port": 6197,
                        "slack_webhook_path": "/astrbot-slack-webhook/callback",
                    },
                    "Line": {
                        "id": "line",
                        "type": "line",
                        "enable": True,
                        "channel_access_token": "",
                        "channel_secret": "",
                        "unified_webhook_mode": True,
                        "webhook_uuid": "",
                    },
                    "Satori": {
                        "id": "satori",
                        "type": "satori",
                        "enable": True,
                        "satori_api_base_url": "http://localhost:5140/satori/v1",
                        "satori_endpoint": "ws://localhost:5140/satori/v1/events",
                        "satori_token": "",
                        "satori_auto_reconnect": True,
                        "satori_heartbeat_interval": 10,
                        "satori_reconnect_delay": 5,
                    },
                    "KOOK": {
                        "id": "kook",
                        "type": "kook",
                        "enable": True,
                        "kook_bot_token": "",
                        "kook_reconnect_delay": 1,
                        "kook_max_reconnect_delay": 60,
                        "kook_max_retry_delay": 60,
                        "kook_heartbeat_interval": 30,
                        "kook_heartbeat_timeout": 6,
                        "kook_max_heartbeat_failures": 3,
                        "kook_max_consecutive_failures": 5,
                    },
                    "Mattermost": {
                        "id": "mattermost",
                        "type": "mattermost",
                        "enable": True,
                        "mattermost_url": "https://chat.example.com",
                        "mattermost_bot_token": "",
                        "mattermost_reconnect_delay": 5.0,
                    },
                    # "WebChat": {
                    #     "id": "webchat",
                    #     "type": "webchat",
                    #     "enable": False,
                    #     "webchat_link_path": "",
                    #     "webchat_present_type": "fullscreen",
                    # },
                },
                "items": {
                    # "webchat_link_path": {
                    #     "description": "链接路径",
                    #     "_special": "webchat_link_path",
                    #     "type": "string",
                    # },
                    # "webchat_present_type": {
                    #     "_special": "webchat_present_type",
                    #     "description": "展现形式",
                    #     "type": "string",
                    #     "options": ["fullscreen", "embedded"],
                    # },
                    "app_id": {
                        "description": "ID da aplicação",
                        "type": "string",
                        "hint": "ID do aplicativo no console de desenvolvedor da plataforma de mensagens.",
                        "show_key": True,
                    },
                    "app_secret": {
                        "description": "Secret da aplicação",
                        "type": "string",
                        "hint": "Mantenha esta credencial protegida.",
                        "show_key": True,
                        "secret": True,
                    },
                    "domain": {
                        "description": "URL da API da plataforma",
                        "type": "string",
                        "hint": "URL base da API da plataforma aberta. Normalmente não é necessário alterar o padrão.",
                        "show_key": True,
                    },
                    "corpid": {
                        "description": "ID da empresa",
                        "type": "string",
                        "hint": "ID da empresa (CorpID) no console de administração do WeCom.",
                        "show_key": True,
                    },
                    "token": {
                        "description": "Token de callback",
                        "type": "string",
                        "hint": "Token usado para verificar requisições nas configurações de callback da plataforma de mensagens.",
                        "show_key": True,
                        "secret": True,
                    },
                    "encoding_aes_key": {
                        "description": "Chave de criptografia das mensagens",
                        "type": "string",
                        "hint": "EncodingAESKey das configurações de callback, usada para criptografar e descriptografar mensagens.",
                        "show_key": True,
                        "secret": True,
                    },
                    "api_base_url": {
                        "description": "URL base da API",
                        "type": "string",
                        "hint": "URL base da API da plataforma de mensagens. Normalmente não é necessário alterar o padrão.",
                        "show_key": True,
                    },
                    "client_id": {
                        "description": "ID do cliente",
                        "type": "string",
                        "hint": "ID do cliente no console de desenvolvedor da plataforma de mensagens.",
                        "show_key": True,
                    },
                    "client_secret": {
                        "description": "Segredo do cliente",
                        "type": "string",
                        "hint": "Mantenha esta credencial protegida.",
                        "show_key": True,
                        "secret": True,
                    },
                    "start_message": {
                        "description": "Resposta ao comando /start",
                        "type": "string",
                        "hint": "Mensagem enviada quando o usuário usa o comando /start no bot do Telegram.",
                        "show_key": True,
                    },
                    "telegram_api_base_url": {
                        "description": "URL da API",
                        "type": "string",
                        "hint": "URL base da API de bots do Telegram. Normalmente não é necessário alterar o padrão oficial.",
                        "show_key": True,
                    },
                    "telegram_file_base_url": {
                        "description": "URL da API de arquivos",
                        "type": "string",
                        "hint": "URL base para baixar arquivos pela API de bots do Telegram. Normalmente não é necessário alterar o padrão oficial.",
                        "show_key": True,
                    },
                    "bot_token": {
                        "description": "Token do bot do Slack",
                        "type": "string",
                        "hint": "Bot User OAuth Token do aplicativo Slack, geralmente iniciado por xoxb-.",
                        "show_key": True,
                        "secret": True,
                    },
                    "app_token": {
                        "description": "Token do aplicativo Slack",
                        "type": "string",
                        "hint": "Token de aplicativo usado pelo Socket Mode do Slack, geralmente iniciado por xapp-.",
                        "condition": {
                            "slack_connection_mode": "socket",
                        },
                        "show_key": True,
                        "secret": True,
                    },
                    "signing_secret": {
                        "description": "Segredo de assinatura do Slack",
                        "type": "string",
                        "hint": "Segredo de assinatura do aplicativo Slack, usado para verificar requisições de webhook.",
                        "condition": {
                            "slack_connection_mode": "webhook",
                        },
                        "show_key": True,
                        "secret": True,
                    },
                    "channel_access_token": {
                        "description": "Token de acesso ao canal do LINE",
                        "type": "string",
                        "hint": "Token de acesso do canal da API de mensagens do LINE.",
                        "show_key": True,
                        "secret": True,
                    },
                    "channel_secret": {
                        "description": "Segredo do canal do LINE",
                        "type": "string",
                        "hint": "Segredo do canal da API de mensagens do LINE.",
                        "show_key": True,
                        "secret": True,
                    },
                    "lark_connection_mode": {
                        "description": "Modo de assinatura",
                        "type": "string",
                        "options": ["socket", "webhook"],
                        "labels": ["Conexão persistente", "Servidor de webhook"],
                    },
                    "lark_encrypt_key": {
                        "description": "Chave de criptografia",
                        "type": "string",
                        "hint": "Chave de criptografia para descriptografar dados de callback do Lark.",
                        "secret": True,
                        "condition": {
                            "lark_connection_mode": "webhook",
                        },
                    },
                    "lark_verification_token": {
                        "description": "Token de verificação",
                        "type": "string",
                        "hint": "Token para verificar requisições de callback do Lark.",
                        "secret": True,
                        "condition": {
                            "lark_connection_mode": "webhook",
                        },
                    },
                    "is_sandbox": {
                        "description": "Modo Sandbox",
                        "type": "bool",
                    },
                    "satori_api_base_url": {
                        "description": "Endpoint da API do Satori",
                        "type": "string",
                        "hint": "URL base da API do Satori.",
                    },
                    "satori_endpoint": {
                        "description": "Endpoint WebSocket do Satori",
                        "type": "string",
                        "hint": "Endpoint WebSocket para eventos do Satori.",
                    },
                    "satori_token": {
                        "description": "Token do Satori",
                        "type": "string",
                        "hint": "Token de autenticação na API do Satori.",
                        "secret": True,
                    },
                    "satori_auto_reconnect": {
                        "description": "Ativar reconexão automática",
                        "type": "bool",
                        "hint": "Reconecta automaticamente o WebSocket quando a conexão é perdida.",
                    },
                    "satori_heartbeat_interval": {
                        "description": "Intervalo de verificação da conexão do Satori",
                        "type": "int",
                        "hint": "Intervalo entre mensagens de verificação da conexão, em segundos.",
                    },
                    "satori_reconnect_delay": {
                        "description": "Espera para reconexão do Satori",
                        "type": "int",
                        "hint": "Espera antes de tentar reconectar, em segundos.",
                    },
                    "slack_connection_mode": {
                        "description": "Modo de conexão do Slack",
                        "type": "string",
                        "options": ["webhook", "socket"],
                        "hint": "Modo de conexão do Slack. `webhook` usa um servidor de webhook; `socket` usa o Socket Mode do Slack.",
                    },
                    "slack_webhook_host": {
                        "description": "Host do webhook do Slack",
                        "type": "string",
                        "hint": "Válido apenas quando o modo de conexão do Slack é `webhook`.",
                        "condition": {
                            "slack_connection_mode": "webhook",
                            "unified_webhook_mode": False,
                        },
                    },
                    "slack_webhook_port": {
                        "description": "Porta do webhook do Slack",
                        "type": "int",
                        "hint": "Válido apenas quando o modo de conexão do Slack é `webhook`.",
                        "condition": {
                            "slack_connection_mode": "webhook",
                            "unified_webhook_mode": False,
                        },
                    },
                    "slack_webhook_path": {
                        "description": "Caminho do webhook do Slack",
                        "type": "string",
                        "hint": "Válido apenas quando o modo de conexão do Slack é `webhook`.",
                        "condition": {
                            "slack_connection_mode": "webhook",
                            "unified_webhook_mode": False,
                        },
                    },
                    "active_send_mode": {
                        "description": "Usar API de envio proativo",
                        "type": "bool",
                        "desc": "Apenas contas oficiais com verificação empresarial podem enviar mensagens proativas. A API de envio proativo tem menos restrições.",
                    },
                    "wpp_active_message_poll": {
                        "description": "Ativar consulta proativa de mensagens",
                        "type": "bool",
                        "hint": "Ative apenas se as mensagens do WeChat não estiverem sendo sincronizadas com o AstrBot a tempo. Desativado por padrão.",
                    },
                    "wpp_active_message_poll_interval": {
                        "description": "Intervalo de consulta proativa de mensagens",
                        "type": "int",
                        "hint": "Intervalo em segundos. Padrão: 3. Não deve ultrapassar 60, pois as mensagens podem ser consideradas antigas.",
                    },
                    "kf_name": {
                        "description": "Nome da conta de atendimento do WeChat",
                        "type": "string",
                        "hint": "Opcional. Nome da conta de atendimento (não o ID). Obtenha em https://kf.weixin.qq.com/kf/frame#/accounts",
                    },
                    "telegram_token": {
                        "description": "Token do bot",
                        "type": "string",
                        "hint": "Se estiver na China continental, configure um proxy ou altere api_base em Outras configurações.",
                        "secret": True,
                    },
                    "mattermost_url": {
                        "description": "URL do Mattermost",
                        "type": "string",
                        "hint": "URL do serviço Mattermost, por exemplo, https://chat.example.com.",
                    },
                    "mattermost_bot_token": {
                        "description": "Token do bot do Mattermost",
                        "type": "string",
                        "hint": "Token de acesso gerado após criar uma conta de bot no Mattermost.",
                        "secret": True,
                    },
                    "mattermost_reconnect_delay": {
                        "description": "Espera para reconexão do Mattermost",
                        "type": "float",
                        "hint": "Espera, em segundos, antes de reconectar após a desconexão do WebSocket. Padrão: 5 segundos.",
                    },
                    "misskey_instance_url": {
                        "description": "URL da instância Misskey",
                        "type": "string",
                        "hint": "Por exemplo, https://misskey.example. Instância Misskey que hospeda a conta do bot.",
                    },
                    "misskey_token": {
                        "description": "Token de acesso ao Misskey",
                        "type": "string",
                        "hint": "Token de acesso à API gerado nas configurações do serviço de conexão.",
                        "secret": True,
                    },
                    "misskey_default_visibility": {
                        "description": "Visibilidade padrão das publicações",
                        "type": "string",
                        "options": ["public", "home", "followers"],
                        "hint": "Visibilidade padrão das publicações do bot. public: pública; home: linha do tempo inicial; followers: apenas seguidores.",
                    },
                    "misskey_local_only": {
                        "description": "Somente local (sem federação)",
                        "type": "bool",
                        "hint": "Quando ativado, as publicações do bot ficam visíveis apenas nesta instância e não são federadas.",
                    },
                    "misskey_enable_chat": {
                        "description": "Ativar respostas às mensagens de conversa",
                        "type": "bool",
                        "hint": "Quando ativado, o bot recebe e responde a mensagens de conversas privadas.",
                    },
                    "misskey_enable_file_upload": {
                        "description": "Ativar envio de arquivos ao Misskey",
                        "type": "bool",
                        "hint": "Quando ativado, o adaptador envia os arquivos das cadeias de mensagens ao Misskey. Para arquivos por URL, tenta primeiro o envio pelo servidor; se o envio assíncrono falhar, baixa e envia o arquivo localmente.",
                    },
                    "misskey_allow_insecure_downloads": {
                        "description": "Permitir downloads inseguros (desativar verificação SSL)",
                        "type": "bool",
                        "hint": "Se os servidores remotos tiverem problemas de certificado, a verificação SSL será desativada como alternativa. Use apenas quando necessário devido aos riscos de segurança.",
                    },
                    "misskey_download_timeout": {
                        "description": "Tempo limite de download remoto (segundos)",
                        "type": "int",
                        "hint": "Tempo limite para baixar arquivos remotos, em segundos, usado na alternativa de envio local.",
                    },
                    "misskey_download_chunk_size": {
                        "description": "Tamanho dos blocos de download em streaming (bytes)",
                        "type": "int",
                        "hint": "Bytes lidos por bloco durante o download em streaming e o cálculo de MD5. Valores muito baixos aumentam o custo de processamento; valores muito altos usam mais memória.",
                    },
                    "misskey_max_download_bytes": {
                        "description": "Tamanho máximo de download (bytes)",
                        "type": "int",
                        "hint": "Defina o máximo de bytes para limitar o download e evitar falta de memória. Vazio ou null significa sem limite.",
                    },
                    "misskey_upload_concurrency": {
                        "description": "Limite de envios simultâneos",
                        "type": "int",
                        "hint": "Número máximo de tarefas de envio simultâneas (inteiro; padrão: 3).",
                    },
                    "misskey_upload_folder": {
                        "description": "ID da pasta de destino no Drive",
                        "type": "string",
                        "hint": "Opcional: ID da pasta de destino no Drive do Misskey. Deixe vazio para usar a pasta raiz.",
                    },
                    "card_template_id": {
                        "description": "ID do template de cartão",
                        "type": "string",
                        "hint": "Opcional. ID do modelo de cartão interativo do DingTalk. Quando ativado, as respostas em streaming usam cartões interativos.",
                    },
                    "telegram_command_register": {
                        "description": "Registrar comandos do Telegram",
                        "type": "bool",
                        "hint": "Quando ativado, o AstrBot registra automaticamente os comandos do Telegram.",
                        "show_key": True,
                    },
                    "telegram_command_auto_refresh": {
                        "description": "Atualizar comandos automaticamente",
                        "type": "bool",
                        "hint": "Quando ativado, o AstrBot atualiza automaticamente os comandos do Telegram durante a execução. Esta opção sozinha não produz efeito.",
                        "show_key": True,
                    },
                    "telegram_command_register_interval": {
                        "description": "Intervalo de atualização automática dos comandos",
                        "type": "int",
                        "hint": "Intervalo de atualização automática dos comandos do Telegram, em segundos.",
                        "show_key": True,
                    },
                    "telegram_polling_restart_delay": {
                        "description": "Espera para reiniciar a consulta de mensagens",
                        "type": "float",
                        "hint": "Espera, em segundos, para reiniciar o ciclo de consulta após um encerramento inesperado. Padrão: 5 segundos.",
                        "show_key": True,
                    },
                    "id": {
                        "description": "Nome do bot",
                        "type": "string",
                        "hint": "Nome do bot",
                    },
                    "type": {
                        "description": "Tipo de adaptador",
                        "type": "string",
                        "invisible": True,
                    },
                    "enable": {
                        "description": "Ativar",
                        "type": "bool",
                        "hint": "Adaptadores desativados não recebem mensagens.",
                    },
                    "appid": {
                        "description": "ID do aplicativo",
                        "type": "string",
                        "hint": "Obrigatório. ID do aplicativo da plataforma de mensagens atual. Consulte a documentação de integração para saber como obtê-lo.",
                    },
                    "secret": {
                        "description": "Segredo",
                        "type": "string",
                        "hint": "Obrigatório.",
                        "secret": True,
                    },
                    "enable_group_c2c": {
                        "description": "Ativar conversas privadas da lista de mensagens",
                        "type": "bool",
                        "hint": "Quando ativado, o bot recebe conversas privadas da lista de mensagens do QQ. Talvez seja necessário adicionar o bot como amigo lendo um código QR na plataforma de bots do QQ. Consulte a documentação.",
                    },
                    "enable_guild_direct_message": {
                        "description": "Ativar mensagens diretas do servidor",
                        "type": "bool",
                        "hint": "Quando ativado, o bot recebe mensagens diretas do servidor.",
                    },
                    "use_markdown": {
                        "description": "Usar Markdown em mensagens proativas",
                        "type": "bool",
                        "hint": "Quando ativado, as mensagens proativas são enviadas em Markdown por padrão; uma chamada explícita de use_markdown() de um plugin tem prioridade sobre esta opção.",
                    },
                    "ws_reverse_host": {
                        "description": "Host do WebSocket reverso",
                        "type": "string",
                        "hint": "O AstrBot atua como servidor.",
                    },
                    "ws_reverse_port": {
                        "description": "Porta do WebSocket reverso",
                        "type": "int",
                    },
                    "ws_reverse_token": {
                        "description": "Token do WebSocket reverso",
                        "type": "string",
                        "hint": "Token do WebSocket reverso. Se não for definido, a verificação de token será desativada.",
                        "secret": True,
                    },
                    "wecom_ai_bot_name": {
                        "description": "Nome do bot de IA do WeCom",
                        "type": "string",
                        "hint": "Deve estar correto; caso contrário, alguns comandos não funcionarão.",
                    },
                    "wecom_ai_bot_connection_mode": {
                        "description": "Modo de conexão do bot de IA do WeCom",
                        "type": "string",
                        "options": ["webhook", "long_connection"],
                        "labels": ["Callback de webhook", "Conexão persistente"],
                        "hint": "O modo webhook exige Token/EncodingAESKey; o modo long_connection exige BotID/Secret.",
                    },
                    "wecomaibot_init_respond_text": {
                        "description": "Texto da resposta inicial do bot de IA do WeCom",
                        "type": "string",
                        "hint": "Primeira resposta quando o bot recebe uma mensagem. Deixe vazio para desativar.",
                    },
                    "wecomaibot_friend_message_welcome_text": {
                        "description": "Mensagem de boas-vindas em conversa privada do bot de IA do WeCom",
                        "type": "string",
                        "hint": "Envia uma mensagem de boas-vindas quando um usuário entra em uma conversa privada naquele dia. Deixe vazio para desativar.",
                    },
                    "wecomaibot_token": {
                        "description": "Token do bot de IA do WeCom",
                        "type": "string",
                        "hint": "Usado para autenticação no modo de callback por webhook.",
                        "secret": True,
                        "condition": {
                            "wecom_ai_bot_connection_mode": "webhook",
                        },
                    },
                    "wecomaibot_encoding_aes_key": {
                        "description": "EncodingAESKey do bot de IA do WeCom",
                        "type": "string",
                        "hint": "Usada para criptografar e descriptografar mensagens no modo de callback por webhook.",
                        "secret": True,
                        "condition": {
                            "wecom_ai_bot_connection_mode": "webhook",
                        },
                    },
                    "msg_push_webhook_url": {
                        "description": "URL do Webhook de envio de mensagens do WeCom",
                        "type": "string",
                        "hint": "Usado para envio proativo de mensagens. A configuração é altamente recomendada para melhorar a experiência de envio.",
                        "secret": True,
                    },
                    "only_use_webhook_url_to_send": {
                        "description": "Enviar respostas somente por webhook",
                        "type": "bool",
                        "hint": "Quando ativado, todas as respostas do bot de IA do WeCom são enviadas por msg_push_webhook_url. Esse webhook aceita mais tipos de mensagem, como imagens e arquivos. Se você não precisa do efeito de digitação, esta opção é altamente recomendada.",
                    },
                    "wecomaibot_ws_bot_id": {
                        "description": "BotID da conexão persistente",
                        "type": "string",
                        "hint": "Credencial BotID do modo de conexão persistente do bot de IA do WeCom.",
                        "condition": {
                            "wecom_ai_bot_connection_mode": "long_connection",
                        },
                    },
                    "wecomaibot_ws_secret": {
                        "description": "Segredo da conexão persistente",
                        "type": "string",
                        "hint": "Credencial Secret do modo de conexão persistente do bot de IA do WeCom.",
                        "secret": True,
                        "condition": {
                            "wecom_ai_bot_connection_mode": "long_connection",
                        },
                    },
                    "wecomaibot_ws_url": {
                        "description": "URL WebSocket da conexão persistente",
                        "type": "string",
                        "invisible": True,
                        "hint": "O padrão é wss://openws.work.weixin.qq.com e normalmente não precisa ser alterado.",
                        "condition": {
                            "wecom_ai_bot_connection_mode": "long_connection",
                        },
                    },
                    "wecomaibot_heartbeat_interval": {
                        "description": "Intervalo de verificação da conexão persistente",
                        "type": "int",
                        "invisible": True,
                        "hint": "Intervalo de verificação da conexão, em segundos, no modo persistente. Recomendado: 30 segundos.",
                        "condition": {
                            "wecom_ai_bot_connection_mode": "long_connection",
                        },
                    },
                    "discord_token": {
                        "description": "Token do bot do Discord",
                        "type": "string",
                        "hint": "Informe aqui o token do seu bot do Discord.",
                        "secret": True,
                    },
                    "discord_proxy": {
                        "description": "URL de proxy do Discord",
                        "type": "string",
                        "hint": "URL de proxy opcional: http://ip:port",
                    },
                    "discord_command_register": {
                        "description": "Registrar slash commands no Discord",
                        "hint": "Quando ativado, o AstrBot registra automaticamente os comandos dos plugins como comandos de barra do Discord.",
                        "type": "bool",
                    },
                    "discord_activity_name": {
                        "description": "Nome da atividade no Discord",
                        "type": "string",
                        "hint": "Nome opcional da atividade no Discord. Deixe vazio para desativar.",
                    },
                    "discord_allow_bot_messages": {
                        "description": "Permitir mensagens de outros bots",
                        "type": "bool",
                        "hint": "Quando ativado, o AstrBot recebe mensagens de outros bots do Discord. Útil para comunicação entre bots, como encaminhamento de mensagens. Desativado por padrão.",
                    },
                    "port": {
                        "description": "Porta do servidor de callback",
                        "type": "int",
                        "hint": "Porta do servidor de callback. Deixe vazio para desativar o servidor.",
                        "condition": {
                            "unified_webhook_mode": False,
                        },
                    },
                    "callback_server_host": {
                        "description": "Host do servidor de callback",
                        "type": "string",
                        "hint": "Host do servidor de callback. Deixe vazio para desativar o servidor.",
                        "condition": {
                            "unified_webhook_mode": False,
                        },
                    },
                    "unified_webhook_mode": {
                        "description": "Modo Webhook unificado",
                        "type": "bool",
                        "hint": "Quando ativado, usa a entrada unificada de webhook do AstrBot sem abrir uma porta separada. URL de callback: /api/v1/webhooks/platforms/{webhook_uuid}.",
                    },
                    **PERSONAL_WECHAT_CONFIG_METADATA,
                    "webhook_uuid": {
                        "invisible": True,
                        "description": "UUID do Webhook",
                        "type": "string",
                        "hint": "Identificador exclusivo do modo de webhook unificado, gerado ao criar a plataforma.",
                    },
                    "kook_bot_token": {
                        "description": "Token do bot",
                        "type": "string",
                        "hint": "Obrigatório. Token do bot obtido na plataforma de desenvolvedores do KOOK.",
                        "secret": True,
                    },
                    "kook_reconnect_delay": {
                        "description": "Espera para reconexão",
                        "type": "int",
                        "hint": "Espera para reconectar, em segundos, usando uma estratégia de espera exponencial.",
                    },
                    "kook_max_reconnect_delay": {
                        "description": "Espera máxima para reconexão",
                        "type": "int",
                        "hint": "Valor máximo da espera para reconectar, em segundos.",
                    },
                    "kook_max_retry_delay": {
                        "description": "Espera máxima entre tentativas",
                        "type": "int",
                        "hint": "Espera máxima entre tentativas, em segundos.",
                    },
                    "kook_heartbeat_interval": {
                        "description": "Intervalo de verificação da conexão",
                        "type": "int",
                        "hint": "Intervalo entre verificações da conexão, em segundos.",
                    },
                    "kook_heartbeat_timeout": {
                        "description": "Tempo limite de verificação da conexão",
                        "type": "int",
                        "hint": "Tempo limite da verificação da conexão, em segundos.",
                    },
                    "kook_max_heartbeat_failures": {
                        "description": "Máximo de falhas na verificação da conexão",
                        "type": "int",
                        "hint": "Número máximo de falhas permitidas na verificação da conexão; a conexão será encerrada se for ultrapassado.",
                    },
                    "kook_max_consecutive_failures": {
                        "description": "Máximo de falhas consecutivas",
                        "type": "int",
                        "hint": "Número máximo de falhas consecutivas permitidas; as tentativas serão interrompidas se for ultrapassado.",
                    },
                },
            },
            "platform_settings": {
                "type": "object",
                "items": {
                    "unique_session": {
                        "type": "bool",
                    },
                    "rate_limit": {
                        "type": "object",
                        "items": {
                            "time": {"type": "int"},
                            "count": {"type": "int"},
                            "strategy": {
                                "type": "string",
                                "options": ["stall", "discard"],
                            },
                        },
                    },
                    "no_permission_reply": {
                        "type": "bool",
                        "hint": "Quando ativado, o bot responde quando o usuário não tem permissão para executar uma operação.",
                    },
                    "empty_mention_waiting": {
                        "type": "bool",
                        "hint": "Quando a mensagem contém apenas uma menção ao bot, aguarda até 60 segundos pela próxima mensagem do mesmo usuário. Útil em plataformas que não permitem enviar menção e áudio ou imagem juntos.",
                    },
                    "empty_mention_waiting_need_reply": {
                        "type": "bool",
                        "hint": "Se a espera pela próxima mensagem estiver ativada, esta opção permite gerar uma resposta com o modelo. Caso contrário, o bot apenas aguarda.",
                    },
                    "friend_message_needs_wake_prefix": {
                        "type": "bool",
                        "hint": "Quando ativado, mensagens privadas exigem o prefixo de ativação, assim como as mensagens em grupo.",
                    },
                    "ignore_bot_self_message": {
                        "type": "bool",
                        "hint": "Algumas plataformas também entregam mensagens da própria conta enviadas por outros aplicativos, o que pode ativar o bot ao enviar mensagens para si mesmo.",
                    },
                    "ignore_at_all": {
                        "type": "bool",
                        "hint": "Quando ativado, o bot ignora mensagens com menção a todos.",
                    },
                    "segmented_reply": {
                        "type": "object",
                        "items": {
                            "enable": {
                                "type": "bool",
                            },
                            "only_llm_result": {
                                "type": "bool",
                            },
                            "interval_method": {
                                "type": "string",
                                "options": ["random", "log"],
                            },
                            "interval": {
                                "type": "string",
                            },
                            "log_base": {
                                "type": "float",
                            },
                            "words_count_threshold": {
                                "type": "int",
                            },
                            "regex": {
                                "type": "string",
                            },
                            "content_cleanup_rule": {
                                "type": "string",
                            },
                        },
                    },
                    "reply_prefix": {
                        "type": "string",
                        "hint": "Prefixo acrescentado às respostas do bot.",
                    },
                    "forward_threshold": {
                        "type": "int",
                        "hint": "Acima de um limite de caracteres, o bot agrupa o texto em uma mensagem encaminhada do QQ para evitar excesso de mensagens. Disponível apenas no adaptador QQ.",
                    },
                    "enable_id_white_list": {
                        "type": "bool",
                    },
                    "id_whitelist": {
                        "type": "list",
                        "items": {"type": "string"},
                        "hint": "Processa apenas mensagens dos IDs informados. Vazio desativa a filtragem. Use /sid para obter o ID da sessão (como abc:GroupMessage:123). Administradores podem editar a lista no painel em Configurações -> Controle de acesso -> Lista de permissões.",
                    },
                    "id_whitelist_log": {
                        "type": "bool",
                        "hint": "Quando ativado, registra em nível INFO as mensagens que não passam pela lista de permissões.",
                    },
                    "wl_ignore_admin_on_group": {
                        "type": "bool",
                    },
                    "wl_ignore_admin_on_friend": {
                        "type": "bool",
                    },
                    "reply_with_mention": {
                        "type": "bool",
                        "hint": "Quando ativado, o bot menciona o remetente na resposta. O efeito depende do adaptador da plataforma.",
                    },
                    "reply_with_quote": {
                        "type": "bool",
                        "hint": "Quando ativado, o bot cita a mensagem original na resposta. O efeito depende do adaptador da plataforma.",
                    },
                    "path_mapping": {
                        "type": "list",
                        "items": {"type": "string"},
                        "hint": "Resolve diferenças de caminhos entre sistemas de arquivos. Formato: <caminho_original>:<caminho_mapeado>. Exemplo: `/app/.config/QQ:/var/lib/docker/volumes/xxxx/_data`. O prefixo `/app/.config/QQ` dos arquivos de imagem e áudio recebidos é substituído pelo caminho mapeado. Útil em implantações com Docker.",
                    },
                },
            },
            "content_safety": {
                "type": "object",
                "items": {
                    "also_use_in_response": {
                        "type": "bool",
                        "hint": "Quando ativado, as respostas do modelo também passam pela moderação de conteúdo.",
                    },
                    "baidu_aip": {
                        "type": "object",
                        "items": {
                            "enable": {
                                "type": "bool",
                                "hint": "Antes de ativar, instale manualmente a biblioteca baidu-aip: `pip3 install baidu-aip`.",
                            },
                            "app_id": {"description": "APP ID", "type": "string"},
                            "api_key": {
                                "description": "API Key",
                                "type": "string",
                                "secret": True,
                            },
                            "secret_key": {
                                "type": "string",
                                "secret": True,
                            },
                        },
                    },
                    "internal_keywords": {
                        "type": "object",
                        "items": {
                            "enable": {
                                "type": "bool",
                            },
                            "extra_keywords": {
                                "type": "list",
                                "items": {"type": "string"},
                                "hint": "Lista adicional de palavras-chave bloqueadas. Aceita expressões regulares.",
                            },
                        },
                    },
                },
            },
        },
    },
    "provider_group": {
        "name": "Provedores de serviços",
        "metadata": {
            "provider": {
                "type": "list",
                # provider sources templates
                "config_template": {
                    "OpenAI Compatible": {
                        "id": "openai",
                        "provider": "openai",
                        "type": "openai_chat_completion",
                        "provider_type": "chat_completion",
                        "enable": True,
                        "key": [],
                        "api_base": "https://api.openai.com/v1",
                        "timeout": 120,
                        "proxy": "",
                        "custom_headers": {},
                    },
                    "OpenAI Responses": {
                        "id": "openai-responses",
                        "provider": "openai",
                        "type": "openai_responses",
                        "provider_type": "chat_completion",
                        "enable": True,
                        "key": [],
                        "api_base": "https://api.openai.com/v1",
                        "timeout": 120,
                        "proxy": "",
                        "custom_headers": {},
                    },
                    "Google Gemini": {
                        "id": "google_gemini",
                        "provider": "google",
                        "type": "googlegenai_chat_completion",
                        "provider_type": "chat_completion",
                        "enable": True,
                        "key": [],
                        "api_base": "https://generativelanguage.googleapis.com/",
                        "timeout": 120,
                        "gm_resp_image_modal": False,
                        "gm_native_search": False,
                        "gm_native_coderunner": False,
                        "gm_url_context": False,
                        "gm_safety_settings": {
                            "harassment": "BLOCK_MEDIUM_AND_ABOVE",
                            "hate_speech": "BLOCK_MEDIUM_AND_ABOVE",
                            "sexually_explicit": "BLOCK_MEDIUM_AND_ABOVE",
                            "dangerous_content": "BLOCK_MEDIUM_AND_ABOVE",
                        },
                        "gm_thinking_config": {"budget": 0, "level": "HIGH"},
                        "proxy": "",
                    },
                    "Anthropic": {
                        "id": "anthropic",
                        "provider": "anthropic",
                        "type": "anthropic_chat_completion",
                        "provider_type": "chat_completion",
                        "enable": True,
                        "key": [],
                        "api_base": "https://api.anthropic.com",
                        "timeout": 120,
                        "proxy": "",
                        "custom_headers": {},
                        "anth_thinking_config": {"type": "", "budget": 0, "effort": ""},
                    },
                    "Kimi Coding Plan": {
                        "id": "kimi-code",
                        "provider": "kimi-code",
                        "type": "kimi_code_chat_completion",
                        "provider_type": "chat_completion",
                        "enable": True,
                        "key": [],
                        "api_base": "https://api.kimi.com/coding",
                        "timeout": 120,
                        "proxy": "",
                        "custom_headers": {},
                        "anth_thinking_config": {"type": "", "budget": 0, "effort": ""},
                    },
                    "Moonshot": {
                        "id": "moonshot",
                        "provider": "moonshot",
                        "type": "openai_chat_completion",
                        "provider_type": "chat_completion",
                        "enable": True,
                        "key": [],
                        "timeout": 120,
                        "api_base": "https://api.moonshot.cn/v1",
                        "proxy": "",
                        "custom_headers": {},
                    },
                    "MiniMax": {
                        "id": "minimax",
                        "provider": "minimax",
                        "type": "openai_chat_completion",
                        "provider_type": "chat_completion",
                        "enable": True,
                        "key": [],
                        "api_base": "https://api.minimaxi.com/v1",
                        "timeout": 120,
                        "proxy": "",
                        "custom_headers": {},
                    },
                    "MiniMax Token Plan": {
                        "id": "minimax-token-plan",
                        "provider": "minimax-token-plan",
                        "type": "minimax_token_plan",
                        "provider_type": "chat_completion",
                        "enable": True,
                        "key": [],
                        "api_base": "https://api.minimaxi.com/anthropic",
                        "timeout": 120,
                        "proxy": "",
                        "custom_headers": {},
                        "anth_thinking_config": {"type": "", "budget": 0, "effort": ""},
                    },
                    "Xiaomi": {
                        "id": "xiaomi",
                        "provider": "xiaomi",
                        "type": "xiaomi_chat_completion",
                        "provider_type": "chat_completion",
                        "enable": True,
                        "key": [],
                        "api_base": "https://api.xiaomimimo.com/v1",
                        "timeout": 120,
                        "proxy": "",
                        "custom_headers": {},
                    },
                    "Xiaomi Token Plan": {
                        "id": "xiaomi-token-plan",
                        "provider": "xiaomi-token-plan",
                        "type": "xiaomi_token_plan",
                        "provider_type": "chat_completion",
                        "enable": True,
                        "key": [],
                        "api_base": "https://token-plan-cn.xiaomimimo.com/anthropic",
                        "timeout": 120,
                        "proxy": "",
                        "custom_headers": {},
                        "anth_thinking_config": {"type": "", "budget": 0, "effort": ""},
                    },
                    "xAI": {
                        "id": "xai",
                        "provider": "xai",
                        "type": "openai_responses",
                        "provider_type": "chat_completion",
                        "enable": True,
                        "key": [],
                        "api_base": "https://api.x.ai/v1",
                        "timeout": 120,
                        "proxy": "",
                        "custom_headers": {},
                    },
                    "DeepSeek": {
                        "id": "deepseek",
                        "provider": "deepseek",
                        "type": "openai_chat_completion",
                        "provider_type": "chat_completion",
                        "enable": True,
                        "key": [],
                        "api_base": "https://api.deepseek.com/v1",
                        "timeout": 120,
                        "proxy": "",
                        "custom_headers": {},
                    },
                    "DeepSeek Responses": {
                        "id": "deepseek-responses",
                        "provider": "deepseek",
                        "type": "openai_responses",
                        "provider_type": "chat_completion",
                        "enable": True,
                        "key": [],
                        "api_base": "https://api.deepseek.com/v1",
                        "timeout": 120,
                        "proxy": "",
                        "custom_headers": {},
                    },
                    "Zhipu": {
                        "id": "zhipu",
                        "provider": "zhipu",
                        "type": "zhipu_chat_completion",
                        "provider_type": "chat_completion",
                        "enable": True,
                        "key": [],
                        "timeout": 120,
                        "api_base": "https://open.bigmodel.cn/api/paas/v4/",
                        "proxy": "",
                        "custom_headers": {},
                    },
                    "LongCat": {
                        "id": "longcat",
                        "provider": "longcat",
                        "type": "longcat_chat_completion",
                        "provider_type": "chat_completion",
                        "enable": True,
                        "key": [],
                        "api_base": "https://api.longcat.chat/openai",
                        "timeout": 120,
                        "proxy": "",
                        "custom_headers": {},
                    },
                    "AIHubMix": {
                        "id": "aihubmix",
                        "provider": "aihubmix",
                        "type": "aihubmix_chat_completion",
                        "provider_type": "chat_completion",
                        "enable": True,
                        "key": [],
                        "timeout": 120,
                        "api_base": "https://aihubmix.com/v1",
                        "proxy": "",
                        "custom_headers": {},
                    },
                    "MiraRouter": {
                        "id": "mirarouter",
                        "provider": "mirarouter",
                        "type": "mirarouter_chat_completion",
                        "provider_type": "chat_completion",
                        "enable": True,
                        "key": [],
                        "timeout": 120,
                        "api_base": "https://api.mirarouter.com/v1",
                        "proxy": "",
                        "custom_headers": {},
                    },
                    "OpenRouter": {
                        "id": "openrouter",
                        "provider": "openrouter",
                        "type": "openrouter_chat_completion",
                        "provider_type": "chat_completion",
                        "enable": True,
                        "key": [],
                        "timeout": 120,
                        "api_base": "https://openrouter.ai/api/v1",
                        "proxy": "",
                        "custom_headers": {},
                    },
                    "SSYCloud(胜算云)": {
                        "id": "ssycloud",
                        "provider": "ssycloud",
                        "type": "ssycloud_chat_completion",
                        "provider_type": "chat_completion",
                        "enable": True,
                        "key": [],
                        "timeout": 120,
                        "api_base": "https://router.shengsuanyun.com/api/v1",
                        "proxy": "",
                        "custom_headers": {"X-Title": "AstrBot"},
                    },
                    "NVIDIA": {
                        "id": "nvidia",
                        "provider": "nvidia",
                        "type": "openai_chat_completion",
                        "provider_type": "chat_completion",
                        "enable": True,
                        "key": [],
                        "api_base": "https://integrate.api.nvidia.com/v1",
                        "timeout": 120,
                        "proxy": "",
                        "custom_headers": {},
                    },
                    "Azure OpenAI": {
                        "id": "azure_openai",
                        "provider": "azure",
                        "type": "openai_chat_completion",
                        "provider_type": "chat_completion",
                        "enable": True,
                        "api_version": "2024-05-01-preview",
                        "key": [],
                        "api_base": "",
                        "timeout": 120,
                        "proxy": "",
                        "custom_headers": {},
                    },
                    "Ollama": {
                        "id": "ollama",
                        "provider": "ollama",
                        "type": "openai_chat_completion",
                        "provider_type": "chat_completion",
                        "enable": True,
                        "key": ["ollama"],  # ollama 的 key 默认是 ollama
                        "api_base": "http://127.0.0.1:11434/v1",
                        "proxy": "",
                        "custom_headers": {},
                        "ollama_disable_thinking": False,
                    },
                    "LM Studio": {
                        "id": "lm_studio",
                        "provider": "lm_studio",
                        "type": "openai_chat_completion",
                        "provider_type": "chat_completion",
                        "enable": True,
                        "key": ["lmstudio"],
                        "api_base": "http://127.0.0.1:1234/v1",
                        "proxy": "",
                        "custom_headers": {},
                    },
                    "Gemini_OpenAI_API": {
                        "id": "google_gemini_openai",
                        "provider": "google",
                        "type": "openai_chat_completion",
                        "provider_type": "chat_completion",
                        "enable": True,
                        "key": [],
                        "api_base": "https://generativelanguage.googleapis.com/v1beta/openai/",
                        "timeout": 120,
                        "proxy": "",
                        "custom_headers": {},
                    },
                    "Groq": {
                        "id": "groq",
                        "provider": "groq",
                        "type": "groq_chat_completion",
                        "provider_type": "chat_completion",
                        "enable": True,
                        "key": [],
                        "api_base": "https://api.groq.com/openai/v1",
                        "timeout": 120,
                        "proxy": "",
                        "custom_headers": {},
                    },
                    "302.AI": {
                        "id": "302ai",
                        "provider": "302ai",
                        "type": "openai_chat_completion",
                        "provider_type": "chat_completion",
                        "enable": True,
                        "key": [],
                        "api_base": "https://api.302.ai/v1",
                        "timeout": 120,
                        "proxy": "",
                        "custom_headers": {},
                    },
                    "SiliconFlow": {
                        "id": "siliconflow",
                        "provider": "siliconflow",
                        "type": "openai_chat_completion",
                        "provider_type": "chat_completion",
                        "enable": True,
                        "key": [],
                        "timeout": 120,
                        "api_base": "https://api.siliconflow.cn/v1",
                        "proxy": "",
                        "custom_headers": {},
                    },
                    "PPIO": {
                        "id": "ppio",
                        "provider": "ppio",
                        "type": "openai_chat_completion",
                        "provider_type": "chat_completion",
                        "enable": True,
                        "key": [],
                        "api_base": "https://api.ppinfra.com/v3/openai",
                        "timeout": 120,
                        "proxy": "",
                        "custom_headers": {},
                    },
                    "TokenPony": {
                        "id": "tokenpony",
                        "provider": "tokenpony",
                        "type": "openai_chat_completion",
                        "provider_type": "chat_completion",
                        "enable": True,
                        "key": [],
                        "api_base": "https://api.tokenpony.cn/v1",
                        "timeout": 120,
                        "proxy": "",
                        "custom_headers": {},
                    },
                    "Compshare": {
                        "id": "compshare",
                        "provider": "compshare",
                        "type": "openai_chat_completion",
                        "provider_type": "chat_completion",
                        "enable": True,
                        "key": [],
                        "api_base": "https://api.modelverse.cn/v1",
                        "timeout": 120,
                        "proxy": "",
                        "custom_headers": {},
                    },
                    "ModelScope": {
                        "id": "modelscope",
                        "provider": "modelscope",
                        "type": "openai_chat_completion",
                        "provider_type": "chat_completion",
                        "enable": True,
                        "key": [],
                        "timeout": 120,
                        "api_base": "https://api-inference.modelscope.cn/v1",
                        "proxy": "",
                        "custom_headers": {},
                    },
                    "FastGPT": {
                        "id": "fastgpt",
                        "provider": "fastgpt",
                        "type": "openai_chat_completion",
                        "provider_type": "chat_completion",
                        "enable": True,
                        "key": [],
                        "api_base": "https://api.fastgpt.in/api/v1",
                        "timeout": 60,
                        "proxy": "",
                        "custom_headers": {},
                        "custom_extra_body": {},
                    },
                    "Whisper(API)": {
                        "id": "whisper",
                        "provider": "openai",
                        "type": "openai_whisper_api",
                        "provider_type": "speech_to_text",
                        "enable": False,
                        "api_key": "",
                        "api_base": "",
                        "model": "whisper-1",
                        "proxy": "",
                    },
                    "MiMo STT(API)": {
                        "id": "mimo_stt",
                        "provider": "mimo",
                        "type": "mimo_stt_api",
                        "provider_type": "speech_to_text",
                        "enable": False,
                        "api_key": "",
                        "api_base": "https://api.xiaomimimo.com/v1",
                        "model": "mimo-v2.5-asr",
                        "timeout": "20",
                        "proxy": "",
                    },
                    "Whisper(Local)": {
                        "provider": "openai",
                        "type": "openai_whisper_selfhost",
                        "provider_type": "speech_to_text",
                        "enable": False,
                        "id": "whisper_selfhost",
                        "model": "tiny",
                        "whisper_device": "cpu",
                    },
                    "SenseVoice(Local)": {
                        "type": "sensevoice_stt_selfhost",
                        "provider": "sensevoice",
                        "provider_type": "speech_to_text",
                        "enable": False,
                        "id": "sensevoice",
                        "stt_model": "iic/SenseVoiceSmall",
                        "is_emotion": False,
                    },
                    "OpenAI TTS(API)": {
                        "id": "openai_tts",
                        "type": "openai_tts_api",
                        "provider": "openai",
                        "provider_type": "text_to_speech",
                        "enable": False,
                        "api_key": "",
                        "api_base": "",
                        "model": "tts-1",
                        "openai-tts-voice": "alloy",
                        "timeout": "20",
                        "proxy": "",
                    },
                    "MiMo TTS(API)": {
                        "id": "mimo_tts",
                        "type": "mimo_tts_api",
                        "provider": "mimo",
                        "provider_type": "text_to_speech",
                        "enable": False,
                        "api_key": "",
                        "api_base": "https://api.xiaomimimo.com/v1",
                        "model": "mimo-v2.5-tts",
                        "mimo-tts-voice": "mimo_default",
                        "mimo-tts-format": "wav",
                        "mimo-tts-style-prompt": "",
                        "mimo-tts-dialect": "",
                        "mimo-tts-seed-text": "Hello, MiMo, have you had lunch?",
                        "timeout": "20",
                        "proxy": "",
                    },
                    "Genie TTS": {
                        "id": "genie_tts",
                        "provider": "genie_tts",
                        "type": "genie_tts",
                        "provider_type": "text_to_speech",
                        "enable": False,
                        "genie_character_name": "mika",
                        "genie_onnx_model_dir": "CharacterModels/v2ProPlus/mika/tts_models",
                        "genie_language": "Japanese",
                        "genie_refer_audio_path": "",
                        "genie_refer_text": "",
                        "timeout": 20,
                    },
                    "Edge TTS": {
                        "id": "edge_tts",
                        "provider": "microsoft",
                        "type": "edge_tts",
                        "provider_type": "text_to_speech",
                        "enable": False,
                        "edge-tts-voice": "zh-CN-XiaoxiaoNeural",
                        "rate": "+0%",
                        "volume": "+0%",
                        "pitch": "+0Hz",
                        "timeout": 20,
                    },
                    "GSV TTS(Local)": {
                        "id": "gsv_tts",
                        "enable": False,
                        "provider": "gpt_sovits",
                        "type": "gsv_tts_selfhost",
                        "provider_type": "text_to_speech",
                        "api_base": "http://127.0.0.1:9880",
                        "gpt_weights_path": "",
                        "sovits_weights_path": "",
                        "timeout": 60,
                        "gsv_default_parms": {
                            "gsv_ref_audio_path": "",
                            "gsv_prompt_text": "",
                            "gsv_prompt_lang": "zh",
                            "gsv_aux_ref_audio_paths": "",
                            "gsv_text_lang": "zh",
                            "gsv_top_k": 5,
                            "gsv_top_p": 1.0,
                            "gsv_temperature": 1.0,
                            "gsv_text_split_method": "cut3",
                            "gsv_batch_size": 1,
                            "gsv_batch_threshold": 0.75,
                            "gsv_split_bucket": True,
                            "gsv_speed_factor": 1,
                            "gsv_fragment_interval": 0.3,
                            "gsv_streaming_mode": False,
                            "gsv_seed": -1,
                            "gsv_parallel_infer": True,
                            "gsv_repetition_penalty": 1.35,
                            "gsv_media_type": "wav",
                        },
                    },
                    "GSVI TTS(API)": {
                        "id": "gsvi_tts",
                        "type": "gsvi_tts_api",
                        "provider": "gpt_sovits_inference",
                        "provider_type": "text_to_speech",
                        "enable": False,
                        "api_key": "",
                        "api_base": "http://127.0.0.1:8000",
                        "version": "v4",
                        "character": "",
                        "prompt_text_lang": "中文",
                        "emotion": "默认",
                        "text_lang": "中文",
                        "timeout": 20,
                    },
                    "FishAudio TTS(API)": {
                        "id": "fishaudio_tts",
                        "provider": "fishaudio",
                        "type": "fishaudio_tts_api",
                        "provider_type": "text_to_speech",
                        "enable": False,
                        "api_key": "",
                        "api_base": "https://api.fish.audio/v1",
                        "model": "s2-pro",
                        "fishaudio-tts-character": "可莉",
                        "fishaudio-tts-reference-id": "",
                        "timeout": "20",
                        "proxy": "",
                    },
                    "阿里云百炼 TTS(API)": {
                        "hint": "Obtenha a chave de API em https://bailian.console.aliyun.com/?tab=model#/api-key. Consulte modelos e vozes em https://help.aliyun.com/zh/model-studio/speech-synthesis-and-speech-recognition.",
                        "id": "dashscope_tts",
                        "provider": "dashscope",
                        "type": "dashscope_tts",
                        "provider_type": "text_to_speech",
                        "enable": False,
                        "api_key": "",
                        "model": "cosyvoice-v1",
                        "dashscope_tts_voice": "loongstella",
                        "timeout": "20",
                    },
                    "Azure TTS": {
                        "id": "azure_tts",
                        "type": "azure_tts",
                        "provider": "azure",
                        "provider_type": "text_to_speech",
                        "enable": True,
                        "azure_tts_voice": "zh-CN-YunxiaNeural",
                        "azure_tts_style": "cheerful",
                        "azure_tts_role": "Boy",
                        "azure_tts_rate": "1",
                        "azure_tts_volume": "100",
                        "azure_tts_subscription_key": "",
                        "azure_tts_region": "eastus",
                        "proxy": "",
                    },
                    "MiniMax TTS(API)": {
                        "id": "minimax_tts",
                        "type": "minimax_tts_api",
                        "provider": "minimax",
                        "provider_type": "text_to_speech",
                        "enable": False,
                        "api_key": "",
                        "api_base": "https://api.minimax.chat/v1/t2a_v2",
                        "minimax-group-id": "",
                        "model": "speech-02-turbo",
                        "minimax-langboost": "auto",
                        "minimax-voice-speed": 1.0,
                        "minimax-voice-vol": 1.0,
                        "minimax-voice-pitch": 0,
                        "minimax-is-timber-weight": False,
                        "minimax-voice-id": "female-shaonv",
                        "minimax-timber-weight": '[\n    {\n        "voice_id": "Chinese (Mandarin)_Warm_Girl",\n        "weight": 25\n    },\n    {\n        "voice_id": "Chinese (Mandarin)_BashfulGirl",\n        "weight": 50\n    }\n]',
                        "minimax-voice-emotion": "auto",
                        "minimax-voice-latex": False,
                        "minimax-voice-english-normalization": False,
                        "timeout": 20,
                        "proxy": "",
                    },
                    "火山引擎_TTS(API)": {
                        "id": "volcengine_tts",
                        "type": "volcengine_tts",
                        "provider": "volcengine",
                        "provider_type": "text_to_speech",
                        "enable": False,
                        "api_key": "",
                        "appid": "",
                        "volcengine_cluster": "volcano_tts",
                        "volcengine_voice_type": "",
                        "volcengine_speed_ratio": 1.0,
                        "api_base": "https://openspeech.bytedance.com/api/v1/tts",
                        "timeout": 20,
                        "proxy": "",
                    },
                    "Gemini TTS": {
                        "id": "gemini_tts",
                        "type": "gemini_tts",
                        "provider": "google",
                        "provider_type": "text_to_speech",
                        "enable": False,
                        "gemini_tts_api_key": "",
                        "gemini_tts_api_base": "",
                        "gemini_tts_timeout": 20,
                        "gemini_tts_model": "gemini-2.5-flash-preview-tts",
                        "gemini_tts_prefix": "",
                        "gemini_tts_voice_name": "Leda",
                        "proxy": "",
                    },
                    "ElevenLabs TTS(API)": {
                        "hint": "Obtenha a chave de API em https://elevenlabs.io/app/settings/api-keys e selecione o ID da voz em https://elevenlabs.io/app/voice-library.",
                        "id": "elevenlabs_tts",
                        "type": "elevenlabs_tts_api",
                        "provider": "elevenlabs",
                        "provider_type": "text_to_speech",
                        "enable": False,
                        "api_key": "",
                        "api_base": "https://api.elevenlabs.io/v1",
                        "model": "eleven_multilingual_v2",
                        "elevenlabs-tts-voice-id": "JBFqnCBsd6RMkjVDRZzb",
                        "elevenlabs-tts-output-format": "mp3_44100_128",
                        "elevenlabs-tts-stability": "",
                        "elevenlabs-tts-similarity-boost": "",
                        "elevenlabs-tts-style": "",
                        "elevenlabs-tts-use-speaker-boost": True,
                        "timeout": "20",
                        "proxy": "",
                    },
                    "OpenAI Embedding": {
                        "id": "openai_embedding",
                        "type": "openai_embedding",
                        "provider": "openai",
                        "provider_type": "embedding",
                        "hint": "provider_group.provider.openai_embedding.hint",
                        "enable": True,
                        "embedding_api_key": "",
                        "embedding_api_base": "",
                        "embedding_model": "",
                        "embedding_dimensions": 1024,
                        "embedding_dimensions_mode": "auto",
                        "timeout": 20,
                        "proxy": "",
                    },
                    "Gemini Embedding": {
                        "id": "gemini_embedding",
                        "type": "gemini_embedding",
                        "provider": "google",
                        "provider_type": "embedding",
                        "hint": "provider_group.provider.gemini_embedding.hint",
                        "enable": True,
                        "embedding_api_key": "",
                        "embedding_api_base": "",
                        "embedding_model": "gemini-embedding-001",
                        "embedding_dimensions": 768,
                        "timeout": 20,
                        "proxy": "",
                    },
                    "NVIDIA Embedding": {
                        "id": "nvidia_embedding",
                        "type": "nvidia_embedding",
                        "provider": "nvidia",
                        "provider_type": "embedding",
                        "hint": "provider_group.provider.nvidia_embedding.hint",
                        "enable": True,
                        "embedding_api_key": "",
                        "embedding_api_base": "https://integrate.api.nvidia.com/v1",
                        "embedding_model": "nvidia/nemotron-3-embed-1b",
                        "input_type": "passage",
                        "embedding_dimensions": 2048,
                        "timeout": 20,
                        "proxy": "",
                    },
                    "Ollama Embedding": {
                        "id": "ollama_embedding",
                        "type": "ollama_embedding",
                        "provider": "ollama",
                        "provider_type": "embedding",
                        "hint": "provider_group.provider.ollama_embedding.hint",
                        "enable": True,
                        "embedding_api_base": "http://localhost:11434",
                        "embedding_model": "nomic-embed-text",
                        "embedding_dimensions": 768,
                        "timeout": 60,
                        "proxy": "",
                    },
                    "DashScope Embedding": {
                        "id": "dashscope_embedding",
                        "type": "dashscope_embedding",
                        "provider": "dashscope",
                        "provider_type": "embedding",
                        "hint": "provider_group.provider.dashscope_embedding.hint",
                        "enable": True,
                        "embedding_api_key": "",
                        "embedding_api_base": "https://dashscope.aliyuncs.com/api/v1",
                        "embedding_model": "text-embedding-v4",
                        "embedding_dimensions": 1024,
                        "timeout": 60,
                        "proxy": "",
                    },
                    "vLLM Rerank": {
                        "id": "vllm_rerank",
                        "type": "vllm_rerank",
                        "provider": "vllm",
                        "provider_type": "rerank",
                        "enable": True,
                        "rerank_api_key": "",
                        "rerank_api_base": "http://127.0.0.1:8000",
                        "rerank_api_suffix": "/v1/rerank",
                        "rerank_model": "BAAI/bge-reranker-base",
                        "timeout": 20,
                    },
                    "Xinference Rerank": {
                        "id": "xinference_rerank",
                        "type": "xinference_rerank",
                        "provider": "xinference",
                        "provider_type": "rerank",
                        "enable": True,
                        "rerank_api_key": "",
                        "rerank_api_base": "http://127.0.0.1:9997",
                        "rerank_model": "BAAI/bge-reranker-base",
                        "timeout": 20,
                        "launch_model_if_not_running": False,
                    },
                    "阿里云百炼重排序": {
                        "id": "bailian_rerank",
                        "type": "bailian_rerank",
                        "provider": "bailian",
                        "provider_type": "rerank",
                        "enable": True,
                        "rerank_api_key": "",
                        "rerank_api_base": "https://dashscope.aliyuncs.com/api/v1/services/rerank/text-rerank/text-rerank",
                        "rerank_model": "qwen3-rerank",
                        "timeout": 30,
                        "return_documents": False,
                        "instruct": "",
                    },
                    "NVIDIA Rerank": {
                        "id": "nvidia_rerank",
                        "type": "nvidia_rerank",
                        "provider": "nvidia",
                        "provider_type": "rerank",
                        "enable": True,
                        "nvidia_rerank_api_key": "",
                        "nvidia_rerank_api_base": "https://ai.api.nvidia.com/v1/retrieval",
                        "nvidia_rerank_model": "nvidia/llama-nemotron-rerank-vl-1b-v2",
                        "nvidia_rerank_model_endpoint": "/reranking",
                        "timeout": 20,
                        "nvidia_rerank_truncate": "",
                    },
                    "TEI Rerank": {
                        "id": "tei_rerank",
                        "type": "tei_rerank",
                        "provider": "huggingface",
                        "provider_type": "rerank",
                        "enable": True,
                        "rerank_api_key": "",
                        "rerank_api_base": "http://127.0.0.1:8080",
                        "timeout": 20,
                        "tei_rerank_truncate": False,
                        "tei_rerank_truncation_direction": "Right",
                        "tei_rerank_raw_scores": False,
                        "tei_rerank_return_text": False,
                    },
                    "Xinference STT": {
                        "id": "xinference_stt",
                        "type": "xinference_stt",
                        "provider": "xinference",
                        "provider_type": "speech_to_text",
                        "enable": False,
                        "api_key": "",
                        "api_base": "http://127.0.0.1:9997",
                        "model": "whisper-large-v3",
                        "timeout": 180,
                        "launch_model_if_not_running": False,
                    },
                },
                "items": {
                    "genie_onnx_model_dir": {
                        "description": "Diretório do modelo ONNX",
                        "type": "string",
                        "hint": "Caminho do diretório que contém os arquivos do modelo ONNX",
                    },
                    "genie_language": {
                        "description": "Idioma",
                        "type": "string",
                        "options": ["Japanese", "English", "Chinese"],
                    },
                    "provider_source_id": {
                        "invisible": True,
                        "type": "string",
                    },
                    "api_key": {
                        "description": "Chave de API",
                        "type": "string",
                        "secret": True,
                    },
                    "dashscope_api_key": {
                        "description": "Chave de API do DashScope",
                        "type": "string",
                        "secret": True,
                    },
                    "gemini_tts_api_key": {
                        "description": "Chave de API do Gemini",
                        "type": "string",
                        "secret": True,
                    },
                    "xai_native_search": {
                        "description": "Ativar busca nativa",
                        "type": "bool",
                        "hint": "Quando ativado, usa a busca nativa Live Search do xAI Chat Completions para consultas na web, cobrada conforme o uso. Válido apenas para provedores xAI.",
                        "condition": {
                            "provider": "xai",
                            "type": "xai_chat_completion",
                        },
                    },
                    "rerank_api_base": {
                        "description": "URL base da API do modelo de rerank",
                        "type": "string",
                        "hint": "A URL completa da requisição combina a URL base com um sufixo de caminho (padrão: /v1/rerank).",
                    },
                    "rerank_api_suffix": {
                        "description": "Sufixo do caminho da URL da API",
                        "type": "string",
                        "hint": "Caminho acrescentado a base_url, por exemplo, /v1/rerank. Deixe vazio para desativar a inclusão automática.",
                    },
                    "rerank_api_key": {
                        "description": "Chave de API",
                        "type": "string",
                        "hint": "Deixe vazio se nenhuma chave de API for necessária.",
                        "secret": True,
                    },
                    "rerank_model": {
                        "description": "Nome do modelo de rerank",
                        "type": "string",
                    },
                    "return_documents": {
                        "description": "Retornar documentos de origem nos resultados de reclassificação",
                        "type": "bool",
                        "hint": "Desativado por padrão para reduzir o tráfego de rede.",
                    },
                    "instruct": {
                        "description": "Descrição personalizada da tarefa de reclassificação",
                        "type": "string",
                        "hint": "Válido apenas para modelos qwen3-rerank. Recomenda-se escrever em inglês.",
                    },
                    "launch_model_if_not_running": {
                        "description": "Iniciar automaticamente o modelo se estiver parado",
                        "type": "bool",
                        "hint": "Se o modelo não estiver em execução no Xinference, tenta iniciá-lo automaticamente. Recomenda-se desativar em produção.",
                    },
                    "nvidia_rerank_api_base": {
                        "description": "URL base da API",
                        "type": "string",
                    },
                    "nvidia_rerank_api_key": {
                        "description": "Chave de API",
                        "type": "string",
                        "secret": True,
                    },
                    "nvidia_rerank_model": {
                        "description": "Nome do modelo de reclassificação",
                        "type": "string",
                        "hint": "Consulte a documentação da NVIDIA para obter o nome do modelo.",
                    },
                    "nvidia_rerank_model_endpoint": {
                        "description": "Endpoint personalizado do modelo",
                        "type": "string",
                        "hint": "Sufixo personalizado do endpoint. Padrão: /reranking.",
                    },
                    "nvidia_rerank_truncate": {
                        "description": "Estratégia de truncamento de texto",
                        "type": "string",
                        "hint": "Define se a entrada será truncada para caber no contexto máximo do modelo quando o texto for muito longo.",
                        "options": [
                            "",
                            "NONE",
                            "END",
                        ],
                    },
                    "tei_rerank_truncate": {
                        "description": "Truncar textos longos",
                        "type": "bool",
                        "hint": "Trunca automaticamente a entrada quando ela ultrapassa o contexto máximo do modelo. Quando ativado, exige definir a direção do truncamento.",
                    },
                    "tei_rerank_truncation_direction": {
                        "description": "Direção do truncamento",
                        "type": "string",
                        "options": ["left", "right"],
                        "hint": "Escolha truncar a partir da esquerda ou da direita do texto. Só funciona quando o truncamento de textos longos está ativado.",
                    },
                    "tei_rerank_raw_scores": {
                        "description": "Retornar pontuações brutas",
                        "type": "bool",
                        "hint": "Quando ativado, retorna os logits brutos do modelo, que podem ser negativos, sem normalização sigmoide. Desativado por padrão.",
                    },
                    "tei_rerank_return_text": {
                        "description": "Retornar o texto dos documentos nos resultados",
                        "type": "bool",
                        "hint": "Quando ativado, cada resultado inclui o texto original do documento. Desativado por padrão para reduzir o tráfego de rede.",
                    },
                    "modalities": {
                        "description": "Recursos do modelo",
                        "type": "list",
                        "items": {"type": "string"},
                        "options": ["text", "image", "audio", "tool_use"],
                        "labels": ["Texto", "Imagem", "Áudio", "Uso de ferramentas"],
                        "render_type": "checkbox",
                        "hint": "Modalidades suportadas pelo modelo.",
                    },
                    "custom_headers": {
                        "description": "Headers personalizados",
                        "type": "dict",
                        "items": {},
                        "hint": "Os pares de chave e valor adicionados aqui são mesclados em default_headers do SDK OpenAI para personalizar os cabeçalhos HTTP. Os valores devem ser textos.",
                    },
                    "ollama_disable_thinking": {
                        "description": "Desativar modo de raciocínio",
                        "type": "bool",
                        "hint": "Desativa o modo de raciocínio do Ollama.",
                    },
                    "custom_extra_body": {
                        "description": "Parâmetros personalizados do corpo da requisição",
                        "type": "dict",
                        "items": {},
                        "hint": "Adicione parâmetros extras às requisições, como temperature, top_p e max_tokens.",
                        "template_schema": {
                            "temperature": {
                                "name": "Temperatura",
                                "description": "Temperatura",
                                "hint": "Controla a aleatoriedade, geralmente de 0 a 2. Quanto maior, mais aleatório.",
                                "type": "float",
                                "default": 0.6,
                                "slider": {"min": 0, "max": 2, "step": 0.1},
                            },
                            "top_p": {
                                "name": "Top-p",
                                "description": "Amostragem top-p",
                                "hint": "Parâmetro de amostragem por núcleo, geralmente de 0 a 1. Controla a massa de probabilidade considerada.",
                                "type": "float",
                                "default": 1.0,
                                "slider": {"min": 0, "max": 1, "step": 0.01},
                            },
                            "max_tokens": {
                                "name": "Máximo de tokens",
                                "description": "Máximo de tokens",
                                "hint": "Número máximo de tokens gerados.",
                                "type": "int",
                                "default": 8192,
                            },
                            "reasoning_effort": {
                                "name": "Esforço de raciocínio",
                                "description": "Esforço de raciocínio",
                                "hint": "Controla o esforço dos modelos de raciocínio. Os valores aceitos dependem do modelo.",
                                "type": "string",
                                "default": "high",
                            },
                        },
                    },
                    "provider": {
                        "type": "string",
                        "invisible": True,
                    },
                    "gpt_weights_path": {
                        "description": "Caminho do arquivo do modelo GPT",
                        "type": "string",
                        "hint": "Arquivo .ckpt. Use um caminho absoluto sem aspas. Deixe vazio para usar o modelo SoVITS interno do GPT_SoVITS (recomenda-se alterar os padrões no GPT_SoVITS).",
                    },
                    "sovits_weights_path": {
                        "description": "Caminho do arquivo do modelo SoVITS",
                        "type": "string",
                        "hint": "Arquivo .pth. Use um caminho absoluto sem aspas. Deixe vazio para usar o modelo SoVITS interno do GPT_SoVITS (recomenda-se alterar os padrões no GPT_SoVITS).",
                    },
                    "gsv_default_parms": {
                        "description": "Parâmetros padrão do GPT_SoVITS",
                        "hint": "O caminho do áudio de referência e seu texto são obrigatórios; os outros parâmetros são opcionais.",
                        "type": "object",
                        "items": {
                            "gsv_ref_audio_path": {
                                "description": "Caminho do áudio de referência",
                                "type": "string",
                                "hint": "Obrigatório! Use um caminho absoluto sem aspas.",
                            },
                            "gsv_prompt_text": {
                                "description": "Texto do áudio de referência",
                                "type": "string",
                                "hint": "Obrigatório! Informe a transcrição do áudio de referência.",
                            },
                            "gsv_prompt_lang": {
                                "description": "Idioma do texto do áudio de referência",
                                "type": "string",
                                "hint": "Idioma do texto do áudio de referência. O padrão é chinês.",
                            },
                            "gsv_aux_ref_audio_paths": {
                                "description": "Caminhos dos áudios de referência auxiliares",
                                "type": "string",
                                "hint": "Arquivos de áudio de referência auxiliares; opcionais.",
                            },
                            "gsv_text_lang": {
                                "description": "Idioma do texto",
                                "type": "string",
                                "hint": "O padrão é chinês.",
                            },
                            "gsv_top_k": {
                                "description": "Diversidade da fala",
                                "type": "int",
                                "hint": "",
                            },
                            "gsv_top_p": {
                                "description": "Limiar de amostragem por núcleo",
                                "type": "float",
                                "hint": "",
                            },
                            "gsv_temperature": {
                                "description": "Aleatoriedade da fala",
                                "type": "float",
                                "hint": "",
                            },
                            "gsv_text_split_method": {
                                "description": "Método de divisão do texto",
                                "type": "string",
                                "hint": "Opções: `cut0` sem divisão; `cut1` a cada 4 frases; `cut2` a cada 50 caracteres; `cut3` por ponto final chinês; `cut4` por ponto final ocidental; `cut5` pela pontuação.",
                                "options": [
                                    "cut0",
                                    "cut1",
                                    "cut2",
                                    "cut3",
                                    "cut4",
                                    "cut5",
                                ],
                            },
                            "gsv_batch_size": {
                                "description": "Tamanho do lote",
                                "type": "int",
                                "hint": "",
                            },
                            "gsv_batch_threshold": {
                                "description": "Limiar do lote",
                                "type": "float",
                                "hint": "",
                            },
                            "gsv_split_bucket": {
                                "description": "Dividir texto em grupos para processamento paralelo",
                                "type": "bool",
                                "hint": "",
                            },
                            "gsv_speed_factor": {
                                "description": "Velocidade de reprodução da fala",
                                "type": "float",
                                "hint": "1 é a velocidade original.",
                            },
                            "gsv_fragment_interval": {
                                "description": "Intervalo entre segmentos de fala",
                                "type": "float",
                                "hint": "",
                            },
                            "gsv_streaming_mode": {
                                "description": "Ativar modo de streaming",
                                "type": "bool",
                                "hint": "",
                            },
                            "gsv_seed": {
                                "description": "Semente aleatória",
                                "type": "int",
                                "hint": "Para resultados reproduzíveis.",
                            },
                            "gsv_parallel_infer": {
                                "description": "Executar inferência em paralelo",
                                "type": "bool",
                                "hint": "",
                            },
                            "gsv_repetition_penalty": {
                                "description": "Penalidade por repetição",
                                "type": "float",
                                "hint": "",
                            },
                            "gsv_media_type": {
                                "description": "Tipo de mídia de saída",
                                "type": "string",
                                "hint": "Recomendado: wav",
                            },
                        },
                    },
                    "embedding_dimensions": {
                        "description": "Dimensões do embedding",
                        "type": "int",
                        "hint": "Dimensões dos vetores de embeddings. Talvez seja necessário ajustar para cada modelo; consulte sua documentação. O valor precisa estar correto para o banco de dados vetorial funcionar.",
                        "_special": "get_embedding_dim",
                    },
                    "embedding_dimensions_mode": {
                        "description": "Modo das dimensões dos embeddings",
                        "type": "string",
                        "options": ["auto", "always", "never"],
                        "hint": "Controla o envio do parâmetro dimensions nas requisições de embeddings compatíveis com OpenAI. auto envia apenas para modelos oficiais OpenAI embedding-3; use always quando a API compatível aceitar o parâmetro, ou never quando ela o rejeitar.",
                    },
                    "embedding_model": {
                        "description": "Modelo de embedding",
                        "type": "string",
                        "hint": "Nome do modelo de embeddings.",
                    },
                    "embedding_api_key": {
                        "description": "Chave de API",
                        "type": "string",
                        "secret": True,
                    },
                    "embedding_api_base": {
                        "description": "URL base da API",
                        "type": "string",
                    },
                    "volcengine_cluster": {
                        "type": "string",
                        "description": "Cluster do Volcengine",
                        "hint": "Para modelos de clonagem de voz, escolha volcano_icl ou volcano_icl_concurr; o padrão é volcano_tts.",
                    },
                    "volcengine_voice_type": {
                        "type": "string",
                        "description": "Voz do Volcengine",
                        "hint": "Informe o ID da voz (Voice_type).",
                    },
                    "volcengine_speed_ratio": {
                        "type": "float",
                        "description": "Velocidade da fala",
                        "hint": "Velocidade da fala, de 0.2 a 3.0. Padrão: 1.0.",
                    },
                    "volcengine_volume_ratio": {
                        "type": "float",
                        "description": "Volume",
                        "hint": "Volume, de 0.0 a 2.0. Padrão: 1.0.",
                    },
                    "azure_tts_voice": {
                        "type": "string",
                        "description": "Estilo da voz",
                        "hint": "Nome da voz na API",
                    },
                    "azure_tts_style": {
                        "type": "string",
                        "description": "Estilo",
                        "hint": "Estilo de fala específico da voz. Pode expressar emoções como alegria, empatia e calma.",
                    },
                    "azure_tts_role": {
                        "type": "string",
                        "description": "Papel (opcional)",
                        "hint": "Interpretação de um papel na fala. A voz pode simular diferentes idades e gêneros sem mudar seu nome. Por exemplo, uma voz masculina pode elevar o tom para simular uma voz feminina. Se o papel estiver ausente ou não for compatível, este atributo será ignorado.",
                        "options": [
                            "Boy",
                            "Girl",
                            "YoungAdultFemale",
                            "YoungAdultMale",
                            "OlderAdultFemale",
                            "OlderAdultMale",
                            "SeniorFemale",
                            "SeniorMale",
                            "Desativado",
                        ],
                    },
                    "azure_tts_rate": {
                        "type": "string",
                        "description": "Velocidade da fala",
                        "hint": "Controla a velocidade da fala por palavra ou frase. Deve ficar entre 0.5 e 2 vezes a velocidade do áudio original.",
                    },
                    "azure_tts_volume": {
                        "type": "string",
                        "description": "Volume da fala",
                        "hint": "Controla o volume por frase. Use de 0.0 a 100.0 (do mais baixo ao mais alto, por exemplo, 75). Padrão: 100.0.",
                    },
                    "azure_tts_region": {
                        "type": "string",
                        "description": "Região da API",
                        "hint": "Região onde o Azure TTS processa os dados. Consulte https://learn.microsoft.com/zh-cn/azure/ai-services/speech-service/regions",
                        "options": [
                            "southafricanorth",
                            "eastasia",
                            "southeastasia",
                            "australiaeast",
                            "centralindia",
                            "japaneast",
                            "japanwest",
                            "koreacentral",
                            "canadacentral",
                            "northeurope",
                            "westeurope",
                            "francecentral",
                            "germanywestcentral",
                            "norwayeast",
                            "swedencentral",
                            "switzerlandnorth",
                            "switzerlandwest",
                            "uksouth",
                            "uaenorth",
                            "brazilsouth",
                            "qatarcentral",
                            "centralus",
                            "eastus",
                            "eastus2",
                            "northcentralus",
                            "southcentralus",
                            "westcentralus",
                            "westus",
                            "westus2",
                            "westus3",
                        ],
                    },
                    "azure_tts_subscription_key": {
                        "type": "string",
                        "description": "Chave de assinatura do serviço",
                        "hint": "Chave de assinatura do Azure TTS, não um token.",
                        "secret": True,
                    },
                    "dashscope_tts_voice": {"description": "Voz", "type": "string"},
                    "gm_resp_image_modal": {
                        "description": "Ativar modalidade de imagem",
                        "type": "bool",
                        "hint": "Quando ativado, as respostas podem incluir imagens. O modelo precisa oferecer suporte ou ocorrerá um erro. Consulte os modelos compatíveis no site do Google Gemini. Dica: para gerar imagens, desative o reconhecimento de membros para obter melhores resultados.",
                    },
                    "gm_native_search": {
                        "description": "Ativar busca nativa",
                        "type": "bool",
                        "hint": "Quando ativado, desativa todas as ferramentas de função. Consulte a documentação oficial para os limites da cota gratuita.",
                    },
                    "gm_native_coderunner": {
                        "description": "Ativar execução nativa de código",
                        "type": "bool",
                        "hint": "Quando ativado, desativa todas as ferramentas de função.",
                    },
                    "gm_url_context": {
                        "description": "Ativar contexto de URLs",
                        "type": "bool",
                        "hint": "Quando ativado, desativa todas as ferramentas de função.",
                    },
                    "gm_safety_settings": {
                        "description": "Filtros de segurança",
                        "type": "object",
                        "hint": "Define o nível de filtragem de segurança da entrada do modelo. Níveis: NONE (sem bloqueio), HIGH (bloquear alto risco), MEDIUM_AND_ABOVE (bloquear risco médio ou superior), LOW_AND_ABOVE (bloquear risco baixo ou superior). Consulte a documentação da API Gemini.",
                        "items": {
                            "harassment": {
                                "description": "Assédio",
                                "type": "string",
                                "hint": "Comentários negativos ou prejudiciais",
                                "options": [
                                    "BLOCK_NONE",
                                    "BLOCK_ONLY_HIGH",
                                    "BLOCK_MEDIUM_AND_ABOVE",
                                    "BLOCK_LOW_AND_ABOVE",
                                ],
                            },
                            "hate_speech": {
                                "description": "Discurso de ódio",
                                "type": "string",
                                "hint": "Conteúdo grosseiro, desrespeitoso ou profano",
                                "options": [
                                    "BLOCK_NONE",
                                    "BLOCK_ONLY_HIGH",
                                    "BLOCK_MEDIUM_AND_ABOVE",
                                    "BLOCK_LOW_AND_ABOVE",
                                ],
                            },
                            "sexually_explicit": {
                                "description": "Conteúdo sexualmente explícito",
                                "type": "string",
                                "hint": "Referências a atos sexuais ou outros conteúdos obscenos",
                                "options": [
                                    "BLOCK_NONE",
                                    "BLOCK_ONLY_HIGH",
                                    "BLOCK_MEDIUM_AND_ABOVE",
                                    "BLOCK_LOW_AND_ABOVE",
                                ],
                            },
                            "dangerous_content": {
                                "description": "Conteúdo perigoso",
                                "type": "string",
                                "hint": "Conteúdo que promove, incentiva ou auxilia comportamentos prejudiciais",
                                "options": [
                                    "BLOCK_NONE",
                                    "BLOCK_ONLY_HIGH",
                                    "BLOCK_MEDIUM_AND_ABOVE",
                                    "BLOCK_LOW_AND_ABOVE",
                                ],
                            },
                        },
                    },
                    "gm_thinking_config": {
                        "description": "Configurações de raciocínio",
                        "type": "object",
                        "items": {
                            "budget": {
                                "description": "Orçamento de raciocínio",
                                "type": "int",
                                "hint": "Orienta o modelo sobre o número de tokens de raciocínio a usar. Consulte https://ai.google.dev/gemini-api/docs/thinking#set-budget",
                            },
                            "level": {
                                "description": "Nível de raciocínio",
                                "type": "string",
                                "hint": "Recomendado para modelos Gemini 3 e posteriores; permite controlar o comportamento de raciocínio. Consulte https://ai.google.dev/gemini-api/docs/thinking#thinking-levels",
                                "options": [
                                    "MINIMAL",
                                    "LOW",
                                    "MEDIUM",
                                    "HIGH",
                                ],
                            },
                        },
                    },
                    "anth_thinking_config": {
                        "description": "Configurações de raciocínio",
                        "type": "object",
                        "items": {
                            "type": {
                                "description": "Tipo de raciocínio",
                                "type": "string",
                                "options": ["", "adaptive"],
                                "hint": "Use 'adaptive' para Opus 4.6+ / Sonnet 4.6+ (recomendado). Deixe vazio para usar orçamento manual. Consulte https://platform.claude.com/docs/en/build-with-claude/adaptive-thinking",
                            },
                            "budget": {
                                "description": "Orçamento de raciocínio",
                                "type": "int",
                                "hint": "Parâmetro thinking.budget_tokens da Anthropic. Deve ser maior ou igual a 1024. Usado apenas quando type está vazio. Obsoleto no Opus 4.6 / Sonnet 4.6. Consulte https://platform.claude.com/docs/en/build-with-claude/extended-thinking",
                            },
                            "effort": {
                                "description": "Nível de esforço",
                                "type": "string",
                                "options": ["", "low", "medium", "high", "max"],
                                "hint": "Controla a profundidade do raciocínio quando type é 'adaptive'. 'high' é o padrão. 'max' só funciona no Opus 4.6. Consulte https://platform.claude.com/docs/en/build-with-claude/effort",
                            },
                        },
                    },
                    "minimax-group-id": {
                        "type": "string",
                        "description": "Grupo de usuários",
                        "hint": "Disponível em Gerenciamento da conta -> Informações básicas.",
                    },
                    "minimax-langboost": {
                        "type": "string",
                        "description": "Idioma ou dialeto de destino",
                        "hint": "Melhora o reconhecimento dos idiomas ou dialetos especificados e o desempenho da fala nesses cenários.",
                        "options": [
                            "Chinese",
                            "Chinese,Yue",
                            "English",
                            "Arabic",
                            "Russian",
                            "Spanish",
                            "French",
                            "Portuguese",
                            "German",
                            "Turkish",
                            "Dutch",
                            "Ukrainian",
                            "Vietnamese",
                            "Indonesian",
                            "Japanese",
                            "Italian",
                            "Korean",
                            "Thai",
                            "Polish",
                            "Romanian",
                            "Greek",
                            "Czech",
                            "Finnish",
                            "Hindi",
                            "auto",
                        ],
                    },
                    "minimax-voice-speed": {
                        "type": "float",
                        "description": "Velocidade da fala",
                        "hint": "Velocidade da fala sintetizada, de 0.5 a 2. Padrão: 1.0. Valores maiores aumentam a velocidade.",
                    },
                    "minimax-voice-vol": {
                        "type": "float",
                        "description": "Volume",
                        "hint": "Volume da síntese, maior que 0 e até 10. Padrão: 1.0. Valores maiores aumentam o volume.",
                    },
                    "minimax-voice-pitch": {
                        "type": "int",
                        "description": "Tom",
                        "hint": "Tom da síntese, de -12 a 12. Padrão: 0.",
                    },
                    "minimax-is-timber-weight": {
                        "type": "bool",
                        "description": "Ativar mistura de vozes",
                        "hint": "Permite misturar até quatro vozes com pesos personalizados. Quando ativado, as configurações de voz única são ignoradas.",
                    },
                    "minimax-timber-weight": {
                        "type": "string",
                        "description": "Vozes misturadas",
                        "editor_mode": True,
                        "hint": "Vozes misturadas e seus pesos. Até quatro vozes, com pesos inteiros de 1 a 100. Obtenha predefinições e modelos no console oficial de testes da API TTS. Deve ser uma string JSON; confirme a interpretação no console. Consulte os padrões e a prévia oficial de código para a estrutura.",
                    },
                    "minimax-voice-id": {
                        "type": "string",
                        "description": "Voz única",
                        "hint": "ID da voz única; consulte a documentação oficial.",
                    },
                    "minimax-voice-emotion": {
                        "type": "string",
                        "description": "Emoção",
                        "hint": "Controla a emoção da fala sintetizada. Em auto, seleciona a emoção conforme o texto.",
                        "options": [
                            "auto",
                            "happy",
                            "sad",
                            "angry",
                            "fearful",
                            "disgusted",
                            "surprised",
                            "calm",
                            "fluent",
                            "whisper",
                        ],
                    },
                    "minimax-voice-latex": {
                        "type": "bool",
                        "description": "Ler fórmulas LaTeX",
                        "hint": "Lê fórmulas LaTeX. O texto de entrada deve seguir o formato exigido pela documentação oficial.",
                    },
                    "minimax-voice-english-normalization": {
                        "type": "bool",
                        "description": "Normalização de texto em inglês",
                        "hint": "Melhora a leitura de números, mas aumenta um pouco a latência.",
                    },
                    "rag_options": {
                        "description": "Opções de RAG",
                        "type": "object",
                        "hint": "Configurações opcionais de busca na base de conhecimento. Disponíveis apenas para aplicativos de agentes, incluindo RAG. Nos aplicativos Bailian, ativar esta opção desativa conversas de vários turnos.",
                        "items": {
                            "pipeline_ids": {
                                "description": "Lista de IDs de bases de conhecimento",
                                "type": "list",
                                "items": {"type": "string"},
                                "hint": "Busca todos os documentos nas bases de conhecimento especificadas. Acesse https://bailian.console.aliyun.com/ e vá a Aplicativos de dados -> Índice de conhecimento para criar e obter os IDs.",
                            },
                            "file_ids": {
                                "description": "IDs de documentos não estruturados",
                                "type": "list",
                                "items": {"type": "string"},
                                "hint": "Busca os documentos não estruturados especificados. Acesse https://bailian.console.aliyun.com/ e vá a Gerenciamento de dados para criar e obter os IDs.",
                            },
                            "output_reference": {
                                "description": "Exibir referências de bases de conhecimento e documentos",
                                "type": "bool",
                                "hint": "Acrescenta as fontes de referência ao final de cada resposta. Desativado por padrão.",
                            },
                        },
                    },
                    "sensevoice_hint": {
                        "description": "Implantar SenseVoice",
                        "type": "string",
                        "hint": "Antes de ativar, instale funasr, funasr_onnx, torchaudio, torch, modelscope e jieba (CPU por padrão; download de cerca de 1 GB), além do ffmpeg. Sem isso, o reconhecimento de fala não funcionará.",
                    },
                    "is_emotion": {
                        "description": "Reconhecimento de emoções",
                        "type": "bool",
                        "hint": "Ativa o reconhecimento de emoções: alegria, tristeza, raiva, neutralidade, medo, repulsa, surpresa ou desconhecida.",
                    },
                    "stt_model": {
                        "description": "Nome do modelo",
                        "type": "string",
                        "hint": "Nome do modelo no ModelScope. Padrão: iic/SenseVoiceSmall.",
                    },
                    "variables": {
                        "description": "Variáveis fixas do workflow",
                        "type": "object",
                        "items": {},
                        "hint": "Opcional. Variáveis fixas de entrada do fluxo de trabalho. Você também pode definir variáveis dinamicamente com /set durante a conversa. Em caso de conflito, as configurações dinâmicas têm prioridade.",
                        "invisible": True,
                    },
                    "dashscope_app_type": {
                        "description": "Tipo de aplicativo",
                        "type": "string",
                        "hint": "Tipo de aplicativo do Bailian.",
                        "options": [
                            "agent",
                            "agent-arrange",
                            "dialog-workflow",
                            "task-workflow",
                        ],
                    },
                    "timeout": {
                        "description": "Tempo limite",
                        "type": "int",
                        "hint": "Tempo limite em segundos.",
                    },
                    "openai-tts-voice": {
                        "description": "Voz",
                        "type": "string",
                        "hint": "Voz do OpenAI TTS. Padrões da OpenAI: 'alloy', 'echo', 'fable', 'onyx', 'nova', 'shimmer'.",
                    },
                    "mimo-tts-voice": {
                        "description": "Voz",
                        "type": "string",
                        "hint": "Nome da voz do MiMo TTS. Valores aceitos incluem 'mimo_default', 'default_en' e 'default_zh'.",
                    },
                    "mimo-tts-format": {
                        "description": "Formato de saída",
                        "type": "string",
                        "hint": "Formato de áudio gerado pelo MiMo TTS. Valores aceitos: 'wav', 'mp3' e 'pcm'.",
                    },
                    "mimo-tts-style-prompt": {
                        "description": "Prompt de estilo",
                        "type": "string",
                        "hint": "Adicionado antes do texto a sintetizar em uma tag <style>...</style> para controlar velocidade, emoção, personagem ou estilo, como alegre, mais rápido, Sun Wukong ou sussurrando. Opcional.",
                    },
                    "mimo-tts-dialect": {
                        "description": "Dialeto",
                        "type": "string",
                        "hint": "Combinado com o prompt de estilo na tag inicial <style>...</style>, por exemplo, mandarim do nordeste, dialeto de Sichuan, dialeto de Henan ou cantonês. Opcional.",
                    },
                    "mimo-tts-seed-text": {
                        "description": "Texto inicial de referência",
                        "type": "string",
                        "hint": "Enviado como uma mensagem opcional do usuário para orientar o tom e o estilo de fala. Não é acrescentado ao texto a sintetizar.",
                    },
                    "fishaudio-tts-character": {
                        "description": "Personagem",
                        "type": "string",
                        "hint": "Personagem do Fish Audio TTS. O padrão é Klee. Mais opções: https://fish.audio/zh-CN/discovery",
                    },
                    "fishaudio-tts-reference-id": {
                        "description": "ID de referência",
                        "type": "string",
                        "hint": "ID opcional do modelo de referência do Fish Audio TTS. Se definido, o ID é usado diretamente em vez de buscar pelo nome do personagem. Exemplo: 626bb6d3f3364c9cbc3aa6a67300a664. Mais modelos: https://fish.audio/zh-CN/discovery; abra a página de um modelo para copiar seu ID.",
                    },
                    "whisper_hint": {
                        "description": "Notas sobre a implantação local do Whisper",
                        "type": "string",
                        "hint": "Antes de ativar, instale a biblioteca openai-whisper (usuários NVIDIA baixam cerca de 2 GB, principalmente torch e CUDA; usuários de CPU, cerca de 1 GB), além do ffmpeg. Sem isso, o reconhecimento de fala não funcionará.",
                    },
                    "whisper_device": {
                        "description": "Dispositivo de inferência",
                        "type": "string",
                        "hint": "Dispositivo de inferência do Whisper. Apple Silicon pode usar mps; outros ambientes devem usar cpu. Se mps estiver selecionado, mas indisponível, o AstrBot usará cpu.",
                        "options": ["cpu", "mps"],
                    },
                    "id": {
                        "description": "ID",
                        "type": "string",
                    },
                    "type": {
                        "description": "Categoria do provedor",
                        "type": "string",
                        "invisible": True,
                    },
                    "provider_type": {
                        "description": "Tipo de capacidade do provedor",
                        "type": "string",
                        "invisible": True,
                    },
                    "enable": {
                        "description": "Ativar",
                        "type": "bool",
                    },
                    "key": {
                        "description": "Chave de API",
                        "type": "list",
                        "items": {"type": "string"},
                        "secret": True,
                    },
                    "api_base": {
                        "description": "URL base da API",
                        "type": "string",
                    },
                    "proxy": {
                        "description": "Endereço de proxy",
                        "type": "string",
                        "hint": "Proxy HTTP/HTTPS aplicado apenas às solicitações deste provedor.",
                    },
                    "model": {
                        "description": "ID do modelo",
                        "type": "string",
                        "hint": "Nome do modelo, por exemplo gpt-4o-mini ou deepseek-chat.",
                    },
                    "max_context_tokens": {
                        "description": "Tamanho da janela de contexto",
                        "type": "int",
                        "hint": "Máximo de tokens de contexto. Use 0 para tentar detectar automaticamente pelos metadados do modelo.",
                    },
                    "dify_api_key": {
                        "description": "Chave de API",
                        "type": "string",
                        "hint": "Chave de API do Dify. Campo obrigatório.",
                        "secret": True,
                    },
                    "dify_api_base": {
                        "description": "URL base da API",
                        "type": "string",
                        "hint": "URL base da API do Dify. Padrão: https://api.dify.ai/v1",
                    },
                    "dify_api_type": {
                        "description": "Tipo de aplicação Dify",
                        "type": "string",
                        "hint": "Tipo de API do Dify. Conforme sua documentação, os tipos aceitos são chat, chatflow, agent e workflow.",
                        "options": ["chat", "chatflow", "agent", "workflow"],
                    },
                    "dify_workflow_output_key": {
                        "description": "Nome da variável de saída do fluxo do Dify",
                        "type": "string",
                        "hint": "Nome da variável de saída do fluxo do Dify. Usado apenas quando o tipo de aplicativo é workflow. Padrão: astrbot_wf_output.",
                    },
                    "dify_query_input_key": {
                        "description": "Nome da variável de entrada do prompt",
                        "type": "string",
                        "hint": "Nome da variável de entrada para o texto da mensagem. Padrão: astrbot_text_query.",
                        "obvious": True,
                    },
                    "coze_api_key": {
                        "description": "Chave de API do Coze",
                        "type": "string",
                        "hint": "Chave de API do Coze para acessar seus serviços.",
                        "secret": True,
                    },
                    "bot_id": {
                        "description": "ID do bot",
                        "type": "string",
                        "hint": "ID do bot do Coze, obtido após criar um bot na plataforma Coze.",
                    },
                    "coze_api_base": {
                        "description": "URL base da API",
                        "type": "string",
                        "hint": "URL base da API do Coze. Padrão: https://api.coze.cn",
                    },
                    "deerflow_api_base": {
                        "description": "URL base da API",
                        "type": "string",
                        "hint": "URL do gateway de API do DeerFlow. Padrão: http://127.0.0.1:2026",
                    },
                    "deerflow_api_key": {
                        "description": "Chave de API do DeerFlow",
                        "type": "string",
                        "hint": "Opcional. Preencha se o gateway do DeerFlow estiver protegido por autenticação Bearer.",
                        "secret": True,
                    },
                    "deerflow_auth_header": {
                        "description": "Header de autorização",
                        "type": "string",
                        "hint": "Opcional. Valor personalizado do cabeçalho Authorization; tem prioridade sobre a chave de API do DeerFlow.",
                        "secret": True,
                    },
                    "deerflow_assistant_id": {
                        "description": "ID do assistente",
                        "type": "string",
                        "hint": "assistant_id do LangGraph. Padrão: lead_agent.",
                    },
                    "deerflow_model_name": {
                        "description": "Substituir nome do modelo",
                        "type": "string",
                        "hint": "Opcional. Substitui o modelo padrão do DeerFlow (corresponde a model_name no contexto de execução).",
                    },
                    "deerflow_thinking_enabled": {
                        "description": "Ativar modo de raciocínio",
                        "type": "bool",
                    },
                    "deerflow_plan_mode": {
                        "description": "Ativar modo de planejamento",
                        "type": "bool",
                        "hint": "Corresponde a is_plan_mode do DeerFlow.",
                    },
                    "deerflow_subagent_enabled": {
                        "description": "Ativar subagente",
                        "type": "bool",
                        "hint": "Corresponde a subagent_enabled do DeerFlow.",
                    },
                    "deerflow_max_concurrent_subagents": {
                        "description": "Máximo de subagentes simultâneos",
                        "type": "int",
                        "hint": "Corresponde a max_concurrent_subagents do DeerFlow. Só funciona quando o subagente está ativado. Padrão: 3.",
                    },
                    "deerflow_recursion_limit": {
                        "description": "Limite de recursão",
                        "type": "int",
                        "hint": "Corresponde a recursion_limit do LangGraph.",
                    },
                    "auto_save_history": {
                        "description": "Histórico gerenciado pelo Coze",
                        "type": "bool",
                        "hint": "Quando ativado, o Coze gerencia o histórico de conversas. O contexto salvo localmente pelo AstrBot fica somente para leitura e suas operações não são aplicadas. Quando desativado, o AstrBot gerencia o contexto.",
                    },
                },
            },
            "provider_settings": {
                "type": "object",
                "items": {
                    "enable": {
                        "type": "bool",
                    },
                    "wake_prefix": {
                        "type": "string",
                    },
                    "web_search": {
                        "type": "bool",
                    },
                    "web_search_link": {
                        "type": "bool",
                    },
                    "display_reasoning_text": {
                        "type": "bool",
                    },
                    "identifier": {
                        "type": "bool",
                    },
                    "group_name_display": {
                        "type": "bool",
                    },
                    "datetime_system_prompt": {
                        "type": "bool",
                    },
                    "prompt_prefix": {
                        "type": "string",
                    },
                    "streaming_response": {
                        "type": "bool",
                    },
                    "show_tool_use_status": {
                        "type": "bool",
                    },
                    "show_tool_call_result": {
                        "type": "bool",
                    },
                    "buffer_intermediate_messages": {
                        "type": "bool",
                    },
                    "unsupported_streaming_strategy": {
                        "type": "string",
                    },
                    "file_extract": {
                        "type": "object",
                        "items": {
                            "enable": {
                                "type": "bool",
                            },
                            "provider": {
                                "type": "string",
                            },
                            "moonshotai_api_key": {
                                "type": "string",
                                "secret": True,
                            },
                        },
                    },
                    "proactive_capability": {
                        "type": "object",
                        "items": {
                            "add_cron_tools": {
                                "type": "bool",
                            },
                        },
                    },
                },
            },
            "agent_runner": {
                "type": "object",
                "items": {
                    "runner_type": {"type": "string"},
                    "config": {"type": "dict"},
                },
            },
            "provider_stt_settings": {
                "type": "object",
                "items": {
                    "enable": {
                        "type": "bool",
                    },
                    "provider_id": {
                        "type": "string",
                    },
                },
            },
            "provider_tts_settings": {
                "type": "object",
                "items": {
                    "enable": {
                        "type": "bool",
                    },
                    "provider_id": {
                        "type": "string",
                    },
                    "dual_output": {
                        "type": "bool",
                    },
                    "use_file_service": {
                        "type": "bool",
                    },
                    "trigger_probability": {
                        "type": "float",
                    },
                },
            },
            "provider_ltm_settings": {
                "type": "object",
                "items": {
                    "group_icl_enable": {
                        "type": "bool",
                    },
                    "group_message_max_cnt": {
                        "type": "int",
                    },
                    "image_caption": {
                        "type": "bool",
                    },
                    "image_caption_provider_id": {
                        "type": "string",
                    },
                    "image_caption_prompt": {
                        "type": "string",
                    },
                    "group_message_history_enable": {
                        "type": "bool",
                    },
                    "group_message_history_max_cnt": {
                        "type": "int",
                    },
                    "active_reply": {
                        "type": "object",
                        "items": {
                            "enable": {
                                "type": "bool",
                            },
                            "whitelist": {
                                "type": "list",
                                "items": {"type": "string"},
                            },
                            "method": {
                                "type": "string",
                                "options": ["possibility_reply"],
                            },
                            "possibility_reply": {
                                "type": "float",
                            },
                        },
                    },
                },
            },
        },
    },
    "misc_config_group": {
        "metadata": {
            "wake_prefix": {
                "type": "list",
                "items": {"type": "string"},
            },
            "t2i": {
                "type": "bool",
            },
            "t2i_word_threshold": {
                "type": "int",
            },
            "admins_id": {
                "type": "list",
                "items": {"type": "string"},
            },
            "http_proxy": {
                "type": "string",
            },
            "no_proxy": {
                "description": "Endereços de conexão direta",
                "type": "list",
                "items": {"type": "string"},
                "hint": "Adicione endereços que devem ser acessados sem proxy, como serviços internos. Pressione Enter para adicionar cada um. Ignore esta opção se não usar proxy.",
            },
            "timezone": {
                "type": "string",
            },
            "callback_api_base": {
                "type": "string",
            },
            "disable_metrics": {
                "description": "Desativar estatísticas anônimas de uso",
                "type": "bool",
                "hint": "Quando desativado, o AstrBot não enviará mais estatísticas anônimas de uso.",
            },
            "log_level": {
                "type": "string",
                "options": ["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"],
            },
            "dashboard.ssl.enable": {"type": "bool"},
            "dashboard.trust_proxy_headers": {"type": "bool"},
            "dashboard.auth_rate_limit.enable": {"type": "bool"},
            "dashboard.auth_rate_limit.average_interval": {"type": "float"},
            "dashboard.auth_rate_limit.max_burst": {"type": "int"},
            "dashboard.ssl.cert_file": {
                "type": "string",
                "condition": {"dashboard.ssl.enable": True},
            },
            "dashboard.ssl.key_file": {
                "type": "string",
                "condition": {"dashboard.ssl.enable": True},
            },
            "dashboard.ssl.ca_certs": {
                "type": "string",
                "condition": {"dashboard.ssl.enable": True},
            },
            "log_file_enable": {"type": "bool"},
            "log_file_path": {"type": "string", "condition": {"log_file_enable": True}},
            "log_file_max_mb": {"type": "int", "condition": {"log_file_enable": True}},
            "temp_dir_max_size": {"type": "int"},
            "trace_log_enable": {"type": "bool"},
            "trace_log_path": {
                "type": "string",
                "condition": {"trace_log_enable": True},
            },
            "trace_log_max_mb": {
                "type": "int",
                "condition": {"trace_log_enable": True},
            },
            "t2i_strategy": {
                "type": "string",
                "options": ["remote", "local"],
            },
            "t2i_endpoint": {
                "type": "string",
            },
            "t2i_use_file_service": {
                "type": "bool",
            },
            "pip_install_arg": {
                "type": "string",
            },
            "pypi_index_url": {
                "type": "string",
            },
            "default_kb_collection": {
                "type": "string",
            },
            "kb_names": {"type": "list", "items": {"type": "string"}},
            "kb_fusion_top_k": {"type": "int", "default": 20},
            "kb_final_top_k": {"type": "int", "default": 5},
            "kb_agentic_mode": {"type": "bool"},
        },
    },
}


"""
Since v4.7.0, fields such as name, description, and hint support i18n.
Their resources are stored in:

- dashboard/src/i18n/locales/<locale>/features/config-metadata.json

When adding configuration fields here, update this file for every supported
Dashboard locale.
"""
CONFIG_METADATA_3 = {
    "ai_group": {
        "name": "IA",
        "metadata": {
            "agent_runner": {
                "description": "Modo de execução do Agent",
                "hint": "Escolha como as conversas de IA serão executadas. Ao trocar o modo, a configuração passa a usar os padrões do novo tipo.",
                "type": "object",
                "items": {
                    "provider_settings.enable": {
                        "description": "Ativar",
                        "type": "bool",
                        "hint": "Chave principal das conversas com IA",
                    },
                    "agent_runner.runner_type": {
                        "description": "Modo de execução",
                        "type": "string",
                        "options": ["local", "dify", "coze", "dashscope", "deerflow"],
                        "labels": [
                            "Agent integrado",
                            "Dify",
                            "Coze",
                            "Aplicação Alibaba Cloud Bailian",
                            "DeerFlow",
                        ],
                        "_special": "agent_runner_type",
                        "runner_defaults": {
                            runner_type: get_agent_runner_config_default(runner_type)
                            for runner_type in (
                                "local",
                                "dify",
                                "coze",
                                "dashscope",
                                "deerflow",
                            )
                        },
                        "condition": {
                            "provider_settings.enable": True,
                        },
                    },
                },
            },
            "dify_runner": {
                "description": "Configuração do Dify",
                "type": "object",
                "condition": {
                    "provider_settings.enable": True,
                    "agent_runner.runner_type": "dify",
                },
                "items": {
                    "agent_runner.config.dify_api_type": {
                        "description": "Tipo de aplicação",
                        "type": "string",
                        "options": ["chat", "chatflow", "agent", "workflow"],
                    },
                    "agent_runner.config.dify_api_key": {
                        "description": "Chave de API",
                        "type": "string",
                        "secret": True,
                    },
                    "agent_runner.config.dify_api_base": {
                        "description": "URL base da API",
                        "type": "string",
                    },
                    "agent_runner.config.dify_workflow_output_key": {
                        "description": "Variável de saída do workflow",
                        "type": "string",
                    },
                    "agent_runner.config.dify_query_input_key": {
                        "description": "Variável de entrada do prompt",
                        "type": "string",
                    },
                    "agent_runner.config.variables": {
                        "description": "Variáveis",
                        "type": "dict",
                    },
                    "agent_runner.config.timeout": {
                        "description": "Tempo limite (segundos)",
                        "type": "int",
                    },
                    "agent_runner.config.proxy": {
                        "description": "URL do proxy",
                        "type": "string",
                    },
                },
            },
            "coze_runner": {
                "description": "Configuração do Coze",
                "type": "object",
                "condition": {
                    "provider_settings.enable": True,
                    "agent_runner.runner_type": "coze",
                },
                "items": {
                    "agent_runner.config.coze_api_key": {
                        "description": "Chave de API",
                        "type": "string",
                        "secret": True,
                    },
                    "agent_runner.config.bot_id": {
                        "description": "ID do bot",
                        "type": "string",
                    },
                    "agent_runner.config.coze_api_base": {
                        "description": "URL base da API",
                        "type": "string",
                    },
                    "agent_runner.config.auto_save_history": {
                        "description": "Deixar o Coze gerenciar o histórico",
                        "type": "bool",
                    },
                    "agent_runner.config.timeout": {
                        "description": "Tempo limite (segundos)",
                        "type": "int",
                    },
                    "agent_runner.config.proxy": {
                        "description": "URL do proxy",
                        "type": "string",
                    },
                },
            },
            "dashscope_runner": {
                "description": "Configuração do Alibaba Cloud Bailian",
                "type": "object",
                "condition": {
                    "provider_settings.enable": True,
                    "agent_runner.runner_type": "dashscope",
                },
                "items": {
                    "agent_runner.config.dashscope_app_type": {
                        "description": "Tipo de aplicação",
                        "type": "string",
                        "options": ["agent", "workflow"],
                    },
                    "agent_runner.config.dashscope_api_key": {
                        "description": "Chave de API",
                        "type": "string",
                        "secret": True,
                    },
                    "agent_runner.config.dashscope_app_id": {
                        "description": "ID da aplicação",
                        "type": "string",
                    },
                    "agent_runner.config.rag_options.pipeline_ids": {
                        "description": "IDs dos pipelines da base de conhecimento",
                        "type": "list",
                        "items": {"type": "string"},
                    },
                    "agent_runner.config.rag_options.file_ids": {
                        "description": "IDs dos arquivos",
                        "type": "list",
                        "items": {"type": "string"},
                    },
                    "agent_runner.config.rag_options.output_reference": {
                        "description": "Incluir referências",
                        "type": "bool",
                    },
                    "agent_runner.config.variables": {
                        "description": "Variáveis",
                        "type": "dict",
                    },
                    "agent_runner.config.timeout": {
                        "description": "Tempo limite (segundos)",
                        "type": "int",
                    },
                    "agent_runner.config.proxy": {
                        "description": "URL do proxy",
                        "type": "string",
                    },
                },
            },
            "deerflow_runner": {
                "description": "Configuração do DeerFlow",
                "type": "object",
                "condition": {
                    "provider_settings.enable": True,
                    "agent_runner.runner_type": "deerflow",
                },
                "items": {
                    "agent_runner.config.deerflow_api_base": {
                        "description": "URL base da API",
                        "type": "string",
                    },
                    "agent_runner.config.deerflow_api_key": {
                        "description": "Chave de API",
                        "type": "string",
                        "secret": True,
                    },
                    "agent_runner.config.deerflow_auth_header": {
                        "description": "Header de autorização",
                        "type": "string",
                        "secret": True,
                    },
                    "agent_runner.config.deerflow_assistant_id": {
                        "description": "ID do assistente",
                        "type": "string",
                    },
                    "agent_runner.config.deerflow_model_name": {
                        "description": "Sobrescrever nome do modelo",
                        "type": "string",
                    },
                    "agent_runner.config.deerflow_thinking_enabled": {
                        "description": "Ativar modo de raciocínio",
                        "type": "bool",
                    },
                    "agent_runner.config.deerflow_plan_mode": {
                        "description": "Ativar modo de planejamento",
                        "type": "bool",
                    },
                    "agent_runner.config.deerflow_subagent_enabled": {
                        "description": "Ativar subagentes",
                        "type": "bool",
                    },
                    "agent_runner.config.deerflow_max_concurrent_subagents": {
                        "description": "Máximo de subagentes simultâneos",
                        "type": "int",
                    },
                    "agent_runner.config.deerflow_recursion_limit": {
                        "description": "Limite de recursão",
                        "type": "int",
                    },
                    "agent_runner.config.timeout": {
                        "description": "Tempo limite (segundos)",
                        "type": "int",
                    },
                    "agent_runner.config.proxy": {
                        "description": "URL do proxy",
                        "type": "string",
                    },
                },
            },
            "ai": {
                "description": "Modelo",
                "hint": "Configure os modelos de chat do Agent integrado e os modelos compartilhados de imagem e voz.",
                "type": "object",
                "items": {
                    "agent_runner.config.model.provider_id": {
                        "description": "Modelo de chat",
                        "type": "string",
                        "_special": "select_provider",
                        "hint": "Usa o primeiro modelo quando vazio",
                        "condition": {
                            "agent_runner.runner_type": "local",
                        },
                    },
                    "agent_runner.config.model.fallback_provider_ids": {
                        "description": "Modelos alternativos",
                        "type": "list",
                        "items": {"type": "string"},
                        "_special": "select_providers",
                        "hint": "Tenta estes modelos em ordem quando o principal falhar.",
                        "condition": {
                            "agent_runner.runner_type": "local",
                        },
                    },
                    "agent_runner.config.model.request_max_retries": {
                        "description": "Tentativas em caso de erro",
                        "type": "int",
                        "hint": "Máximo de tentativas para uma solicitação do modelo quando o erro permitir nova tentativa.",
                        "condition": {
                            "agent_runner.runner_type": "local",
                        },
                    },
                    "provider_settings.default_image_caption_provider_id": {
                        "description": "Modelo para descrição de imagens",
                        "type": "string",
                        "_special": "select_provider",
                        "hint": "Deixe vazio para desativar; útil quando o modelo principal não é multimodal",
                    },
                    "provider_stt_settings.enable": {
                        "description": "Reconhecimento de voz",
                        "type": "bool",
                        "hint": "Transcreve mensagens de voz para texto.",
                    },
                    "provider_stt_settings.provider_id": {
                        "description": "Modelo padrão de fala para texto",
                        "type": "string",
                        "hint": "Também é possível escolher um modelo STT específico por sessão usando /provider.",
                        "_special": "select_provider_stt",
                        "condition": {
                            "provider_stt_settings.enable": True,
                        },
                    },
                    "provider_tts_settings.enable": {
                        "description": "Respostas por voz",
                        "type": "bool",
                        "hint": "Converte respostas de texto em voz.",
                    },
                    "provider_tts_settings.provider_id": {
                        "description": "Modelo padrão de texto para fala",
                        "type": "string",
                        "_special": "select_provider_tts",
                        "condition": {
                            "provider_tts_settings.enable": True,
                        },
                    },
                    "provider_tts_settings.trigger_probability": {
                        "description": "Probabilidade de acionar TTS",
                        "type": "float",
                        "slider": {"min": 0, "max": 1, "step": 0.05},
                        "condition": {
                            "provider_tts_settings.enable": True,
                        },
                    },
                    "provider_settings.image_caption_prompt": {
                        "description": "Prompt para descrição de imagem",
                        "type": "text",
                        "collapsed": True,
                    },
                },
                "condition": {
                    "provider_settings.enable": True,
                },
            },
            "persona": {
                "description": "Persona",
                "hint": "Defina a persona padrão das conversas com IA.",
                "type": "object",
                "items": {
                    "agent_runner.config.persona.persona_id": {
                        "description": "Persona padrão",
                        "type": "string",
                        "_special": "select_persona",
                    },
                    "agent_runner.config.persona.safety_mode": {
                        "description": "Modo de segurança",
                        "type": "bool",
                        "hint": "Orienta o modelo para conteúdo seguro e reduz respostas sobre tópicos nocivos ou sensíveis.",
                    },
                    "agent_runner.config.persona.safety_mode_strategy": {
                        "description": "Estratégia do modo de segurança",
                        "type": "string",
                        "invisible": True,
                        "options": ["system_prompt"],
                        "hint": "Escolha como o modo de segurança será aplicado.",
                        "condition": {
                            "agent_runner.config.persona.safety_mode": True,
                        },
                    },
                },
                "condition": {
                    "agent_runner.runner_type": "local",
                    "provider_settings.enable": True,
                },
            },
            "knowledgebase": {
                "description": "Base de conhecimento",
                "hint": "Funciona como um cérebro externo do AstrBot.",
                "type": "object",
                "items": {
                    "kb_names": {
                        "description": "Lista de bases de conhecimento",
                        "type": "list",
                        "items": {"type": "string"},
                        "_special": "select_knowledgebase",
                        "hint": "Permite múltiplas seleções",
                    },
                    "kb_fusion_top_k": {
                        "description": "Quantidade de resultados após fusão",
                        "type": "int",
                        "hint": "Número de resultados retornados após combinar buscas em várias bases",
                    },
                    "kb_final_top_k": {
                        "description": "Quantidade final de resultados",
                        "type": "int",
                        "hint": "Quantidade de resultados enviados ao modelo. Valores maiores trazem mais contexto, mas podem introduzir ruído.",
                    },
                    "kb_agentic_mode": {
                        "description": "Recuperação agentic da base",
                        "type": "bool",
                        "hint": "Transforma a consulta à base em uma ferramenta do LLM, permitindo que o modelo decida quando pesquisar. Exige suporte a function calling.",
                    },
                },
                "condition": {
                    "agent_runner.runner_type": "local",
                    "provider_settings.enable": True,
                },
            },
            "websearch": {
                "description": "Pesquisa na web",
                "hint": "Permite que o AstrBot acesse a internet para obter informações atuais.",
                "type": "object",
                "items": {
                    "provider_settings.web_search": {
                        "description": "Ativar pesquisa na web",
                        "type": "bool",
                    },
                    "provider_settings.websearch_provider": {
                        "description": "Provedor de pesquisa",
                        "type": "string",
                        "options": [
                            "tavily",
                            "baidu_ai_search",
                            "bocha",
                            "brave",
                            "firecrawl",
                            "exa",
                            "anysearch",
                        ],
                        "condition": {
                            "provider_settings.web_search": True,
                        },
                    },
                    "provider_settings.websearch_tavily_key": {
                        "description": "Chave de API do Tavily",
                        "type": "list",
                        "items": {"type": "string"},
                        "hint": "É possível adicionar várias chaves para rotação.",
                        "secret": True,
                        "condition": {
                            "provider_settings.websearch_provider": "tavily",
                            "provider_settings.web_search": True,
                        },
                    },
                    "provider_settings.websearch_bocha_key": {
                        "description": "Chave de API do BoCha",
                        "type": "list",
                        "items": {"type": "string"},
                        "hint": "É possível adicionar várias chaves para rotação.",
                        "secret": True,
                        "condition": {
                            "provider_settings.websearch_provider": "bocha",
                            "provider_settings.web_search": True,
                        },
                    },
                    "provider_settings.websearch_brave_key": {
                        "description": "Chave de API do Brave Search",
                        "type": "list",
                        "items": {"type": "string"},
                        "hint": "É possível adicionar várias chaves para rotação.",
                        "secret": True,
                        "condition": {
                            "provider_settings.websearch_provider": "brave",
                            "provider_settings.web_search": True,
                        },
                    },
                    "provider_settings.websearch_firecrawl_key": {
                        "description": "Chave de API do Firecrawl",
                        "type": "list",
                        "items": {"type": "string"},
                        "hint": "É possível adicionar várias chaves para rotação.",
                        "secret": True,
                        "condition": {
                            "provider_settings.websearch_provider": "firecrawl",
                            "provider_settings.web_search": True,
                        },
                    },
                    "provider_settings.websearch_baidu_app_builder_key": {
                        "description": "Chave de API do Baidu Qianfan Smart Cloud APP Builder",
                        "type": "string",
                        "hint": "Referência: [https://console.bce.baidu.com/iam/#/iam/apikey/list](https://console.bce.baidu.com/iam/#/iam/apikey/list)",
                        "secret": True,
                        "condition": {
                            "provider_settings.websearch_provider": "baidu_ai_search",
                            "provider_settings.web_search": True,
                        },
                    },
                    "provider_settings.websearch_exa_key": {
                        "description": "Chave de API do Exa",
                        "type": "list",
                        "items": {"type": "string"},
                        "hint": "Permite várias chaves para rotação.",
                        "secret": True,
                        "condition": {
                            "provider_settings.websearch_provider": "exa",
                            "provider_settings.web_search": True,
                        },
                    },
                    "provider_settings.websearch_anysearch_key": {
                        "description": "Chave de API do AnySearch",
                        "type": "list",
                        "items": {"type": "string"},
                        "hint": "Deixe vazio para usar o modo anônimo quando disponível.",
                        "condition": {
                            "provider_settings.websearch_provider": "anysearch",
                            "provider_settings.web_search": True,
                        },
                    },
                    "provider_settings.web_search_link": {
                        "description": "Exibir citações das fontes",
                        "type": "bool",
                        "condition": {
                            "provider_settings.web_search": True,
                        },
                    },
                },
                "condition": {
                    "agent_runner.runner_type": "local",
                    "provider_settings.enable": True,
                },
            },
            "agent_computer_use": {
                "description": "Acesso do Agent ao computador",
                "hint": "Permite que o AstrBot use o computador local ou um ambiente Sandbox para tarefas mais complexas.",
                "type": "object",
                "items": {
                    "provider_settings.computer_use_runtime": {
                        "description": "Runtime do Computer Use",
                        "type": "string",
                        "options": ["none", "local", "sandbox"],
                        "labels": [
                            "Nenhum ambiente",
                            "Máquina local",
                            "Sandbox de terceiros",
                        ],
                        "hint": "Ambiente ao qual o Agent poderá ter acesso.",
                    },
                    "provider_settings.computer_use_local_permissions": {
                        "description": "Políticas de permissão local",
                        "type": "object",
                        "_special": "local_permission_matrix",
                        "full_width": True,
                        "items": {
                            "member": {
                                "type": "object",
                                "items": {
                                    "allow_execution": {"type": "bool"},
                                    "allow_network": {"type": "bool"},
                                    "filesystem_scope": {
                                        "type": "string",
                                        "options": ["none", "workspace", "host"],
                                    },
                                },
                            },
                            "admin": {
                                "type": "object",
                                "items": {
                                    "allow_execution": {"type": "bool"},
                                    "allow_network": {"type": "bool"},
                                    "filesystem_scope": {
                                        "type": "string",
                                        "options": ["none", "workspace", "host"],
                                    },
                                },
                            },
                        },
                        "condition": {
                            "provider_settings.computer_use_runtime": "local",
                        },
                    },
                    "provider_settings.computer_use_require_admin": {
                        "description": "Exigir administrador para Sandbox",
                        "type": "bool",
                        "hint": "Quando ativado, somente administradores do AstrBot podem usar recursos de Sandbox remoto.",
                        "condition": {
                            "provider_settings.computer_use_runtime": "sandbox",
                        },
                    },
                    "provider_settings.sandbox.booter": {
                        "description": "Driver do ambiente Sandbox",
                        "type": "string",
                        "options": ["shipyard_neo", "shipyard", "cua"],
                        "labels": ["Shipyard Neo", "Shipyard", "CUA"],
                        "condition": {
                            "provider_settings.computer_use_runtime": "sandbox",
                        },
                    },
                    "provider_settings.sandbox.shipyard_neo_endpoint": {
                        "description": "Endpoint da API Shipyard Neo",
                        "type": "string",
                        "hint": "Endereço da API do Bay. Padrão: http://127.0.0.1:8114.",
                        "condition": {
                            "provider_settings.computer_use_runtime": "sandbox",
                            "provider_settings.sandbox.booter": "shipyard_neo",
                        },
                    },
                    "provider_settings.sandbox.shipyard_neo_access_token": {
                        "description": "Access token do Shipyard Neo",
                        "type": "string",
                        "hint": "Chave de API do Bay (sk-bay-...). Deixe vazio para descobrir automaticamente em credentials.json.",
                        "secret": True,
                        "condition": {
                            "provider_settings.computer_use_runtime": "sandbox",
                            "provider_settings.sandbox.booter": "shipyard_neo",
                        },
                    },
                    "provider_settings.sandbox.shipyard_neo_profile": {
                        "description": "Perfil do Shipyard Neo",
                        "type": "string",
                        "hint": "Perfil do ambiente isolado do Shipyard Neo, por exemplo, python-default. Deixe vazio para selecionar automaticamente o perfil mais completo.",
                        "condition": {
                            "provider_settings.computer_use_runtime": "sandbox",
                            "provider_settings.sandbox.booter": "shipyard_neo",
                        },
                    },
                    "provider_settings.sandbox.shipyard_neo_ttl": {
                        "description": "TTL do Sandbox Shipyard Neo",
                        "type": "int",
                        "hint": "Tempo de vida do ambiente isolado, em segundos.",
                        "condition": {
                            "provider_settings.computer_use_runtime": "sandbox",
                            "provider_settings.sandbox.booter": "shipyard_neo",
                        },
                    },
                    "provider_settings.sandbox.cua_image": {
                        "description": "Imagem CUA",
                        "type": "string",
                        "hint": "Imagem ou tipo de sistema operacional do ambiente isolado CUA. Padrão: linux. Os valores aceitos dependem do SDK CUA instalado.",
                        "condition": {
                            "provider_settings.computer_use_runtime": "sandbox",
                            "provider_settings.sandbox.booter": "cua",
                        },
                    },
                    "provider_settings.sandbox.cua_os_type": {
                        "description": "Sistema operacional CUA",
                        "type": "string",
                        "options": ["linux", "macos", "windows", "android"],
                        "labels": ["Linux", "macOS", "Windows", "Android"],
                        "hint": "Tipo de sistema operacional do ambiente isolado CUA. Padrão: linux.",
                        "condition": {
                            "provider_settings.computer_use_runtime": "sandbox",
                            "provider_settings.sandbox.booter": "cua",
                        },
                    },
                    "provider_settings.sandbox.cua_idle_timeout": {
                        "description": "Tempo limite de inatividade CUA",
                        "type": "int",
                        "hint": "Tempo limite de inatividade das sessões CUA, em segundos. Quando maior que 0, o AstrBot encerra o ambiente isolado após esse período de inatividade; 0 desativa o limite.",
                        "condition": {
                            "provider_settings.computer_use_runtime": "sandbox",
                            "provider_settings.sandbox.booter": "cua",
                        },
                    },
                    "provider_settings.sandbox.cua_telemetry_enabled": {
                        "description": "Telemetria CUA",
                        "type": "bool",
                        "hint": "Permitir que o SDK CUA envie dados de telemetria. Desativado por padrão.",
                        "condition": {
                            "provider_settings.computer_use_runtime": "sandbox",
                            "provider_settings.sandbox.booter": "cua",
                        },
                    },
                    "provider_settings.sandbox.cua_local": {
                        "description": "Sandbox CUA local",
                        "type": "bool",
                        "hint": "Preferir um ambiente isolado CUA local. Ativado por padrão para dispensar CUA_API_KEY para ambientes na nuvem. Desative para usar os ambientes CUA na nuvem.",
                        "condition": {
                            "provider_settings.computer_use_runtime": "sandbox",
                            "provider_settings.sandbox.booter": "cua",
                        },
                    },
                    "provider_settings.sandbox.cua_api_key": {
                        "description": "Chave de API do CUA",
                        "type": "string",
                        "hint": "Chave de API dos ambientes CUA na nuvem. Necessária apenas quando o ambiente local está desativado. Também pode ser informada pela variável de ambiente CUA_API_KEY.",
                        "obvious_hint": True,
                        "secret": True,
                        "condition": {
                            "provider_settings.computer_use_runtime": "sandbox",
                            "provider_settings.sandbox.booter": "cua",
                            "provider_settings.sandbox.cua_local": False,
                        },
                    },
                    "provider_settings.sandbox.shipyard_endpoint": {
                        "description": "Endpoint da API Shipyard",
                        "type": "string",
                        "hint": "Endereço de acesso à API do serviço Shipyard.",
                        "condition": {
                            "provider_settings.computer_use_runtime": "sandbox",
                            "provider_settings.sandbox.booter": "shipyard",
                        },
                        "_special": "check_shipyard_connection",
                    },
                    "provider_settings.sandbox.shipyard_access_token": {
                        "description": "Access token do Shipyard",
                        "type": "string",
                        "hint": "Token de acesso ao serviço Shipyard.",
                        "secret": True,
                        "condition": {
                            "provider_settings.computer_use_runtime": "sandbox",
                            "provider_settings.sandbox.booter": "shipyard",
                        },
                    },
                    "provider_settings.sandbox.shipyard_ttl": {
                        "description": "TTL da sessão Shipyard",
                        "type": "int",
                        "hint": "Tempo de vida da sessão, em segundos.",
                        "condition": {
                            "provider_settings.computer_use_runtime": "sandbox",
                            "provider_settings.sandbox.booter": "shipyard",
                        },
                    },
                    "provider_settings.sandbox.shipyard_max_sessions": {
                        "description": "Máximo de sessões Shipyard",
                        "type": "int",
                        "hint": "Número máximo de sessões Shipyard que uma instância pode gerenciar.",
                        "condition": {
                            "provider_settings.computer_use_runtime": "sandbox",
                            "provider_settings.sandbox.booter": "shipyard",
                        },
                    },
                },
                "condition": {
                    "agent_runner.runner_type": "local",
                    "provider_settings.enable": True,
                },
            },
            # "file_extract": {
            #     "description": "文档解析能力 [beta]",
            #     "type": "object",
            #     "items": {
            #         "provider_settings.file_extract.enable": {
            #             "description": "启用文档解析能力",
            #             "type": "bool",
            #         },
            #         "provider_settings.file_extract.provider": {
            #             "description": "文档解析提供商",
            #             "type": "string",
            #             "options": ["moonshotai"],
            #             "condition": {
            #                 "provider_settings.file_extract.enable": True,
            #             },
            #         },
            #         "provider_settings.file_extract.moonshotai_api_key": {
            #             "description": "Moonshot AI API Key",
            #             "type": "string",
            #             "condition": {
            #                 "provider_settings.file_extract.provider": "moonshotai",
            #                 "provider_settings.file_extract.enable": True,
            #             },
            #         },
            #     },
            #     "condition": {
            #         "agent_runner.runner_type": "local",
            #         "provider_settings.enable": True,
            #     },
            # },
            "proactive_capability": {
                "description": "Agent proativo",
                "hint": "O AstrBot pode acordar, executar tarefas agendadas e entregar o resultado.",
                "type": "object",
                "items": {
                    "provider_settings.proactive_capability.add_cron_tools": {
                        "description": "Ativar",
                        "type": "bool",
                        "hint": "Disponibiliza ao Agent as ferramentas necessárias para criar e executar tarefas futuras.",
                    },
                },
                "condition": {
                    "agent_runner.runner_type": "local",
                    "provider_settings.enable": True,
                },
            },
            "truncate_and_compress": {
                "hint": "Gerencie truncamento e compressão de histórico.",
                "description": "Estratégia de gerenciamento de contexto",
                "type": "object",
                "items": {
                    "agent_runner.config.compression.max_turns": {
                        "description": "Máximo de turnos antes da compressão",
                        "type": "int",
                        "hint": "O histórico persistente da conversa só é truncado ou comprimido pelo modelo conforme a estratégia abaixo após ultrapassar este número de turnos. Os contextos das requisições também são limitados por este valor antes do envio. -1 significa sem limite por turnos.",
                        "condition": {
                            "agent_runner.runner_type": "local",
                        },
                    },
                    "agent_runner.config.compression.trim_turns": {
                        "description": "Turnos descartados ao exceder o limite",
                        "type": "int",
                        "hint": "Quando o histórico ultrapassa o limite de turnos antes da compressão e a compressão pelo modelo não está disponível, descarta este número de turnos mais antigos de uma vez. O truncamento das requisições também usa este valor.",
                        "condition": {
                            "agent_runner.runner_type": "local",
                        },
                    },
                    "agent_runner.config.compression.overflow_strategy": {
                        "description": "Tratamento do limite do histórico ou da janela de contexto",
                        "type": "string",
                        "options": ["truncate_by_turns", "llm_compress"],
                        "labels": ["Truncar por turnos", "Comprimir com LLM"],
                        "condition": {
                            "agent_runner.runner_type": "local",
                        },
                        "hint": "O histórico persistente usa esta estratégia somente após ultrapassar o limite de turnos antes da compressão. Antes de cada requisição, a mesma estratégia pode proteger o contexto em andamento quando o número de tokens se aproxima da janela do modelo.",
                    },
                    "agent_runner.config.compression.instruction": {
                        "description": "Instrução de compressão do contexto",
                        "type": "text",
                        "hint": "Se ficar vazio, será usado o prompt padrão.",
                        "condition": {
                            "agent_runner.config.compression.overflow_strategy": "llm_compress",
                            "agent_runner.runner_type": "local",
                        },
                    },
                    "agent_runner.config.compression.keep_recent_ratio": {
                        "description": "Proporção de contexto recente preservada",
                        "type": "float",
                        "slider": {"min": 0, "max": 0.3, "step": 0.01},
                        "hint": "Preserva o contexto recente exato conforme a proporção de tokens do contexto atual, de 0 a 0.3. O valor 0.15 preserva 15%; valores acima de 0 preservam pelo menos a rodada mais recente.",
                        "condition": {
                            "agent_runner.config.compression.overflow_strategy": "llm_compress",
                            "agent_runner.runner_type": "local",
                        },
                    },
                    "agent_runner.config.compression.provider_id": {
                        "description": "Modelo usado para compressão",
                        "type": "string",
                        "_special": "select_provider",
                        "hint": "Se ficar vazio, o modelo de conversa atual será usado para a compressão. Se ele estiver indisponível ou a compressão falhar, o AstrBot usará a estratégia de truncamento por turnos.",
                        "condition": {
                            "agent_runner.config.compression.overflow_strategy": "llm_compress",
                            "agent_runner.runner_type": "local",
                        },
                    },
                    "agent_runner.config.compression.fallback_max_tokens": {
                        "description": "Tamanho alternativo da janela de contexto",
                        "type": "int",
                        "hint": "Quando max_context_tokens é 0 e o modelo não está nos metadados internos, usa este valor como tamanho da janela de contexto. Padrão: 128000.",
                        "condition": {
                            "agent_runner.runner_type": "local",
                        },
                    },
                },
                "condition": {
                    "agent_runner.runner_type": "local",
                    "provider_settings.enable": True,
                },
            },
            "others": {
                "description": "Outras configurações",
                "type": "object",
                "items": {
                    "provider_settings.display_reasoning_text": {
                        "description": "Exibir conteúdo de raciocínio",
                        "type": "bool",
                        "condition": {
                            "agent_runner.runner_type": "local",
                        },
                    },
                    "provider_settings.streaming_response": {
                        "description": "Resposta em tempo real",
                        "type": "bool",
                    },
                    "provider_settings.unsupported_streaming_strategy": {
                        "description": "Plataformas sem suporte a streaming",
                        "type": "string",
                        "options": ["realtime_segmenting", "turn_off"],
                        "hint": "Selecione como lidar com plataformas que não oferecem respostas em streaming. A resposta segmentada em tempo real envia o conteúdo assim que o sistema detecta pontos de divisão, como pontuação, durante o recebimento.",
                        "labels": [
                            "Resposta segmentada em tempo real",
                            "Desativar streaming",
                        ],
                        "condition": {
                            "provider_settings.streaming_response": True,
                        },
                    },
                    "provider_settings.identifier": {
                        "description": "Identificação do usuário",
                        "type": "bool",
                        "hint": "Inclui o ID do usuário no prompt.",
                    },
                    "provider_settings.group_name_display": {
                        "description": "Exibir nome do grupo",
                        "type": "bool",
                        "hint": "Quando ativado, inclui o nome do grupo no prompt nas plataformas compatíveis (OneBot v11).",
                    },
                    "provider_settings.datetime_system_prompt": {
                        "description": "Consciência de data e hora reais",
                        "type": "bool",
                        "hint": "Quando ativado, acrescenta a hora atual ao prompt de sistema.",
                        "condition": {
                            "agent_runner.runner_type": "local",
                        },
                    },
                    "provider_settings.show_tool_use_status": {
                        "description": "Exibir informações das chamadas de ferramentas",
                        "type": "bool",
                        "condition": {
                            "agent_runner.runner_type": "local",
                        },
                    },
                    "provider_settings.show_tool_call_result": {
                        "description": "Exibir resultado das ferramentas",
                        "type": "bool",
                        "hint": "Só funciona quando a exibição das informações das chamadas de ferramentas está ativada e mostra no máximo 70 caracteres.",
                        "condition": {
                            "agent_runner.runner_type": "local",
                            "provider_settings.show_tool_use_status": True,
                        },
                    },
                    "provider_settings.buffer_intermediate_messages": {
                        "description": "Agrupar mensagens intermediárias do Agent",
                        "type": "bool",
                        "hint": "Quando ativado, armazena o texto intermediário gerado por chamadas de ferramentas em várias etapas no modo sem streaming e o envia como uma resposta única quando o agente termina.",
                        "condition": {
                            "agent_runner.runner_type": "local",
                            "provider_settings.streaming_response": False,
                        },
                    },
                    "agent_runner.config.misc.sanitize_context_by_modalities": {
                        "description": "Sanitizar histórico conforme modalidades",
                        "type": "bool",
                        "hint": "Quando ativado, limpa os contextos antes de cada requisição ao modelo, removendo blocos de imagem e estruturas de chamadas de ferramentas incompatíveis com as modalidades do provedor atual (isso altera o que o modelo recebe).",
                        "condition": {
                            "agent_runner.runner_type": "local",
                        },
                    },
                    "agent_runner.config.misc.max_steps": {
                        "description": "Máximo de rodadas de chamadas de ferramentas",
                        "type": "int",
                        "condition": {
                            "agent_runner.runner_type": "local",
                        },
                    },
                    "agent_runner.config.misc.tool_call_timeout": {
                        "description": "Tempo limite da ferramenta (segundos)",
                        "type": "int",
                        "condition": {
                            "agent_runner.runner_type": "local",
                        },
                    },
                    "agent_runner.config.misc.tool_schema_mode": {
                        "description": "Modo do schema de ferramentas",
                        "type": "string",
                        "options": ["skills_like", "full"],
                        "labels": ["Estilo Skills (duas etapas)", "Schema completo"],
                        "hint": "O modo semelhante a Skills envia primeiro o nome e a descrição e consulta os parâmetros depois; o modo completo envia todo o esquema de uma vez.",
                        "condition": {
                            "agent_runner.runner_type": "local",
                        },
                    },
                    "provider_settings.wake_prefix": {
                        "description": "Prefixo adicional de ativação",
                        "type": "string",
                        "hint": "Se o prefixo de ativação for / e o prefixo adicional de conversa for chat, será necessário usar /chat para acionar requisições ao modelo.",
                    },
                    "provider_settings.image_compress_options.max_size": {
                        "description": "Comprimento máximo da borda da imagem de entrada",
                        "type": "int",
                        "hint": "Maior borda enviada ao modelo, em pixels. As imagens podem ser reduzidas ainda mais para ficar abaixo de 512 KiB; os caminhos dos anexos originais são preservados.",
                        "slider": {"min": 256, "max": 4096, "step": 64},
                    },
                    "provider_settings.prompt_prefix": {
                        "description": "Prompt do usuário",
                        "type": "string",
                        "hint": "Use {{prompt}} como marcador da entrada do usuário. Sem esse marcador, o texto será adicionado antes da entrada do usuário.",
                        "collapsed": True,
                    },
                    "provider_tts_settings.dual_output": {
                        "description": "Enviar voz e texto quando TTS estiver ativo",
                        "type": "bool",
                        "collapsed": True,
                    },
                    "provider_settings.reachability_check": {
                        "description": "Verificar disponibilidade dos provedores",
                        "type": "bool",
                        "hint": "Ao executar o comando /provider, testa a conectividade dos provedores em paralelo. Isso consulta os modelos ativamente e pode consumir tokens adicionais.",
                        "collapsed": True,
                    },
                    "provider_settings.max_quoted_fallback_images": {
                        "description": "Limite de imagens encaminhadas",
                        "type": "int",
                        "hint": "Número máximo de imagens inseridas pela análise de mensagens encaminhadas; imagens excedentes são descartadas.",
                        "condition": {
                            "agent_runner.runner_type": "local",
                        },
                        "collapsed": True,
                    },
                    "provider_settings.quoted_message_parser.max_component_chain_depth": {
                        "description": "Profundidade de análise de texto formatado encaminhado",
                        "type": "int",
                        "hint": "Profundidade máxima de recursão ao analisar cadeias de componentes de texto formatado em mensagens encaminhadas.",
                        "condition": {
                            "agent_runner.runner_type": "local",
                        },
                        "collapsed": True,
                    },
                    "provider_settings.quoted_message_parser.max_forward_node_depth": {
                        "description": "Profundidade de análise de encaminhamentos aninhados",
                        "type": "int",
                        "hint": "Profundidade máxima de recursão ao analisar nós de encaminhamento aninhados.",
                        "condition": {
                            "agent_runner.runner_type": "local",
                        },
                        "collapsed": True,
                    },
                    "provider_settings.quoted_message_parser.max_forward_fetch": {
                        "description": "Limite de busca recursiva de encaminhamentos",
                        "type": "int",
                        "hint": "Número máximo de operações recursivas get_forward_msg.",
                        "condition": {
                            "agent_runner.runner_type": "local",
                        },
                        "collapsed": True,
                    },
                    "provider_settings.quoted_message_parser.warn_on_action_failure": {
                        "description": "Avisar sobre falha na análise de encaminhamentos",
                        "type": "bool",
                        "hint": "Quando ativado, registra avisos quando todas as tentativas de get_msg/get_forward_msg falham.",
                        "condition": {
                            "agent_runner.runner_type": "local",
                        },
                        "collapsed": True,
                    },
                },
                "condition": {
                    "provider_settings.enable": True,
                },
            },
        },
    },
    "platform_group": {
        "name": "Plataformas e mensagens",
        "metadata": {
            "general": {
                "description": "Geral",
                "type": "object",
                "items": {
                    "platform_settings.unique_session": {
                        "description": "Isolar conversa",
                        "type": "bool",
                        "hint": "Cada membro do grupo recebe um contexto separado quando a plataforma oferece suporte.",
                    },
                    "wake_prefix": {
                        "description": "Palavra de ativação",
                        "type": "list",
                        "items": {"type": "string"},
                    },
                    "platform_settings.friend_message_needs_wake_prefix": {
                        "description": "Mensagens privadas exigem palavra de ativação",
                        "type": "bool",
                    },
                    "platform_settings.reply_prefix": {
                        "description": "Prefixo das respostas",
                        "type": "string",
                    },
                    "platform_settings.reply_with_mention": {
                        "description": "Mencionar remetente na resposta",
                        "type": "bool",
                    },
                    "platform_settings.reply_with_quote": {
                        "description": "Citar mensagem do remetente",
                        "type": "bool",
                    },
                    "platform_settings.forward_threshold": {
                        "description": "Limite de tamanho para encaminhamento",
                        "type": "int",
                    },
                    "platform_settings.empty_mention_waiting": {
                        "description": "Aguardar após mensagem contendo apenas menção",
                        "type": "bool",
                    },
                    "disable_builtin_commands": {
                        "description": "Desativar comandos internos",
                        "type": "bool",
                        "hint": "Desativa todos os comandos internos do AstrBot, como help, sid, new e outros.",
                    },
                },
            },
            "rate_limit": {
                "description": "Limite de requisições",
                "type": "object",
                "items": {
                    "platform_settings.rate_limit.time": {
                        "description": "Janela do limite de mensagens (segundos)",
                        "type": "int",
                    },
                    "platform_settings.rate_limit.count": {
                        "description": "Quantidade limite de mensagens",
                        "type": "int",
                    },
                    "platform_settings.rate_limit.strategy": {
                        "description": "Estratégia de limitação de mensagens",
                        "type": "string",
                        "options": ["stall", "discard"],
                    },
                },
            },
            "content_safety": {
                "description": "Segurança de conteúdo",
                "type": "object",
                "items": {
                    "content_safety.also_use_in_response": {
                        "description": "Verificar também o conteúdo das respostas do modelo",
                        "type": "bool",
                    },
                    "content_safety.baidu_aip.enable": {
                        "description": "Usar moderação de conteúdo do Baidu",
                        "type": "bool",
                        "hint": "É necessário instalar manualmente a biblioteca baidu-aip.",
                    },
                    "content_safety.baidu_aip.app_id": {
                        "description": "ID do aplicativo",
                        "type": "string",
                        "condition": {
                            "content_safety.baidu_aip.enable": True,
                        },
                    },
                    "content_safety.baidu_aip.api_key": {
                        "description": "Chave de API",
                        "type": "string",
                        "secret": True,
                        "condition": {
                            "content_safety.baidu_aip.enable": True,
                        },
                    },
                    "content_safety.baidu_aip.secret_key": {
                        "description": "Chave secreta",
                        "type": "string",
                        "secret": True,
                        "condition": {
                            "content_safety.baidu_aip.enable": True,
                        },
                    },
                    "content_safety.internal_keywords.enable": {
                        "description": "Verificação de palavras-chave",
                        "type": "bool",
                    },
                    "content_safety.internal_keywords.extra_keywords": {
                        "description": "Palavras-chave adicionais",
                        "type": "list",
                        "items": {"type": "string"},
                        "hint": "Lista adicional de palavras-chave bloqueadas. Aceita expressões regulares.",
                    },
                },
            },
            "others": {
                "description": "Outras configurações",
                "type": "object",
                "items": {
                    "platform_settings.ignore_bot_self_message": {
                        "description": "Ignorar mensagens do próprio bot",
                        "type": "bool",
                    },
                    "platform_settings.ignore_at_all": {
                        "description": "Ignorar eventos de menção a todos",
                        "type": "bool",
                    },
                    "platform_settings.no_permission_reply": {
                        "description": "Responder quando o usuário não tiver permissões suficientes",
                        "type": "bool",
                    },
                    "platform_specific.lark.pre_ack_emoji.enable": {
                        "description": "[Lark] Ativar emoji de confirmação de recebimento",
                        "type": "bool",
                    },
                    "platform_specific.lark.pre_ack_emoji.emojis": {
                        "description": "Lista de emojis (nomes enumerados do Lark)",
                        "type": "list",
                        "items": {"type": "string"},
                        "hint": "Referência dos nomes enumerados de emojis: [https://open.feishu.cn/document/server-docs/im-v1/message-reaction/emojis-introduce](https://open.feishu.cn/document/server-docs/im-v1/message-reaction/emojis-introduce)",
                        "condition": {
                            "platform_specific.lark.pre_ack_emoji.enable": True,
                        },
                    },
                    "platform_specific.telegram.pre_ack_emoji.enable": {
                        "description": "[Telegram] Ativar emoji de confirmação de recebimento",
                        "type": "bool",
                    },
                    "platform_specific.telegram.pre_ack_emoji.emojis": {
                        "description": "Lista de emojis (Unicode)",
                        "type": "list",
                        "items": {"type": "string"},
                        "hint": "O Telegram aceita apenas um conjunto fixo de reações. Referência: [https://gist.github.com/Soulter/3f22c8e5f9c7e152e967e8bc28c97fc9](https://gist.github.com/Soulter/3f22c8e5f9c7e152e967e8bc28c97fc9)",
                        "condition": {
                            "platform_specific.telegram.pre_ack_emoji.enable": True,
                        },
                    },
                    "platform_specific.discord.pre_ack_emoji.enable": {
                        "description": "[Discord] Ativar emoji de confirmação de recebimento",
                        "type": "bool",
                    },
                    "platform_specific.discord.pre_ack_emoji.emojis": {
                        "description": "Lista de emojis (Unicode ou nome de emoji personalizado)",
                        "type": "list",
                        "items": {"type": "string"},
                        "hint": "Informe símbolos de emoji Unicode, por exemplo, 👍, 🤔, ⏳",
                        "condition": {
                            "platform_specific.discord.pre_ack_emoji.enable": True,
                        },
                    },
                },
            },
        },
    },
    "access_group": {
        "name": "Controle de acesso",
        "metadata": {
            "admins": {
                "description": "Administradores",
                "type": "object",
                "items": {
                    "admins_id": {
                        "description": "IDs dos administradores",
                        "type": "list",
                        "items": {"type": "string"},
                        "hint": "Envie /sid ao bot para descobrir o ID.",
                    },
                },
            },
            "whitelist": {
                "description": "Lista de permissões",
                "type": "object",
                "items": {
                    "platform_settings.enable_id_white_list": {
                        "description": "Ativar lista de permissões",
                        "type": "bool",
                        "hint": "Quando ativada, apenas sessões cadastradas recebem resposta.",
                    },
                    "platform_settings.id_whitelist": {
                        "description": "IDs permitidos",
                        "type": "list",
                        "items": {"type": "string"},
                        "hint": "Use /sid para obter o ID. Lista vazia desativa a restrição.",
                    },
                    "platform_settings.id_whitelist_log": {
                        "description": "Registrar mensagens bloqueadas",
                        "type": "bool",
                        "hint": "Registra mensagens que não passam pela verificação da lista de permissões.",
                    },
                    "platform_settings.wl_ignore_admin_on_group": {
                        "description": "Administradores ignoram a lista em grupos",
                        "type": "bool",
                    },
                    "platform_settings.wl_ignore_admin_on_friend": {
                        "description": "Administradores ignoram a lista em chats privados",
                        "type": "bool",
                    },
                },
            },
        },
    },
    "plugin_group": {
        "name": "Plugins",
        "metadata": {
            "plugin": {
                "description": "Plugins",
                "type": "object",
                "items": {
                    "plugin_set": {
                        "description": "Plugins disponíveis",
                        "type": "bool",
                        "hint": "Todos os plugins não desativados ficam disponíveis por padrão.",
                        "_special": "select_plugin_set",
                    },
                },
            },
        },
    },
    "ext_group": {
        "name": "Extras",
        "metadata": {
            "segmented_reply": {
                "description": "Resposta segmentada",
                "type": "object",
                "items": {
                    "platform_settings.segmented_reply.enable": {
                        "description": "Ativar resposta segmentada",
                        "type": "bool",
                    },
                    "platform_settings.segmented_reply.only_llm_result": {
                        "description": "Segmentar apenas resultados do LLM",
                        "type": "bool",
                    },
                    "platform_settings.segmented_reply.interval_method": {
                        "description": "Método do intervalo",
                        "hint": "O modo random usa uma espera aleatória. O modo log calcula a espera pelo tamanho da mensagem: $y=log_{log\\_base}(x)$, em que x é a quantidade de palavras e y é o tempo em segundos.",
                        "type": "string",
                        "options": ["random", "log"],
                    },
                    "platform_settings.segmented_reply.interval": {
                        "description": "Intervalo aleatório",
                        "type": "string",
                        "hint": "Formato: mínimo,máximo (por exemplo, 1.5,3.5)",
                        "condition": {
                            "platform_settings.segmented_reply.interval_method": "random",
                        },
                    },
                    "platform_settings.segmented_reply.log_base": {
                        "description": "Base logarítmica",
                        "type": "float",
                        "hint": "Base dos intervalos logarítmicos. Padrão: 2.6. Faixa de valores: 1.0 a 10.0.",
                        "condition": {
                            "platform_settings.segmented_reply.interval_method": "log",
                        },
                    },
                    "platform_settings.segmented_reply.words_count_threshold": {
                        "description": "Limite de palavras para segmentação",
                        "hint": "Limite de palavras para respostas segmentadas. Apenas mensagens com menos palavras que este limite serão segmentadas; mensagens maiores serão enviadas diretamente, sem divisão.",
                        "type": "int",
                    },
                    "platform_settings.segmented_reply.split_mode": {
                        "description": "Modo de divisão",
                        "type": "string",
                        "options": ["regex", "words"],
                        "labels": ["Regex", "Lista de palavras"],
                    },
                    "platform_settings.segmented_reply.regex": {
                        "description": "Expressão regular de segmentação",
                        "hint": "Usado para identificar pontos de divisão com uma expressão regular. Prefira padrões que correspondam a separadores.",
                        "type": "string",
                        "condition": {
                            "platform_settings.segmented_reply.split_mode": "regex",
                        },
                    },
                    "platform_settings.segmented_reply.split_words": {
                        "description": "Lista de palavras de divisão",
                        "type": "list",
                        "hint": "Divide ao detectar qualquer palavra da lista",
                        "condition": {
                            "platform_settings.segmented_reply.split_mode": "words",
                        },
                    },
                    "platform_settings.segmented_reply.content_cleanup_rule": {
                        "description": "Regex para limpeza de conteúdo",
                        "type": "string",
                        "hint": "Remove o conteúdo especificado dos segmentos. Por exemplo, `[。?!]` remove todos esses sinais de pontuação.",
                    },
                },
            },
            "ltm": {
                "description": "Contexto de chat em grupo",
                "type": "object",
                "items": {
                    "provider_ltm_settings.group_icl_enable": {
                        "description": "Injetar mensagens do grupo no contexto",
                        "type": "bool",
                    },
                    "provider_ltm_settings.group_message_max_cnt": {
                        "description": "Máximo de mensagens injetadas",
                        "type": "int",
                        "condition": {
                            "provider_ltm_settings.group_icl_enable": True,
                        },
                    },
                    "provider_ltm_settings.image_caption": {
                        "description": "Entender imagens automaticamente",
                        "type": "bool",
                        "hint": "Exige configurar um modelo de descrição de imagens para conversas em grupo.",
                        "condition": {
                            "provider_ltm_settings.group_icl_enable": True,
                        },
                    },
                    "provider_ltm_settings.image_caption_provider_id": {
                        "description": "Modelo de descrição de imagens do grupo",
                        "type": "string",
                        "_special": "select_provider",
                        "hint": "Usado para compreender imagens inseridas dos registros de conversas em grupo, configurado separadamente do modelo padrão de descrição de imagens.",
                        "condition": {
                            "provider_ltm_settings.group_icl_enable": True,
                            "provider_ltm_settings.image_caption": True,
                        },
                    },
                    "provider_ltm_settings.group_message_history_enable": {
                        "description": "Persistir mensagens do grupo",
                        "type": "bool",
                        "hint": "Salva as mensagens do grupo e fornece ao modelo uma ferramenta para consultar o histórico do grupo atual. O conteúdo de mídia ainda não é persistido; mensagens de mídia são armazenadas como marcadores, como [Imagem].",
                    },
                    "provider_ltm_settings.group_message_history_max_cnt": {
                        "description": "Máximo de mensagens persistidas",
                        "type": "int",
                        "condition": {
                            "provider_ltm_settings.group_message_history_enable": True,
                        },
                    },
                    "provider_ltm_settings.active_reply.enable": {
                        "description": "Resposta ativa",
                        "type": "bool",
                    },
                    "provider_ltm_settings.active_reply.method": {
                        "description": "Método de resposta ativa",
                        "type": "string",
                        "options": ["possibility_reply"],
                        "condition": {
                            "provider_ltm_settings.active_reply.enable": True,
                        },
                    },
                    "provider_ltm_settings.active_reply.possibility_reply": {
                        "description": "Probabilidade de resposta",
                        "type": "float",
                        "hint": "Valor entre 0.0 e 1.0",
                        "slider": {"min": 0, "max": 1, "step": 0.05},
                        "condition": {
                            "provider_ltm_settings.active_reply.enable": True,
                        },
                    },
                    "provider_ltm_settings.active_reply.whitelist": {
                        "description": "Lista permitida para resposta ativa",
                        "type": "list",
                        "items": {"type": "string"},
                        "hint": "A filtragem pela lista de permissões fica desativada quando ela está vazia. Use /sid para obter os IDs.",
                        "condition": {
                            "provider_ltm_settings.active_reply.enable": True,
                        },
                    },
                },
            },
            "t2i": {
                "description": "Texto para imagem",
                "type": "object",
                "items": {
                    "t2i": {
                        "description": "Saída texto para imagem",
                        "type": "bool",
                    },
                    "t2i_word_threshold": {
                        "description": "Limite de palavras para texto para imagem",
                        "type": "int",
                        "condition": {
                            "t2i": True,
                        },
                    },
                    "t2i_strategy": {
                        "description": "Estratégia de texto para imagem",
                        "type": "string",
                        "hint": "Estratégia de conversão de texto em imagem. `remote` usa um serviço remoto de renderização HTML; `local` usa PIL para renderização local. No modo local, coloque uma fonte TTF chamada 'font.ttf' no diretório data/ para personalizar a fonte.",
                        "options": ["remote", "local"],
                        "condition": {
                            "t2i": True,
                        },
                    },
                    "t2i_endpoint": {
                        "description": "Endpoint da API de texto para imagem",
                        "type": "string",
                        "hint": "Usa o serviço de API do AstrBot quando vazio",
                        "condition": {
                            "t2i": True,
                            "t2i_strategy": "remote",
                        },
                    },
                    "t2i_template": {
                        "description": "Template personalizado",
                        "type": "bool",
                        "hint": "Quando ativado, permite personalizar modelos HTML para converter texto em imagem.",
                        "condition": {
                            "t2i": True,
                            "t2i_strategy": "remote",
                        },
                        "_special": "t2i_template",
                    },
                    "t2i_active_template": {
                        "description": "Template ativo",
                        "type": "string",
                        "hint": "Este valor é mantido pela página de gerenciamento de modelos de texto em imagem.",
                        "invisible": True,
                    },
                },
            },
        },
    },
}

CONFIG_METADATA_3_SYSTEM = {
    "system_group": {
        "name": "Sistema",
        "metadata": {
            "system": {
                "description": "Configurações do sistema",
                "type": "object",
                "items": {
                    "log_level": {
                        "description": "Nível de log do console",
                        "type": "string",
                        "hint": "Nível de registro exibido no console.",
                        "options": ["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"],
                    },
                    "dashboard.ssl.enable": {
                        "description": "Ativar HTTPS na WebUI",
                        "type": "bool",
                        "hint": "Quando ativado, a interface web é servida diretamente por HTTPS.",
                    },
                    "dashboard.trust_proxy_headers": {
                        "description": "Confiar em headers de proxy para o IP do cliente",
                        "type": "bool",
                        "hint": "Quando desativado, ignora X-Forwarded-For/X-Real-IP e usa apenas o endereço da conexão.",
                    },
                    "dashboard.auth_rate_limit.enable": {
                        "description": "Ativar limite de tentativas de login",
                        "type": "bool",
                        "hint": "Quando desativado, os endpoints de autenticação, como login e TOTP, não terão limite de requisições.",
                    },
                    "dashboard.auth_rate_limit.average_interval": {
                        "description": "Intervalo médio entre tentativas (segundos)",
                        "type": "float",
                        "hint": "Intervalo médio mínimo entre requisições de autenticação. Por exemplo, 1.0 permite no máximo uma requisição por segundo.",
                        "condition": {"dashboard.auth_rate_limit.enable": True},
                    },
                    "dashboard.auth_rate_limit.max_burst": {
                        "description": "Máximo de tentativas em sequência",
                        "type": "int",
                        "hint": "Número máximo de requisições consecutivas em uma rajada. Por exemplo, 3 permite até três requisições em uma sequência curta.",
                        "condition": {"dashboard.auth_rate_limit.enable": True},
                    },
                    "dashboard.totp.enable": {
                        "description": "Ativar TOTP na WebUI",
                        "type": "bool",
                        "hint": "Quando ativado, exige um código TOTP para entrar no painel.",
                        "_special": "dashboard_totp_manager",
                    },
                    "dashboard.ssl.cert_file": {
                        "description": "Caminho do certificado SSL",
                        "type": "string",
                        "hint": "Caminho do certificado (PEM). Aceita caminhos absolutos e relativos ao diretório de trabalho atual.",
                        "condition": {"dashboard.ssl.enable": True},
                    },
                    "dashboard.ssl.key_file": {
                        "description": "Caminho da chave privada SSL",
                        "type": "string",
                        "hint": "Caminho da chave privada (PEM). Aceita caminhos absolutos e relativos ao diretório de trabalho atual.",
                        "condition": {"dashboard.ssl.enable": True},
                    },
                    "dashboard.ssl.ca_certs": {
                        "description": "Caminho do certificado da CA",
                        "type": "string",
                        "hint": "Opcional. Caminho do arquivo de certificados da autoridade certificadora (CA).",
                        "condition": {"dashboard.ssl.enable": True},
                    },
                    "log_file_enable": {
                        "description": "Ativar log em arquivo",
                        "type": "bool",
                        "hint": "Grava os registros em um arquivo além de exibi-los no console.",
                    },
                    "log_file_path": {
                        "description": "Caminho do arquivo de log",
                        "type": "string",
                        "hint": "Caminhos relativos são resolvidos a partir do diretório data, por exemplo, logs/astrbot.log. Caminhos absolutos são aceitos.",
                    },
                    "log_file_max_mb": {
                        "description": "Tamanho máximo do log (MB)",
                        "type": "int",
                        "hint": "Rotaciona o arquivo quando ultrapassa este tamanho. Padrão: 20 MB.",
                    },
                    "temp_dir_max_size": {
                        "description": "Limite do diretório temporário (MB)",
                        "type": "int",
                        "hint": "Limita o tamanho total de data/temp, em MB. O sistema verifica a cada 10 minutos e, quando o limite é ultrapassado, exclui os arquivos mais antigos para liberar cerca de 30% do tamanho atual.",
                    },
                    "trace_log_enable": {
                        "description": "Ativar arquivo de Trace",
                        "type": "bool",
                        "hint": "Grava eventos de rastreamento em um arquivo separado, sem alterar a saída do console.",
                    },
                    "trace_log_path": {
                        "description": "Caminho do arquivo de Trace",
                        "type": "string",
                        "hint": "Caminhos relativos são resolvidos a partir do diretório data, por exemplo, logs/astrbot.trace.log. Caminhos absolutos são aceitos.",
                    },
                    "trace_log_max_mb": {
                        "description": "Tamanho máximo do Trace (MB)",
                        "type": "int",
                        "hint": "Rotaciona o arquivo quando ultrapassa este tamanho. Padrão: 20 MB.",
                    },
                    "pip_install_arg": {
                        "description": "Argumentos adicionais do pip",
                        "type": "string",
                        "hint": "As dependências dos plugins são instaladas com o pip do Python. Informe argumentos adicionais aqui, como `--break-system-package`.",
                    },
                    "pypi_index_url": {
                        "description": "URL do repositório PyPI",
                        "type": "string",
                        "hint": "URL do repositório PyPI para instalar dependências Python. Padrão: [https://mirrors.aliyun.com/pypi/simple/](https://mirrors.aliyun.com/pypi/simple/)",
                    },
                    "callback_api_base": {
                        "description": "Endereço externo da API de callback",
                        "type": "string",
                        "hint": "Serviços externos podem acessar o backend do AstrBot pelos links de callback que ele gera, como links de download. Como o AstrBot não consegue determinar automaticamente o endereço acessível externamente no ambiente de implantação, esta configuração informa como os serviços externos devem acessá-lo. Exemplos: [http://localhost:6185](http://localhost:6185), [https://example.com](https://example.com).",
                    },
                    "timezone": {
                        "description": "Fuso horário",
                        "type": "string",
                        "hint": "Use um nome IANA, como America/Sao_Paulo. Se vazio, usa o fuso do sistema.",
                    },
                    "http_proxy": {
                        "description": "Proxy HTTP",
                        "type": "string",
                        "hint": "Quando ativado, o proxy será configurado por variáveis de ambiente. Formato: `http://ip:port`",
                    },
                    "no_proxy": {
                        "description": "Endereços com conexão direta",
                        "type": "list",
                        "items": {"type": "string"},
                    },
                },
            },
        },
    },
}


DEFAULT_VALUE_MAP = {
    "int": 0,
    "float": 0.0,
    "bool": False,
    "string": "",
    "text": "",
    "list": [],
    "file": [],
    "object": {},
    "template_list": [],
    "dict": {},
}
