// Functions to forward a signed message

/* This function trans-cypher of the initial message with the public key of the new reciever */
function transCypher(msg, key) {
    return 0
}


/* This fonction adds the 'X-Transfered-By' header */
function addHeader(msg, destinataire) {

    return msg
}

/* This function loads the current message */
async function load() {
    // Identification of the active tab, and of the current message
    let tabs = await messenger.tabs.query({active: true, currentWindow: true});
    let message = await messenger.messageDisplay.getDisplayedMessage(tabs[0].id);

    // Extraction of interesting fields
    document.getElementById("from").textContent = message.author; /// Celui-ci ne changera pas
    /// Todo: déterminer le champ qui va bien pour le destinataire => il deviendra le champ 'X-Transfered-by'
    /// Todo: afficher l'empreinte de la signature si elle existe

    // Les headers:
    let full = await messenger.messages.getFull(message.id);
    document.getElementById("recieved").textContent = full.headers.recieved[0];
}

document.addEventListener("DOMContentLoaded", load);
