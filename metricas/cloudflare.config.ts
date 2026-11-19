// Worker de métricas de Generala maldita: recibe eventos anónimos y muestra un tablero con clave.
import { bindings, defineConfig } from "cf/config";
import * as entrypoint from "./worker.js" with { type: "cf-worker" };

export default defineConfig({
	worker: {
		name: "generala-metricas",
		compatibilityDate: "2026-11-13",
		entrypoint,
		env: {
			DB: bindings.d1({ id: "bc9cb817-cf61-4c30-b777-f47177cf41f2", name: "generala-metricas" }),
		},
	},
});
