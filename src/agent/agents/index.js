import { helpdeskAgent } from './helpdesk-agent.js';
import { triageAgent } from './triage-agent.js';
import { cepAgent } from './cep-agent.js';

// Registro de agentes. Para adicionar um: crie o arquivo e liste aqui.
export const agents = [helpdeskAgent, triageAgent, cepAgent];

export function getAgent(name = 'helpdesk') {
  const agent = agents.find((a) => a.name === name);
  if (!agent) throw new Error(`Agente desconhecido: ${name}. Disponíveis: ${agents.map((a) => a.name).join(', ')}`);
  return agent;
}
