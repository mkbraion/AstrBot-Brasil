// AstrBot Brasil — pacote de idioma pt-BR.
// A edição brasileira usa merge recursivo: qualquer chave ainda não traduzida
// continua disponível via en-US sem apagar campos internos da configuração.
import enUS from '../en-US';
import common from './core/common.json'; import actions from './core/actions.json'; import status from './core/status.json'; import navigation from './core/navigation.json'; import header from './core/header.json'; import shared from './core/shared.json';
import auth from './features/auth.json'; import welcome from './features/welcome.json'; import dashboard from './features/dashboard.json'; import about from './features/about.json'; import consoleMessages from './features/console.json'; import settings from './features/settings.json'; import provider from './features/provider.json'; import platform from './features/platform.json'; import config from './features/config.json'; import configMetadata from './features/config-metadata.json'; import chat from './features/chat.json'; import conversation from './features/conversation.json'; import command from './features/command.json'; import persona from './features/persona.json'; import sessionManagement from './features/session-management.json'; import cron from './features/cron.json'; import stats from './features/stats.json'; import subagent from './features/subagent.json'; import toolUse from './features/tool-use.json'; import trace from './features/trace.json'; import chart from './features/chart.json'; import extension from './features/extension.json'; import knowledgeBaseIndex from './features/knowledge-base/index.json'; import knowledgeBaseDetail from './features/knowledge-base/detail.json'; import knowledgeBaseDocument from './features/knowledge-base/document.json'; import alkaidIndex from './features/alkaid/index.json'; import alkaidKnowledgeBase from './features/alkaid/knowledge-base.json'; import alkaidMemory from './features/alkaid/memory.json';
import errors from './messages/errors.json'; import success from './messages/success.json'; import validation from './messages/validation.json';

function mergeDeep(base: any, patch: any): any {
  if (Array.isArray(patch)) return [...patch];
  if (patch === null || typeof patch !== 'object') return patch;
  const result: any = base && typeof base === 'object' && !Array.isArray(base) ? { ...base } : {};
  for (const [key, value] of Object.entries(patch)) {
    result[key] = value && typeof value === 'object' && !Array.isArray(value)
      ? mergeDeep(result[key], value)
      : Array.isArray(value) ? [...value] : value;
  }
  return result;
}

const ptBR = {
  core:{common,actions,status,navigation,header,shared},
  features:{extension,auth,welcome,dashboard,about,console:consoleMessages,settings,provider,platform,config,'config-metadata':configMetadata,chat,conversation,command,persona,'session-management':sessionManagement,cron,stats,subagent,tooluse:toolUse,trace,chart,alkaid:{index:alkaidIndex,'knowledge-base':alkaidKnowledgeBase,memory:alkaidMemory},'knowledge-base':{index:knowledgeBaseIndex,detail:knowledgeBaseDetail,document:knowledgeBaseDocument}},
  messages:{errors,success,validation}
};

export default mergeDeep(enUS, ptBR) as typeof enUS;
