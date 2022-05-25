/* function msgPartToString(msg) {
    let msgString = new String();
    msgString += ("Body: " + msg.body + "; ");
    msgString += ("ContentType: " + msg.contentType + "; ");
    msgString += ("Headers: " + msg.headers.received[0] + "; ");
    msgString += ("Name: " + msg.name + "; ");
    msgString += ("PartName: " + msg.partName + "; ");
    if (typeof msg.part  !== 'undefined') {
        for (const part in msg.parts) {
            msgString += ("part: {" + msgPartToString(msg.part) + "}");
        }
    }
    msgString += ("Size: " + msg.size.toString() + "; ");
    return msgString;
} */

/* function byte2print(byteStr) {
    let printStr = new String();
    let len = byteStr.length;
    for (let i=0; i<len; i++) {
        let byte = byteStr.charCodeAt(i);
        printStr += ((byte>=32 && byte<=126) ? byteStr.charAt(i) : "§"+byteStr.toString() );
    }
    return printStr;
} */


/**
 * This function loads the current message and gets particular informations of it
 *  */ 
async function load() {
    // Identification of the active tab, and of the current message
    const tabs = await messenger.tabs.query({active: true, currentWindow: true});
    const message = await messenger.messageDisplay.getDisplayedMessage(tabs[0].id);
    const full = await messenger.messages.getFull(message.id);

    try {
        // Extraction of interesting fields
        document.getElementById("from").textContent = message.author;
        document.getElementById("to").textContent = message.recipients;
        //console.log(message)
        console.log("[OK] Msg from/to");

        // Collecting X-Forward-By field
        document.getElementById("x-forward-by").textContent = typeof full.headers["x-forward-by"] !== "undefined"
            ? full.headers["x-forward-by"] 
            : "No X-Forward-By header"
    } catch(e) {
        console.error("Error while accessing basic infos on the message (from/to):\n" + e);
    }

    // Les headers:
    try {
        let headers = new String();
        for (let [key, value] of Object.entries(full.headers)) {
             headers += `${key}: ${value} <br> `;
        }
        document.getElementById("headers").textContent = headers.keys();
        console.log(full);
        console.log("[OK] Msg headers");
    } catch (e) {
        console.error("Error while accessing headers of the message:\n" + e);
    }

    let raw = await messenger.messages.getRaw(message.id);
    console.log(raw);

/*     // Récupération du message raw
    let raw = await messenger.messages.getRaw(message.id);
    try {
        document.getElementById("raw").textContent = byte2print(raw);
        console.log("[OK] Msg raw");
    } catch (e) {
        console.error("Error while exploiting the raw message:\n" + e);
    }
 */


    /// Todo: déterminer le champ qui va bien pour le destinataire => il deviendra le champ 'X-Transfered-by'
    /// Todo: afficher l'empreinte de la signature si elle existe
}

document.addEventListener("DOMContentLoaded", load);
