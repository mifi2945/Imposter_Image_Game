export interface ServiceUrls {
  accounts: string;
  files: string;
  lobby: string;
  orchestrator: string;
  questions: string;
}

const localServiceUrls: ServiceUrls = {
  accounts: 'http://127.0.0.1:8000',
  files: 'http://127.0.0.1:8003',
  lobby: 'http://127.0.0.1:8004',
  orchestrator: 'http://127.0.0.1:8002',
  questions: 'http://127.0.0.1:8005',
};

function requireProductionUrl(name: string, value: string | undefined) {
  if (!value) {
    throw new Error(`Missing ${name}. Set production service URLs before making API requests.`);
  }

  return value.replace(/\/+$/, '');
}

function getProductionServiceUrls(): ServiceUrls {
  return {
    accounts: requireProductionUrl('VITE_ACCOUNTS_API_URL', import.meta.env.VITE_ACCOUNTS_API_URL),
    files: requireProductionUrl('VITE_FILES_API_URL', import.meta.env.VITE_FILES_API_URL),
    lobby: requireProductionUrl('VITE_LOBBY_API_URL', import.meta.env.VITE_LOBBY_API_URL),
    orchestrator: requireProductionUrl(
      'VITE_ORCHESTRATOR_API_URL',
      import.meta.env.VITE_ORCHESTRATOR_API_URL
    ),
    questions: requireProductionUrl(
      'VITE_QUESTIONS_API_URL',
      import.meta.env.VITE_QUESTIONS_API_URL
    ),
  };
}

export function getServiceUrls(): ServiceUrls {
  return import.meta.env.DEV ? localServiceUrls : getProductionServiceUrls();
}
