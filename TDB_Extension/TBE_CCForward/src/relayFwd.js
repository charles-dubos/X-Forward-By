/* Put focus on input field */
var input = document.getElementById('forward-to');
input.focus();
input.select();

/**
 * Send a forward-by message
 */
async function forward() {
    let fwd_to = document.getElementById("forward-to").value;

    /* Identification of the active tab, and collection of the current message */
    const tabs = await messenger.tabs.query({active: true, currentWindow: true});
    const message = await messenger.messageDisplay.getDisplayedMessage(tabs[0].id);
    const messageRaw = await messenger.messages.getRaw(message.id);
    const messageFull = await messenger.messages.getFull(message.id);
    console.log ('Raw message',messageRaw)
    
    console.log ("from: " + messageFull.author);
    console.log ("x-forward-by: " + messageFull.recipients);
    console.log ("subject: " + messageFull.subject);
    console.log ("to: " + fwd_to);

    const tab = await messenger.accounts.list();

    console.log(tab);

    /* Close the popup */
    window.close();
}

/** 
 * Sent a crafted e-mail with SMTP
 */
function sendEmail(from, to, subject, body) {
	Email.send({
	Host: "smtp.bob.loc",
	Username : "bob@mta2.loc",
	Password : "bob",
	To : to,
	From : from,
	Subject : subject,
	Body : body,
	}).then(
		message => alert("mail sent successfully")
	);
}


/* Detection of enter pressed */
document.getElementById("forward-to").addEventListener("keyup", ({key}) => {
    if (key === "Enter") { forward(); }
}); 
