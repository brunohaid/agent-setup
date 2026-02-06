import type { ExtensionAPI } from "@mariozechner/pi-coding-agent";

export default function (pi: ExtensionAPI) {
  // Intercept /noop commands before any parsing
  pi.on("input", async (event, ctx) => {
    // Check if input starts with /noop
    if (!event.text.startsWith("/noop ")) return { action: "continue" };

    // Extract everything after "/noop "
    const userPrompt = event.text.slice(6);

    // Build the transformed prompt with planning instructions
    const transformed = `${userPrompt}

---

**Important:** Do not implement the changes yet. Instead, report what you would do:
- List the files you would modify
- Describe the changes you would make to each file
- Explain your reasoning

Only proceed with implementation if I explicitly ask you to.`;

    return { action: "transform", text: transformed };
  });
}
