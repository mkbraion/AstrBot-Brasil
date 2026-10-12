// AstrBot Brasil — pacote de idioma pt-BR.
// Enquanto a cobertura é ampliada, chaves ainda não localizadas usam en-US
// para preservar funcionalidade e evitar strings ausentes na interface.
import enUS from '../en-US';
import common from './core/common.json';
import actions from './core/actions.json';
import status from './core/status.json';
import navigation from './core/navigation.json';
import auth from './features/auth.json';
import welcome from './features/welcome.json';

export default {
  ...enUS,
  core: {
    ...enUS.core,
    common: { ...enUS.core.common, ...common },
    actions: { ...enUS.core.actions, ...actions },
    status: { ...enUS.core.status, ...status },
    navigation: { ...enUS.core.navigation, ...navigation }
  },
  features: {
    ...enUS.features,
    auth: { ...enUS.features.auth, ...auth },
    welcome: { ...enUS.features.welcome, ...welcome }
  }
};
