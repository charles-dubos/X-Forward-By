const showBanner = async () => {
  let xForwardBy = await browser.runtime.sendMessage({
    command: "x-forward-by",
  });

  // get the details back from the formerly serialized content
  const { text } = xForwardBy;
  console.log(xForwardBy);

  // if (and only if) the x-forward-by field is not empty, add a banner
  if (xForwardBy.text !== "undefined") {
    // create the banner element itself
    const banner = document.createElement("div");
    banner.className = "DisplayXFB";

    // create the banner text element
    const bannerContent = document.createElement("div");
    bannerContent.className = "BannerXFB";
    const bannerTitle = document.createElement("span");
    bannerTitle.className = "titleXFB";
    bannerTitle.textContent = "Forwarded by ";
    const bannerText = document.createElement("span");
    bannerText.textContent = text;
    bannerContent.appendChild(bannerTitle);
    bannerContent.appendChild(bannerText);

    // add text to the banner
    banner.appendChild(bannerContent);

    // and insert it as the very first element in the message
    document.body.insertBefore(banner, document.body.firstChild);

  }
};

showBanner();