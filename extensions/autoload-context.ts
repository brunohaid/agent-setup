/**
 * Autoload Context Extension
 *
 * Automatically loads all .md files from docs/agents/context/ into the
 * system prompt at the start of each session.
 */

import type { ExtensionAPI } from "@mariozechner/pi-coding-agent";
import * as fs from "node:fs";
import * as path from "node:path";

export default function (pi: ExtensionAPI) {
	let contextContent = "";

	// Read context files on session start
	pi.on("session_start", async (_event, ctx) => {
		const contextDir = path.join(ctx.cwd, "docs/agents/context");
		if (!fs.existsSync(contextDir)) return;

		// Get all .md files
		const files = fs.readdirSync(contextDir).filter(f => f.endsWith(".md")).sort();
		if (files.length === 0) return;

		// Read and combine contents
		const contents: string[] = [];
		for (const file of files) {
			const filePath = path.join(contextDir, file);
			const content = fs.readFileSync(filePath, "utf-8");
			contents.push(content);
		}

		contextContent = contents.join("\n\n");

		// Show loaded files (bold filenames stand out from dim notify wrapper)
		const bold = "\x1b[1m";
		const reset = "\x1b[0m";
		const fileNames = files.join(", ");
		ctx.ui.notify(`Loaded ${files.length} context file(s): ${bold}${fileNames}${reset}`, "info");
	});

	// Append to system prompt before each LLM call
	pi.on("before_agent_start", async (event) => {
		if (!contextContent) return;
		return {
			systemPrompt: event.systemPrompt + "\n\n" + contextContent,
		};
	});
}
