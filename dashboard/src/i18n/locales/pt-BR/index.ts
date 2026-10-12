// AstrBot Brasil — pacote de idioma pt-BR.
// Chaves ainda não localizadas usam en-US como fallback temporário para preservar funcionalidade.
import enUS from '../en-US';
import common from './core/common.json'; import actions from './core/actions.json'; import status from './core/status.json'; import navigation from './core/navigation.json'; import header from './core/header.json'; import shared from './core/shared.json';
import auth from './features/auth.json'; import welcome from './features/welcome.json'; import dashboard from './features/dashboard.json'; import about from './features/about.json'; import consoleMessages from './features/console.json'; import settings from './features/settings.json'; import provider from './features/provider.json'; import platform from './features/platform.json'; import config from './features/config.json'; import chat from './features/chat.json'; import conversation from './features/conversation.json'; import command from './features/command.json'; import persona from './features/persona.json'; import sessionManagement from './features/session-management.json'; import cron from './features/cron.json'; import stats from './features/stats.json'; import subagent from './features/subagent.json'; import toolUse from './features/tool-use.json'; import knowledgeBaseIndex from './features/knowledge-base/index.json';
import errors from './messages/errors.json'; import success from './messages/success.json'; import validation from './messages/validation.json';

export default {
  ...enUS,
  core: { ...enUS.core, common:{...enUS.core.common,...common}, actions:{...enUS.core.actions,...actions}, status:{...enUS.core.status,...status}, navigation:{...enUS.core.navigation,...navigation}, header:{...enUS.core.header,...header}, shared:{...enUS.core.shared,...shared} },
  features: {
    ...enUS.features,
    auth:{...enUS.features.auth,...auth}, welcome:{...enUS.features.welcome,...welcome}, dashboard:{...enUS.features.dashboard,...dashboard}, about:{...enUS.features.about,...about}, console:{...enUS.features.console,...consoleMessages}, settings:{...enUS.features.settings,...settings}, provider:{...enUS.features.provider,...provider}, platform:{...enUS.features.platform,...platform}, config:{...enUS.features.config,...config}, chat:{...enUS.features.chat,...chat}, conversation:{...enUS.features.conversation,...conversation}, command:{...enUS.features.command,...command}, persona:{...enUS.features.persona,...persona}, 'session-management':{...enUS.features['session-management'],...sessionManagement}, cron:{...enUS.features.cron,...cron}, stats:{...enUS.features.stats,...stats}, subagent:{...enUS.features.subagent,...subagent}, 'tool-use':{...enUS.features['tool-use'],...toolUse}, 'knowledge-base':{...enUS.features['knowledge-base'], index:{...enUS.features['knowledge-base'].index,...knowledgeBaseIndex}}
  },
  messages:{...enUS.messages, errors:{...enUS.messages.errors,...errors}, success:{...enUS.messages.success,...success}, validation:{...enUS.messages.validation,...validation}}
};
