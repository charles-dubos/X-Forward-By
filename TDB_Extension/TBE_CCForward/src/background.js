async function load() {
  /**
   * Add a handler for communication with other parts of the extension,
   * like our message display script.
   *
   * Note: If this handler is defined async, there should be only one such
   *       handler in the background script for all incoming messages.
   */
  messenger.runtime.onMessage.addListener(async (message, sender, sendResponse) => {
    // Check if the message includes our command member.
    if (message && message.hasOwnProperty("command")) {
        // Get the message currently displayed in the sending tab, abort if
        // that failed.
        const messageHeader = await messenger.messageDisplay.getDisplayedMessage(sender.tab.id);
        if (!messageHeader) {
            return;
        }
        //console.log (messageHeader);
        const fullMsg = await messenger.messages.getFull(messageHeader.id);
        //console.log (fullMsg);
        const xForwardBy = fullMsg.headers["x-forward-by"];
        // ExpandedHeader???
        window.addEventListener("DOMContentLoaded", (event) => { console/log("DOM chargé"); })

        // Check for known commands.
        switch (message.command) {
            case "x-forward-by":
                // Create the information we want to return to our message display script.
                return { text: `${xForwardBy}` };
                // >>> Is the xForwardBy in the contacts ???
        }
    }
  });

// Register the message display script.
messenger.messageDisplayScripts.register({
    js: [{ file: "src/message-content-script.js" }],
    css: [{ file: "src/message-content-styles.css" }],
  });
}

document.addEventListener("DOMContentLoaded", load);