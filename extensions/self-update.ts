import type { ExtensionAPI } from "@mariozechner/pi-coding-agent";
import { spawnSync } from "node:child_process";

export default function (pi: ExtensionAPI) {
  pi.registerCommand("update", {
    description: "Update pi and restart with current session",
    handler: async (args, ctx) => {
      // Get session file before we do anything
      const sessionFile = ctx.sessionManager.getSessionFile();

      // Build the command: update then exec pi (exec replaces the shell process)
      let cmd = "npm update -g @mariozechner/pi-coding-agent && exec pi";
      if (sessionFile) {
        cmd = `npm update -g @mariozechner/pi-coding-agent && exec pi --session "${sessionFile}"`;
      }

      // Use custom UI to get TUI access, stop it, and hand off terminal
      await ctx.ui.custom<void>((tui, _theme, _kb, done) => {
        // Release terminal
        tui.stop();

        // Clear screen
        process.stdout.write("\x1b[2J\x1b[H");
        console.log("Updating pi...\n");

        // Run update + exec pi with full terminal access
        // spawnSync blocks until the exec'd pi exits
        const shell = process.env.SHELL || "/bin/sh";
        spawnSync(shell, ["-c", cmd], {
          stdio: "inherit",
          env: process.env,
        });

        // Only reached after the new pi exits
        done();
        return { render: () => [], invalidate: () => {} };
      });

      // Exit this old pi instance
      process.exit(0);
    },
  });
}
