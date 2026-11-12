import { config } from '../config.js';

// Tracing mínimo: spans com duração + contagem de tokens e custo (FinOps de LLM).
// Em produção: OpenTelemetry + Langfuse/LangSmith/Phoenix.
export class Tracer {
  constructor(name) {
    this.name = name;
    this.spans = [];
    this.usage = { input: 0, output: 0, cacheRead: 0 };
  }
  async span(name, fn, attrs = {}) {
    const t0 = performance.now();
    try {
      return await fn();
    } finally {
      this.spans.push({ name, ms: Math.round(performance.now() - t0), ...attrs });
    }
  }
  addUsage(u = {}) {
    this.usage.input += u.input_tokens ?? 0;
    this.usage.output += u.output_tokens ?? 0;
    this.usage.cacheRead += u.cache_read_input_tokens ?? 0;
  }
  get costUSD() {
    const { inPerM, outPerM } = config.pricing;
    return (this.usage.input * inPerM + this.usage.output * outPerM) / 1e6;
  }
  report() {
    const lines = this.spans.map((s) => `  • ${s.name.padEnd(16)} ${String(s.ms).padStart(5)} ms`);
    const u = this.usage;
    return `[trace:${this.name}]\n${lines.join('\n')}\n  tokens in/out: ${u.input}/${u.output} · custo ≈ US$ ${this.costUSD.toFixed(5)}`;
  }
}
