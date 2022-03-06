/**
 * This function loads the current message and gets header fields
 *  */ 
async function load() {
    /* Identification of the active tab, and collection of the current message */
    const tabs = await messenger.tabs.query({active: true, currentWindow: true});
    const message = await messenger.messageDisplay.getDisplayedMessage(tabs[0].id);
    const full = await messenger.messages.getFull(message.id);

    /* Extraction of interesting fields */
    try {
        document.getElementById("from").textContent = message.author;
        document.getElementById("to").textContent = message.recipients;
        /* Collecting x-forward-by field */
        document.getElementById("x-forward-by").textContent = full.headers["x-forward-by"] 

        console.log("[OK] Msg from/to/x-forward-by");
    } catch(e) {
        console.error("Error while accessing basic infos on the message (from/to/x-forward-by):\n" + e);
    }


    /* Getting all header items */
    try {
        let headers = document.getElementById("headers");
        for (let [key, value] of Object.entries(full.headers)) {
            /* DOM elements */
            let p = document.createElement('p');
            let keyElt = document.createElement('b');
            let valElt = document.createElement('span');

            keyElt.textContent = `${key}: `;
            p.appendChild(keyElt);
            valElt.textContent = `${value}`;
            p.appendChild(valElt);

            headers.appendChild(p);
        }
        console.log("[OK] Msg headers");
    } catch (e) {
        console.error("Error while accessing headers of the message:\n" + e);
    }
}

document.addEventListener("DOMContentLoaded", load);
