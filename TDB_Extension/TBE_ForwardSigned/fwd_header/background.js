/**
 * Use the startup phase to tell Thunderbird that it should load
 * our message-content-script.js file whenever a message is displayed
 */
 const handleStartup = () => {
    messenger.messageDisplayScripts.register({
      js: [{ file: "/fwd_header/message-content-script.js" }],
      css: [{ file: "/fwd_header/message-content-styles.css" }],
    });
  };
  
  /**
   * command handler: handles the commands received from the content script
   */
  const doHandleCommand = async (message, sender) => {
    const { command } = message;
    const {
      tab: { id: tabId },
    } = sender;
  
    const messageHeader = await browser.messageDisplay.getDisplayedMessage(tabId);
    const xForwardBy = await messenger.messages.getFull(messageHeader.id).headers["x-forward-by"];
  
    // check for known commands
    switch (command.toLocaleLowerCase()) {
      case "getnotificationdetails":
        {
          // create the information chunk we want to return to our message content script
          return {
            text: `X_Forward_By "${xForwardBy}"`,
          };
        }
        break;
  
    }
  };
  
  /**
   * handle the received message by filtering for all messages
   * whose "type" property is set to "command".
   */
  const handleMessage = (message, sender, sendResponse) => {
    if (message && message.hasOwnProperty("command")) {
      // if we have a command, return a promise from the command handler
      return doHandleCommand(message, sender);
    }
  };
  
  /**
   * Add a handler for communication with other parts of the extension,
   * like our messageDisplayScript.
   *
   * 👉 There should be only one handler in the background script
   *    for all incoming messages
   */
  browser.runtime.onMessage.addListener(handleMessage);
  
  /**
   * Execute the startup handler whenever Thunderbird starts
   */
  document.addEventListener("DOMContentLoaded", handleStartup);